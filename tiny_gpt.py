"""
tiny_gpt_rope.py
────────────────
A GPT-1-style decoder-only transformer with RoPE positional encoding.
Pure NumPy — every matrix multiply, activation, normalisation,
and gradient is written by hand.  No PyTorch, no JAX, no autograd.

Architecture
  character-level tokeniser
  token embedding  (no separate positional table — RoPE handles position)
  N_LAYERS × Transformer block
      pre-LayerNorm → multi-head causal self-attention (RoPE on Q,K)
                    → residual
      pre-LayerNorm → Feed-Forward (GELU)
                    → residual
  final LayerNorm → linear LM head (weight-tied to embedding)
  Adam optimiser with gradient clipping

Run:  python tiny_gpt_rope.py
"""

import numpy as np

# ──────────────────────────────────────────────────────────────────────────────
#  HYPER-PARAMETERS
# ──────────────────────────────────────────────────────────────────────────────

D_MODEL     = 128    # embedding / hidden dimension
N_HEADS     = 4      # attention heads  (head_dim = D_MODEL // N_HEADS = 32)
N_LAYERS    = 2      # transformer blocks
D_FF        = 256    # feed-forward inner dimension
MAX_SEQ     = 64     # maximum context length
LR          = 3e-4   # Adam learning rate
EPOCHS      = 1000
BATCH       = 4

CORPUS = """
the cat sat on the mat
the dog sat on the log
the cat ate the rat
the rat ran from the cat
a dog and a cat are friends
the mat is on the floor
the log is in the fire
cats and dogs are animals
the cat chased the dog around the house
the dog barked at the cat near the tree
a cat and a dog played in the garden
""".strip()


# ──────────────────────────────────────────────────────────────────────────────
#  1.  TOKENISER  (character-level)
# ──────────────────────────────────────────────────────────────────────────────

class CharTokenizer:
    PAD, BOS, EOS = 0, 1, 2

    def __init__(self, text: str):
        chars       = sorted(set(text))
        self.vocab  = ['<pad>', '<bos>', '<eos>'] + chars
        self.stoi   = {c: i for i, c in enumerate(self.vocab)}
        self.itos   = {i: c for c, i in self.stoi.items()}

    def encode(self, text: str) -> list[int]:
        ids = [self.stoi[c] for c in text if c in self.stoi]
        return [self.BOS] + ids + [self.EOS]

    def decode(self, ids: list[int]) -> str:
        skip = {self.PAD, self.BOS, self.EOS}
        return ''.join(self.itos[i] for i in ids if i not in skip)

    def __len__(self) -> int:
        return len(self.vocab)


# ──────────────────────────────────────────────────────────────────────────────
#  2.  MATHS PRIMITIVES  (forward + their exact gradients)
# ──────────────────────────────────────────────────────────────────────────────

def softmax(x, axis=-1):
    """Numerically stable softmax."""
    x  = x - x.max(axis=axis, keepdims=True)
    ex = np.exp(x)
    return ex / ex.sum(axis=axis, keepdims=True)


def gelu(x):
    """
    GELU(x) = x * Φ(x)
    Approximation used in GPT-2 / GPT-1:
      GELU(x) ≈ 0.5·x·(1 + tanh(√(2/π)·(x + 0.044715·x³)))
    """
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))


def gelu_grad(x):
    """
    d(GELU)/dx  — needed for FF backward pass.
    Let t = tanh(√(2/π)·(x + 0.044715·x³))
    GELU = 0.5·x·(1+t)
    d(GELU)/dx = 0.5·(1+t) + 0.5·x·(1-t²)·√(2/π)·(1 + 3·0.044715·x²)
    """
    arg   = np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)
    t     = np.tanh(arg)
    sech2 = 1.0 - t**2
    darg  = np.sqrt(2.0 / np.pi) * (1.0 + 3.0 * 0.044715 * x**2)
    return 0.5 * (1.0 + t) + 0.5 * x * sech2 * darg


def ln_forward(x, gamma, beta, eps=1e-5):
    """
    LayerNorm forward.
      mu    = mean(x, axis=-1)
      var   = mean((x-mu)², axis=-1)
      x_hat = (x - mu) / sqrt(var + eps)
      out   = gamma * x_hat + beta
    Returns out, x_hat, var  (x_hat and var needed for backward).
    """
    mu    = x.mean(axis=-1, keepdims=True)
    var   = ((x - mu) ** 2).mean(axis=-1, keepdims=True)
    x_hat = (x - mu) / np.sqrt(var + eps)
    return gamma * x_hat + beta, x_hat, var


