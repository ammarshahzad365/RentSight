# ─────────────────────────────────────────────────────────────────────────────
# Islamabad sectors + sub-sectors bounding boxes
# Strategy: generous boxes (~0.012° padding from verified centers) with overlap
# to ensure full coverage. Verified anchor centers sourced from OSM/findlatlong.
# Each sector ~2km x 2km; sub-sectors split into 4 quadrants (~1km each).
# Overlap is intentional — cumulative coverage beats precision gaps.
# ─────────────────────────────────────────────────────────────────────────────

islamabad_sectors = [

    # ══════════════════════════════════════════════════════════════
    # F SECTORS  (west column, north row)
    # Verified: F-6 Markaz ~33.7299,73.0763 | F-7 ~33.7023,73.0417
    #           F-10 bbox from user | F-11 center ~33.6836,72.9907
    # ══════════════════════════════════════════════════════════════

    # ── F-5 (Diplomatic/Constitution Ave area) ───────────────────
    "ne_lat=33.7450&ne_lng=73.0950&sw_lat=33.7350&sw_lng=73.0850",  # F-5/1
    "ne_lat=33.7450&ne_lng=73.0850&sw_lat=33.7350&sw_lng=73.0750",  # F-5/2
    "ne_lat=33.7350&ne_lng=73.0950&sw_lat=33.7250&sw_lng=73.0850",  # F-5/3
    "ne_lat=33.7350&ne_lng=73.0850&sw_lat=33.7250&sw_lng=73.0750",  # F-5/4

    # ── F-6 (verified center ~33.7299, 73.0763) ──────────────────
    "ne_lat=33.7400&ne_lng=73.0870&sw_lat=33.7300&sw_lng=73.0760",  # F-6/1
    "ne_lat=33.7400&ne_lng=73.0760&sw_lat=33.7300&sw_lng=73.0650",  # F-6/2
    "ne_lat=33.7300&ne_lng=73.0870&sw_lat=33.7200&sw_lng=73.0760",  # F-6/3
    "ne_lat=33.7300&ne_lng=73.0760&sw_lat=33.7200&sw_lng=73.0650",  # F-6/4

    # ── F-7 (verified center ~33.7023, 73.0417) ──────────────────
    "ne_lat=33.7200&ne_lng=73.0620&sw_lat=33.7100&sw_lng=73.0510",  # F-7/1
    "ne_lat=33.7200&ne_lng=73.0510&sw_lat=33.7100&sw_lng=73.0400",  # F-7/2
    "ne_lat=33.7100&ne_lng=73.0620&sw_lat=33.7000&sw_lng=73.0510",  # F-7/3
    "ne_lat=33.7100&ne_lng=73.0510&sw_lat=33.7000&sw_lng=73.0400",  # F-7/4

    # ── F-8 (between F-7 and F-9, ~33.718, 73.022) ───────────────
    "ne_lat=33.7280&ne_lng=73.0420&sw_lat=33.7180&sw_lng=73.0310",  # F-8/1
    "ne_lat=33.7280&ne_lng=73.0310&sw_lat=33.7180&sw_lng=73.0200",  # F-8/2
    "ne_lat=33.7180&ne_lng=73.0420&sw_lat=33.7080&sw_lng=73.0310",  # F-8/3
    "ne_lat=33.7180&ne_lng=73.0310&sw_lat=33.7080&sw_lng=73.0200",  # F-8/4

    # ── F-9 (Fatima Jinnah Park, ~33.710, 73.002) ────────────────
    "ne_lat=33.7180&ne_lng=73.0220&sw_lat=33.7080&sw_lng=73.0110",  # F-9/1
    "ne_lat=33.7180&ne_lng=73.0110&sw_lat=33.7080&sw_lng=73.0000",  # F-9/2
    "ne_lat=33.7080&ne_lng=73.0220&sw_lat=33.6980&sw_lng=73.0110",  # F-9/3
    "ne_lat=33.7080&ne_lng=73.0110&sw_lat=33.6980&sw_lng=73.0000",  # F-9/4

    # ── F-10 (GROUND TRUTH from user bbox) ───────────────────────
    "ne_lat=33.7012&ne_lng=73.0149&sw_lat=33.6932&sw_lng=73.0059",  # F-10/1
    "ne_lat=33.7012&ne_lng=73.0059&sw_lat=33.6932&sw_lng=72.9969",  # F-10/2
    "ne_lat=33.6932&ne_lng=73.0149&sw_lat=33.6852&sw_lng=73.0059",  # F-10/3
    "ne_lat=33.6932&ne_lng=73.0059&sw_lat=33.6852&sw_lng=72.9969",  # F-10/4

    # ── F-11 (verified center ~33.6836, 72.9907) ─────────────────
    "ne_lat=33.6980&ne_lng=73.0010&sw_lat=33.6880&sw_lng=72.9900",  # F-11/1
    "ne_lat=33.6980&ne_lng=72.9900&sw_lat=33.6880&sw_lng=72.9790",  # F-11/2
    "ne_lat=33.6880&ne_lng=73.0010&sw_lat=33.6780&sw_lng=72.9900",  # F-11/3
    "ne_lat=33.6880&ne_lng=72.9900&sw_lat=33.6780&sw_lng=72.9790",  # F-11/4

    # ── F-17 (Tarlai area, north ~33.710, lng ~72.957) ───────────
    "ne_lat=33.7200&ne_lng=72.9700&sw_lat=33.7100&sw_lng=72.9590",  # F-17/1
    "ne_lat=33.7200&ne_lng=72.9590&sw_lat=33.7100&sw_lng=72.9480",  # F-17/2
    "ne_lat=33.7100&ne_lng=72.9700&sw_lat=33.7000&sw_lng=72.9590",  # F-17/3
    "ne_lat=33.7100&ne_lng=72.9590&sw_lat=33.7000&sw_lng=72.9480",  # F-17/4

    # ══════════════════════════════════════════════════════════════
    # E SECTORS (north of F, same lng column)
    # ══════════════════════════════════════════════════════════════

    # ── E-7 (~33.748, 73.040) ─────────────────────────────────────
    "ne_lat=33.7580&ne_lng=73.0520&sw_lat=33.7480&sw_lng=73.0410",  # E-7/1
    "ne_lat=33.7580&ne_lng=73.0410&sw_lat=33.7480&sw_lng=73.0300",  # E-7/2
    "ne_lat=33.7480&ne_lng=73.0520&sw_lat=33.7380&sw_lng=73.0410",  # E-7/3
    "ne_lat=33.7480&ne_lng=73.0410&sw_lat=33.7380&sw_lng=73.0300",  # E-7/4

    # ── E-8 (~33.748, 73.022) ─────────────────────────────────────
    "ne_lat=33.7580&ne_lng=73.0320&sw_lat=33.7480&sw_lng=73.0210",  # E-8/1
    "ne_lat=33.7580&ne_lng=73.0210&sw_lat=33.7480&sw_lng=73.0100",  # E-8/2
    "ne_lat=33.7480&ne_lng=73.0320&sw_lat=33.7380&sw_lng=73.0210",  # E-8/3
    "ne_lat=33.7480&ne_lng=73.0210&sw_lat=33.7380&sw_lng=73.0100",  # E-8/4

    # ── E-9 (Air University area, ~33.748, 73.003) ────────────────
    "ne_lat=33.7580&ne_lng=73.0130&sw_lat=33.7480&sw_lng=73.0020",  # E-9/1
    "ne_lat=33.7580&ne_lng=73.0020&sw_lat=33.7480&sw_lng=72.9910",  # E-9/2
    "ne_lat=33.7480&ne_lng=73.0130&sw_lat=33.7380&sw_lng=73.0020",  # E-9/3
    "ne_lat=33.7480&ne_lng=73.0020&sw_lat=33.7380&sw_lng=72.9910",  # E-9/4

    # ── E-10 (~33.748, 72.984) ────────────────────────────────────
    "ne_lat=33.7580&ne_lng=72.9940&sw_lat=33.7480&sw_lng=72.9830",  # E-10/1
    "ne_lat=33.7580&ne_lng=72.9830&sw_lat=33.7480&sw_lng=72.9720",  # E-10/2
    "ne_lat=33.7480&ne_lng=72.9940&sw_lat=33.7380&sw_lng=72.9830",  # E-10/3
    "ne_lat=33.7480&ne_lng=72.9830&sw_lat=33.7380&sw_lng=72.9720",  # E-10/4

    # ── E-11 (~33.748, 72.966) ────────────────────────────────────
    "ne_lat=33.7580&ne_lng=72.9760&sw_lat=33.7480&sw_lng=72.9650",  # E-11/1
    "ne_lat=33.7580&ne_lng=72.9650&sw_lat=33.7480&sw_lng=72.9540",  # E-11/2
    "ne_lat=33.7480&ne_lng=72.9760&sw_lat=33.7380&sw_lng=72.9650",  # E-11/3
    "ne_lat=33.7480&ne_lng=72.9650&sw_lat=33.7380&sw_lng=72.9540",  # E-11/4

    # ── E-12 (~33.748, 72.948) ────────────────────────────────────
    "ne_lat=33.7580&ne_lng=72.9580&sw_lat=33.7480&sw_lng=72.9470",  # E-12/1
    "ne_lat=33.7580&ne_lng=72.9470&sw_lat=33.7480&sw_lng=72.9360",  # E-12/2
    "ne_lat=33.7480&ne_lng=72.9580&sw_lat=33.7380&sw_lng=72.9470",  # E-12/3
    "ne_lat=33.7480&ne_lng=72.9470&sw_lat=33.7380&sw_lng=72.9360",  # E-12/4

    # ── E-16 / E-17 (far west, Margalla/PWD fringe) ──────────────
    "ne_lat=33.7580&ne_lng=72.9000&sw_lat=33.7380&sw_lng=72.8800",  # E-16 (wide box)
    "ne_lat=33.7680&ne_lng=72.9200&sw_lat=33.7480&sw_lng=72.9000",  # E-17 (wide box)

    # ══════════════════════════════════════════════════════════════
    # D SECTORS
    # ══════════════════════════════════════════════════════════════

    # ── D-12 (~33.765, 73.000) ────────────────────────────────────
    "ne_lat=33.7750&ne_lng=73.0100&sw_lat=33.7650&sw_lng=72.9990",  # D-12/1
    "ne_lat=33.7750&ne_lng=72.9990&sw_lat=33.7650&sw_lng=72.9880",  # D-12/2
    "ne_lat=33.7650&ne_lng=73.0100&sw_lat=33.7550&sw_lng=72.9990",  # D-12/3
    "ne_lat=33.7650&ne_lng=72.9990&sw_lat=33.7550&sw_lng=72.9880",  # D-12/4

    # ── D-17 (Multi Gardens, B-17 adjacent, ~33.775, 72.944) ─────
    "ne_lat=33.7850&ne_lng=72.9550&sw_lat=33.7750&sw_lng=72.9440",  # D-17/1
    "ne_lat=33.7850&ne_lng=72.9440&sw_lat=33.7750&sw_lng=72.9330",  # D-17/2
    "ne_lat=33.7750&ne_lng=72.9550&sw_lat=33.7650&sw_lng=72.9440",  # D-17/3
    "ne_lat=33.7750&ne_lng=72.9440&sw_lat=33.7650&sw_lng=72.9330",  # D-17/4

    # ══════════════════════════════════════════════════════════════
    # C SECTORS
    # ══════════════════════════════════════════════════════════════

    # ── C-14 (~33.793, 72.970) ────────────────────────────────────
    "ne_lat=33.8030&ne_lng=72.9800&sw_lat=33.7930&sw_lng=72.9690",  # C-14/1
    "ne_lat=33.8030&ne_lng=72.9690&sw_lat=33.7930&sw_lng=72.9580",  # C-14/2
    "ne_lat=33.7930&ne_lng=72.9800&sw_lat=33.7830&sw_lng=72.9690",  # C-14/3
    "ne_lat=33.7930&ne_lng=72.9690&sw_lat=33.7830&sw_lng=72.9580",  # C-14/4

    # ── C-15 (~33.793, 72.950) ────────────────────────────────────
    "ne_lat=33.8030&ne_lng=72.9600&sw_lat=33.7930&sw_lng=72.9490",  # C-15/1
    "ne_lat=33.8030&ne_lng=72.9490&sw_lat=33.7930&sw_lng=72.9380",  # C-15/2
    "ne_lat=33.7930&ne_lng=72.9600&sw_lat=33.7830&sw_lng=72.9490",  # C-15/3
    "ne_lat=33.7930&ne_lng=72.9490&sw_lat=33.7830&sw_lng=72.9380",  # C-15/4

    # ══════════════════════════════════════════════════════════════
    # B SECTORS
    # ══════════════════════════════════════════════════════════════

    # ── B-17 (Multi Gardens, ~33.803, 72.942) ────────────────────
    "ne_lat=33.8130&ne_lng=72.9530&sw_lat=33.8030&sw_lng=72.9420",  # B-17/1
    "ne_lat=33.8130&ne_lng=72.9420&sw_lat=33.8030&sw_lng=72.9310",  # B-17/2
    "ne_lat=33.8030&ne_lng=72.9530&sw_lat=33.7930&sw_lng=72.9420",  # B-17/3
    "ne_lat=33.8030&ne_lng=72.9420&sw_lat=33.7930&sw_lng=72.9310",  # B-17/4

    # ══════════════════════════════════════════════════════════════
    # G SECTORS  (south of F row)
    # Verified: G-7 ~33.7053,73.0671 | G-10 ~33.6760,73.0140
    #           G-11 ~33.6681,72.9963 | G-13 ~33.6500,72.9638
    # ══════════════════════════════════════════════════════════════

    # ── G-5 (Diplomatic Enclave fringe, ~33.718, 73.085) ─────────
    "ne_lat=33.7280&ne_lng=73.0960&sw_lat=33.7180&sw_lng=73.0850",  # G-5/1
    "ne_lat=33.7280&ne_lng=73.0850&sw_lat=33.7180&sw_lng=73.0740",  # G-5/2
    "ne_lat=33.7180&ne_lng=73.0960&sw_lat=33.7080&sw_lng=73.0850",  # G-5/3
    "ne_lat=33.7180&ne_lng=73.0850&sw_lat=33.7080&sw_lng=73.0740",  # G-5/4

    # ── G-6 (Aabpara, ~33.710, 73.076) ───────────────────────────
    "ne_lat=33.7180&ne_lng=73.0870&sw_lat=33.7080&sw_lng=73.0760",  # G-6/1
    "ne_lat=33.7180&ne_lng=73.0760&sw_lat=33.7080&sw_lng=73.0650",  # G-6/2
    "ne_lat=33.7080&ne_lng=73.0870&sw_lat=33.6980&sw_lng=73.0760",  # G-6/3
    "ne_lat=33.7080&ne_lng=73.0760&sw_lat=33.6980&sw_lng=73.0650",  # G-6/4

    # ── G-7 (verified center ~33.7053, 73.0671) ──────────────────
    "ne_lat=33.7150&ne_lng=73.0780&sw_lat=33.7050&sw_lng=73.0670",  # G-7/1
    "ne_lat=33.7150&ne_lng=73.0670&sw_lat=33.7050&sw_lng=73.0560",  # G-7/2
    "ne_lat=33.7050&ne_lng=73.0780&sw_lat=33.6950&sw_lng=73.0670",  # G-7/3
    "ne_lat=33.7050&ne_lng=73.0670&sw_lat=33.6950&sw_lng=73.0560",  # G-7/4

    # ── G-8 (~33.692, 73.056) ─────────────────────────────────────
    "ne_lat=33.7020&ne_lng=73.0670&sw_lat=33.6920&sw_lng=73.0560",  # G-8/1
    "ne_lat=33.7020&ne_lng=73.0560&sw_lat=33.6920&sw_lng=73.0450",  # G-8/2
    "ne_lat=33.6920&ne_lng=73.0670&sw_lat=33.6820&sw_lng=73.0560",  # G-8/3
    "ne_lat=33.6920&ne_lng=73.0560&sw_lat=33.6820&sw_lng=73.0450",  # G-8/4

    # ── G-9 (Karachi Company, ~33.683, 73.039) ───────────────────
    "ne_lat=33.6930&ne_lng=73.0490&sw_lat=33.6830&sw_lng=73.0380",  # G-9/1
    "ne_lat=33.6930&ne_lng=73.0380&sw_lat=33.6830&sw_lng=73.0270",  # G-9/2
    "ne_lat=33.6830&ne_lng=73.0490&sw_lat=33.6730&sw_lng=73.0380",  # G-9/3
    "ne_lat=33.6830&ne_lng=73.0380&sw_lat=33.6730&sw_lng=73.0270",  # G-9/4

    # ── G-10 (verified center ~33.6760, 73.0140) ─────────────────
    "ne_lat=33.6860&ne_lng=73.0240&sw_lat=33.6760&sw_lng=73.0130",  # G-10/1
    "ne_lat=33.6860&ne_lng=73.0130&sw_lat=33.6760&sw_lng=73.0020",  # G-10/2
    "ne_lat=33.6760&ne_lng=73.0240&sw_lat=33.6660&sw_lng=73.0130",  # G-10/3
    "ne_lat=33.6760&ne_lng=73.0130&sw_lat=33.6660&sw_lng=73.0020",  # G-10/4

    # ── G-11 (verified center ~33.6681, 72.9963) ─────────────────
    "ne_lat=33.6780&ne_lng=73.0060&sw_lat=33.6680&sw_lng=72.9950",  # G-11/1
    "ne_lat=33.6780&ne_lng=72.9950&sw_lat=33.6680&sw_lng=72.9840",  # G-11/2
    "ne_lat=33.6680&ne_lng=73.0060&sw_lat=33.6580&sw_lng=72.9950",  # G-11/3
    "ne_lat=33.6680&ne_lng=72.9950&sw_lat=33.6580&sw_lng=72.9840",  # G-11/4

    # ── G-13 (verified center ~33.6500, 72.9638) ─────────────────
    "ne_lat=33.6600&ne_lng=72.9740&sw_lat=33.6500&sw_lng=72.9630",  # G-13/1
    "ne_lat=33.6600&ne_lng=72.9630&sw_lat=33.6500&sw_lng=72.9520",  # G-13/2
    "ne_lat=33.6500&ne_lng=72.9740&sw_lat=33.6400&sw_lng=72.9630",  # G-13/3
    "ne_lat=33.6500&ne_lng=72.9630&sw_lat=33.6400&sw_lng=72.9520",  # G-13/4

    # ── G-14 (~33.632, 72.946) ────────────────────────────────────
    "ne_lat=33.6420&ne_lng=72.9560&sw_lat=33.6320&sw_lng=72.9450",  # G-14/1
    "ne_lat=33.6420&ne_lng=72.9450&sw_lat=33.6320&sw_lng=72.9340",  # G-14/2
    "ne_lat=33.6320&ne_lng=72.9560&sw_lat=33.6220&sw_lng=72.9450",  # G-14/3
    "ne_lat=33.6320&ne_lng=72.9450&sw_lat=33.6220&sw_lng=72.9340",  # G-14/4

    # ── G-15 (~33.615, 72.928) ────────────────────────────────────
    "ne_lat=33.6250&ne_lng=72.9380&sw_lat=33.6150&sw_lng=72.9270",  # G-15/1
    "ne_lat=33.6250&ne_lng=72.9270&sw_lat=33.6150&sw_lng=72.9160",  # G-15/2
    "ne_lat=33.6150&ne_lng=72.9380&sw_lat=33.6050&sw_lng=72.9270",  # G-15/3
    "ne_lat=33.6150&ne_lng=72.9270&sw_lat=33.6050&sw_lng=72.9160",  # G-15/4

    # ── G-16 (~33.598, 72.910) ────────────────────────────────────
    "ne_lat=33.6080&ne_lng=72.9200&sw_lat=33.5980&sw_lng=72.9090",  # G-16/1
    "ne_lat=33.6080&ne_lng=72.9090&sw_lat=33.5980&sw_lng=72.8980",  # G-16/2
    "ne_lat=33.5980&ne_lng=72.9200&sw_lat=33.5880&sw_lng=72.9090",  # G-16/3
    "ne_lat=33.5980&ne_lng=72.9090&sw_lat=33.5880&sw_lng=72.8980",  # G-16/4

    # ══════════════════════════════════════════════════════════════
    # H SECTORS (south of G row)
    # ══════════════════════════════════════════════════════════════

    # ── H-8 (~33.659, 73.065) ─────────────────────────────────────
    "ne_lat=33.6690&ne_lng=73.0760&sw_lat=33.6590&sw_lng=73.0650",  # H-8/1
    "ne_lat=33.6690&ne_lng=73.0650&sw_lat=33.6590&sw_lng=73.0540",  # H-8/2
    "ne_lat=33.6590&ne_lng=73.0760&sw_lat=33.6490&sw_lng=73.0650",  # H-8/3
    "ne_lat=33.6590&ne_lng=73.0650&sw_lat=33.6490&sw_lng=73.0540",  # H-8/4

    # ── H-9 (~33.650, 73.049) ─────────────────────────────────────
    "ne_lat=33.6600&ne_lng=73.0590&sw_lat=33.6500&sw_lng=73.0480",  # H-9/1
    "ne_lat=33.6600&ne_lng=73.0480&sw_lat=33.6500&sw_lng=73.0370",  # H-9/2
    "ne_lat=33.6500&ne_lng=73.0590&sw_lat=33.6400&sw_lng=73.0480",  # H-9/3
    "ne_lat=33.6500&ne_lng=73.0480&sw_lat=33.6400&sw_lng=73.0370",  # H-9/4

    # ── H-10 (IIUI, ~33.650, 73.032) ─────────────────────────────
    "ne_lat=33.6600&ne_lng=73.0420&sw_lat=33.6500&sw_lng=73.0310",  # H-10/1
    "ne_lat=33.6600&ne_lng=73.0310&sw_lat=33.6500&sw_lng=73.0200",  # H-10/2
    "ne_lat=33.6500&ne_lng=73.0420&sw_lat=33.6400&sw_lng=73.0310",  # H-10/3
    "ne_lat=33.6500&ne_lng=73.0310&sw_lat=33.6400&sw_lng=73.0200",  # H-10/4

    # ── H-11 (~33.650, 73.015) ────────────────────────────────────
    "ne_lat=33.6600&ne_lng=73.0250&sw_lat=33.6500&sw_lng=73.0140",  # H-11/1
    "ne_lat=33.6600&ne_lng=73.0140&sw_lat=33.6500&sw_lng=73.0030",  # H-11/2
    "ne_lat=33.6500&ne_lng=73.0250&sw_lat=33.6400&sw_lng=73.0140",  # H-11/3
    "ne_lat=33.6500&ne_lng=73.0140&sw_lat=33.6400&sw_lng=73.0030",  # H-11/4

    # ── H-12 (NUST, ~33.645, 72.998) ─────────────────────────────
    "ne_lat=33.6550&ne_lng=73.0080&sw_lat=33.6450&sw_lng=72.9970",  # H-12/1
    "ne_lat=33.6550&ne_lng=72.9970&sw_lat=33.6450&sw_lng=72.9860",  # H-12/2
    "ne_lat=33.6450&ne_lng=73.0080&sw_lat=33.6350&sw_lng=72.9970",  # H-12/3
    "ne_lat=33.6450&ne_lng=72.9970&sw_lat=33.6350&sw_lng=72.9860",  # H-12/4

    # ── H-13 (~33.633, 72.981) ────────────────────────────────────
    "ne_lat=33.6430&ne_lng=72.9910&sw_lat=33.6330&sw_lng=72.9800",  # H-13/1
    "ne_lat=33.6430&ne_lng=72.9800&sw_lat=33.6330&sw_lng=72.9690",  # H-13/2
    "ne_lat=33.6330&ne_lng=72.9910&sw_lat=33.6230&sw_lng=72.9800",  # H-13/3
    "ne_lat=33.6330&ne_lng=72.9800&sw_lat=33.6230&sw_lng=72.9690",  # H-13/4

    # ══════════════════════════════════════════════════════════════
    # I SECTORS (south of H row, east side — industrial/residential)
    # Verified: I-8 ~33.6691,73.0730 | I-9 ~33.6601,73.0553
    # ══════════════════════════════════════════════════════════════

    # ── I-8 (verified center ~33.6691, 73.0730) ──────────────────
    "ne_lat=33.6790&ne_lng=73.0840&sw_lat=33.6690&sw_lng=73.0730",  # I-8/1
    "ne_lat=33.6790&ne_lng=73.0730&sw_lat=33.6690&sw_lng=73.0620",  # I-8/2
    "ne_lat=33.6690&ne_lng=73.0840&sw_lat=33.6590&sw_lng=73.0730",  # I-8/3
    "ne_lat=33.6690&ne_lng=73.0730&sw_lat=33.6590&sw_lng=73.0620",  # I-8/4

    # ── I-9 (verified center ~33.6601, 73.0553) ──────────────────
    "ne_lat=33.6700&ne_lng=73.0660&sw_lat=33.6600&sw_lng=73.0550",  # I-9/1
    "ne_lat=33.6700&ne_lng=73.0550&sw_lat=33.6600&sw_lng=73.0440",  # I-9/2
    "ne_lat=33.6600&ne_lng=73.0660&sw_lat=33.6500&sw_lng=73.0550",  # I-9/3
    "ne_lat=33.6600&ne_lng=73.0550&sw_lat=33.6500&sw_lng=73.0440",  # I-9/4

    # ── I-10 (~33.660, 73.038) ────────────────────────────────────
    "ne_lat=33.6700&ne_lng=73.0480&sw_lat=33.6600&sw_lng=73.0370",  # I-10/1
    "ne_lat=33.6700&ne_lng=73.0370&sw_lat=33.6600&sw_lng=73.0260",  # I-10/2
    "ne_lat=33.6600&ne_lng=73.0480&sw_lat=33.6500&sw_lng=73.0370",  # I-10/3
    "ne_lat=33.6600&ne_lng=73.0370&sw_lat=33.6500&sw_lng=73.0260",  # I-10/4

    # ── I-11 (Fruit/Vegetable Market area, ~33.660, 73.020) ──────
    "ne_lat=33.6700&ne_lng=73.0300&sw_lat=33.6600&sw_lng=73.0190",  # I-11/1
    "ne_lat=33.6700&ne_lng=73.0190&sw_lat=33.6600&sw_lng=73.0080",  # I-11/2
    "ne_lat=33.6600&ne_lng=73.0300&sw_lat=33.6500&sw_lng=73.0190",  # I-11/3
    "ne_lat=33.6600&ne_lng=73.0190&sw_lat=33.6500&sw_lng=73.0080",  # I-11/4

    # ── I-12 (~33.650, 73.003) ────────────────────────────────────
    "ne_lat=33.6600&ne_lng=73.0130&sw_lat=33.6500&sw_lng=73.0020",  # I-12/1
    "ne_lat=33.6600&ne_lng=73.0020&sw_lat=33.6500&sw_lng=72.9910",  # I-12/2
    "ne_lat=33.6500&ne_lng=73.0130&sw_lat=33.6400&sw_lng=73.0020",  # I-12/3
    "ne_lat=33.6500&ne_lng=73.0020&sw_lat=33.6400&sw_lng=72.9910",  # I-12/4

    # ── I-14 (~33.630, 72.975) ────────────────────────────────────
    "ne_lat=33.6400&ne_lng=72.9850&sw_lat=33.6300&sw_lng=72.9740",  # I-14/1
    "ne_lat=33.6400&ne_lng=72.9740&sw_lat=33.6300&sw_lng=72.9630",  # I-14/2
    "ne_lat=33.6300&ne_lng=72.9850&sw_lat=33.6200&sw_lng=72.9740",  # I-14/3
    "ne_lat=33.6300&ne_lng=72.9740&sw_lat=33.6200&sw_lng=72.9630",  # I-14/4

    # ── I-15 (~33.615, 72.958) ────────────────────────────────────
    "ne_lat=33.6250&ne_lng=72.9680&sw_lat=33.6150&sw_lng=72.9570",  # I-15/1
    "ne_lat=33.6250&ne_lng=72.9570&sw_lat=33.6150&sw_lng=72.9460",  # I-15/2
    "ne_lat=33.6150&ne_lng=72.9680&sw_lat=33.6050&sw_lng=72.9570",  # I-15/3
    "ne_lat=33.6150&ne_lng=72.9570&sw_lat=33.6050&sw_lng=72.9460",  # I-15/4

    # ── I-16 (~33.600, 72.941) ────────────────────────────────────
    "ne_lat=33.6100&ne_lng=72.9510&sw_lat=33.6000&sw_lng=72.9400",  # I-16/1
    "ne_lat=33.6100&ne_lng=72.9400&sw_lat=33.6000&sw_lng=72.9290",  # I-16/2
    "ne_lat=33.6000&ne_lng=72.9510&sw_lat=33.5900&sw_lng=72.9400",  # I-16/3
    "ne_lat=33.6000&ne_lng=72.9400&sw_lat=33.5900&sw_lng=72.9290",  # I-16/4

    # ══════════════════════════════════════════════════════════════
    # DHA ISLAMABAD / RAWALPINDI
    # (southeast of main sectors, ~33.52-33.58, 73.07-73.14)
    # ══════════════════════════════════════════════════════════════

    # ── DHA Phase 1 ───────────────────────────────────────────────
    "ne_lat=33.5800&ne_lng=73.1200&sw_lat=33.5650&sw_lng=73.1050",  # DHA Ph1 - NE
    "ne_lat=33.5800&ne_lng=73.1050&sw_lat=33.5650&sw_lng=73.0900",  # DHA Ph1 - NW
    "ne_lat=33.5650&ne_lng=73.1200&sw_lat=33.5500&sw_lng=73.1050",  # DHA Ph1 - SE
    "ne_lat=33.5650&ne_lng=73.1050&sw_lat=33.5500&sw_lng=73.0900",  # DHA Ph1 - SW

    # ── DHA Phase 2 ───────────────────────────────────────────────
    "ne_lat=33.5500&ne_lng=73.1300&sw_lat=33.5350&sw_lng=73.1150",  # DHA Ph2 - NE
    "ne_lat=33.5500&ne_lng=73.1150&sw_lat=33.5350&sw_lng=73.1000",  # DHA Ph2 - NW
    "ne_lat=33.5350&ne_lng=73.1300&sw_lat=33.5200&sw_lng=73.1150",  # DHA Ph2 - SE
    "ne_lat=33.5350&ne_lng=73.1150&sw_lat=33.5200&sw_lng=73.1000",  # DHA Ph2 - SW

    # ── DHA Phase 3 ───────────────────────────────────────────────
    "ne_lat=33.5450&ne_lng=73.1100&sw_lat=33.5300&sw_lng=73.0950",  # DHA Ph3 - NE
    "ne_lat=33.5450&ne_lng=73.0950&sw_lat=33.5300&sw_lng=73.0800",  # DHA Ph3 - NW
    "ne_lat=33.5300&ne_lng=73.1100&sw_lat=33.5150&sw_lng=73.0950",  # DHA Ph3 - SE
    "ne_lat=33.5300&ne_lng=73.0950&sw_lat=33.5150&sw_lng=73.0800",  # DHA Ph3 - SW

    # ── DHA Phase 4 ───────────────────────────────────────────────
    "ne_lat=33.5200&ne_lng=73.1100&sw_lat=33.5050&sw_lng=73.0950",  # DHA Ph4 - NE
    "ne_lat=33.5200&ne_lng=73.0950&sw_lat=33.5050&sw_lng=73.0800",  # DHA Ph4 - NW
    "ne_lat=33.5050&ne_lng=73.1100&sw_lat=33.4900&sw_lng=73.0950",  # DHA Ph4 - SE
    "ne_lat=33.5050&ne_lng=73.0950&sw_lat=33.4900&sw_lng=73.0800",  # DHA Ph4 - SW

    # ── DHA Phase 5 ───────────────────────────────────────────────
    "ne_lat=33.5700&ne_lng=73.1450&sw_lat=33.5550&sw_lng=73.1300",  # DHA Ph5 - NE
    "ne_lat=33.5700&ne_lng=73.1300&sw_lat=33.5550&sw_lng=73.1150",  # DHA Ph5 - NW
    "ne_lat=33.5550&ne_lng=73.1450&sw_lat=33.5400&sw_lng=73.1300",  # DHA Ph5 - SE
    "ne_lat=33.5550&ne_lng=73.1300&sw_lat=33.5400&sw_lng=73.1150",  # DHA Ph5 - SW

    # ══════════════════════════════════════════════════════════════
    # BAHRIA TOWN ISLAMABAD
    # (southwest of main sectors, ~33.48-33.55, 72.97-73.04)
    # ══════════════════════════════════════════════════════════════

    # ── Bahria Town Phase 1 ───────────────────────────────────────
    "ne_lat=33.5550&ne_lng=73.0400&sw_lat=33.5400&sw_lng=73.0250",  # Bahria Ph1 - NE
    "ne_lat=33.5550&ne_lng=73.0250&sw_lat=33.5400&sw_lng=73.0100",  # Bahria Ph1 - NW
    "ne_lat=33.5400&ne_lng=73.0400&sw_lat=33.5250&sw_lng=73.0250",  # Bahria Ph1 - SE
    "ne_lat=33.5400&ne_lng=73.0250&sw_lat=33.5250&sw_lng=73.0100",  # Bahria Ph1 - SW

    # ── Bahria Town Phase 2 ───────────────────────────────────────
    "ne_lat=33.5250&ne_lng=73.0350&sw_lat=33.5100&sw_lng=73.0200",  # Bahria Ph2 - NE
    "ne_lat=33.5250&ne_lng=73.0200&sw_lat=33.5100&sw_lng=73.0050",  # Bahria Ph2 - NW
    "ne_lat=33.5100&ne_lng=73.0350&sw_lat=33.4950&sw_lng=73.0200",  # Bahria Ph2 - SE
    "ne_lat=33.5100&ne_lng=73.0200&sw_lat=33.4950&sw_lng=73.0050",  # Bahria Ph2 - SW

    # ── Bahria Town Phase 3 ───────────────────────────────────────
    "ne_lat=33.5050&ne_lng=73.0100&sw_lat=33.4900&sw_lng=72.9950",  # Bahria Ph3 - NE
    "ne_lat=33.5050&ne_lng=72.9950&sw_lat=33.4900&sw_lng=72.9800",  # Bahria Ph3 - NW
    "ne_lat=33.4900&ne_lng=73.0100&sw_lat=33.4750&sw_lng=72.9950",  # Bahria Ph3 - SE
    "ne_lat=33.4900&ne_lng=72.9950&sw_lat=33.4750&sw_lng=72.9800",  # Bahria Ph3 - SW

    # ── Bahria Town Phase 4 ───────────────────────────────────────
    "ne_lat=33.5400&ne_lng=72.9950&sw_lat=33.5250&sw_lng=72.9800",  # Bahria Ph4 - NE
    "ne_lat=33.5400&ne_lng=72.9800&sw_lat=33.5250&sw_lng=72.9650",  # Bahria Ph4 - NW
    "ne_lat=33.5250&ne_lng=72.9950&sw_lat=33.5100&sw_lng=72.9800",  # Bahria Ph4 - SE
    "ne_lat=33.5250&ne_lng=72.9800&sw_lat=33.5100&sw_lng=72.9650",  # Bahria Ph4 - SW

    # ── Bahria Town Phase 7 (Enclave / newer phases) ──────────────
    "ne_lat=33.5700&ne_lng=73.0100&sw_lat=33.5550&sw_lng=72.9950",  # Bahria Ph7 - NE
    "ne_lat=33.5700&ne_lng=72.9950&sw_lat=33.5550&sw_lng=72.9800",  # Bahria Ph7 - NW
    "ne_lat=33.5550&ne_lng=73.0100&sw_lat=33.5400&sw_lng=72.9950",  # Bahria Ph7 - SE
    "ne_lat=33.5550&ne_lng=72.9950&sw_lat=33.5400&sw_lng=72.9800",  # Bahria Ph7 - SW

    # ══════════════════════════════════════════════════════════════
    # GULBERG ISLAMABAD
    # ══════════════════════════════════════════════════════════════

    # ── Gulberg Greens (~33.625, 72.994) ─────────────────────────
    "ne_lat=33.6350&ne_lng=73.0040&sw_lat=33.6250&sw_lng=72.9930",  # Gulberg Greens - NE
    "ne_lat=33.6350&ne_lng=72.9930&sw_lat=33.6250&sw_lng=72.9820",  # Gulberg Greens - NW
    "ne_lat=33.6250&ne_lng=73.0040&sw_lat=33.6150&sw_lng=72.9930",  # Gulberg Greens - SE
    "ne_lat=33.6250&ne_lng=72.9930&sw_lat=33.6150&sw_lng=72.9820",  # Gulberg Greens - SW

    # ── Gulberg Residencia (~33.610, 72.984) ─────────────────────
    "ne_lat=33.6200&ne_lng=72.9940&sw_lat=33.6100&sw_lng=72.9830",  # Gulberg Res - NE
    "ne_lat=33.6200&ne_lng=72.9830&sw_lat=33.6100&sw_lng=72.9720",  # Gulberg Res - NW
    "ne_lat=33.6100&ne_lng=72.9940&sw_lat=33.6000&sw_lng=72.9830",  # Gulberg Res - SE
    "ne_lat=33.6100&ne_lng=72.9830&sw_lat=33.6000&sw_lng=72.9720",  # Gulberg Res - SW

    # ══════════════════════════════════════════════════════════════
    # SATELLITE TOWN / PWD / MISC ISLAMABAD AREAS
    # ══════════════════════════════════════════════════════════════

    # ── PWD Housing Society (~33.644, 73.092) ────────────────────
    "ne_lat=33.6540&ne_lng=73.1020&sw_lat=33.6440&sw_lng=73.0920",  # PWD - NE
    "ne_lat=33.6540&ne_lng=73.0920&sw_lat=33.6440&sw_lng=73.0820",  # PWD - NW
    "ne_lat=33.6440&ne_lng=73.1020&sw_lat=33.6340&sw_lng=73.0920",  # PWD - SE
    "ne_lat=33.6440&ne_lng=73.0920&sw_lat=33.6340&sw_lng=73.0820",  # PWD - SW

    # ── Satellite Town (~33.636, 73.078) ─────────────────────────
    "ne_lat=33.6460&ne_lng=73.0880&sw_lat=33.6360&sw_lng=73.0780",  # Satellite Town - NE
    "ne_lat=33.6460&ne_lng=73.0780&sw_lat=33.6360&sw_lng=73.0680",  # Satellite Town - NW
    "ne_lat=33.6360&ne_lng=73.0880&sw_lat=33.6260&sw_lng=73.0780",  # Satellite Town - SE
    "ne_lat=33.6360&ne_lng=73.0780&sw_lat=33.6260&sw_lng=73.0680",  # Satellite Town - SW

    # ── Blue Area / Zero Point (~33.726, 73.090) ─────────────────
    "ne_lat=33.7360&ne_lng=73.1000&sw_lat=33.7260&sw_lng=73.0900",  # Blue Area - East
    "ne_lat=33.7360&ne_lng=73.0900&sw_lat=33.7260&sw_lng=73.0800",  # Blue Area - West

    # ── Rawat / East Islamabad (~33.597, 73.191) ──────────────────
    "ne_lat=33.6100&ne_lng=73.2050&sw_lat=33.5900&sw_lng=73.1850",  # Rawat - North
    "ne_lat=33.5900&ne_lng=73.2050&sw_lat=33.5700&sw_lng=73.1850",  # Rawat - South

    # ── Golra / West fringe (~33.668, 72.910) ────────────────────
    "ne_lat=33.6780&ne_lng=72.9200&sw_lat=33.6580&sw_lng=72.9000",  # Golra - North
    "ne_lat=33.6580&ne_lng=72.9200&sw_lat=33.6380&sw_lng=72.9000",  # Golra - South

    # ── Tarlai Kalan (~33.698, 72.936) ───────────────────────────
    "ne_lat=33.7080&ne_lng=72.9460&sw_lat=33.6880&sw_lng=72.9260",  # Tarlai - North
    "ne_lat=33.6880&ne_lng=72.9460&sw_lat=33.6680&sw_lng=72.9260",  # Tarlai - South

]

