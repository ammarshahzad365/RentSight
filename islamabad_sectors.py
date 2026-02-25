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