def ln_backward(dout, x_hat, var, gamma, eps=1e-5):
    """
    LayerNorm backward.
    Derivation (N = last-dim size):
      dx_hat = dout * gamma
      dL/dx  = (1/√(var+ε)) * (
                 dx_hat
               − mean(dx_hat)               ← comes from dmu
               − x_hat·mean(dx_hat·x_hat)   ← comes from dvar
               )
    dgamma = sum(dout * x_hat, over batch+seq)
    dbeta  = sum(dout,         over batch+seq)
    """
    dx_hat  = dout * gamma
    std_inv = 1.0 / np.sqrt(var + eps)
    dx      = std_inv * (
        dx_hat
        - dx_hat.mean(axis=-1, keepdims=True)
        - x_hat * (dx_hat * x_hat).mean(axis=-1, keepdims=True)
    )
    sum_ax = tuple(range(dout.ndim - 1))   # all axes except last
    return dx, (dout * x_hat).sum(axis=sum_ax), dout.sum(axis=sum_ax)


# ──────────────────────────────────────────────────────────────────────────────
#  3.  ROPE  (Rotary Position Embedding)
# ──────────────────────────────────────────────────────────────────────────────

def rope_freqs(seq_len: int, head_dim: int):
    """
    Precompute cos/sin tables.

    For each dimension-pair index i ∈ [0, head_dim/2):
      θ_i = 10000^(-2i / head_dim)          ← frequency (slow for large i)

    For each position m ∈ [0, seq_len):
      angle(m, i) = m · θ_i

    cos_table[m, i] = cos(m · θ_i)
    sin_table[m, i] = sin(m · θ_i)
    shape: (seq_len, head_dim // 2)
    """
    half   = head_dim // 2
    i      = np.arange(half, dtype=np.float32)
    theta  = 10000.0 ** (-2.0 * i / head_dim)       # (half,)
    pos    = np.arange(seq_len, dtype=np.float32)    # (seq,)
    angles = np.outer(pos, theta)                     # (seq, half)
    return np.cos(angles), np.sin(angles)


def rotate_half(x):
    """
    Given x with shape (..., head_dim):
    Split into [x_first | x_second] and return [-x_second | x_first].

    This implements the "rotate by 90°" trick that makes RoPE work.
    For a 2D pair (x_a, x_b):
      rotate_half → (-x_b, x_a)
    Which appears in the 2D rotation matrix:
      [cos θ  -sin θ] [x_a]   [x_a·cosθ - x_b·sinθ]
      [sin θ   cos θ] [x_b] = [x_a·sinθ + x_b·cosθ]
                             = [x_a, x_b]·cosθ  +  [-x_b, x_a]·sinθ
    """
    h  = x.shape[-1] // 2
    return np.concatenate([-x[..., h:], x[..., :h]], axis=-1)


def rope_apply(x, cos, sin):
    """
    Apply RoPE rotation to x.

    x   : (B, S, H, head_dim)
    cos : (S, head_dim//2)
    sin : (S, head_dim//2)

    Formula:
      cos_full = [cos | cos]   shape (S, head_dim)  ← one cos per dimension
      sin_full = [sin | sin]   shape (S, head_dim)
      x_rope = x · cos_full + rotate_half(x) · sin_full
    """
    # tile: (S, half) → (S, head_dim)
    cos_f = np.concatenate([cos, cos], axis=-1)   # (S, D_head)
    sin_f = np.concatenate([sin, sin], axis=-1)

    # broadcast over batch and heads: (1, S, 1, D_head)
    cos_f = cos_f[None, :, None, :]
    sin_f = sin_f[None, :, None, :]

    return x * cos_f + rotate_half(x) * sin_f


def rope_backward(dout, cos, sin):
    """
    Backward pass through rope_apply.

    The rotation R(θ) is an orthogonal matrix, so R(θ)^T = R(-θ).
    Therefore: dL/dx = R(-θ) · dL/dy = rope_apply(dL/dy, cos, -sin)

    Proof for one 2D pair:
      y = [x₁·cosθ - x₂·sinθ,  x₁·sinθ + x₂·cosθ]

      dL/dx₁ = dL/dy₁·cosθ + dL/dy₂·sinθ
      dL/dx₂ = -dL/dy₁·sinθ + dL/dy₂·cosθ

      = rope_apply([dL/dy₁, dL/dy₂], cosθ, -sinθ)  ✓
    """
    return rope_apply(dout, cos, -sin)


