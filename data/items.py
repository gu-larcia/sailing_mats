"""
OSRS Item ID mappings for Sailing materials and related items.

All IDs verified against the OSRS Wiki API /mapping endpoint.
Sailing skill released November 19, 2025.

v4.7 additions: Textile seeds, yarns, bolts, coral frags, and coral items.
"""

# ============================================================================
# LOGS
# ============================================================================

ALL_LOGS = {
    1511: "Logs",
    1521: "Oak logs",
    1519: "Willow logs",
    1517: "Maple logs",
    1515: "Yew logs",
    1513: "Magic logs",
    6333: "Teak logs",
    6332: "Mahogany logs",
    19669: "Redwood logs",
    2862: "Achey tree logs",
    10810: "Arctic pine logs",
    3239: "Bark",
    # Sailing logs (32904-32910 range)
    32904: "Camphor logs",
    32907: "Ironwood logs",
    32910: "Rosewood logs",
}

# ============================================================================
# PLANKS
# ============================================================================

ALL_PLANKS = {
    960: "Plank",
    8778: "Oak plank",
    8780: "Teak plank",
    8782: "Mahogany plank",
    # Sailing planks
    31432: "Camphor plank",
    31435: "Ironwood plank",
    31438: "Rosewood plank",
}

# ============================================================================
# HULL PARTS (32041-32080 range)
# ============================================================================

HULL_PARTS = {
    32041: "Wooden hull parts",
    32044: "Oak hull parts",
    32047: "Teak hull parts",
    32050: "Mahogany hull parts",
    32053: "Camphor hull parts",
    32056: "Ironwood hull parts",
    32059: "Rosewood hull parts",
}

LARGE_HULL_PARTS = {
    32062: "Large wooden hull parts",
    32065: "Large oak hull parts",
    32068: "Large teak hull parts",
    32071: "Large mahogany hull parts",
    32074: "Large camphor hull parts",
    32077: "Large ironwood hull parts",
    32080: "Large rosewood hull parts",
}

# ============================================================================
# HULL REPAIR KITS (31964-31982 range)
# ============================================================================

HULL_REPAIR_KITS = {
    31964: "Repair kit",
    31967: "Oak repair kit",
    31970: "Teak repair kit",
    31973: "Mahogany repair kit",
    31976: "Camphor repair kit",
    31979: "Ironwood repair kit",
    31982: "Rosewood repair kit",
}

# ============================================================================
# ORES & BARS
# ============================================================================

ALL_ORES = {
    436: "Copper ore",
    438: "Tin ore",
    440: "Iron ore",
    442: "Silver ore",
    453: "Coal",
    444: "Gold ore",
    447: "Mithril ore",
    449: "Adamantite ore",
    451: "Runite ore",
    21341: "Amethyst",
    # Sailing ores
    31716: "Lead ore",
    31719: "Nickel ore",
    # Rune essence
    1436: "Rune essence",
    1440: "Pure essence",
}

ALL_BARS = {
    2349: "Bronze bar",
    2351: "Iron bar",
    2355: "Silver bar",
    2357: "Gold bar",
    2353: "Steel bar",
    2359: "Mithril bar",
    2361: "Adamantite bar",
    2363: "Runite bar",
    # Sailing bars
    32889: "Lead bar",
    32892: "Cupronickel bar",
    31996: "Dragon metal sheet",
}

# ============================================================================
# KEEL PARTS (31999-32038 range)
# ============================================================================

KEEL_PARTS = {
    31999: "Bronze keel parts",
    32002: "Iron keel parts",
    32005: "Steel keel parts",
    32008: "Mithril keel parts",
    32011: "Adamant keel parts",
    32014: "Rune keel parts",
    32017: "Dragon keel parts",
}

LARGE_KEEL_PARTS = {
    32020: "Large bronze keel parts",
    32023: "Large iron keel parts",
    32026: "Large steel keel parts",
    32029: "Large mithril keel parts",
    32032: "Large adamant keel parts",
    32035: "Large rune keel parts",
    32038: "Large dragon keel parts",
}

# ============================================================================
# NAILS
# ============================================================================

ALL_NAILS = {
    4819: "Bronze nails",
    4820: "Iron nails",
    4821: "Black nails",
    1539: "Steel nails",
    4822: "Mithril nails",
    4823: "Adamantite nails",
    4824: "Rune nails",
    31406: "Dragon nails",
}

# ============================================================================
# CANNONBALLS
# ============================================================================