# ─────────────────────────────────────────────────────────────────────────────
# Lahore areas + sub-areas bounding boxes
# Strategy: generous boxes (~0.010° padding from verified centers) with overlap
# to ensure full coverage. Verified anchor centers sourced from OSM/findlatlong.
# Each area ~2km x 2km; sub-areas split into 4 quadrants (~1km each).
# Overlap is intentional — cumulative coverage beats precision gaps.
# Lahore center: ~31.5204°N, 74.3587°E
# ─────────────────────────────────────────────────────────────────────────────

lahore_areas = [

    # ══════════════════════════════════════════════════════════════
    # DHA LAHORE  (east / southeast Lahore)
    # Verified: DHA Ph1 ~31.524,74.401 | Ph5 ~31.469,74.383
    #           DHA Ph6 ~31.441,74.370 | Ph9 (Prism) ~31.408,74.358
    # ══════════════════════════════════════════════════════════════

    # ── DHA Phase 1 (verified center ~31.524, 74.401) ────────────
    "ne_lat=31.5350&ne_lng=74.4120&sw_lat=31.5250&sw_lng=74.4020",  # DHA-Ph1/1
    "ne_lat=31.5350&ne_lng=74.4020&sw_lat=31.5250&sw_lng=74.3920",  # DHA-Ph1/2
    "ne_lat=31.5250&ne_lng=74.4120&sw_lat=31.5150&sw_lng=74.4020",  # DHA-Ph1/3
    "ne_lat=31.5250&ne_lng=74.4020&sw_lat=31.5150&sw_lng=74.3920",  # DHA-Ph1/4

    # ── DHA Phase 2 (~31.505, 74.402) ────────────────────────────
    "ne_lat=31.5150&ne_lng=74.4130&sw_lat=31.5050&sw_lng=74.4030",  # DHA-Ph2/1
    "ne_lat=31.5150&ne_lng=74.4030&sw_lat=31.5050&sw_lng=74.3930",  # DHA-Ph2/2
    "ne_lat=31.5050&ne_lng=74.4130&sw_lat=31.4950&sw_lng=74.4030",  # DHA-Ph2/3
    "ne_lat=31.5050&ne_lng=74.4030&sw_lat=31.4950&sw_lng=74.3930",  # DHA-Ph2/4

    # ── DHA Phase 3 (~31.487, 74.421) ────────────────────────────
    "ne_lat=31.4970&ne_lng=74.4310&sw_lat=31.4870&sw_lng=74.4210",  # DHA-Ph3/1
    "ne_lat=31.4970&ne_lng=74.4210&sw_lat=31.4870&sw_lng=74.4110",  # DHA-Ph3/2
    "ne_lat=31.4870&ne_lng=74.4310&sw_lat=31.4770&sw_lng=74.4210",  # DHA-Ph3/3
    "ne_lat=31.4870&ne_lng=74.4210&sw_lat=31.4770&sw_lng=74.4110",  # DHA-Ph3/4

    # ── DHA Phase 4 (~31.469, 74.402) ────────────────────────────
    "ne_lat=31.4790&ne_lng=74.4120&sw_lat=31.4690&sw_lng=74.4020",  # DHA-Ph4/1
    "ne_lat=31.4790&ne_lng=74.4020&sw_lat=31.4690&sw_lng=74.3920",  # DHA-Ph4/2
    "ne_lat=31.4690&ne_lng=74.4120&sw_lat=31.4590&sw_lng=74.4020",  # DHA-Ph4/3
    "ne_lat=31.4690&ne_lng=74.4020&sw_lat=31.4590&sw_lng=74.3920",  # DHA-Ph4/4

    # ── DHA Phase 5 (~31.469, 74.383) ────────────────────────────
    "ne_lat=31.4790&ne_lng=74.3930&sw_lat=31.4690&sw_lng=74.3830",  # DHA-Ph5/1
    "ne_lat=31.4790&ne_lng=74.3830&sw_lat=31.4690&sw_lng=74.3730",  # DHA-Ph5/2
    "ne_lat=31.4690&ne_lng=74.3930&sw_lat=31.4590&sw_lng=74.3830",  # DHA-Ph5/3
    "ne_lat=31.4690&ne_lng=74.3830&sw_lat=31.4590&sw_lng=74.3730",  # DHA-Ph5/4

    # ── DHA Phase 6 (verified center ~31.441, 74.370) ────────────
    "ne_lat=31.4510&ne_lng=74.3800&sw_lat=31.4410&sw_lng=74.3700",  # DHA-Ph6/1
    "ne_lat=31.4510&ne_lng=74.3700&sw_lat=31.4410&sw_lng=74.3600",  # DHA-Ph6/2
    "ne_lat=31.4410&ne_lng=74.3800&sw_lat=31.4310&sw_lng=74.3700",  # DHA-Ph6/3
    "ne_lat=31.4410&ne_lng=74.3700&sw_lat=31.4310&sw_lng=74.3600",  # DHA-Ph6/4

    # ── DHA Phase 7 / Overseas (~31.461, 74.358) ─────────────────
    "ne_lat=31.4710&ne_lng=74.3680&sw_lat=31.4610&sw_lng=74.3580",  # DHA-Ph7/1
    "ne_lat=31.4710&ne_lng=74.3580&sw_lat=31.4610&sw_lng=74.3480",  # DHA-Ph7/2
    "ne_lat=31.4610&ne_lng=74.3680&sw_lat=31.4510&sw_lng=74.3580",  # DHA-Ph7/3
    "ne_lat=31.4610&ne_lng=74.3580&sw_lat=31.4510&sw_lng=74.3480",  # DHA-Ph7/4

    # ── DHA Phase 8 (~31.428, 74.342) ────────────────────────────
    "ne_lat=31.4380&ne_lng=74.3520&sw_lat=31.4280&sw_lng=74.3420",  # DHA-Ph8/1
    "ne_lat=31.4380&ne_lng=74.3420&sw_lat=31.4280&sw_lng=74.3320",  # DHA-Ph8/2
    "ne_lat=31.4280&ne_lng=74.3520&sw_lat=31.4180&sw_lng=74.3420",  # DHA-Ph8/3
    "ne_lat=31.4280&ne_lng=74.3420&sw_lat=31.4180&sw_lng=74.3320",  # DHA-Ph8/4

    # ── DHA Phase 9 / Prism (~31.408, 74.358) ────────────────────
    "ne_lat=31.4180&ne_lng=74.3680&sw_lat=31.4080&sw_lng=74.3580",  # DHA-Ph9/1
    "ne_lat=31.4180&ne_lng=74.3580&sw_lat=31.4080&sw_lng=74.3480",  # DHA-Ph9/2
    "ne_lat=31.4080&ne_lng=74.3680&sw_lat=31.3980&sw_lng=74.3580",  # DHA-Ph9/3
    "ne_lat=31.4080&ne_lng=74.3580&sw_lat=31.3980&sw_lng=74.3480",  # DHA-Ph9/4

    # ══════════════════════════════════════════════════════════════
    # CANTONMENT / GARRISON / ASKARI
    # Verified: Cantt Station ~31.532,74.393 | Walton ~31.510,74.412
    # ══════════════════════════════════════════════════════════════

    # ── Cantonment (verified center ~31.530, 74.388) ──────────────
    "ne_lat=31.5400&ne_lng=74.3980&sw_lat=31.5300&sw_lng=74.3880",  # Cantt/1
    "ne_lat=31.5400&ne_lng=74.3880&sw_lat=31.5300&sw_lng=74.3780",  # Cantt/2
    "ne_lat=31.5300&ne_lng=74.3980&sw_lat=31.5200&sw_lng=74.3880",  # Cantt/3
    "ne_lat=31.5300&ne_lng=74.3880&sw_lat=31.5200&sw_lng=74.3780",  # Cantt/4

    # ── Cavalry Ground (~31.527, 74.367) ─────────────────────────
    "ne_lat=31.5370&ne_lng=74.3770&sw_lat=31.5270&sw_lng=74.3670",  # Cavalry/1
    "ne_lat=31.5370&ne_lng=74.3670&sw_lat=31.5270&sw_lng=74.3570",  # Cavalry/2
    "ne_lat=31.5270&ne_lng=74.3770&sw_lat=31.5170&sw_lng=74.3670",  # Cavalry/3
    "ne_lat=31.5270&ne_lng=74.3670&sw_lat=31.5170&sw_lng=74.3570",  # Cavalry/4

    # ── Walton / Lahore Airport (~31.522, 74.404) ─────────────────
    "ne_lat=31.5320&ne_lng=74.4140&sw_lat=31.5220&sw_lng=74.4040",  # Walton/1
    "ne_lat=31.5220&ne_lng=74.4140&sw_lat=31.5120&sw_lng=74.4040",  # Walton/2

    # ── Askari 10 (~31.453, 74.363) ──────────────────────────────
    "ne_lat=31.4630&ne_lng=74.3730&sw_lat=31.4530&sw_lng=74.3630",  # Askari10/1
    "ne_lat=31.4630&ne_lng=74.3630&sw_lat=31.4530&sw_lng=74.3530",  # Askari10/2
    "ne_lat=31.4530&ne_lng=74.3730&sw_lat=31.4430&sw_lng=74.3630",  # Askari10/3
    "ne_lat=31.4530&ne_lng=74.3630&sw_lat=31.4430&sw_lng=74.3530",  # Askari10/4

    # ── Askari 11 (~31.437, 74.304) ──────────────────────────────
    "ne_lat=31.4470&ne_lng=74.3140&sw_lat=31.4370&sw_lng=74.3040",  # Askari11/1
    "ne_lat=31.4470&ne_lng=74.3040&sw_lat=31.4370&sw_lng=74.2940",  # Askari11/2
    "ne_lat=31.4370&ne_lng=74.3140&sw_lat=31.4270&sw_lng=74.3040",  # Askari11/3
    "ne_lat=31.4370&ne_lng=74.3040&sw_lat=31.4270&sw_lng=74.2940",  # Askari11/4

    # ══════════════════════════════════════════════════════════════
    # GULBERG  (central Lahore — premium commercial + residential)
    # Verified: Liberty Market ~31.508,74.338 | MM Alam Rd ~31.503,74.345
    #           Gulberg Main Blvd ~31.513,74.343
    # ══════════════════════════════════════════════════════════════

    # ── Gulberg I (~31.516, 74.338) ──────────────────────────────
    "ne_lat=31.5260&ne_lng=74.3480&sw_lat=31.5160&sw_lng=74.3380",  # Gulberg-I/1
    "ne_lat=31.5260&ne_lng=74.3380&sw_lat=31.5160&sw_lng=74.3280",  # Gulberg-I/2
    "ne_lat=31.5160&ne_lng=74.3480&sw_lat=31.5060&sw_lng=74.3380",  # Gulberg-I/3
    "ne_lat=31.5160&ne_lng=74.3380&sw_lat=31.5060&sw_lng=74.3280",  # Gulberg-I/4

    # ── Gulberg II / MM Alam Road (~31.509, 74.349) ───────────────
    "ne_lat=31.5190&ne_lng=74.3590&sw_lat=31.5090&sw_lng=74.3490",  # Gulberg-II/1
    "ne_lat=31.5190&ne_lng=74.3490&sw_lat=31.5090&sw_lng=74.3390",  # Gulberg-II/2
    "ne_lat=31.5090&ne_lng=74.3590&sw_lat=31.4990&sw_lng=74.3490",  # Gulberg-II/3
    "ne_lat=31.5090&ne_lng=74.3490&sw_lat=31.4990&sw_lng=74.3390",  # Gulberg-II/4

    # ── Gulberg III (~31.503, 74.337) ────────────────────────────
    "ne_lat=31.5130&ne_lng=74.3470&sw_lat=31.5030&sw_lng=74.3370",  # Gulberg-III/1
    "ne_lat=31.5130&ne_lng=74.3370&sw_lat=31.5030&sw_lng=74.3270",  # Gulberg-III/2
    "ne_lat=31.5030&ne_lng=74.3470&sw_lat=31.4930&sw_lng=74.3370",  # Gulberg-III/3
    "ne_lat=31.5030&ne_lng=74.3370&sw_lat=31.4930&sw_lng=74.3270",  # Gulberg-III/4

    # ── Gulberg IV / V (~31.492, 74.329) ─────────────────────────
    "ne_lat=31.5020&ne_lng=74.3390&sw_lat=31.4920&sw_lng=74.3290",  # Gulberg-IV/1
    "ne_lat=31.5020&ne_lng=74.3290&sw_lat=31.4920&sw_lng=74.3190",  # Gulberg-IV/2
    "ne_lat=31.4920&ne_lng=74.3390&sw_lat=31.4820&sw_lng=74.3290",  # Gulberg-IV/3
    "ne_lat=31.4920&ne_lng=74.3290&sw_lat=31.4820&sw_lng=74.3190",  # Gulberg-IV/4

    # ── Gulberg Greens (~31.440, 74.305) ─────────────────────────
    "ne_lat=31.4500&ne_lng=74.3150&sw_lat=31.4400&sw_lng=74.3050",  # GulbergGreens/1
    "ne_lat=31.4500&ne_lng=74.3050&sw_lat=31.4400&sw_lng=74.2950",  # GulbergGreens/2
    "ne_lat=31.4400&ne_lng=74.3150&sw_lat=31.4300&sw_lng=74.3050",  # GulbergGreens/3
    "ne_lat=31.4400&ne_lng=74.3050&sw_lat=31.4300&sw_lng=74.2950",  # GulbergGreens/4

    # ══════════════════════════════════════════════════════════════
    # MODEL TOWN / GARDEN TOWN / SHADMAN
    # Verified: Model Town center ~31.497,74.308
    #           Garden Town (Barkat Market) ~31.510,74.323
    # ══════════════════════════════════════════════════════════════

    # ── Model Town (verified center ~31.497, 74.308) ──────────────
    "ne_lat=31.5070&ne_lng=74.3180&sw_lat=31.4970&sw_lng=74.3080",  # ModelTown/1
    "ne_lat=31.5070&ne_lng=74.3080&sw_lat=31.4970&sw_lng=74.2980",  # ModelTown/2
    "ne_lat=31.4970&ne_lng=74.3180&sw_lat=31.4870&sw_lng=74.3080",  # ModelTown/3
    "ne_lat=31.4970&ne_lng=74.3080&sw_lat=31.4870&sw_lng=74.2980",  # ModelTown/4

    # ── Garden Town (~31.509, 74.323) ────────────────────────────
    "ne_lat=31.5190&ne_lng=74.3330&sw_lat=31.5090&sw_lng=74.3230",  # GardenTown/1
    "ne_lat=31.5190&ne_lng=74.3230&sw_lat=31.5090&sw_lng=74.3130",  # GardenTown/2
    "ne_lat=31.5090&ne_lng=74.3330&sw_lat=31.4990&sw_lng=74.3230",  # GardenTown/3
    "ne_lat=31.5090&ne_lng=74.3230&sw_lat=31.4990&sw_lng=74.3130",  # GardenTown/4

    # ── Shadman (~31.524, 74.318) ─────────────────────────────────
    "ne_lat=31.5340&ne_lng=74.3280&sw_lat=31.5240&sw_lng=74.3180",  # Shadman/1
    "ne_lat=31.5340&ne_lng=74.3180&sw_lat=31.5240&sw_lng=74.3080",  # Shadman/2
    "ne_lat=31.5240&ne_lng=74.3280&sw_lat=31.5140&sw_lng=74.3180",  # Shadman/3
    "ne_lat=31.5240&ne_lng=74.3180&sw_lat=31.5140&sw_lng=74.3080",  # Shadman/4

    # ── New Garden Town / Thokar Rd (~31.505, 74.310) ────────────
    "ne_lat=31.5150&ne_lng=74.3200&sw_lat=31.5050&sw_lng=74.3100",  # NewGardenTown/1
    "ne_lat=31.5050&ne_lng=74.3200&sw_lat=31.4950&sw_lng=74.3100",  # NewGardenTown/2

    # ══════════════════════════════════════════════════════════════
    # FAISAL TOWN / TOWNSHIP / ICHHRA / SAMANABAD
    # ══════════════════════════════════════════════════════════════

    # ── Faisal Town (~31.510, 74.292) ────────────────────────────
    "ne_lat=31.5200&ne_lng=74.3020&sw_lat=31.5100&sw_lng=74.2920",  # FaisalTown/1
    "ne_lat=31.5200&ne_lng=74.2920&sw_lat=31.5100&sw_lng=74.2820",  # FaisalTown/2
    "ne_lat=31.5100&ne_lng=74.3020&sw_lat=31.5000&sw_lng=74.2920",  # FaisalTown/3
    "ne_lat=31.5100&ne_lng=74.2920&sw_lat=31.5000&sw_lng=74.2820",  # FaisalTown/4

    # ── Township (~31.520, 74.263) ───────────────────────────────
    "ne_lat=31.5300&ne_lng=74.2730&sw_lat=31.5200&sw_lng=74.2630",  # Township/1
    "ne_lat=31.5300&ne_lng=74.2630&sw_lat=31.5200&sw_lng=74.2530",  # Township/2
    "ne_lat=31.5200&ne_lng=74.2730&sw_lat=31.5100&sw_lng=74.2630",  # Township/3
    "ne_lat=31.5200&ne_lng=74.2630&sw_lat=31.5100&sw_lng=74.2530",  # Township/4

    # ── Samanabad (~31.532, 74.294) ──────────────────────────────
    "ne_lat=31.5420&ne_lng=74.3040&sw_lat=31.5320&sw_lng=74.2940",  # Samanabad/1
    "ne_lat=31.5420&ne_lng=74.2940&sw_lat=31.5320&sw_lng=74.2840",  # Samanabad/2
    "ne_lat=31.5320&ne_lng=74.3040&sw_lat=31.5220&sw_lng=74.2940",  # Samanabad/3
    "ne_lat=31.5320&ne_lng=74.2940&sw_lat=31.5220&sw_lng=74.2840",  # Samanabad/4

    # ── Ichhra (~31.524, 74.302) ──────────────────────────────────
    "ne_lat=31.5340&ne_lng=74.3120&sw_lat=31.5240&sw_lng=74.3020",  # Ichhra/1
    "ne_lat=31.5340&ne_lng=74.3020&sw_lat=31.5240&sw_lng=74.2920",  # Ichhra/2
    "ne_lat=31.5240&ne_lng=74.3120&sw_lat=31.5140&sw_lng=74.3020",  # Ichhra/3
    "ne_lat=31.5240&ne_lng=74.3020&sw_lat=31.5140&sw_lng=74.2920",  # Ichhra/4

    # ── Pak Arab Housing Society (~31.545, 74.273) ───────────────
    "ne_lat=31.5550&ne_lng=74.2830&sw_lat=31.5450&sw_lng=74.2730",  # PakArab/1
    "ne_lat=31.5550&ne_lng=74.2730&sw_lat=31.5450&sw_lng=74.2630",  # PakArab/2
    "ne_lat=31.5450&ne_lng=74.2830&sw_lat=31.5350&sw_lng=74.2730",  # PakArab/3
    "ne_lat=31.5450&ne_lng=74.2730&sw_lat=31.5350&sw_lng=74.2630",  # PakArab/4

    # ══════════════════════════════════════════════════════════════
    # ALLAMA IQBAL TOWN / JOHAR TOWN / WAPDA TOWN / LDA AVENUE
    # ══════════════════════════════════════════════════════════════

    # ── Allama Iqbal Town (~31.490, 74.291) ──────────────────────
    "ne_lat=31.5000&ne_lng=74.3010&sw_lat=31.4900&sw_lng=74.2910",  # AIqbalTown/1
    "ne_lat=31.5000&ne_lng=74.2910&sw_lat=31.4900&sw_lng=74.2810",  # AIqbalTown/2
    "ne_lat=31.4900&ne_lng=74.3010&sw_lat=31.4800&sw_lng=74.2910",  # AIqbalTown/3
    "ne_lat=31.4900&ne_lng=74.2910&sw_lat=31.4800&sw_lng=74.2810",  # AIqbalTown/4

    # ── Johar Town North (~31.478, 74.271) ───────────────────────
    "ne_lat=31.4880&ne_lng=74.2810&sw_lat=31.4780&sw_lng=74.2710",  # JoharTown-N/1
    "ne_lat=31.4880&ne_lng=74.2710&sw_lat=31.4780&sw_lng=74.2610",  # JoharTown-N/2
    "ne_lat=31.4780&ne_lng=74.2810&sw_lat=31.4680&sw_lng=74.2710",  # JoharTown-N/3
    "ne_lat=31.4780&ne_lng=74.2710&sw_lat=31.4680&sw_lng=74.2610",  # JoharTown-N/4

    # ── Johar Town South (~31.460, 74.268) ───────────────────────
    "ne_lat=31.4700&ne_lng=74.2780&sw_lat=31.4600&sw_lng=74.2680",  # JoharTown-S/1
    "ne_lat=31.4700&ne_lng=74.2680&sw_lat=31.4600&sw_lng=74.2580",  # JoharTown-S/2
    "ne_lat=31.4600&ne_lng=74.2780&sw_lat=31.4500&sw_lng=74.2680",  # JoharTown-S/3
    "ne_lat=31.4600&ne_lng=74.2680&sw_lat=31.4500&sw_lng=74.2580",  # JoharTown-S/4

    # ── Wapda Town (~31.461, 74.256) ─────────────────────────────
    "ne_lat=31.4710&ne_lng=74.2660&sw_lat=31.4610&sw_lng=74.2560",  # WapdaTown/1
    "ne_lat=31.4710&ne_lng=74.2560&sw_lat=31.4610&sw_lng=74.2460",  # WapdaTown/2
    "ne_lat=31.4610&ne_lng=74.2660&sw_lat=31.4510&sw_lng=74.2560",  # WapdaTown/3
    "ne_lat=31.4610&ne_lng=74.2560&sw_lat=31.4510&sw_lng=74.2460",  # WapdaTown/4

    # ── LDA Avenue (~31.442, 74.241) ─────────────────────────────
    "ne_lat=31.4520&ne_lng=74.2510&sw_lat=31.4420&sw_lng=74.2410",  # LDA-Ave/1
    "ne_lat=31.4520&ne_lng=74.2410&sw_lat=31.4420&sw_lng=74.2310",  # LDA-Ave/2
    "ne_lat=31.4420&ne_lng=74.2510&sw_lat=31.4320&sw_lng=74.2410",  # LDA-Ave/3
    "ne_lat=31.4420&ne_lng=74.2410&sw_lat=31.4320&sw_lng=74.2310",  # LDA-Ave/4

    # ── Sui Gas Housing Society (~31.459, 74.300) ────────────────
    "ne_lat=31.4690&ne_lng=74.3100&sw_lat=31.4590&sw_lng=74.3000",  # SuiGas/1
    "ne_lat=31.4690&ne_lng=74.3000&sw_lat=31.4590&sw_lng=74.2900",  # SuiGas/2
    "ne_lat=31.4590&ne_lng=74.3100&sw_lat=31.4490&sw_lng=74.3000",  # SuiGas/3
    "ne_lat=31.4590&ne_lng=74.3000&sw_lat=31.4490&sw_lng=74.2900",  # SuiGas/4

    # ══════════════════════════════════════════════════════════════
    # BAHRIA TOWN LAHORE (Raiwind Road, SW Lahore)
    # Main entrance ~31.372, 74.197 | Civic Centre ~31.393, 74.205
    # ══════════════════════════════════════════════════════════════

    # ── Bahria Town Phase 1-2 / Civic (~31.393, 74.205) ──────────
    "ne_lat=31.4030&ne_lng=74.2150&sw_lat=31.3930&sw_lng=74.2050",  # Bahria-L1/1
    "ne_lat=31.4030&ne_lng=74.2050&sw_lat=31.3930&sw_lng=74.1950",  # Bahria-L1/2
    "ne_lat=31.3930&ne_lng=74.2150&sw_lat=31.3830&sw_lng=74.2050",  # Bahria-L1/3
    "ne_lat=31.3930&ne_lng=74.2050&sw_lat=31.3830&sw_lng=74.1950",  # Bahria-L1/4

    # ── Bahria Town Phase 3-4 / Orchard (~31.413, 74.215) ────────
    "ne_lat=31.4230&ne_lng=74.2250&sw_lat=31.4130&sw_lng=74.2150",  # Bahria-L2/1
    "ne_lat=31.4230&ne_lng=74.2150&sw_lat=31.4130&sw_lng=74.2050",  # Bahria-L2/2
    "ne_lat=31.4130&ne_lng=74.2250&sw_lat=31.4030&sw_lng=74.2150",  # Bahria-L2/3
    "ne_lat=31.4130&ne_lng=74.2150&sw_lat=31.4030&sw_lng=74.2050",  # Bahria-L2/4

    # ── Bahria Town Phase 5-6 / Safari / Zoo (~31.378, 74.183) ───
    "ne_lat=31.3880&ne_lng=74.1930&sw_lat=31.3780&sw_lng=74.1830",  # Bahria-L3/1
    "ne_lat=31.3880&ne_lng=74.1830&sw_lat=31.3780&sw_lng=74.1730",  # Bahria-L3/2
    "ne_lat=31.3780&ne_lng=74.1930&sw_lat=31.3680&sw_lng=74.1830",  # Bahria-L3/3
    "ne_lat=31.3780&ne_lng=74.1830&sw_lat=31.3680&sw_lng=74.1730",  # Bahria-L3/4

    # ── Bahria Town Phase 7-8 / Tauheed / Nargis (~31.425, 74.197)
    "ne_lat=31.4350&ne_lng=74.2070&sw_lat=31.4250&sw_lng=74.1970",  # Bahria-L4/1
    "ne_lat=31.4350&ne_lng=74.1970&sw_lat=31.4250&sw_lng=74.1870",  # Bahria-L4/2
    "ne_lat=31.4250&ne_lng=74.2070&sw_lat=31.4150&sw_lng=74.1970",  # Bahria-L4/3
    "ne_lat=31.4250&ne_lng=74.1970&sw_lat=31.4150&sw_lng=74.1870",  # Bahria-L4/4

    # ══════════════════════════════════════════════════════════════
    # VALENCIA TOWN / PARAGON CITY / LAKE CITY
    # ══════════════════════════════════════════════════════════════

    # ── Valencia Town (~31.503, 74.373) ──────────────────────────
    "ne_lat=31.5130&ne_lng=74.3830&sw_lat=31.5030&sw_lng=74.3730",  # Valencia/1
    "ne_lat=31.5130&ne_lng=74.3730&sw_lat=31.5030&sw_lng=74.3630",  # Valencia/2
    "ne_lat=31.5030&ne_lng=74.3830&sw_lat=31.4930&sw_lng=74.3730",  # Valencia/3
    "ne_lat=31.5030&ne_lng=74.3730&sw_lat=31.4930&sw_lng=74.3630",  # Valencia/4

    # ── Paragon City (~31.432, 74.327) ───────────────────────────
    "ne_lat=31.4420&ne_lng=74.3370&sw_lat=31.4320&sw_lng=74.3270",  # Paragon/1
    "ne_lat=31.4420&ne_lng=74.3270&sw_lat=31.4320&sw_lng=74.3170",  # Paragon/2
    "ne_lat=31.4320&ne_lng=74.3370&sw_lat=31.4220&sw_lng=74.3270",  # Paragon/3
    "ne_lat=31.4320&ne_lng=74.3270&sw_lat=31.4220&sw_lng=74.3170",  # Paragon/4

    # ── Lake City (~31.563, 74.419) ──────────────────────────────
    "ne_lat=31.5730&ne_lng=74.4290&sw_lat=31.5630&sw_lng=74.4190",  # LakeCity/1
    "ne_lat=31.5730&ne_lng=74.4190&sw_lat=31.5630&sw_lng=74.4090",  # LakeCity/2
    "ne_lat=31.5630&ne_lng=74.4290&sw_lat=31.5530&sw_lng=74.4190",  # LakeCity/3
    "ne_lat=31.5630&ne_lng=74.4190&sw_lat=31.5530&sw_lng=74.4090",  # LakeCity/4

    # ══════════════════════════════════════════════════════════════
    # MALL ROAD / MOZANG / GARHI SHAHU / ANARKALI
    # (inner-city commercial spine)
    # Verified: GPO ~31.553,74.313 | Anarkali ~31.563,74.318
    # ══════════════════════════════════════════════════════════════

    # ── Mall Road North (~31.562, 74.315) ────────────────────────
    "ne_lat=31.5720&ne_lng=74.3250&sw_lat=31.5620&sw_lng=74.3150",  # Mall-N/1
    "ne_lat=31.5720&ne_lng=74.3150&sw_lat=31.5620&sw_lng=74.3050",  # Mall-N/2
    "ne_lat=31.5620&ne_lng=74.3250&sw_lat=31.5520&sw_lng=74.3150",  # Mall-N/3
    "ne_lat=31.5620&ne_lng=74.3150&sw_lat=31.5520&sw_lng=74.3050",  # Mall-N/4

    # ── Mall Road South / GPO / AI Hospital (~31.543, 74.313) ────
    "ne_lat=31.5530&ne_lng=74.3230&sw_lat=31.5430&sw_lng=74.3130",  # Mall-S/1
    "ne_lat=31.5530&ne_lng=74.3130&sw_lat=31.5430&sw_lng=74.3030",  # Mall-S/2
    "ne_lat=31.5430&ne_lng=74.3230&sw_lat=31.5330&sw_lng=74.3130",  # Mall-S/3
    "ne_lat=31.5430&ne_lng=74.3130&sw_lat=31.5330&sw_lng=74.3030",  # Mall-S/4

    # ── Garhi Shahu / Anarkali (~31.548, 74.328) ─────────────────
    "ne_lat=31.5580&ne_lng=74.3380&sw_lat=31.5480&sw_lng=74.3280",  # GarhiAnarkali/1
    "ne_lat=31.5580&ne_lng=74.3280&sw_lat=31.5480&sw_lng=74.3180",  # GarhiAnarkali/2
    "ne_lat=31.5480&ne_lng=74.3380&sw_lat=31.5380&sw_lng=74.3280",  # GarhiAnarkali/3
    "ne_lat=31.5480&ne_lng=74.3280&sw_lat=31.5380&sw_lng=74.3180",  # GarhiAnarkali/4

    # ── Mozang (~31.533, 74.316) ──────────────────────────────────
    "ne_lat=31.5430&ne_lng=74.3260&sw_lat=31.5330&sw_lng=74.3160",  # Mozang/1
    "ne_lat=31.5430&ne_lng=74.3160&sw_lat=31.5330&sw_lng=74.3060",  # Mozang/2
    "ne_lat=31.5330&ne_lng=74.3260&sw_lat=31.5230&sw_lng=74.3160",  # Mozang/3
    "ne_lat=31.5330&ne_lng=74.3160&sw_lat=31.5230&sw_lng=74.3060",  # Mozang/4

    # ══════════════════════════════════════════════════════════════
    # WALLED CITY / OLD LAHORE
    # Verified: Lahore Fort ~31.588,74.315 | Badshahi Mosque ~31.588,74.309
    #           Data Darbar ~31.579,74.296
    # ══════════════════════════════════════════════════════════════

    # ── Walled City core / Fort (~31.588, 74.313) ────────────────
    "ne_lat=31.5980&ne_lng=74.3230&sw_lat=31.5880&sw_lng=74.3130",  # WalledCity/1
    "ne_lat=31.5980&ne_lng=74.3130&sw_lat=31.5880&sw_lng=74.3030",  # WalledCity/2
    "ne_lat=31.5880&ne_lng=74.3230&sw_lat=31.5780&sw_lng=74.3130",  # WalledCity/3
    "ne_lat=31.5880&ne_lng=74.3130&sw_lat=31.5780&sw_lng=74.3030",  # WalledCity/4

    # ── Data Darbar / Bhati Gate (~31.578, 74.296) ───────────────
    "ne_lat=31.5880&ne_lng=74.3060&sw_lat=31.5780&sw_lng=74.2960",  # DataDarbar/1
    "ne_lat=31.5880&ne_lng=74.2960&sw_lat=31.5780&sw_lng=74.2860",  # DataDarbar/2
    "ne_lat=31.5780&ne_lng=74.3060&sw_lat=31.5680&sw_lng=74.2960",  # DataDarbar/3
    "ne_lat=31.5780&ne_lng=74.2960&sw_lat=31.5680&sw_lng=74.2860",  # DataDarbar/4

    # ── Lohari Gate / Delhi Gate / Androon Shehr (~31.573, 74.315)
    "ne_lat=31.5830&ne_lng=74.3250&sw_lat=31.5730&sw_lng=74.3150",  # InnerCity-E/1
    "ne_lat=31.5730&ne_lng=74.3250&sw_lat=31.5630&sw_lng=74.3150",  # InnerCity-E/2

    # ── Shalimar / Baghbanpura (~31.592, 74.355) ─────────────────
    "ne_lat=31.6020&ne_lng=74.3650&sw_lat=31.5920&sw_lng=74.3550",  # Shalimar/1
    "ne_lat=31.6020&ne_lng=74.3550&sw_lat=31.5920&sw_lng=74.3450",  # Shalimar/2
    "ne_lat=31.5920&ne_lng=74.3650&sw_lat=31.5820&sw_lng=74.3550",  # Shalimar/3
    "ne_lat=31.5920&ne_lng=74.3550&sw_lat=31.5820&sw_lng=74.3450",  # Shalimar/4

    # ══════════════════════════════════════════════════════════════
    # NORTH LAHORE  (Shahdara, Ravi bridge, Harbanspura)
    # ══════════════════════════════════════════════════════════════

    # ── Shahdara (~31.609, 74.293) ───────────────────────────────
    "ne_lat=31.6190&ne_lng=74.3030&sw_lat=31.6090&sw_lng=74.2930",  # Shahdara/1
    "ne_lat=31.6190&ne_lng=74.2930&sw_lat=31.6090&sw_lng=74.2830",  # Shahdara/2
    "ne_lat=31.6090&ne_lng=74.3030&sw_lat=31.5990&sw_lng=74.2930",  # Shahdara/3
    "ne_lat=31.6090&ne_lng=74.2930&sw_lat=31.5990&sw_lng=74.2830",  # Shahdara/4

    # ── Harbanspura (~31.564, 74.283) ────────────────────────────
    "ne_lat=31.5740&ne_lng=74.2930&sw_lat=31.5640&sw_lng=74.2830",  # Harbanspura/1
    "ne_lat=31.5740&ne_lng=74.2830&sw_lat=31.5640&sw_lng=74.2730",  # Harbanspura/2
    "ne_lat=31.5640&ne_lng=74.2930&sw_lat=31.5540&sw_lng=74.2830",  # Harbanspura/3
    "ne_lat=31.5640&ne_lng=74.2830&sw_lat=31.5540&sw_lng=74.2730",  # Harbanspura/4

    # ── Badami Bagh / Chauburji (~31.560, 74.303) ────────────────
    "ne_lat=31.5700&ne_lng=74.3130&sw_lat=31.5600&sw_lng=74.3030",  # BadamiBagh/1
    "ne_lat=31.5600&ne_lng=74.3130&sw_lat=31.5500&sw_lng=74.3030",  # BadamiBagh/2

    # ══════════════════════════════════════════════════════════════
    # EAST LAHORE (Mughalpura, Mustafaabad, GT Road corridor)
    # ══════════════════════════════════════════════════════════════

    # ── Mughalpura (~31.558, 74.348) ─────────────────────────────
    "ne_lat=31.5680&ne_lng=74.3580&sw_lat=31.5580&sw_lng=74.3480",  # Mughalpura/1
    "ne_lat=31.5680&ne_lng=74.3480&sw_lat=31.5580&sw_lng=74.3380",  # Mughalpura/2
    "ne_lat=31.5580&ne_lng=74.3580&sw_lat=31.5480&sw_lng=74.3480",  # Mughalpura/3
    "ne_lat=31.5580&ne_lng=74.3480&sw_lat=31.5480&sw_lng=74.3380",  # Mughalpura/4

    # ── Mustafaabad / Hanjarwal (~31.531, 74.363) ─────────────────
    "ne_lat=31.5410&ne_lng=74.3730&sw_lat=31.5310&sw_lng=74.3630",  # Mustafaabad/1
    "ne_lat=31.5410&ne_lng=74.3630&sw_lat=31.5310&sw_lng=74.3530",  # Mustafaabad/2
    "ne_lat=31.5310&ne_lng=74.3730&sw_lat=31.5210&sw_lng=74.3630",  # Mustafaabad/3
    "ne_lat=31.5310&ne_lng=74.3630&sw_lat=31.5210&sw_lng=74.3530",  # Mustafaabad/4

    # ── GT Road / Shahdara to Baghbanpura corridor (~31.577, 74.337)
    "ne_lat=31.5870&ne_lng=74.3470&sw_lat=31.5770&sw_lng=74.3370",  # GTRoad-E/1
    "ne_lat=31.5770&ne_lng=74.3470&sw_lat=31.5670&sw_lng=74.3370",  # GTRoad-E/2

    # ══════════════════════════════════════════════════════════════
    # SOUTH LAHORE (Thokar, Raiwind, Manga Mandi fringe)
    # ══════════════════════════════════════════════════════════════

    # ── Thokar Niaz Baig (~31.430, 74.271) ───────────────────────
    "ne_lat=31.4400&ne_lng=74.2810&sw_lat=31.4300&sw_lng=74.2710",  # Thokar/1
    "ne_lat=31.4400&ne_lng=74.2710&sw_lat=31.4300&sw_lng=74.2610",  # Thokar/2
    "ne_lat=31.4300&ne_lng=74.2810&sw_lat=31.4200&sw_lng=74.2710",  # Thokar/3
    "ne_lat=31.4300&ne_lng=74.2710&sw_lat=31.4200&sw_lng=74.2610",  # Thokar/4

    # ── Raiwind (~31.381, 74.247) ────────────────────────────────
    "ne_lat=31.3910&ne_lng=74.2570&sw_lat=31.3810&sw_lng=74.2470",  # Raiwind/1
    "ne_lat=31.3910&ne_lng=74.2470&sw_lat=31.3810&sw_lng=74.2370",  # Raiwind/2
    "ne_lat=31.3810&ne_lng=74.2570&sw_lat=31.3710&sw_lng=74.2470",  # Raiwind/3
    "ne_lat=31.3810&ne_lng=74.2470&sw_lat=31.3710&sw_lng=74.2370",  # Raiwind/4

    # ── Manga Mandi fringe (~31.362, 74.310) ─────────────────────
    "ne_lat=31.3720&ne_lng=74.3200&sw_lat=31.3620&sw_lng=74.3100",  # Manga/1
    "ne_lat=31.3620&ne_lng=74.3200&sw_lat=31.3520&sw_lng=74.3100",  # Manga/2

    # ══════════════════════════════════════════════════════════════
    # WEST LAHORE (Kot Lakhpat, Sundar, industrial zones)
    # ══════════════════════════════════════════════════════════════

    # ── Kot Lakhpat / Industrial Estate (~31.499, 74.248) ────────
    "ne_lat=31.5090&ne_lng=74.2580&sw_lat=31.4990&sw_lng=74.2480",  # KotLakhpat/1
    "ne_lat=31.5090&ne_lng=74.2480&sw_lat=31.4990&sw_lng=74.2380",  # KotLakhpat/2
    "ne_lat=31.4990&ne_lng=74.2580&sw_lat=31.4890&sw_lng=74.2480",  # KotLakhpat/3
    "ne_lat=31.4990&ne_lng=74.2480&sw_lat=31.4890&sw_lng=74.2380",  # KotLakhpat/4

    # ── Sundar Industrial Estate (~31.440, 74.186) ───────────────
    "ne_lat=31.4500&ne_lng=74.1960&sw_lat=31.4400&sw_lng=74.1860",  # Sundar/1
    "ne_lat=31.4500&ne_lng=74.1860&sw_lat=31.4400&sw_lng=74.1760",  # Sundar/2
    "ne_lat=31.4400&ne_lng=74.1960&sw_lat=31.4300&sw_lng=74.1860",  # Sundar/3
    "ne_lat=31.4400&ne_lng=74.1860&sw_lat=31.4300&sw_lng=74.1760",  # Sundar/4

    # ── Nishtar Colony / Icchra fringe (~31.516, 74.282) ─────────
    "ne_lat=31.5260&ne_lng=74.2920&sw_lat=31.5160&sw_lng=74.2820",  # NishtarCol/1
    "ne_lat=31.5160&ne_lng=74.2920&sw_lat=31.5060&sw_lng=74.2820",  # NishtarCol/2

    # ══════════════════════════════════════════════════════════════
    # MISC / LANDMARK ZONES
    # ══════════════════════════════════════════════════════════════

    # ── LUMS / OPF area (~31.481, 74.396) ────────────────────────
    "ne_lat=31.4910&ne_lng=74.4060&sw_lat=31.4810&sw_lng=74.3960",  # LUMS/1
    "ne_lat=31.4810&ne_lng=74.4060&sw_lat=31.4710&sw_lng=74.3960",  # LUMS/2

    # ── Johar Town / COMSATS Rd (~31.453, 74.310) ────────────────
    "ne_lat=31.4630&ne_lng=74.3200&sw_lat=31.4530&sw_lng=74.3100",  # COMSATS/1
    "ne_lat=31.4530&ne_lng=74.3200&sw_lat=31.4430&sw_lng=74.3100",  # COMSATS/2

    # ── Lahore Ring Road / Southern Loop fringe (~31.412, 74.323) ─
    "ne_lat=31.4220&ne_lng=74.3330&sw_lat=31.4120&sw_lng=74.3230",  # RingRoad-S/1
    "ne_lat=31.4120&ne_lng=74.3330&sw_lat=31.4020&sw_lng=74.3230",  # RingRoad-S/2

    # ── Barki Road / Bedian Road corridor (~31.463, 74.431) ───────
    "ne_lat=31.4730&ne_lng=74.4410&sw_lat=31.4630&sw_lng=74.4310",  # Barki/1
    "ne_lat=31.4630&ne_lng=74.4410&sw_lat=31.4530&sw_lng=74.4310",  # Barki/2

    # ── Sheikhupura Road / Kala Shah Kaku fringe (~31.585, 74.241)
    "ne_lat=31.5950&ne_lng=74.2510&sw_lat=31.5850&sw_lng=74.2410",  # SKaku/1
    "ne_lat=31.5850&ne_lng=74.2510&sw_lat=31.5750&sw_lng=74.2410",  # SKaku/2

]