# ──────────────────────────────────────────────────────────────────────────────
#  4.  PARAMETER INITIALISATION
# ──────────────────────────────────────────────────────────────────────────────

def init_params(vocab_size, d_model, n_heads, n_layers, d_ff, seed=42):
    rng = np.random.default_rng(seed)

    def xavier(shape):
        # Xavier / Glorot uniform
        limit = np.sqrt(6.0 / (shape[0] + (shape[1] if len(shape) > 1 else shape[0])))
        return rng.uniform(-limit, limit, shape).astype(np.float32)

    p = {}
    # token embedding: each vocabulary id → d_model-dim vector
    p['wte'] = xavier((vocab_size, d_model))

    for l in range(n_layers):
        # LayerNorm parameters (scale γ and shift β)
        p[f'ln1_g_{l}'] = np.ones( d_model, dtype=np.float32)
        p[f'ln1_b_{l}'] = np.zeros(d_model, dtype=np.float32)
        p[f'ln2_g_{l}'] = np.ones( d_model, dtype=np.float32)
        p[f'ln2_b_{l}'] = np.zeros(d_model, dtype=np.float32)

        # Attention projections  W: (D, D)
        p[f'Wq_{l}'] = xavier((d_model, d_model))
        p[f'Wk_{l}'] = xavier((d_model, d_model))
        p[f'Wv_{l}'] = xavier((d_model, d_model))
        p[f'Wo_{l}'] = xavier((d_model, d_model))
        p[f'bq_{l}'] = np.zeros(d_model, dtype=np.float32)
        p[f'bk_{l}'] = np.zeros(d_model, dtype=np.float32)
        p[f'bv_{l}'] = np.zeros(d_model, dtype=np.float32)
        p[f'bo_{l}'] = np.zeros(d_model, dtype=np.float32)

        # Feed-forward  W1: (D, D_ff),  W2: (D_ff, D)
        p[f'W1_{l}'] = xavier((d_model, d_ff))
        p[f'b1_{l}'] = np.zeros(d_ff,    dtype=np.float32)
        p[f'W2_{l}'] = xavier((d_ff,   d_model))
        p[f'b2_{l}'] = np.zeros(d_model, dtype=np.float32)

    # Final LayerNorm + LM head
    p['lnf_g']   = np.ones( d_model, dtype=np.float32)
    p['lnf_b']   = np.zeros(d_model, dtype=np.float32)
    p['lm_head'] = xavier((d_model, vocab_size))
    return p


# ──────────────────────────────────────────────────────────────────────────────
#  5.  FORWARD PASS
# ──────────────────────────────────────────────────────────────────────────────