ALL_CANNONBALLS = {
    2: "Steel cannonball",  # Original cannonball
    31906: "Bronze cannonball",
    31908: "Iron cannonball",
    31910: "Mithril cannonball",
    31912: "Adamant cannonball",
    31914: "Rune cannonball",
    31916: "Dragon cannonball",  # Drop-only, cannot be smithed
}

# ============================================================================
# TOOLS & MISC
# ============================================================================

AMMO_MOULDS = {
    4: "Ammo mould",
    27012: "Double ammo mould",
}

MISC_ITEMS = {
    1941: "Swamp paste",
    25580: "Plank sack",
    227: "Vial of water",
}

# ============================================================================
# RUNES (for Plank Make spell)
# ============================================================================

RUNE_IDS = {
    "Astral rune": 9075,
    "Nature rune": 561,
    "Earth rune": 557,
}

# ============================================================================
# TEXTILE SEEDS (Sailing v4.7)
# ============================================================================

TEXTILE_SEEDS = {
    31541: "Flax seed",
    31543: "Hemp seed",
    31545: "Cotton seed",
}

# ============================================================================
# RAW TEXTILES (Sailing v4.7)
# ============================================================================

RAW_TEXTILES = {
    1779: "Flax",           # Pre-existing, now farmable
    31457: "Hemp",
    31460: "Cotton boll",
}

# ============================================================================
# YARNS (Sailing v4.7)
# Spinning wheel: 1 raw material -> 1 yarn
# ============================================================================

YARNS = {
    31463: "Linen yarn",    # From flax, 12 Crafting
    31466: "Hemp yarn",     # From hemp, 39 Crafting
    31469: "Cotton yarn",   # From cotton boll, 73 Crafting
}

# ============================================================================
# BOLTS OF CLOTH (Sailing v4.7)
# Loom: 2 yarn -> 1 bolt
# ============================================================================

BOLTS = {
    31472: "Bolt of linen",     # From 2 linen yarn, 12 Crafting
    31475: "Bolt of canvas",    # From 2 hemp yarn, 39 Crafting
    31478: "Bolt of cotton",    # From 2 cotton yarn, 73 Crafting
}

# ============================================================================
# CORAL FRAGS (Sailing v4.7)
# Planted in coral nursery patches
# ============================================================================

CORAL_FRAGS = {
    31511: "Elkhorn frag",  # 28 Farming
    31513: "Pillar frag",   # 52 Farming
    31515: "Umbral frag",   # 77 Farming
}

# ============================================================================
# CORAL (Sailing v4.7)
# Harvested from coral nursery patches
# ============================================================================

CORAL = {
    31481: "Elkhorn coral",
    31484: "Pillar coral",
    31487: "Umbral coral",
}

# ============================================================================
# CORAL CRAFTED ITEMS (Sailing v4.7)
# ============================================================================

CORAL_PRODUCTS = {
    31712: "Anti-odour salt",           # 15 per craft from Elkhorn
    31599: "Haemostatic dressing (1)",  # From Elkhorn potion chain
    31605: "Super fishing potion (3)",  # From Pillar coral
    31626: "Super hunter potion (4)",   # From Pillar coral
    31650: "Armadyl brew (4)",          # From Umbral coral
    31659: "Armadyl brew (1)",          # 1-dose variant
}

# ============================================================================
# HERBLORE INTERMEDIATES (Sailing v4.7)
# ============================================================================

HERBLORE_INTERMEDIATES = {
    # Paste items used in coral crafting
    31700: "Crab paste",
    31703: "Squid paste",
    31706: "Rainbow crab paste",
    31709: "Haddock eye",
}

# ============================================================================
# COMBINED ITEM DICTIONARY
# ============================================================================

ALL_ITEMS = {
    **ALL_LOGS, 
    **ALL_PLANKS, 
    **HULL_PARTS, 
    **LARGE_HULL_PARTS,
    **HULL_REPAIR_KITS, 
    **ALL_ORES, 
    **ALL_BARS, 
    **KEEL_PARTS,
    **LARGE_KEEL_PARTS, 
    **ALL_NAILS, 
    **ALL_CANNONBALLS, 
    **AMMO_MOULDS,
    **MISC_ITEMS,
    # v4.7 additions
    **TEXTILE_SEEDS,
    **RAW_TEXTILES,
    **YARNS,
    **BOLTS,
    **CORAL_FRAGS,
    **CORAL,
    **CORAL_PRODUCTS,
    **HERBLORE_INTERMEDIATES,
}