# ─────────────────────────────────────────────────────────────────────────────
# Karachi areas + sub-areas bounding boxes
# Strategy: generous boxes (~0.010° padding from verified centers) with overlap
# to ensure full coverage. Verified anchor centers sourced from OSM/findlatlong.
# Each area ~2km x 2km; sub-areas split into 4 quadrants (~1km each).
# Overlap is intentional — cumulative coverage beats precision gaps.
# Karachi center: ~24.8607°N, 67.0011°E
# At this latitude: 0.01° lat ≈ 1.11 km | 0.01° lng ≈ 1.01 km
# ─────────────────────────────────────────────────────────────────────────────

karachi_areas = [

    # ══════════════════════════════════════════════════════════════
    # DHA KARACHI  (south / southeast coastal corridor)
    # Verified: DHA Ph1 ~24.822,67.066 | Ph6 ~24.764,67.081
    #           Ph8 ~24.840,67.093 | DHA City ~24.746,67.079
    # ══════════════════════════════════════════════════════════════

    # ── DHA Phase 1 (verified ~24.822, 67.066) ───────────────────
    "ne_lat=24.8320&ne_lng=67.0760&sw_lat=24.8220&sw_lng=67.0660",  # DHA-Ph1/1
    "ne_lat=24.8320&ne_lng=67.0660&sw_lat=24.8220&sw_lng=67.0560",  # DHA-Ph1/2
    "ne_lat=24.8220&ne_lng=67.0760&sw_lat=24.8120&sw_lng=67.0660",  # DHA-Ph1/3
    "ne_lat=24.8220&ne_lng=67.0660&sw_lat=24.8120&sw_lng=67.0560",  # DHA-Ph1/4

    # ── DHA Phase 2 (~24.807, 67.068) ────────────────────────────
    "ne_lat=24.8170&ne_lng=67.0780&sw_lat=24.8070&sw_lng=67.0680",  # DHA-Ph2/1
    "ne_lat=24.8170&ne_lng=67.0680&sw_lat=24.8070&sw_lng=67.0580",  # DHA-Ph2/2
    "ne_lat=24.8070&ne_lng=67.0780&sw_lat=24.7970&sw_lng=67.0680",  # DHA-Ph2/3
    "ne_lat=24.8070&ne_lng=67.0680&sw_lat=24.7970&sw_lng=67.0580",  # DHA-Ph2/4

    # ── DHA Phase 3 (~24.800, 67.074) ────────────────────────────
    "ne_lat=24.8100&ne_lng=67.0840&sw_lat=24.8000&sw_lng=67.0740",  # DHA-Ph3/1
    "ne_lat=24.8100&ne_lng=67.0740&sw_lat=24.8000&sw_lng=67.0640",  # DHA-Ph3/2
    "ne_lat=24.8000&ne_lng=67.0840&sw_lat=24.7900&sw_lng=67.0740",  # DHA-Ph3/3
    "ne_lat=24.8000&ne_lng=67.0740&sw_lat=24.7900&sw_lng=67.0640",  # DHA-Ph3/4

    # ── DHA Phase 4 (~24.789, 67.073) ────────────────────────────
    "ne_lat=24.7990&ne_lng=67.0830&sw_lat=24.7890&sw_lng=67.0730",  # DHA-Ph4/1
    "ne_lat=24.7990&ne_lng=67.0730&sw_lat=24.7890&sw_lng=67.0630",  # DHA-Ph4/2
    "ne_lat=24.7890&ne_lng=67.0830&sw_lat=24.7790&sw_lng=67.0730",  # DHA-Ph4/3
    "ne_lat=24.7890&ne_lng=67.0730&sw_lat=24.7790&sw_lng=67.0630",  # DHA-Ph4/4

    # ── DHA Phase 5 (~24.779, 67.075) ────────────────────────────
    "ne_lat=24.7890&ne_lng=67.0850&sw_lat=24.7790&sw_lng=67.0750",  # DHA-Ph5/1
    "ne_lat=24.7890&ne_lng=67.0750&sw_lat=24.7790&sw_lng=67.0650",  # DHA-Ph5/2
    "ne_lat=24.7790&ne_lng=67.0850&sw_lat=24.7690&sw_lng=67.0750",  # DHA-Ph5/3
    "ne_lat=24.7790&ne_lng=67.0750&sw_lat=24.7690&sw_lng=67.0650",  # DHA-Ph5/4

    # ── DHA Phase 6 (verified ~24.764, 67.081) ────────────────────
    "ne_lat=24.7740&ne_lng=67.0910&sw_lat=24.7640&sw_lng=67.0810",  # DHA-Ph6/1
    "ne_lat=24.7740&ne_lng=67.0810&sw_lat=24.7640&sw_lng=67.0710",  # DHA-Ph6/2
    "ne_lat=24.7640&ne_lng=67.0910&sw_lat=24.7540&sw_lng=67.0810",  # DHA-Ph6/3
    "ne_lat=24.7640&ne_lng=67.0810&sw_lat=24.7540&sw_lng=67.0710",  # DHA-Ph6/4

    # ── DHA Phase 7A / 7B (~24.825, 67.083) ──────────────────────
    "ne_lat=24.8350&ne_lng=67.0930&sw_lat=24.8250&sw_lng=67.0830",  # DHA-Ph7/1
    "ne_lat=24.8350&ne_lng=67.0830&sw_lat=24.8250&sw_lng=67.0730",  # DHA-Ph7/2
    "ne_lat=24.8250&ne_lng=67.0930&sw_lat=24.8150&sw_lng=67.0830",  # DHA-Ph7/3
    "ne_lat=24.8250&ne_lng=67.0830&sw_lat=24.8150&sw_lng=67.0730",  # DHA-Ph7/4

    # ── DHA Phase 8 (verified ~24.840, 67.093) ────────────────────
    "ne_lat=24.8500&ne_lng=67.1030&sw_lat=24.8400&sw_lng=67.0930",  # DHA-Ph8/1
    "ne_lat=24.8500&ne_lng=67.0930&sw_lat=24.8400&sw_lng=67.0830",  # DHA-Ph8/2
    "ne_lat=24.8400&ne_lng=67.1030&sw_lat=24.8300&sw_lng=67.0930",  # DHA-Ph8/3
    "ne_lat=24.8400&ne_lng=67.0930&sw_lat=24.8300&sw_lng=67.0830",  # DHA-Ph8/4

    # ── DHA City (~24.746, 67.079) ────────────────────────────────
    "ne_lat=24.7560&ne_lng=67.0890&sw_lat=24.7460&sw_lng=67.0790",  # DHACity/1
    "ne_lat=24.7560&ne_lng=67.0790&sw_lat=24.7460&sw_lng=67.0690",  # DHACity/2
    "ne_lat=24.7460&ne_lng=67.0890&sw_lat=24.7360&sw_lng=67.0790",  # DHACity/3
    "ne_lat=24.7460&ne_lng=67.0790&sw_lat=24.7360&sw_lng=67.0690",  # DHACity/4

    # ══════════════════════════════════════════════════════════════
    # CLIFTON / BATH ISLAND / SEA VIEW / ZAMZAMA
    # Verified: Clifton Beach ~24.812,67.018 | Boat Basin ~24.832,67.058
    #           Zamzama Blvd ~24.836,67.059 | Sea View ~24.805,67.033
    # ══════════════════════════════════════════════════════════════

    # ── Clifton (verified ~24.818, 67.025) ───────────────────────
    "ne_lat=24.8280&ne_lng=67.0350&sw_lat=24.8180&sw_lng=67.0250",  # Clifton/1
    "ne_lat=24.8280&ne_lng=67.0250&sw_lat=24.8180&sw_lng=67.0150",  # Clifton/2
    "ne_lat=24.8180&ne_lng=67.0350&sw_lat=24.8080&sw_lng=67.0250",  # Clifton/3
    "ne_lat=24.8180&ne_lng=67.0250&sw_lat=24.8080&sw_lng=67.0150",  # Clifton/4

    # ── Bath Island / Creek (~24.827, 67.043) ────────────────────
    "ne_lat=24.8370&ne_lng=67.0530&sw_lat=24.8270&sw_lng=67.0430",  # BathIsland/1
    "ne_lat=24.8370&ne_lng=67.0430&sw_lat=24.8270&sw_lng=67.0330",  # BathIsland/2
    "ne_lat=24.8270&ne_lng=67.0530&sw_lat=24.8170&sw_lng=67.0430",  # BathIsland/3
    "ne_lat=24.8270&ne_lng=67.0430&sw_lat=24.8170&sw_lng=67.0330",  # BathIsland/4

    # ── Boat Basin / Zamzama (~24.834, 67.057) ────────────────────
    "ne_lat=24.8440&ne_lng=67.0670&sw_lat=24.8340&sw_lng=67.0570",  # Zamzama/1
    "ne_lat=24.8440&ne_lng=67.0570&sw_lat=24.8340&sw_lng=67.0470",  # Zamzama/2
    "ne_lat=24.8340&ne_lng=67.0670&sw_lat=24.8240&sw_lng=67.0570",  # Zamzama/3
    "ne_lat=24.8340&ne_lng=67.0570&sw_lat=24.8240&sw_lng=67.0470",  # Zamzama/4

    # ── Sea View / Clifton Beach South (~24.804, 67.032) ─────────
    "ne_lat=24.8140&ne_lng=67.0420&sw_lat=24.8040&sw_lng=67.0320",  # SeaView/1
    "ne_lat=24.8040&ne_lng=67.0420&sw_lat=24.7940&sw_lng=67.0320",  # SeaView/2

    # ── Khayaban-e-Ittehad / Seaview Blvd (~24.845, 67.067) ──────
    "ne_lat=24.8550&ne_lng=67.0770&sw_lat=24.8450&sw_lng=67.0670",  # KhayabanIt/1
    "ne_lat=24.8450&ne_lng=67.0770&sw_lat=24.8350&sw_lng=67.0670",  # KhayabanIt/2

    # ══════════════════════════════════════════════════════════════
    # PECHS / TARIQ ROAD / KCHS / JAMSHED TOWN
    # Verified: PECHS Block 2 ~24.867,67.060 | Tariq Rd ~24.869,67.065
    #           Nursery ~24.873,67.068
    # ══════════════════════════════════════════════════════════════

    # ── PECHS West / Tariq Road (~24.868, 67.058) ─────────────────
    "ne_lat=24.8780&ne_lng=67.0680&sw_lat=24.8680&sw_lng=67.0580",  # PECHS-W/1
    "ne_lat=24.8780&ne_lng=67.0580&sw_lat=24.8680&sw_lng=67.0480",  # PECHS-W/2
    "ne_lat=24.8680&ne_lng=67.0680&sw_lat=24.8580&sw_lng=67.0580",  # PECHS-W/3
    "ne_lat=24.8680&ne_lng=67.0580&sw_lat=24.8580&sw_lng=67.0480",  # PECHS-W/4

    # ── PECHS East / Nursery (~24.874, 67.073) ────────────────────
    "ne_lat=24.8840&ne_lng=67.0830&sw_lat=24.8740&sw_lng=67.0730",  # PECHS-E/1
    "ne_lat=24.8840&ne_lng=67.0730&sw_lat=24.8740&sw_lng=67.0630",  # PECHS-E/2
    "ne_lat=24.8740&ne_lng=67.0830&sw_lat=24.8640&sw_lng=67.0730",  # PECHS-E/3
    "ne_lat=24.8740&ne_lng=67.0730&sw_lat=24.8640&sw_lng=67.0630",  # PECHS-E/4

    # ── KCHS / Khayaban-e-Rahat (~24.851, 67.067) ─────────────────
    "ne_lat=24.8610&ne_lng=67.0770&sw_lat=24.8510&sw_lng=67.0670",  # KCHS/1
    "ne_lat=24.8610&ne_lng=67.0670&sw_lat=24.8510&sw_lng=67.0570",  # KCHS/2
    "ne_lat=24.8510&ne_lng=67.0770&sw_lat=24.8410&sw_lng=67.0670",  # KCHS/3
    "ne_lat=24.8510&ne_lng=67.0670&sw_lat=24.8410&sw_lng=67.0570",  # KCHS/4

    # ── Jamshed Town / Akhtar Colony (~24.884, 67.050) ────────────
    "ne_lat=24.8940&ne_lng=67.0600&sw_lat=24.8840&sw_lng=67.0500",  # Jamshed/1
    "ne_lat=24.8940&ne_lng=67.0500&sw_lat=24.8840&sw_lng=67.0400",  # Jamshed/2
    "ne_lat=24.8840&ne_lng=67.0600&sw_lat=24.8740&sw_lng=67.0500",  # Jamshed/3
    "ne_lat=24.8840&ne_lng=67.0500&sw_lat=24.8740&sw_lng=67.0400",  # Jamshed/4

    # ══════════════════════════════════════════════════════════════
    # SADDAR / CITY AREA / CIVIL LINES / GARDEN
    # Verified: Empress Market ~24.861,67.018 | Burns Rd ~24.863,67.015
    #           Civil Lines ~24.857,66.992 | Karachi Press Club ~24.862,67.012
    # ══════════════════════════════════════════════════════════════

    # ── Saddar (verified ~24.861, 67.013) ────────────────────────
    "ne_lat=24.8710&ne_lng=67.0230&sw_lat=24.8610&sw_lng=67.0130",  # Saddar/1
    "ne_lat=24.8710&ne_lng=67.0130&sw_lat=24.8610&sw_lng=67.0030",  # Saddar/2
    "ne_lat=24.8610&ne_lng=67.0230&sw_lat=24.8510&sw_lng=67.0130",  # Saddar/3
    "ne_lat=24.8610&ne_lng=67.0130&sw_lat=24.8510&sw_lng=67.0030",  # Saddar/4

    # ── Garden / Soldier Bazaar / New Town (~24.875, 67.024) ──────
    "ne_lat=24.8850&ne_lng=67.0340&sw_lat=24.8750&sw_lng=67.0240",  # Garden/1
    "ne_lat=24.8850&ne_lng=67.0240&sw_lat=24.8750&sw_lng=67.0140",  # Garden/2
    "ne_lat=24.8750&ne_lng=67.0340&sw_lat=24.8650&sw_lng=67.0240",  # Garden/3
    "ne_lat=24.8750&ne_lng=67.0240&sw_lat=24.8650&sw_lng=67.0140",  # Garden/4

    # ── Civil Lines / Frere Town / KPT (~24.857, 66.993) ─────────
    "ne_lat=24.8670&ne_lng=67.0030&sw_lat=24.8570&sw_lng=66.9930",  # CivilLines/1
    "ne_lat=24.8670&ne_lng=66.9930&sw_lat=24.8570&sw_lng=66.9830",  # CivilLines/2
    "ne_lat=24.8570&ne_lng=67.0030&sw_lat=24.8470&sw_lng=66.9930",  # CivilLines/3
    "ne_lat=24.8570&ne_lng=66.9930&sw_lat=24.8470&sw_lng=66.9830",  # CivilLines/4

    # ── Kharadar / Old Town / Abdullah Haroon Rd (~24.847, 67.004)
    "ne_lat=24.8570&ne_lng=67.0140&sw_lat=24.8470&sw_lng=67.0040",  # Kharadar/1
    "ne_lat=24.8570&ne_lng=67.0040&sw_lat=24.8470&sw_lng=66.9940",  # Kharadar/2
    "ne_lat=24.8470&ne_lng=67.0140&sw_lat=24.8370&sw_lng=67.0040",  # Kharadar/3
    "ne_lat=24.8470&ne_lng=67.0040&sw_lat=24.8370&sw_lng=66.9940",  # Kharadar/4

    # ── Lyari / Ranchore Line (~24.857, 66.998) ───────────────────
    "ne_lat=24.8670&ne_lng=67.0080&sw_lat=24.8570&sw_lng=66.9980",  # Lyari/1
    "ne_lat=24.8670&ne_lng=66.9980&sw_lat=24.8570&sw_lng=66.9880",  # Lyari/2
    "ne_lat=24.8570&ne_lng=67.0080&sw_lat=24.8470&sw_lng=66.9980",  # Lyari/3
    "ne_lat=24.8570&ne_lng=66.9980&sw_lat=24.8470&sw_lng=66.9880",  # Lyari/4

    # ── Lines Area / Pakistan Chowk (~24.870, 67.003) ─────────────
    "ne_lat=24.8800&ne_lng=67.0130&sw_lat=24.8700&sw_lng=67.0030",  # LinesArea/1
    "ne_lat=24.8700&ne_lng=67.0130&sw_lat=24.8600&sw_lng=67.0030",  # LinesArea/2

    # ══════════════════════════════════════════════════════════════
    # NAZIMABAD / LIAQUATABAD / NEW KARACHI TOWN
    # Verified: Nazimabad No.1 ~24.913,67.019 | North Nazimabad ~24.940,67.033
    #           Liaquatabad No.10 ~24.892,67.028
    # ══════════════════════════════════════════════════════════════

    # ── Nazimabad (verified ~24.913, 67.019) ─────────────────────
    "ne_lat=24.9230&ne_lng=67.0290&sw_lat=24.9130&sw_lng=67.0190",  # Nazimabad/1
    "ne_lat=24.9230&ne_lng=67.0190&sw_lat=24.9130&sw_lng=67.0090",  # Nazimabad/2
    "ne_lat=24.9130&ne_lng=67.0290&sw_lat=24.9030&sw_lng=67.0190",  # Nazimabad/3
    "ne_lat=24.9130&ne_lng=67.0190&sw_lat=24.9030&sw_lng=67.0090",  # Nazimabad/4

    # ── North Nazimabad (verified ~24.940, 67.033) ────────────────
    "ne_lat=24.9500&ne_lng=67.0430&sw_lat=24.9400&sw_lng=67.0330",  # NNazimabad/1
    "ne_lat=24.9500&ne_lng=67.0330&sw_lat=24.9400&sw_lng=67.0230",  # NNazimabad/2
    "ne_lat=24.9400&ne_lng=67.0430&sw_lat=24.9300&sw_lng=67.0330",  # NNazimabad/3
    "ne_lat=24.9400&ne_lng=67.0330&sw_lat=24.9300&sw_lng=67.0230",  # NNazimabad/4

    # ── Liaquatabad (verified ~24.892, 67.028) ────────────────────
    "ne_lat=24.9020&ne_lng=67.0380&sw_lat=24.8920&sw_lng=67.0280",  # Liaquatabad/1
    "ne_lat=24.9020&ne_lng=67.0280&sw_lat=24.8920&sw_lng=67.0180",  # Liaquatabad/2
    "ne_lat=24.8920&ne_lng=67.0380&sw_lat=24.8820&sw_lng=67.0280",  # Liaquatabad/3
    "ne_lat=24.8920&ne_lng=67.0280&sw_lat=24.8820&sw_lng=67.0180",  # Liaquatabad/4

    # ── New Karachi Town / Paposh Nagar (~24.962, 67.042) ─────────
    "ne_lat=24.9720&ne_lng=67.0520&sw_lat=24.9620&sw_lng=67.0420",  # NewKarachi/1
    "ne_lat=24.9720&ne_lng=67.0420&sw_lat=24.9620&sw_lng=67.0320",  # NewKarachi/2
    "ne_lat=24.9620&ne_lng=67.0520&sw_lat=24.9520&sw_lng=67.0420",  # NewKarachi/3
    "ne_lat=24.9620&ne_lng=67.0420&sw_lat=24.9520&sw_lng=67.0320",  # NewKarachi/4

    # ══════════════════════════════════════════════════════════════
    # FEDERAL B AREA (FB Area) / NAGAN CHOWRANGI
    # Verified: FB Area Nagan Chowrangi ~24.929,67.059
    # ══════════════════════════════════════════════════════════════

    # ── Federal B Area North (~24.938, 67.060) ────────────────────
    "ne_lat=24.9480&ne_lng=67.0700&sw_lat=24.9380&sw_lng=67.0600",  # FBA-N/1
    "ne_lat=24.9480&ne_lng=67.0600&sw_lat=24.9380&sw_lng=67.0500",  # FBA-N/2
    "ne_lat=24.9380&ne_lng=67.0700&sw_lat=24.9280&sw_lng=67.0600",  # FBA-N/3
    "ne_lat=24.9380&ne_lng=67.0600&sw_lat=24.9280&sw_lng=67.0500",  # FBA-N/4

    # ── Federal B Area South / Nagan Chowrangi (~24.918, 67.058) ──
    "ne_lat=24.9280&ne_lng=67.0680&sw_lat=24.9180&sw_lng=67.0580",  # FBA-S/1
    "ne_lat=24.9280&ne_lng=67.0580&sw_lat=24.9180&sw_lng=67.0480",  # FBA-S/2
    "ne_lat=24.9180&ne_lng=67.0680&sw_lat=24.9080&sw_lng=67.0580",  # FBA-S/3
    "ne_lat=24.9180&ne_lng=67.0580&sw_lat=24.9080&sw_lng=67.0480",  # FBA-S/4

    # ══════════════════════════════════════════════════════════════
    # GULSHAN-E-IQBAL  (large east-central residential township)
    # Verified: Gulshan Chowrangi ~24.914,67.093
    #           Block 13D/13C ~24.930,67.083 | Block 7 ~24.904,67.104
    # ══════════════════════════════════════════════════════════════

    # ── Gulshan West (Blocks 2-6, ~24.910, 67.079) ────────────────
    "ne_lat=24.9200&ne_lng=67.0890&sw_lat=24.9100&sw_lng=67.0790",  # Gulshan-W/1
    "ne_lat=24.9200&ne_lng=67.0790&sw_lat=24.9100&sw_lng=67.0690",  # Gulshan-W/2
    "ne_lat=24.9100&ne_lng=67.0890&sw_lat=24.9000&sw_lng=67.0790",  # Gulshan-W/3
    "ne_lat=24.9100&ne_lng=67.0790&sw_lat=24.9000&sw_lng=67.0690",  # Gulshan-W/4

    # ── Gulshan Central (Blocks 7-9, ~24.912, 67.098) ─────────────
    "ne_lat=24.9220&ne_lng=67.1080&sw_lat=24.9120&sw_lng=67.0980",  # Gulshan-C/1
    "ne_lat=24.9220&ne_lng=67.0980&sw_lat=24.9120&sw_lng=67.0880",  # Gulshan-C/2
    "ne_lat=24.9120&ne_lng=67.1080&sw_lat=24.9020&sw_lng=67.0980",  # Gulshan-C/3
    "ne_lat=24.9120&ne_lng=67.0980&sw_lat=24.9020&sw_lng=67.0880",  # Gulshan-C/4

    # ── Gulshan East (Blocks 10-14, ~24.910, 67.114) ──────────────
    "ne_lat=24.9200&ne_lng=67.1240&sw_lat=24.9100&sw_lng=67.1140",  # Gulshan-E/1
    "ne_lat=24.9200&ne_lng=67.1140&sw_lat=24.9100&sw_lng=67.1040",  # Gulshan-E/2
    "ne_lat=24.9100&ne_lng=67.1240&sw_lat=24.9000&sw_lng=67.1140",  # Gulshan-E/3
    "ne_lat=24.9100&ne_lng=67.1140&sw_lat=24.9000&sw_lng=67.1040",  # Gulshan-E/4

    # ── Gulshan North (Blocks 13-D/C, ~24.934, 67.087) ────────────
    "ne_lat=24.9440&ne_lng=67.0970&sw_lat=24.9340&sw_lng=67.0870",  # Gulshan-N/1
    "ne_lat=24.9440&ne_lng=67.0870&sw_lat=24.9340&sw_lng=67.0770",  # Gulshan-N/2
    "ne_lat=24.9340&ne_lng=67.0970&sw_lat=24.9240&sw_lng=67.0870",  # Gulshan-N/3
    "ne_lat=24.9340&ne_lng=67.0870&sw_lat=24.9240&sw_lng=67.0770",  # Gulshan-N/4

    # ── University Road / KU fringe (~24.945, 67.113) ─────────────
    "ne_lat=24.9550&ne_lng=67.1230&sw_lat=24.9450&sw_lng=67.1130",  # UniRd/1
    "ne_lat=24.9450&ne_lng=67.1230&sw_lat=24.9350&sw_lng=67.1130",  # UniRd/2

    # ══════════════════════════════════════════════════════════════
    # GULISTAN-E-JAUHAR  (east Karachi)
    # Verified: Jauhar Chowrangi ~24.922,67.133 | Block 15 ~24.933,67.141
    # ══════════════════════════════════════════════════════════════

    # ── Jauhar West (Blocks 1-6, ~24.920, 67.122) ─────────────────
    "ne_lat=24.9300&ne_lng=67.1320&sw_lat=24.9200&sw_lng=67.1220",  # Jauhar-W/1
    "ne_lat=24.9300&ne_lng=67.1220&sw_lat=24.9200&sw_lng=67.1120",  # Jauhar-W/2
    "ne_lat=24.9200&ne_lng=67.1320&sw_lat=24.9100&sw_lng=67.1220",  # Jauhar-W/3
    "ne_lat=24.9200&ne_lng=67.1220&sw_lat=24.9100&sw_lng=67.1120",  # Jauhar-W/4

    # ── Jauhar East (Blocks 12-18, ~24.920, 67.142) ───────────────
    "ne_lat=24.9300&ne_lng=67.1520&sw_lat=24.9200&sw_lng=67.1420",  # Jauhar-E/1
    "ne_lat=24.9300&ne_lng=67.1420&sw_lat=24.9200&sw_lng=67.1320",  # Jauhar-E/2
    "ne_lat=24.9200&ne_lng=67.1520&sw_lat=24.9100&sw_lng=67.1420",  # Jauhar-E/3
    "ne_lat=24.9200&ne_lng=67.1420&sw_lat=24.9100&sw_lng=67.1320",  # Jauhar-E/4

    # ── Jauhar North (~24.938, 67.136) ────────────────────────────
    "ne_lat=24.9480&ne_lng=67.1460&sw_lat=24.9380&sw_lng=67.1360",  # Jauhar-N/1
    "ne_lat=24.9480&ne_lng=67.1360&sw_lat=24.9380&sw_lng=67.1260",  # Jauhar-N/2
    "ne_lat=24.9380&ne_lng=67.1460&sw_lat=24.9280&sw_lng=67.1360",  # Jauhar-N/3
    "ne_lat=24.9380&ne_lng=67.1360&sw_lat=24.9280&sw_lng=67.1260",  # Jauhar-N/4

    # ══════════════════════════════════════════════════════════════
    # SITE / ORANGI TOWN / BALDIA TOWN / WEST KARACHI
    # Verified: SITE ~24.900,67.008 | Orangi Town ~24.958,66.992
    #           Baldia ~24.890,66.977 | Keamari ~24.837,66.987
    # ══════════════════════════════════════════════════════════════

    # ── SITE West (verified ~24.900, 67.005) ─────────────────────
    "ne_lat=24.9100&ne_lng=67.0150&sw_lat=24.9000&sw_lng=67.0050",  # SITE-W/1
    "ne_lat=24.9100&ne_lng=67.0050&sw_lat=24.9000&sw_lng=66.9950",  # SITE-W/2
    "ne_lat=24.9000&ne_lng=67.0150&sw_lat=24.8900&sw_lng=67.0050",  # SITE-W/3
    "ne_lat=24.9000&ne_lng=67.0050&sw_lat=24.8900&sw_lng=66.9950",  # SITE-W/4

    # ── SITE Super Highway / SITE-B (~24.920, 67.024) ─────────────
    "ne_lat=24.9300&ne_lng=67.0340&sw_lat=24.9200&sw_lng=67.0240",  # SITE-B/1
    "ne_lat=24.9200&ne_lng=67.0340&sw_lat=24.9100&sw_lng=67.0240",  # SITE-B/2

    # ── Orangi Town North (~24.966, 66.991) ──────────────────────
    "ne_lat=24.9760&ne_lng=67.0010&sw_lat=24.9660&sw_lng=66.9910",  # Orangi-N/1
    "ne_lat=24.9760&ne_lng=66.9910&sw_lat=24.9660&sw_lng=66.9810",  # Orangi-N/2
    "ne_lat=24.9660&ne_lng=67.0010&sw_lat=24.9560&sw_lng=66.9910",  # Orangi-N/3
    "ne_lat=24.9660&ne_lng=66.9910&sw_lat=24.9560&sw_lng=66.9810",  # Orangi-N/4

    # ── Orangi Town South (~24.945, 66.990) ──────────────────────
    "ne_lat=24.9550&ne_lng=67.0000&sw_lat=24.9450&sw_lng=66.9900",  # Orangi-S/1
    "ne_lat=24.9550&ne_lng=66.9900&sw_lat=24.9450&sw_lng=66.9800",  # Orangi-S/2
    "ne_lat=24.9450&ne_lng=67.0000&sw_lat=24.9350&sw_lng=66.9900",  # Orangi-S/3
    "ne_lat=24.9450&ne_lng=66.9900&sw_lat=24.9350&sw_lng=66.9800",  # Orangi-S/4

    # ── Baldia Town (~24.890, 66.977) ────────────────────────────
    "ne_lat=24.9000&ne_lng=66.9870&sw_lat=24.8900&sw_lng=66.9770",  # Baldia/1
    "ne_lat=24.9000&ne_lng=66.9770&sw_lat=24.8900&sw_lng=66.9670",  # Baldia/2
    "ne_lat=24.8900&ne_lng=66.9870&sw_lat=24.8800&sw_lng=66.9770",  # Baldia/3
    "ne_lat=24.8900&ne_lng=66.9770&sw_lat=24.8800&sw_lng=66.9670",  # Baldia/4

    # ── Keamari / Old Harbour (~24.837, 66.987) ───────────────────
    "ne_lat=24.8470&ne_lng=66.9970&sw_lat=24.8370&sw_lng=66.9870",  # Keamari/1
    "ne_lat=24.8470&ne_lng=66.9870&sw_lat=24.8370&sw_lng=66.9770",  # Keamari/2
    "ne_lat=24.8370&ne_lng=66.9970&sw_lat=24.8270&sw_lng=66.9870",  # Keamari/3
    "ne_lat=24.8370&ne_lng=66.9870&sw_lat=24.8270&sw_lng=66.9770",  # Keamari/4

    # ── Mauripur (~24.862, 66.958) ────────────────────────────────
    "ne_lat=24.8720&ne_lng=66.9680&sw_lat=24.8620&sw_lng=66.9580",  # Mauripur/1
    "ne_lat=24.8720&ne_lng=66.9580&sw_lat=24.8620&sw_lng=66.9480",  # Mauripur/2
    "ne_lat=24.8620&ne_lng=66.9680&sw_lat=24.8520&sw_lng=66.9580",  # Mauripur/3
    "ne_lat=24.8620&ne_lng=66.9580&sw_lat=24.8520&sw_lng=66.9480",  # Mauripur/4

    # ── Hawks Bay / Manora (~24.805, 66.898) ──────────────────────
    "ne_lat=24.8150&ne_lng=66.9080&sw_lat=24.8050&sw_lng=66.8980",  # HawksBay/1
    "ne_lat=24.8050&ne_lng=66.9080&sw_lat=24.7950&sw_lng=66.8980",  # HawksBay/2
    "ne_lat=24.8150&ne_lng=66.8980&sw_lat=24.8050&sw_lng=66.8880",  # HawksBay/3

    # ══════════════════════════════════════════════════════════════
    # NORTH KARACHI / SURJANI TOWN / SCHEME 33 / SCHEME 45
    # ══════════════════════════════════════════════════════════════

    # ── North Karachi (~24.975, 67.060) ──────────────────────────
    "ne_lat=24.9850&ne_lng=67.0700&sw_lat=24.9750&sw_lng=67.0600",  # NKarachi/1
    "ne_lat=24.9850&ne_lng=67.0600&sw_lat=24.9750&sw_lng=67.0500",  # NKarachi/2
    "ne_lat=24.9750&ne_lng=67.0700&sw_lat=24.9650&sw_lng=67.0600",  # NKarachi/3
    "ne_lat=24.9750&ne_lng=67.0600&sw_lat=24.9650&sw_lng=67.0500",  # NKarachi/4

    # ── North Karachi Industrial (~24.966, 67.068) ────────────────
    "ne_lat=24.9760&ne_lng=67.0780&sw_lat=24.9660&sw_lng=67.0680",  # NKarachiInd/1
    "ne_lat=24.9660&ne_lng=67.0780&sw_lat=24.9560&sw_lng=67.0680",  # NKarachiInd/2

    # ── Surjani Town (~25.020, 67.035) ───────────────────────────
    "ne_lat=25.0300&ne_lng=67.0450&sw_lat=25.0200&sw_lng=67.0350",  # Surjani/1
    "ne_lat=25.0300&ne_lng=67.0350&sw_lat=25.0200&sw_lng=67.0250",  # Surjani/2
    "ne_lat=25.0200&ne_lng=67.0450&sw_lat=25.0100&sw_lng=67.0350",  # Surjani/3
    "ne_lat=25.0200&ne_lng=67.0350&sw_lat=25.0100&sw_lng=67.0250",  # Surjani/4

    # ── Scheme 33 (~24.970, 67.113) ──────────────────────────────
    "ne_lat=24.9800&ne_lng=67.1230&sw_lat=24.9700&sw_lng=67.1130",  # Sch33/1
    "ne_lat=24.9800&ne_lng=67.1130&sw_lat=24.9700&sw_lng=67.1030",  # Sch33/2
    "ne_lat=24.9700&ne_lng=67.1230&sw_lat=24.9600&sw_lng=67.1130",  # Sch33/3
    "ne_lat=24.9700&ne_lng=67.1130&sw_lat=24.9600&sw_lng=67.1030",  # Sch33/4

    # ── Scheme 45 (~24.999, 67.089) ──────────────────────────────
    "ne_lat=25.0090&ne_lng=67.0990&sw_lat=24.9990&sw_lng=67.0890",  # Sch45/1
    "ne_lat=25.0090&ne_lng=67.0890&sw_lat=24.9990&sw_lng=67.0790",  # Sch45/2
    "ne_lat=24.9990&ne_lng=67.0990&sw_lat=24.9890&sw_lng=67.0890",  # Sch45/3
    "ne_lat=24.9990&ne_lng=67.0890&sw_lat=24.9890&sw_lng=67.0790",  # Sch45/4

    # ── Manghopir (~24.995, 66.994) ──────────────────────────────
    "ne_lat=25.0050&ne_lng=67.0040&sw_lat=24.9950&sw_lng=66.9940",  # Manghopir/1
    "ne_lat=24.9950&ne_lng=67.0040&sw_lat=24.9850&sw_lng=66.9940",  # Manghopir/2
    "ne_lat=25.0050&ne_lng=66.9940&sw_lat=24.9950&sw_lng=66.9840",  # Manghopir/3

    # ── Gadap Town / Superhighway N fringe (~25.042, 67.116) ──────
    "ne_lat=25.0520&ne_lng=67.1260&sw_lat=25.0420&sw_lng=67.1160",  # Gadap/1
    "ne_lat=25.0420&ne_lng=67.1260&sw_lat=25.0320&sw_lng=67.1160",  # Gadap/2

    # ═══════════════════════════════════════════════════════════════
    # KORANGI / LANDHI / SHAH FAISAL COLONY (SE industrial belt)
    # Verified: Korangi Crossing ~24.834,67.133 | Landhi ~24.856,67.180
    #           Shah Faisal Colony No.1 ~24.872,67.128
    # ═══════════════════════════════════════════════════════════════

    # ── Korangi Town (~24.834, 67.132) ────────────────────────────
    "ne_lat=24.8440&ne_lng=67.1420&sw_lat=24.8340&sw_lng=67.1320",  # Korangi/1
    "ne_lat=24.8440&ne_lng=67.1320&sw_lat=24.8340&sw_lng=67.1220",  # Korangi/2
    "ne_lat=24.8340&ne_lng=67.1420&sw_lat=24.8240&sw_lng=67.1320",  # Korangi/3
    "ne_lat=24.8340&ne_lng=67.1320&sw_lat=24.8240&sw_lng=67.1220",  # Korangi/4

    # ── Korangi Industrial Area (~24.808, 67.147) ─────────────────
    "ne_lat=24.8180&ne_lng=67.1570&sw_lat=24.8080&sw_lng=67.1470",  # KorangiInd/1
    "ne_lat=24.8080&ne_lng=67.1570&sw_lat=24.7980&sw_lng=67.1470",  # KorangiInd/2
    "ne_lat=24.8180&ne_lng=67.1470&sw_lat=24.8080&sw_lng=67.1370",  # KorangiInd/3

    # ── Creek City / Khayaban-e-Amin (~24.809, 67.107) ────────────
    "ne_lat=24.8190&ne_lng=67.1170&sw_lat=24.8090&sw_lng=67.1070",  # CreekCity/1
    "ne_lat=24.8090&ne_lng=67.1170&sw_lat=24.7990&sw_lng=67.1070",  # CreekCity/2

    # ── Shah Faisal Colony (verified ~24.872, 67.128) ─────────────
    "ne_lat=24.8820&ne_lng=67.1380&sw_lat=24.8720&sw_lng=67.1280",  # ShahFaisal/1
    "ne_lat=24.8820&ne_lng=67.1280&sw_lat=24.8720&sw_lng=67.1180",  # ShahFaisal/2
    "ne_lat=24.8720&ne_lng=67.1380&sw_lat=24.8620&sw_lng=67.1280",  # ShahFaisal/3
    "ne_lat=24.8720&ne_lng=67.1280&sw_lat=24.8620&sw_lng=67.1180",  # ShahFaisal/4

    # ── Landhi (~24.856, 67.179) ─────────────────────────────────
    "ne_lat=24.8660&ne_lng=67.1890&sw_lat=24.8560&sw_lng=67.1790",  # Landhi/1
    "ne_lat=24.8660&ne_lng=67.1790&sw_lat=24.8560&sw_lng=67.1690",  # Landhi/2
    "ne_lat=24.8560&ne_lng=67.1890&sw_lat=24.8460&sw_lng=67.1790",  # Landhi/3
    "ne_lat=24.8560&ne_lng=67.1790&sw_lat=24.8460&sw_lng=67.1690",  # Landhi/4

    # ── Quaidabad / Landhi Colony (~24.838, 67.162) ───────────────
    "ne_lat=24.8480&ne_lng=67.1720&sw_lat=24.8380&sw_lng=67.1620",  # Quaidabad/1
    "ne_lat=24.8380&ne_lng=67.1720&sw_lat=24.8280&sw_lng=67.1620",  # Quaidabad/2

    # ── Malir Town (~24.888, 67.191) ─────────────────────────────
    "ne_lat=24.8980&ne_lng=67.2010&sw_lat=24.8880&sw_lng=67.1910",  # Malir/1
    "ne_lat=24.8980&ne_lng=67.1910&sw_lat=24.8880&sw_lng=67.1810",  # Malir/2
    "ne_lat=24.8880&ne_lng=67.2010&sw_lat=24.8780&sw_lng=67.1910",  # Malir/3
    "ne_lat=24.8880&ne_lng=67.1910&sw_lat=24.8780&sw_lng=67.1810",  # Malir/4

    # ── Malir City / Gulshan-e-Hadeed (~24.910, 67.215) ───────────
    "ne_lat=24.9200&ne_lng=67.2250&sw_lat=24.9100&sw_lng=67.2150",  # MalirCity/1
    "ne_lat=24.9100&ne_lng=67.2250&sw_lat=24.9000&sw_lng=67.2150",  # MalirCity/2

    # ── Karachi Airport / PAF Faisal Base (~24.906, 67.161) ───────
    "ne_lat=24.9160&ne_lng=67.1710&sw_lat=24.9060&sw_lng=67.1610",  # Airport/1
    "ne_lat=24.9060&ne_lng=67.1710&sw_lat=24.8960&sw_lng=67.1610",  # Airport/2

    # ══════════════════════════════════════════════════════════════
    # BAHRIA TOWN KARACHI  (far west, M-9 Motorway / Superhighway)
    # Verified: Main gate ~24.856,66.937 | Precinct 35 ~24.849,66.950
    #           Sports City ~24.870,66.943
    # ══════════════════════════════════════════════════════════════

    # ── BTK East / Precincts 1-18 (~24.858, 66.957) ───────────────
    "ne_lat=24.8680&ne_lng=66.9670&sw_lat=24.8580&sw_lng=66.9570",  # BTK-E/1
    "ne_lat=24.8680&ne_lng=66.9570&sw_lat=24.8580&sw_lng=66.9470",  # BTK-E/2
    "ne_lat=24.8580&ne_lng=66.9670&sw_lat=24.8480&sw_lng=66.9570",  # BTK-E/3
    "ne_lat=24.8580&ne_lng=66.9570&sw_lat=24.8480&sw_lng=66.9470",  # BTK-E/4

    # ── BTK West / Precincts 25-45 (~24.848, 66.928) ──────────────
    "ne_lat=24.8580&ne_lng=66.9380&sw_lat=24.8480&sw_lng=66.9280",  # BTK-W/1
    "ne_lat=24.8580&ne_lng=66.9280&sw_lat=24.8480&sw_lng=66.9180",  # BTK-W/2
    "ne_lat=24.8480&ne_lng=66.9380&sw_lat=24.8380&sw_lng=66.9280",  # BTK-W/3
    "ne_lat=24.8480&ne_lng=66.9280&sw_lat=24.8380&sw_lng=66.9180",  # BTK-W/4

    # ── BTK North / Sports City (~24.872, 66.942) ─────────────────
    "ne_lat=24.8820&ne_lng=66.9520&sw_lat=24.8720&sw_lng=66.9420",  # BTK-N/1
    "ne_lat=24.8820&ne_lng=66.9420&sw_lat=24.8720&sw_lng=66.9320",  # BTK-N/2
    "ne_lat=24.8720&ne_lng=66.9520&sw_lat=24.8620&sw_lng=66.9420",  # BTK-N/3
    "ne_lat=24.8720&ne_lng=66.9420&sw_lat=24.8620&sw_lng=66.9320",  # BTK-N/4

    # ── BTK South / Precinct 35-40 (~24.832, 66.942) ──────────────
    "ne_lat=24.8420&ne_lng=66.9520&sw_lat=24.8320&sw_lng=66.9420",  # BTK-S/1
    "ne_lat=24.8420&ne_lng=66.9420&sw_lat=24.8320&sw_lng=66.9320",  # BTK-S/2
    "ne_lat=24.8320&ne_lng=66.9520&sw_lat=24.8220&sw_lng=66.9420",  # BTK-S/3
    "ne_lat=24.8320&ne_lng=66.9420&sw_lat=24.8220&sw_lng=66.9320",  # BTK-S/4

    # ══════════════════════════════════════════════════════════════
    # PORT QASIM / BIN QASIM TOWN  (far east industrial)
    # Verified: Port Qasim ~24.786,67.319 | Pakistan Steel ~24.756,67.265
    # ══════════════════════════════════════════════════════════════

    # ── Port Qasim (~24.786, 67.319) ─────────────────────────────
    "ne_lat=24.7960&ne_lng=67.3290&sw_lat=24.7860&sw_lng=67.3190",  # PortQasim/1
    "ne_lat=24.7960&ne_lng=67.3190&sw_lat=24.7860&sw_lng=67.3090",  # PortQasim/2
    "ne_lat=24.7860&ne_lng=67.3290&sw_lat=24.7760&sw_lng=67.3190",  # PortQasim/3
    "ne_lat=24.7860&ne_lng=67.3190&sw_lat=24.7760&sw_lng=67.3090",  # PortQasim/4

    # ── Pakistan Steel / Bin Qasim (~24.756, 67.265) ──────────────
    "ne_lat=24.7660&ne_lng=67.2750&sw_lat=24.7560&sw_lng=67.2650",  # PakSteel/1
    "ne_lat=24.7660&ne_lng=67.2650&sw_lat=24.7560&sw_lng=67.2550",  # PakSteel/2
    "ne_lat=24.7560&ne_lng=67.2750&sw_lat=24.7460&sw_lng=67.2650",  # PakSteel/3
    "ne_lat=24.7560&ne_lng=67.2650&sw_lat=24.7460&sw_lng=67.2550",  # PakSteel/4

    # ── Bin Qasim Town / IBD Road fringe (~24.828, 67.248) ────────
    "ne_lat=24.8380&ne_lng=67.2580&sw_lat=24.8280&sw_lng=67.2480",  # BQTown/1
    "ne_lat=24.8280&ne_lng=67.2580&sw_lat=24.8180&sw_lng=67.2480",  # BQTown/2

    # ══════════════════════════════════════════════════════════════
    # MISC / LANDMARK ZONES
    # ══════════════════════════════════════════════════════════════

    # ── Karachi University (~24.942, 67.115) ──────────────────────
    "ne_lat=24.9520&ne_lng=67.1250&sw_lat=24.9420&sw_lng=67.1150",  # KU/1
    "ne_lat=24.9420&ne_lng=67.1250&sw_lat=24.9320&sw_lng=67.1150",  # KU/2

    # ── Askari IV / V Karachi (~24.895, 67.073) ───────────────────
    "ne_lat=24.9050&ne_lng=67.0830&sw_lat=24.8950&sw_lng=67.0730",  # AskariK/1
    "ne_lat=24.8950&ne_lng=67.0830&sw_lat=24.8850&sw_lng=67.0730",  # AskariK/2

    # ── Karachi Expo / Stadium (~24.930, 67.103) ──────────────────
    "ne_lat=24.9400&ne_lng=67.1130&sw_lat=24.9300&sw_lng=67.1030",  # Expo/1
    "ne_lat=24.9300&ne_lng=67.1130&sw_lat=24.9200&sw_lng=67.1030",  # Expo/2

    # ── Superhighway / M-9 South fringe (~24.895, 66.973) ─────────
    "ne_lat=24.9050&ne_lng=66.9830&sw_lat=24.8950&sw_lng=66.9730",  # M9-South/1
    "ne_lat=24.8950&ne_lng=66.9830&sw_lat=24.8850&sw_lng=66.9730",  # M9-South/2

    # ── Super Highway North corridor (~25.048, 67.091) ────────────
    "ne_lat=25.0580&ne_lng=67.1010&sw_lat=25.0480&sw_lng=67.0910",  # SuperHwy/1
    "ne_lat=25.0480&ne_lng=67.1010&sw_lat=25.0380&sw_lng=67.0910",  # SuperHwy/2

    # ── Korangi Creek / Ibrahim Hyderi (~24.786, 67.128) ──────────
    "ne_lat=24.7960&ne_lng=67.1380&sw_lat=24.7860&sw_lng=67.1280",  # IbrahimH/1
    "ne_lat=24.7860&ne_lng=67.1380&sw_lat=24.7760&sw_lng=67.1280",  # IbrahimH/2

    # ── Kemari / West Wharf port area (~24.829, 66.980) ───────────
    "ne_lat=24.8390&ne_lng=66.9900&sw_lat=24.8290&sw_lng=66.9800",  # WestWharf/1
    "ne_lat=24.8290&ne_lng=66.9900&sw_lat=24.8190&sw_lng=66.9800",  # WestWharf/2

    # ── Korangi No.1 / No.2 / No.3 blocks (~24.855, 67.118) ──────
    "ne_lat=24.8650&ne_lng=67.1280&sw_lat=24.8550&sw_lng=67.1180",  # KorangiBlk/1
    "ne_lat=24.8550&ne_lng=67.1280&sw_lat=24.8450&sw_lng=67.1180",  # KorangiBlk/2

]