def forward(tokens, params, n_heads, cos, sin):
    """
    tokens : (B, S)  int32 token ids
    cos    : (MAX_SEQ, head_dim//2)   precomputed RoPE tables
    sin    : (MAX_SEQ, head_dim//2)

    Returns
      logits : (B, S, V)   unnormalised next-token scores
      cache  : dict of all intermediates needed for backward
    """
    B, S      = tokens.shape
    D         = params['wte'].shape[1]
    head_dim  = D // n_heads
    n_layers  = sum(1 for k in params if k.startswith('W1_'))
    scale     = 1.0 / np.sqrt(head_dim)   # 1/√d_k  for attention scaling
    cache     = {'tokens': tokens}

    # ── causal mask: position j cannot attend to position i > j ─────────────
    # upper triangle = -∞  so softmax(scores + mask) = 0 for future positions
    causal = np.triu(np.full((S, S), -1e9, dtype=np.float32), k=1)

    # ── token embedding ──────────────────────────────────────────────────────
    x = params['wte'][tokens]    # (B, S, D)

    # ── N transformer blocks ─────────────────────────────────────────────────
    for l in range(n_layers):

        # (a) pre-attention LayerNorm
        ln1, xh1, v1 = ln_forward(x, params[f'ln1_g_{l}'], params[f'ln1_b_{l}'])
        cache[f'x_in_{l}']    = x       # residual bypass
        cache[f'xh1_{l}']     = xh1
        cache[f'v1_{l}']      = v1

        # (b) QKV projections: (B, S, D) → (B, S, D)
        Q = ln1 @ params[f'Wq_{l}'] + params[f'bq_{l}']
        K = ln1 @ params[f'Wk_{l}'] + params[f'bk_{l}']
        V = ln1 @ params[f'Wv_{l}'] + params[f'bv_{l}']
        cache[f'ln1_out_{l}'] = ln1     # needed for Wq/Wk/Wv grad

        # (c) reshape to multi-head: (B, S, H, head_dim)
        Q = Q.reshape(B, S, n_heads, head_dim)
        K = K.reshape(B, S, n_heads, head_dim)
        V = V.reshape(B, S, n_heads, head_dim)

        # (d) apply RoPE to Q and K  (V is not rotated)
        #     Each head's query/key pair is rotated by position-dependent angle.
        #     This bakes "how far apart are these two tokens" into the dot product.
        Q = rope_apply(Q, cos[:S], sin[:S])
        K = rope_apply(K, cos[:S], sin[:S])

        # (e) transpose to (B, H, S, head_dim) for batched matmul
        Qt = Q.transpose(0, 2, 1, 3)   # (B, H, S, hd)
        Kt = K.transpose(0, 2, 1, 3)
        Vt = V.transpose(0, 2, 1, 3)
        cache[f'Qt_{l}'] = Qt           # stored for backward
        cache[f'Kt_{l}'] = Kt
        cache[f'Vt_{l}'] = Vt

        # (f) scaled dot-product attention
        #   scores  = Q · Kᵀ / √head_dim     (B, H, S, S)
        #   weights = softmax(scores + causal_mask)
        #   output  = weights · V
        scores = Qt @ Kt.transpose(0, 1, 3, 2) * scale  # (B, H, S, S)
        scores = scores + causal                          # mask future
        attn_w = softmax(scores, axis=-1)                 # (B, H, S, S)
        av     = attn_w @ Vt                              # (B, H, S, hd)
        cache[f'attn_w_{l}'] = attn_w

        # (g) merge heads: (B, H, S, hd) → (B, S, D)
        merged = av.transpose(0, 2, 1, 3).reshape(B, S, D)
        cache[f'merged_{l}'] = merged

        # (h) output projection
        attn_out = merged @ params[f'Wo_{l}'] + params[f'bo_{l}']  # (B, S, D)
        cache[f'attn_out_{l}'] = attn_out

        # (i) residual 1
        x = x + attn_out

        # (j) pre-FF LayerNorm
        ln2, xh2, v2 = ln_forward(x, params[f'ln2_g_{l}'], params[f'ln2_b_{l}'])
        cache[f'res1_{l}']    = x       # residual bypass
        cache[f'xh2_{l}']     = xh2
        cache[f'v2_{l}']      = v2
        cache[f'ln2_out_{l}'] = ln2

        # (k) feed-forward: D → D_ff (GELU) → D
        ff1     = ln2 @ params[f'W1_{l}'] + params[f'b1_{l}']    # (B, S, D_ff)
        ff1_act = gelu(ff1)                                        # (B, S, D_ff)
        ff2     = ff1_act @ params[f'W2_{l}'] + params[f'b2_{l}'] # (B, S, D)
        cache[f'ff1_{l}']     = ff1
        cache[f'ff1_act_{l}'] = ff1_act
        cache[f'ff2_{l}']     = ff2

        # (l) residual 2
        x = x + ff2
        cache[f'res2_{l}'] = x

    # ── final LayerNorm + LM head ─────────────────────────────────────────────
    lnf, xhf, vf = ln_forward(x, params['lnf_g'], params['lnf_b'])
    cache['lnf_out'] = lnf
    cache['xhf']     = xhf
    cache['vf']      = vf

    logits = lnf @ params['lm_head']   # (B, S, vocab_size)
    return logits, cache


# ──────────────────────────────────────────────────────────────────────────────
#  6.  LOSS  — cross-entropy on next-token prediction
# ──────────────────────────────────────────────────────────────────────────────

def loss_fn(logits, targets, pad_id=0):
    """
    logits  : (B, S, V)   raw model output
    targets : (B, S)      token ids shifted by 1  (the "next" tokens)

    Cross-entropy:
      p = softmax(logits)
      L = -mean(log p[correct_token])  over non-pad positions
    """
    B, S, _ = logits.shape
    probs   = softmax(logits, axis=-1)                              # (B, S, V)
    mask    = (targets != pad_id).astype(np.float32)               # (B, S)
    correct = probs[np.arange(B)[:, None], np.arange(S), targets]  # (B, S)
    loss    = -(np.log(correct + 1e-9) * mask).sum() / (mask.sum() + 1e-9)
    return loss, probs


# ──────────────────────────────────────────────────────────────────────────────
#  7.  BACKWARD PASS  — manual chain rule, mirrors forward exactly
# ──────────────────────────────────────────────────────────────────────────────

def backward(logits, probs, targets, params, cache, n_heads, cos, sin, pad_id=0):
    """
    Chain rule in reverse order of the forward pass.
    Every gradient is derived analytically — no autograd magic.
    """
    B, S, V  = logits.shape
    D        = params['wte'].shape[1]
    head_dim = D // n_heads
    n_layers = sum(1 for k in params if k.startswith('W1_'))
    scale    = 1.0 / np.sqrt(head_dim)
    mask     = (targets != pad_id).astype(np.float32)
    n_tok    = mask.sum() + 1e-9
    grads    = {k: np.zeros_like(v) for k, v in params.items()}

    # ── dL/d(logits) ────────────────────────────────────────────────────────
    # For cross-entropy + softmax the derivative simplifies beautifully:
    #   dL/d(logit_c) = (prob_c - 1[c is correct]) / N_tokens
    dlogits = probs.copy()
    dlogits[np.arange(B)[:, None], np.arange(S), targets] -= 1.0
    dlogits *= (mask / n_tok)[:, :, None]              # (B, S, V)

    # ── LM head: logits = lnf_out @ lm_head ─────────────────────────────────
    lnf = cache['lnf_out']                             # (B, S, D)
    grads['lm_head'] = lnf.reshape(-1, D).T @ dlogits.reshape(-1, V)
    d_lnf = dlogits @ params['lm_head'].T              # (B, S, D)

    # ── final LayerNorm backward ─────────────────────────────────────────────
    dx, grads['lnf_g'], grads['lnf_b'] = ln_backward(
        d_lnf, cache['xhf'], cache['vf'], params['lnf_g']
    )

    # ── N transformer blocks in REVERSE order ───────────────────────────────
    for l in reversed(range(n_layers)):

        # ── residual 2: gradient flows through both FF and identity path ────
        # x = res1 + ff2  →  dx is gradient w.r.t. x after residual 2
        dx_ff = dx.copy()          # portion going into the FF backward

        # ── Feed-Forward backward ────────────────────────────────────────────
        ff1_act = cache[f'ff1_act_{l}']    # (B, S, D_ff)
        ff1     = cache[f'ff1_{l}']        # (B, S, D_ff)
        ln2_out = cache[f'ln2_out_{l}']    # (B, S, D)
        D_ff    = ff1.shape[-1]

        # ff2 = ff1_act @ W2 + b2
        grads[f'W2_{l}'] = ff1_act.reshape(-1, D_ff).T @ dx_ff.reshape(-1, D)
        grads[f'b2_{l}'] = dx_ff.sum(axis=(0, 1))
        d_ff1_act = dx_ff @ params[f'W2_{l}'].T        # (B, S, D_ff)

        # ff1_act = gelu(ff1)  →  chain rule through GELU
        d_ff1 = d_ff1_act * gelu_grad(ff1)             # (B, S, D_ff)

        # ff1 = ln2_out @ W1 + b1
        grads[f'W1_{l}'] = ln2_out.reshape(-1, D).T @ d_ff1.reshape(-1, D_ff)
        grads[f'b1_{l}'] = d_ff1.sum(axis=(0, 1))
        d_ln2_out = d_ff1 @ params[f'W1_{l}'].T        # (B, S, D)

        # ── LN2 backward ─────────────────────────────────────────────────────
        d_res1, grads[f'ln2_g_{l}'], grads[f'ln2_b_{l}'] = ln_backward(
            d_ln2_out, cache[f'xh2_{l}'], cache[f'v2_{l}'], params[f'ln2_g_{l}']
        )
        # residual 1: gradient is sum of FF path and identity bypass
        d_after_res1 = dx_ff + d_res1

        # ── Output projection backward: attn_out = merged @ Wo + bo ─────────
        merged = cache[f'merged_{l}']                              # (B, S, D)
        grads[f'Wo_{l}'] = merged.reshape(-1, D).T @ d_after_res1.reshape(-1, D)
        grads[f'bo_{l}'] = d_after_res1.sum(axis=(0, 1))
        d_merged = d_after_res1 @ params[f'Wo_{l}'].T             # (B, S, D)

        # ── Un-merge heads: (B, S, D) → (B, H, S, hd) ──────────────────────
        d_av = d_merged.reshape(B, S, n_heads, head_dim).transpose(0, 2, 1, 3)

        # ── Attention value & weight backward ────────────────────────────────
        # av     = attn_w @ Vt
        # d_Vt   = attn_wᵀ @ d_av
        # d_attn_w = d_av @ Vtᵀ
        Vt     = cache[f'Vt_{l}']                                  # (B, H, S, hd)
        attn_w = cache[f'attn_w_{l}']                              # (B, H, S, S)
        Qt     = cache[f'Qt_{l}']                                  # (B, H, S, hd)
        Kt     = cache[f'Kt_{l}']                                  # (B, H, S, hd)

        d_Vt     = attn_w.transpose(0, 1, 3, 2) @ d_av            # (B, H, S, hd)
        d_attn_w = d_av @ Vt.transpose(0, 1, 3, 2)                # (B, H, S, S)

        # ── Softmax backward ─────────────────────────────────────────────────
        # For s = softmax(z):  dL/dz_i = s_i·(dL/ds_i − Σ_j s_j·dL/ds_j)
        # Compact form: dL/dz = s·(dL/ds − dot(dL/ds, s))
        s       = (d_attn_w * attn_w).sum(axis=-1, keepdims=True) # (B,H,S,1)
        d_scores = attn_w * (d_attn_w - s) * scale                 # (B, H, S, S)
        # causal-masked positions had attn_w=0 so their grad is already 0

        # ── Q·Kᵀ backward ────────────────────────────────────────────────────
        # scores = Q·Kᵀ  →  dQ = dscores·K,  dK = dscoresᵀ·Q
        d_Qt = d_scores @ Kt                                        # (B, H, S, hd)
        d_Kt = d_scores.transpose(0, 1, 3, 2) @ Qt                 # (B, H, S, hd)

        # ── Transpose back: (B, H, S, hd) → (B, S, H, hd) ──────────────────
        d_Q_rope = d_Qt.transpose(0, 2, 1, 3)
        d_K_rope = d_Kt.transpose(0, 2, 1, 3)
        d_Vt_t   = d_Vt.transpose(0, 2, 1, 3)

        # ── RoPE backward ────────────────────────────────────────────────────
        # Rotation is orthogonal: R(θ)^T = R(-θ)
        # So dL/dx = R(-θ)·dL/dy = rope_apply(dL/dy, cos, -sin)
        d_Q = rope_backward(d_Q_rope, cos[:S], sin[:S])             # (B, S, H, hd)
        d_K = rope_backward(d_K_rope, cos[:S], sin[:S])
        # V has no RoPE — gradient flows straight through reshape
        d_V = d_Vt_t                                                 # (B, S, H, hd)

        # reshape to (B, S, D)
        d_Q = d_Q.reshape(B, S, D)
        d_K = d_K.reshape(B, S, D)
        d_V = d_V.reshape(B, S, D)

        # ── QKV projection backward ──────────────────────────────────────────
        ln1_out = cache[f'ln1_out_{l}']                             # (B, S, D)

        grads[f'Wq_{l}'] = ln1_out.reshape(-1, D).T @ d_Q.reshape(-1, D)
        grads[f'bq_{l}'] = d_Q.sum(axis=(0, 1))

        grads[f'Wk_{l}'] = ln1_out.reshape(-1, D).T @ d_K.reshape(-1, D)
        grads[f'bk_{l}'] = d_K.sum(axis=(0, 1))

        grads[f'Wv_{l}'] = ln1_out.reshape(-1, D).T @ d_V.reshape(-1, D)
        grads[f'bv_{l}'] = d_V.sum(axis=(0, 1))

        # gradient w.r.t. ln1 output = sum of Q, K, V paths
        d_ln1_out = (d_Q @ params[f'Wq_{l}'].T
                   + d_K @ params[f'Wk_{l}'].T
                   + d_V @ params[f'Wv_{l}'].T)

        # ── LN1 backward ─────────────────────────────────────────────────────
        d_x_ln1, grads[f'ln1_g_{l}'], grads[f'ln1_b_{l}'] = ln_backward(
            d_ln1_out, cache[f'xh1_{l}'], cache[f'v1_{l}'], params[f'ln1_g_{l}']
        )

        # ── Residual 1: gradient flows through both attention and bypass ─────
        dx = d_after_res1 + d_x_ln1

    # ── Token embedding backward ─────────────────────────────────────────────
    # dx holds dL/d(embedding_output); scatter back to the embedding table
    np.add.at(grads['wte'], cache['tokens'], dx)

    return grads