# ─────────────────────────────────────────────────────────────────────────────
# Faisalabad areas + sub-areas bounding boxes
# Strategy: generous boxes (~0.010° padding from verified centers) with overlap
# to ensure full coverage. Verified anchor centers sourced from OSM/findlatlong.
# Each area ~2km x 2km; sub-areas split into 4 quadrants (~1km each).
# Overlap is intentional — cumulative coverage beats precision gaps.
# Faisalabad center: ~31.4175°N, 73.0910°E (Clock Tower / Ghanta Ghar)
# At this latitude: 0.01° lat ≈ 1.11 km | 0.01° lng ≈ 0.95 km
# ─────────────────────────────────────────────────────────────────────────────

faisalabad_areas = [

    # ══════════════════════════════════════════════════════════════
    # OLD CITY / CLOCK TOWER BAZAARS
    # The famous 8-road radial plan from Ghanta Ghar (~31.418, 73.091)
    # Bazaars: Katchehry, Rail, Karkhana, Bhawana, Mochiwala,
    #          Chiniot, Jail, Montgomery
    # ══════════════════════════════════════════════════════════════

    # ── Clock Tower core (verified ~31.418, 73.091) ───────────────
    "ne_lat=31.4280&ne_lng=73.1010&sw_lat=31.4180&sw_lng=73.0910",  # ClockTower/1
    "ne_lat=31.4280&ne_lng=73.0910&sw_lat=31.4180&sw_lng=73.0810",  # ClockTower/2
    "ne_lat=31.4180&ne_lng=73.1010&sw_lat=31.4080&sw_lng=73.0910",  # ClockTower/3
    "ne_lat=31.4180&ne_lng=73.0910&sw_lat=31.4080&sw_lng=73.0810",  # ClockTower/4

    # ── Rail Bazaar / Railway Station (~31.422, 73.095) ────────────
    "ne_lat=31.4320&ne_lng=73.1050&sw_lat=31.4220&sw_lng=73.0950",  # RailBazaar/1
    "ne_lat=31.4220&ne_lng=73.1050&sw_lat=31.4120&sw_lng=73.0950",  # RailBazaar/2

    # ── Karkhana Bazaar / West old city (~31.418, 73.082) ─────────
    "ne_lat=31.4280&ne_lng=73.0920&sw_lat=31.4180&sw_lng=73.0820",  # Karkhana/1
    "ne_lat=31.4180&ne_lng=73.0920&sw_lat=31.4080&sw_lng=73.0820",  # Karkhana/2

    # ── Chiniot Bazaar / East old city (~31.418, 73.100) ──────────
    "ne_lat=31.4280&ne_lng=73.1100&sw_lat=31.4180&sw_lng=73.1000",  # ChiniotBzr/1
    "ne_lat=31.4180&ne_lng=73.1100&sw_lat=31.4080&sw_lng=73.1000",  # ChiniotBzr/2

    # ── Jail Road / Katchehry Bazaar (~31.410, 73.090) ────────────
    "ne_lat=31.4200&ne_lng=73.1000&sw_lat=31.4100&sw_lng=73.0900",  # JailRd/1
    "ne_lat=31.4100&ne_lng=73.1000&sw_lat=31.4000&sw_lng=73.0900",  # JailRd/2

    # ── Lyallpur / Mochiwala Bazaar south (~31.406, 73.085) ───────
    "ne_lat=31.4160&ne_lng=73.0950&sw_lat=31.4060&sw_lng=73.0850",  # Mochiwala/1
    "ne_lat=31.4060&ne_lng=73.0950&sw_lat=31.3960&sw_lng=73.0850",  # Mochiwala/2

    # ══════════════════════════════════════════════════════════════
    # CIVIL LINES / D-GROUND / NEW CIVIL LINES
    # Verified: Civil Lines ~31.431,73.093 | D-Ground ~31.426,73.090
    #           Allied Hospital ~31.427,73.093
    # ══════════════════════════════════════════════════════════════

    # ── Civil Lines (verified ~31.431, 73.093) ────────────────────
    "ne_lat=31.4410&ne_lng=73.1030&sw_lat=31.4310&sw_lng=73.0930",  # CivilLines/1
    "ne_lat=31.4410&ne_lng=73.0930&sw_lat=31.4310&sw_lng=73.0830",  # CivilLines/2
    "ne_lat=31.4310&ne_lng=73.1030&sw_lat=31.4210&sw_lng=73.0930",  # CivilLines/3
    "ne_lat=31.4310&ne_lng=73.0930&sw_lat=31.4210&sw_lng=73.0830",  # CivilLines/4

    # ── GC University / GCU area (~31.422, 73.086) ────────────────
    "ne_lat=31.4320&ne_lng=73.0960&sw_lat=31.4220&sw_lng=73.0860",  # GCU/1
    "ne_lat=31.4320&ne_lng=73.0860&sw_lat=31.4220&sw_lng=73.0760",  # GCU/2
    "ne_lat=31.4220&ne_lng=73.0960&sw_lat=31.4120&sw_lng=73.0860",  # GCU/3
    "ne_lat=31.4220&ne_lng=73.0860&sw_lat=31.4120&sw_lng=73.0760",  # GCU/4

    # ── New Civil Lines (~31.443, 73.097) ─────────────────────────
    "ne_lat=31.4530&ne_lng=73.1070&sw_lat=31.4430&sw_lng=73.0970",  # NewCivil/1
    "ne_lat=31.4530&ne_lng=73.0970&sw_lat=31.4430&sw_lng=73.0870",  # NewCivil/2
    "ne_lat=31.4430&ne_lng=73.1070&sw_lat=31.4330&sw_lng=73.0970",  # NewCivil/3
    "ne_lat=31.4430&ne_lng=73.0970&sw_lat=31.4330&sw_lng=73.0870",  # NewCivil/4

    # ══════════════════════════════════════════════════════════════
    # PEOPLES COLONY / OFFICERS COLONY / BATALA COLONY
    # Verified: Peoples Colony No.1 ~31.438,73.107
    #           Peoples Colony No.2 ~31.444,73.116
    # ══════════════════════════════════════════════════════════════

    # ── Peoples Colony No.1 (verified ~31.438, 73.107) ────────────
    "ne_lat=31.4480&ne_lng=73.1170&sw_lat=31.4380&sw_lng=73.1070",  # PC1/1
    "ne_lat=31.4480&ne_lng=73.1070&sw_lat=31.4380&sw_lng=73.0970",  # PC1/2
    "ne_lat=31.4380&ne_lng=73.1170&sw_lat=31.4280&sw_lng=73.1070",  # PC1/3
    "ne_lat=31.4380&ne_lng=73.1070&sw_lat=31.4280&sw_lng=73.0970",  # PC1/4

    # ── Peoples Colony No.2 (~31.444, 73.117) ─────────────────────
    "ne_lat=31.4540&ne_lng=73.1270&sw_lat=31.4440&sw_lng=73.1170",  # PC2/1
    "ne_lat=31.4540&ne_lng=73.1170&sw_lat=31.4440&sw_lng=73.1070",  # PC2/2
    "ne_lat=31.4440&ne_lng=73.1270&sw_lat=31.4340&sw_lng=73.1170",  # PC2/3
    "ne_lat=31.4440&ne_lng=73.1170&sw_lat=31.4340&sw_lng=73.1070",  # PC2/4

    # ── Officers Colony (~31.443, 73.109) ─────────────────────────
    "ne_lat=31.4530&ne_lng=73.1190&sw_lat=31.4430&sw_lng=73.1090",  # Officers/1
    "ne_lat=31.4430&ne_lng=73.1190&sw_lat=31.4330&sw_lng=73.1090",  # Officers/2

    # ── Batala Colony (~31.427, 73.118) ───────────────────────────
    "ne_lat=31.4370&ne_lng=73.1280&sw_lat=31.4270&sw_lng=73.1180",  # Batala/1
    "ne_lat=31.4370&ne_lng=73.1180&sw_lat=31.4270&sw_lng=73.1080",  # Batala/2
    "ne_lat=31.4270&ne_lng=73.1280&sw_lat=31.4170&sw_lng=73.1180",  # Batala/3
    "ne_lat=31.4270&ne_lng=73.1180&sw_lat=31.4170&sw_lng=73.1080",  # Batala/4

    # ══════════════════════════════════════════════════════════════
    # MODEL TOWN / D-TYPE COLONY / NISHTAR COLONY
    # ══════════════════════════════════════════════════════════════

    # ── Model Town (~31.458, 73.103) ──────────────────────────────
    "ne_lat=31.4680&ne_lng=73.1130&sw_lat=31.4580&sw_lng=73.1030",  # ModelTown/1
    "ne_lat=31.4680&ne_lng=73.1030&sw_lat=31.4580&sw_lng=73.0930",  # ModelTown/2
    "ne_lat=31.4580&ne_lng=73.1130&sw_lat=31.4480&sw_lng=73.1030",  # ModelTown/3
    "ne_lat=31.4580&ne_lng=73.1030&sw_lat=31.4480&sw_lng=73.0930",  # ModelTown/4

    # ── D-Type Colony (~31.425, 73.100) ───────────────────────────
    "ne_lat=31.4350&ne_lng=73.1100&sw_lat=31.4250&sw_lng=73.1000",  # DType/1
    "ne_lat=31.4350&ne_lng=73.1000&sw_lat=31.4250&sw_lng=73.0900",  # DType/2
    "ne_lat=31.4250&ne_lng=73.1100&sw_lat=31.4150&sw_lng=73.1000",  # DType/3
    "ne_lat=31.4250&ne_lng=73.1000&sw_lat=31.4150&sw_lng=73.0900",  # DType/4

    # ── Nishtar Colony (~31.407, 73.120) ──────────────────────────
    "ne_lat=31.4170&ne_lng=73.1300&sw_lat=31.4070&sw_lng=73.1200",  # Nishtar/1
    "ne_lat=31.4170&ne_lng=73.1200&sw_lat=31.4070&sw_lng=73.1100",  # Nishtar/2
    "ne_lat=31.4070&ne_lng=73.1300&sw_lat=31.3970&sw_lng=73.1200",  # Nishtar/3
    "ne_lat=31.4070&ne_lng=73.1200&sw_lat=31.3970&sw_lng=73.1100",  # Nishtar/4

    # ── Jinnah Colony (~31.408, 73.111) ───────────────────────────
    "ne_lat=31.4180&ne_lng=73.1210&sw_lat=31.4080&sw_lng=73.1110",  # Jinnah/1
    "ne_lat=31.4180&ne_lng=73.1110&sw_lat=31.4080&sw_lng=73.1010",  # Jinnah/2
    "ne_lat=31.4080&ne_lng=73.1210&sw_lat=31.3980&sw_lng=73.1110",  # Jinnah/3
    "ne_lat=31.4080&ne_lng=73.1110&sw_lat=31.3980&sw_lng=73.1010",  # Jinnah/4

    # ══════════════════════════════════════════════════════════════
    # CANAL ROAD / GULBERG / AZIZ COLONY
    # Verified: Gulberg No.1 ~31.454,73.143 | Canal Rd ~31.453,73.132
    #           Firdous Market ~31.448,73.130
    # ══════════════════════════════════════════════════════════════

    # ── Canal Road West (~31.452, 73.122) ─────────────────────────
    "ne_lat=31.4620&ne_lng=73.1320&sw_lat=31.4520&sw_lng=73.1220",  # Canal-W/1
    "ne_lat=31.4620&ne_lng=73.1220&sw_lat=31.4520&sw_lng=73.1120",  # Canal-W/2
    "ne_lat=31.4520&ne_lng=73.1320&sw_lat=31.4420&sw_lng=73.1220",  # Canal-W/3
    "ne_lat=31.4520&ne_lng=73.1220&sw_lat=31.4420&sw_lng=73.1120",  # Canal-W/4

    # ── Canal Road East / Firdous (~31.450, 73.138) ───────────────
    "ne_lat=31.4600&ne_lng=73.1480&sw_lat=31.4500&sw_lng=73.1380",  # Canal-E/1
    "ne_lat=31.4600&ne_lng=73.1380&sw_lat=31.4500&sw_lng=73.1280",  # Canal-E/2
    "ne_lat=31.4500&ne_lng=73.1480&sw_lat=31.4400&sw_lng=73.1380",  # Canal-E/3
    "ne_lat=31.4500&ne_lng=73.1380&sw_lat=31.4400&sw_lng=73.1280",  # Canal-E/4

    # ── Gulberg No.1 / No.2 (~31.454, 73.144) ─────────────────────
    "ne_lat=31.4640&ne_lng=73.1540&sw_lat=31.4540&sw_lng=73.1440",  # Gulberg/1
    "ne_lat=31.4640&ne_lng=73.1440&sw_lat=31.4540&sw_lng=73.1340",  # Gulberg/2
    "ne_lat=31.4540&ne_lng=73.1540&sw_lat=31.4440&sw_lng=73.1440",  # Gulberg/3
    "ne_lat=31.4540&ne_lng=73.1440&sw_lat=31.4440&sw_lng=73.1340",  # Gulberg/4

    # ── Aziz Colony (~31.436, 73.132) ─────────────────────────────
    "ne_lat=31.4460&ne_lng=73.1420&sw_lat=31.4360&sw_lng=73.1320",  # Aziz/1
    "ne_lat=31.4460&ne_lng=73.1320&sw_lat=31.4360&sw_lng=73.1220",  # Aziz/2
    "ne_lat=31.4360&ne_lng=73.1420&sw_lat=31.4260&sw_lng=73.1320",  # Aziz/3
    "ne_lat=31.4360&ne_lng=73.1320&sw_lat=31.4260&sw_lng=73.1220",  # Aziz/4

    # ── Gulshan-e-Iqbal (~31.454, 73.127) ─────────────────────────
    "ne_lat=31.4640&ne_lng=73.1370&sw_lat=31.4540&sw_lng=73.1270",  # GulshaneIqbal/1
    "ne_lat=31.4540&ne_lng=73.1370&sw_lat=31.4440&sw_lng=73.1270",  # GulshaneIqbal/2

    # ══════════════════════════════════════════════════════════════
    # MADINA TOWN / SUSAN ROAD / SAMANABAD
    # Verified: Madina Town ~31.463,73.095 | Susan Road ~31.476,73.114
    # ══════════════════════════════════════════════════════════════

    # ── Madina Town (~31.463, 73.095) ─────────────────────────────
    "ne_lat=31.4730&ne_lng=73.1050&sw_lat=31.4630&sw_lng=73.0950",  # Madina/1
    "ne_lat=31.4730&ne_lng=73.0950&sw_lat=31.4630&sw_lng=73.0850",  # Madina/2
    "ne_lat=31.4630&ne_lng=73.1050&sw_lat=31.4530&sw_lng=73.0950",  # Madina/3
    "ne_lat=31.4630&ne_lng=73.0950&sw_lat=31.4530&sw_lng=73.0850",  # Madina/4

    # ── Susan Road North (~31.476, 73.114) ────────────────────────
    "ne_lat=31.4860&ne_lng=73.1240&sw_lat=31.4760&sw_lng=73.1140",  # Susan-N/1
    "ne_lat=31.4860&ne_lng=73.1140&sw_lat=31.4760&sw_lng=73.1040",  # Susan-N/2
    "ne_lat=31.4760&ne_lng=73.1240&sw_lat=31.4660&sw_lng=73.1140",  # Susan-N/3
    "ne_lat=31.4760&ne_lng=73.1140&sw_lat=31.4660&sw_lng=73.1040",  # Susan-N/4

    # ── Susan Road South / Susan Gardens (~31.460, 73.113) ────────
    "ne_lat=31.4700&ne_lng=73.1230&sw_lat=31.4600&sw_lng=73.1130",  # Susan-S/1
    "ne_lat=31.4600&ne_lng=73.1230&sw_lat=31.4500&sw_lng=73.1130",  # Susan-S/2

    # ── Samanabad (~31.476, 73.098) ───────────────────────────────
    "ne_lat=31.4860&ne_lng=73.1080&sw_lat=31.4760&sw_lng=73.0980",  # Samanabad/1
    "ne_lat=31.4760&ne_lng=73.1080&sw_lat=31.4660&sw_lng=73.0980",  # Samanabad/2

    # ══════════════════════════════════════════════════════════════
    # DHA FAISALABAD / NEW CITY / NORTHERN EXPANSION
    # ══════════════════════════════════════════════════════════════

    # ── DHA Faisalabad (~31.478, 73.108) ──────────────────────────
    "ne_lat=31.4880&ne_lng=73.1180&sw_lat=31.4780&sw_lng=73.1080",  # DHA-FSD/1
    "ne_lat=31.4880&ne_lng=73.1080&sw_lat=31.4780&sw_lng=73.0980",  # DHA-FSD/2
    "ne_lat=31.4780&ne_lng=73.1180&sw_lat=31.4680&sw_lng=73.1080",  # DHA-FSD/3
    "ne_lat=31.4780&ne_lng=73.1080&sw_lat=31.4680&sw_lng=73.0980",  # DHA-FSD/4

    # ── New City / Faisalabad North (~31.496, 73.110) ─────────────
    "ne_lat=31.5060&ne_lng=73.1200&sw_lat=31.4960&sw_lng=73.1100",  # NewCity/1
    "ne_lat=31.5060&ne_lng=73.1100&sw_lat=31.4960&sw_lng=73.1000",  # NewCity/2
    "ne_lat=31.4960&ne_lng=73.1200&sw_lat=31.4860&sw_lng=73.1100",  # NewCity/3
    "ne_lat=31.4960&ne_lng=73.1100&sw_lat=31.4860&sw_lng=73.1000",  # NewCity/4

    # ── Chak Jhumra Road / far north (~31.505, 73.094) ────────────
    "ne_lat=31.5150&ne_lng=73.1040&sw_lat=31.5050&sw_lng=73.0940",  # ChakJhumra/1
    "ne_lat=31.5050&ne_lng=73.1040&sw_lat=31.4950&sw_lng=73.0940",  # ChakJhumra/2

    # ══════════════════════════════════════════════════════════════
    # MILLAT ROAD / SARGODHA ROAD (west Faisalabad)
    # Verified: Millat Road ~31.430,73.068
    #           UAF (Agriculture University) ~31.430,73.063
    # ══════════════════════════════════════════════════════════════

    # ── Millat Road / Millat Town (~31.430, 73.068) ───────────────
    "ne_lat=31.4400&ne_lng=73.0780&sw_lat=31.4300&sw_lng=73.0680",  # Millat/1
    "ne_lat=31.4400&ne_lng=73.0680&sw_lat=31.4300&sw_lng=73.0580",  # Millat/2
    "ne_lat=31.4300&ne_lng=73.0780&sw_lat=31.4200&sw_lng=73.0680",  # Millat/3
    "ne_lat=31.4300&ne_lng=73.0680&sw_lat=31.4200&sw_lng=73.0580",  # Millat/4

    # ── Sargodha Road / Khurarianwala (~31.441, 73.075) ───────────
    "ne_lat=31.4510&ne_lng=73.0850&sw_lat=31.4410&sw_lng=73.0750",  # SargodhRd/1
    "ne_lat=31.4510&ne_lng=73.0750&sw_lat=31.4410&sw_lng=73.0650",  # SargodhRd/2
    "ne_lat=31.4410&ne_lng=73.0850&sw_lat=31.4310&sw_lng=73.0750",  # SargodhRd/3
    "ne_lat=31.4410&ne_lng=73.0750&sw_lat=31.4310&sw_lng=73.0650",  # SargodhRd/4

    # ── Jhang Road / West fringe (~31.415, 73.060) ────────────────
    "ne_lat=31.4250&ne_lng=73.0700&sw_lat=31.4150&sw_lng=73.0600",  # JhangRd/1
    "ne_lat=31.4250&ne_lng=73.0600&sw_lat=31.4150&sw_lng=73.0500",  # JhangRd/2
    "ne_lat=31.4150&ne_lng=73.0700&sw_lat=31.4050&sw_lng=73.0600",  # JhangRd/3
    "ne_lat=31.4150&ne_lng=73.0600&sw_lat=31.4050&sw_lng=73.0500",  # JhangRd/4

    # ══════════════════════════════════════════════════════════════
    # UAF / AGRICULTURE UNIVERSITY / INDUSTRIAL ESTATE (FIEDMC)
    # Verified: UAF main gate ~31.430,73.063
    #           FIEDMC / Industrial Estate ~31.462,73.070
    # ══════════════════════════════════════════════════════════════

    # ── University of Agriculture Faisalabad (~31.430, 73.063) ────
    "ne_lat=31.4400&ne_lng=73.0730&sw_lat=31.4300&sw_lng=73.0630",  # UAF/1
    "ne_lat=31.4300&ne_lng=73.0730&sw_lat=31.4200&sw_lng=73.0630",  # UAF/2

    # ── FIEDMC Industrial Estate North (~31.462, 73.070) ──────────
    "ne_lat=31.4720&ne_lng=73.0800&sw_lat=31.4620&sw_lng=73.0700",  # FIEDMC-N/1
    "ne_lat=31.4720&ne_lng=73.0700&sw_lat=31.4620&sw_lng=73.0600",  # FIEDMC-N/2
    "ne_lat=31.4620&ne_lng=73.0800&sw_lat=31.4520&sw_lng=73.0700",  # FIEDMC-N/3
    "ne_lat=31.4620&ne_lng=73.0700&sw_lat=31.4520&sw_lng=73.0600",  # FIEDMC-N/4

    # ── FIEDMC / M3 Industrial City South (~31.445, 73.063) ───────
    "ne_lat=31.4550&ne_lng=73.0730&sw_lat=31.4450&sw_lng=73.0630",  # FIEDMC-S/1
    "ne_lat=31.4450&ne_lng=73.0730&sw_lat=31.4350&sw_lng=73.0630",  # FIEDMC-S/2

    # ── Sitara / Textile Mills cluster (~31.430, 73.050) ──────────
    "ne_lat=31.4400&ne_lng=73.0600&sw_lat=31.4300&sw_lng=73.0500",  # Sitara/1
    "ne_lat=31.4300&ne_lng=73.0600&sw_lat=31.4200&sw_lng=73.0500",  # Sitara/2

    # ══════════════════════════════════════════════════════════════
    # KOHINOOR / SHEIKHUPURA ROAD (east Faisalabad)
    # Verified: Kohinoor Textile area ~31.430,73.148
    # ══════════════════════════════════════════════════════════════

    # ── Kohinoor / Lyallpur Road East (~31.430, 73.148) ───────────
    "ne_lat=31.4400&ne_lng=73.1580&sw_lat=31.4300&sw_lng=73.1480",  # Kohinoor/1
    "ne_lat=31.4400&ne_lng=73.1480&sw_lat=31.4300&sw_lng=73.1380",  # Kohinoor/2
    "ne_lat=31.4300&ne_lng=73.1580&sw_lat=31.4200&sw_lng=73.1480",  # Kohinoor/3
    "ne_lat=31.4300&ne_lng=73.1480&sw_lat=31.4200&sw_lng=73.1380",  # Kohinoor/4

    # ── Sheikhupura Road corridor (~31.425, 73.155) ───────────────
    "ne_lat=31.4350&ne_lng=73.1650&sw_lat=31.4250&sw_lng=73.1550",  # ShpuraRd/1
    "ne_lat=31.4250&ne_lng=73.1650&sw_lat=31.4150&sw_lng=73.1550",  # ShpuraRd/2

    # ── Mansoorabad (~31.442, 73.158) ─────────────────────────────
    "ne_lat=31.4520&ne_lng=73.1680&sw_lat=31.4420&sw_lng=73.1580",  # Mansoorabad/1
    "ne_lat=31.4420&ne_lng=73.1680&sw_lat=31.4320&sw_lng=73.1580",  # Mansoorabad/2

    # ── Chiniot Road / NE corridor (~31.447, 73.165) ──────────────
    "ne_lat=31.4570&ne_lng=73.1750&sw_lat=31.4470&sw_lng=73.1650",  # ChiniotRd/1
    "ne_lat=31.4470&ne_lng=73.1750&sw_lat=31.4370&sw_lng=73.1650",  # ChiniotRd/2

    # ══════════════════════════════════════════════════════════════
    # NISHATABAD / JINNAH COLONY / SOUTH CITY
    # ══════════════════════════════════════════════════════════════

    # ── Nishatabad (~31.406, 73.112) ──────────────────────────────
    "ne_lat=31.4160&ne_lng=73.1220&sw_lat=31.4060&sw_lng=73.1120",  # Nishatabad/1
    "ne_lat=31.4160&ne_lng=73.1120&sw_lat=31.4060&sw_lng=73.1020",  # Nishatabad/2
    "ne_lat=31.4060&ne_lng=73.1220&sw_lat=31.3960&sw_lng=73.1120",  # Nishatabad/3
    "ne_lat=31.4060&ne_lng=73.1120&sw_lat=31.3960&sw_lng=73.1020",  # Nishatabad/4

    # ── Raja Garh / East South (~31.415, 73.140) ──────────────────
    "ne_lat=31.4250&ne_lng=73.1500&sw_lat=31.4150&sw_lng=73.1400",  # RajaGarh/1
    "ne_lat=31.4150&ne_lng=73.1500&sw_lat=31.4050&sw_lng=73.1400",  # RajaGarh/2

    # ── Gulberg Town / South (~31.434, 73.145) ────────────────────
    "ne_lat=31.4440&ne_lng=73.1550&sw_lat=31.4340&sw_lng=73.1450",  # GulbergS/1
    "ne_lat=31.4340&ne_lng=73.1550&sw_lat=31.4240&sw_lng=73.1450",  # GulbergS/2

    # ══════════════════════════════════════════════════════════════
    # SAMMUNDRI ROAD / SATIANA ROAD (south Faisalabad)
    # ══════════════════════════════════════════════════════════════

    # ── Sammundri Road South (~31.395, 73.080) ────────────────────
    "ne_lat=31.4050&ne_lng=73.0900&sw_lat=31.3950&sw_lng=73.0800",  # Sammundri/1
    "ne_lat=31.4050&ne_lng=73.0800&sw_lat=31.3950&sw_lng=73.0700",  # Sammundri/2
    "ne_lat=31.3950&ne_lng=73.0900&sw_lat=31.3850&sw_lng=73.0800",  # Sammundri/3
    "ne_lat=31.3950&ne_lng=73.0800&sw_lat=31.3850&sw_lng=73.0700",  # Sammundri/4

    # ── Satiana Road (~31.388, 73.098) ────────────────────────────
    "ne_lat=31.3980&ne_lng=73.1080&sw_lat=31.3880&sw_lng=73.0980",  # Satiana/1
    "ne_lat=31.3980&ne_lng=73.0980&sw_lat=31.3880&sw_lng=73.0880",  # Satiana/2
    "ne_lat=31.3880&ne_lng=73.1080&sw_lat=31.3780&sw_lng=73.0980",  # Satiana/3
    "ne_lat=31.3880&ne_lng=73.0980&sw_lat=31.3780&sw_lng=73.0880",  # Satiana/4

    # ── Jaranwala Road / SE corridor (~31.394, 73.133) ────────────
    "ne_lat=31.4040&ne_lng=73.1430&sw_lat=31.3940&sw_lng=73.1330",  # Jaranwala/1
    "ne_lat=31.4040&ne_lng=73.1330&sw_lat=31.3940&sw_lng=73.1230",  # Jaranwala/2
    "ne_lat=31.3940&ne_lng=73.1430&sw_lat=31.3840&sw_lng=73.1330",  # Jaranwala/3
    "ne_lat=31.3940&ne_lng=73.1330&sw_lat=31.3840&sw_lng=73.1230",  # Jaranwala/4

    # ── Tandlianwala Road / far south (~31.368, 73.105) ───────────
    "ne_lat=31.3780&ne_lng=73.1150&sw_lat=31.3680&sw_lng=73.1050",  # Tandlianwala/1
    "ne_lat=31.3680&ne_lng=73.1150&sw_lat=31.3580&sw_lng=73.1050",  # Tandlianwala/2

    # ══════════════════════════════════════════════════════════════
    # MISC / LANDMARK ZONES
    # ══════════════════════════════════════════════════════════════

    # ── Faisalabad Airport / Allama Iqbal (~31.365, 72.994) ───────
    "ne_lat=31.3750&ne_lng=73.0040&sw_lat=31.3650&sw_lng=72.9940",  # FSDairport/1
    "ne_lat=31.3650&ne_lng=73.0040&sw_lat=31.3550&sw_lng=72.9940",  # FSDairport/2

    # ── Lyallpur Thermal Power / Sheikhupura Rd NE (~31.455, 73.172)
    "ne_lat=31.4650&ne_lng=73.1820&sw_lat=31.4550&sw_lng=73.1720",  # LyallpurPwr/1
    "ne_lat=31.4550&ne_lng=73.1820&sw_lat=31.4450&sw_lng=73.1720",  # LyallpurPwr/2

    # ── Sargodha Road far NW fringe (~31.455, 73.052) ─────────────
    "ne_lat=31.4650&ne_lng=73.0620&sw_lat=31.4550&sw_lng=73.0520",  # SargodhFar/1
    "ne_lat=31.4550&ne_lng=73.0620&sw_lat=31.4450&sw_lng=73.0520",  # SargodhFar/2

    # ── Raza Abad / Gulberg No.3 East (~31.465, 73.155) ───────────
    "ne_lat=31.4750&ne_lng=73.1650&sw_lat=31.4650&sw_lng=73.1550",  # GulbergE/1
    "ne_lat=31.4650&ne_lng=73.1650&sw_lat=31.4550&sw_lng=73.1550",  # GulbergE/2

    # ── Khurianwala / NW industrial (~31.455, 73.048) ─────────────
    "ne_lat=31.4650&ne_lng=73.0580&sw_lat=31.4550&sw_lng=73.0480",  # Khurianwala/1
    "ne_lat=31.4550&ne_lng=73.0580&sw_lat=31.4450&sw_lng=73.0480",  # Khurianwala/2

    # ── Gatwala / Forest Park (~31.445, 73.088) ───────────────────
    "ne_lat=31.4550&ne_lng=73.0980&sw_lat=31.4450&sw_lng=73.0880",  # Gatwala/1
    "ne_lat=31.4450&ne_lng=73.0980&sw_lat=31.4350&sw_lng=73.0880",  # Gatwala/2

    # ── Doolat Gate / Montgomery Bazaar South (~31.395, 73.095) ───
    "ne_lat=31.4050&ne_lng=73.1050&sw_lat=31.3950&sw_lng=73.0950",  # DoolatGate/1
    "ne_lat=31.3950&ne_lng=73.1050&sw_lat=31.3850&sw_lng=73.0950",  # DoolatGate/2

    # ── Muzaffarabad / West South (~31.408, 73.070) ───────────────
    "ne_lat=31.4180&ne_lng=73.0800&sw_lat=31.4080&sw_lng=73.0700",  # Muzaffarabad/1
    "ne_lat=31.4080&ne_lng=73.0800&sw_lat=31.3980&sw_lng=73.0700",  # Muzaffarabad/2

    # ── Bosan Road / SW mixed (~31.426, 73.052) ───────────────────
    "ne_lat=31.4360&ne_lng=73.0620&sw_lat=31.4260&sw_lng=73.0520",  # BosanRd/1
    "ne_lat=31.4260&ne_lng=73.0620&sw_lat=31.4160&sw_lng=73.0520",  # BosanRd/2

]