# ──────────────────────────────────────────────────────────────────────────────
#  8.  ADAM OPTIMISER
# ──────────────────────────────────────────────────────────────────────────────

class Adam:
    """
    Adaptive moment estimation.
      m_t = β1·m_{t-1} + (1−β1)·g          ← first moment  (mean of grads)
      v_t = β2·v_{t-1} + (1−β2)·g²         ← second moment (mean of grad²)
      m̂  = m_t / (1−β1^t)                  ← bias correction
      v̂  = v_t / (1−β2^t)
      θ  ← θ − lr · m̂ / (√v̂ + ε)
    """
    def __init__(self, lr=3e-4, b1=0.9, b2=0.999, eps=1e-8, grad_clip=1.0):
        self.lr   = lr
        self.b1   = b1
        self.b2   = b2
        self.eps  = eps
        self.clip = grad_clip
        self.t    = 0
        self.m = self.v = None

    def step(self, params, grads):
        if self.m is None:
            self.m = {k: np.zeros_like(v) for k, v in params.items()}
            self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t += 1
        for k in params:
            g = np.clip(grads[k], -self.clip, self.clip)   # gradient clipping
            self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g
            self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * g * g
            m_hat = self.m[k] / (1 - self.b1 ** self.t)
            v_hat = self.v[k] / (1 - self.b2 ** self.t)
            params[k] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        return params


# ──────────────────────────────────────────────────────────────────────────────
#  9.  DATA UTILITIES
# ──────────────────────────────────────────────────────────────────────────────

def make_batches(corpus, tokenizer, seq_len, batch_size):
    """
    Tokenise every line, pad/truncate to seq_len+1,
    split into (input, target) pairs shifted by 1.
    """
    lines   = [l.strip() for l in corpus.splitlines() if l.strip()]
    samples = []
    for line in lines:
        ids = tokenizer.encode(line)
        # pad with PAD tokens to fill seq_len+1 slots
        ids = ids + [tokenizer.PAD] * max(0, seq_len + 1 - len(ids))
        ids = ids[:seq_len + 1]
        samples.append(ids)

    arr = np.array(samples, dtype=np.int32)                  # (N, seq+1)
    arr = arr[np.random.permutation(len(arr))]               # shuffle

    batches = []
    for i in range(0, len(arr) - batch_size + 1, batch_size):
        b = arr[i:i + batch_size]
        batches.append((b[:, :-1], b[:, 1:]))               # x, y
    return batches


# ──────────────────────────────────────────────────────────────────────────────
#  10. GRADIENT CHECK  (finite differences vs analytic)
# ──────────────────────────────────────────────────────────────────────────────

def grad_check(params, tokens, targets, n_heads, cos, sin, n_checks=3, eps=1e-4):
    """
    For a random sample of weights, compare:
      analytic gradient  (from backward())
      numerical gradient (finite difference: (L(w+ε) - L(w-ε)) / 2ε)
    A relative error < 1% means the backward is correct.
    """
    print("\n── gradient check ──────────────────────────────────────")
    logits, cache = forward(tokens, params, n_heads, cos, sin)
    loss0, probs  = loss_fn(logits, targets)
    grads         = backward(logits, probs, targets, params, cache, n_heads, cos, sin)

    keys = ['wte', 'Wq_0', 'W1_0', 'lm_head']
    rng  = np.random.default_rng(7)

    for key in keys:
        W = params[key]
        G = grads[key]
        idx = tuple(rng.integers(0, s, n_checks) for s in W.shape)
        for i in range(n_checks):
            coord = tuple(ix[i] for ix in idx)
            old   = float(W[coord])
            W[coord] = old + eps
            lp, _  = loss_fn(forward(tokens, params, n_heads, cos, sin)[0], targets)
            W[coord] = old - eps
            lm, _  = loss_fn(forward(tokens, params, n_heads, cos, sin)[0], targets)
            W[coord] = old

            fd  = (lp - lm) / (2 * eps)
            an  = float(G[coord])
            rel = abs(fd - an) / (abs(fd) + abs(an) + 1e-9)
            tag = "✓" if rel < 1e-2 else "✗  ← MISMATCH"
            coord_str = str(list(coord))
            print(f"  {tag}  {key}{coord_str:30s}  "
                  f"fd={fd:+.5f}  analytic={an:+.5f}  rel_err={rel:.2e}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  11. TEXT GENERATION  (top-k sampling)
# ──────────────────────────────────────────────────────────────────────────────

def generate(prompt, params, tokenizer, n_heads, cos, sin,
             max_new=60, temperature=0.8, top_k=10):
    """
    Autoregressive generation.
    At each step:
      1. Run the model on current context
      2. Take logits of the LAST position only
      3. Apply temperature scaling + top-k masking
      4. Sample from the resulting distribution
      5. Append sampled token and repeat
    """
    ids = tokenizer.encode(prompt)[:-1]   # encode prompt, drop <eos>

    for _ in range(max_new):
        ctx    = np.array(ids[-MAX_SEQ:], dtype=np.int32)[None, :]
        logits, _ = forward(ctx, params, n_heads, cos, sin)

        next_l = logits[0, -1, :] / temperature    # (V,)  last position

        # top-k: keep only the k highest logits
        if top_k > 0:
            topk_vals = np.partition(next_l, -top_k)[-top_k]
            next_l    = np.where(next_l >= topk_vals, next_l, -1e9)

        probs  = softmax(next_l)
        nxt_id = int(np.random.choice(len(probs), p=probs))

        if nxt_id == tokenizer.EOS:
            break
        ids.append(nxt_id)

    return tokenizer.decode(ids)


# ──────────────────────────────────────────────────────────────────────────────
#  12. TRAINING LOOP
# ──────────────────────────────────────────────────────────────────────────────

def train():
    np.random.seed(0)

    tok  = CharTokenizer(CORPUS)
    V    = len(tok)
    hd   = D_MODEL // N_HEADS
    cos, sin = rope_freqs(MAX_SEQ, hd)

    params = init_params(V, D_MODEL, N_HEADS, N_LAYERS, D_FF)
    opt    = Adam(lr=LR, grad_clip=1.0)

    n_p = sum(v.size for v in params.values())
    print("=" * 60)
    print("  Tiny GPT + RoPE  —  pure NumPy")
    print("=" * 60)
    print(f"  vocab size   : {V}")
    print(f"  d_model      : {D_MODEL}    (head_dim = {hd})")
    print(f"  n_heads      : {N_HEADS}")
    print(f"  n_layers     : {N_LAYERS}")
    print(f"  d_ff         : {D_FF}")
    print(f"  parameters   : {n_p:,}")
    print(f"  max seq len  : {MAX_SEQ}")
    print("=" * 60)

    # ── gradient check on a tiny example before training ─────────────────────
    sx = np.array([[tok.BOS,
                    tok.stoi.get('t', 3),
                    tok.stoi.get('h', 4),
                    tok.stoi.get('e', 5)]], dtype=np.int32)
    sy = np.array([[tok.stoi.get('t', 3),
                    tok.stoi.get('h', 4),
                    tok.stoi.get('e', 5),
                    tok.EOS]], dtype=np.int32)
    grad_check(params, sx, sy, N_HEADS, cos, sin)

    # ── main training loop ────────────────────────────────────────────────────
    print(f"Training for {EPOCHS} epochs …\n")
    for epoch in range(1, EPOCHS + 1):
        batches    = make_batches(CORPUS, tok, MAX_SEQ - 1, BATCH)
        epoch_loss = 0.0

        for x, y in batches:
            logits, cache = forward(x, params, N_HEADS, cos, sin)
            loss, probs   = loss_fn(logits, y)
            grads         = backward(logits, probs, y, params, cache, N_HEADS, cos, sin)
            params        = opt.step(params, grads)
            epoch_loss   += loss

        if epoch % 100 == 0:
            avg = epoch_loss / max(len(batches), 1)
            print(f"  epoch {epoch:5d} / {EPOCHS}   loss = {avg:.4f}")

    # ── generation after training ─────────────────────────────────────────────
    print("\n── generation (temperature=0.8, top-k=10) ──────────────")
    prompts = ["the cat", "the dog", "a dog and", "cats and dogs"]
    for p in prompts:
        out = generate(p, params, tok, N_HEADS, cos, sin,
                       max_new=60, temperature=0.8, top_k=10)
        print(f"  prompt: '{p}'")
        print(f"  output: '{out}'\n")

    return params, tok


if __name__ == '__main__':
    params, tok = train() 