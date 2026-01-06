"""
Item ID mappings for Sailing materials.

IDs from OSRS Wiki API /mapping endpoint.
Sailing released November 19, 2025.
"""

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
    32904: "Camphor logs",
    32907: "Ironwood logs",
    32910: "Rosewood logs",
}

ALL_PLANKS = {
    960: "Plank",
    8778: "Oak plank",
    8780: "Teak plank",
    8782: "Mahogany plank",
    31432: "Camphor plank",
    31435: "Ironwood plank",
    31438: "Rosewood plank",
}

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

HULL_REPAIR_KITS = {
    31964: "Repair kit",
    31967: "Oak repair kit",
    31970: "Teak repair kit",
    31973: "Mahogany repair kit",
    31976: "Camphor repair kit",
    31979: "Ironwood repair kit",
    31982: "Rosewood repair kit",
}

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
    31716: "Lead ore",
    31719: "Nickel ore",
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
    32889: "Lead bar",
    32892: "Cupronickel bar",
    31996: "Dragon metal sheet",
}

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

ALL_CANNONBALLS = {
    2: "Steel cannonball",
    31906: "Bronze cannonball",
    31908: "Iron cannonball",
    31910: "Mithril cannonball",
    31912: "Adamant cannonball",
    31914: "Rune cannonball",
    31916: "Dragon cannonball",  # Drop only
}

AMMO_MOULDS = {
    4: "Ammo mould",
    27012: "Double ammo mould",
}

MISC_ITEMS = {
    1941: "Swamp paste",
    25580: "Plank sack",
}

# For Plank Make spell
RUNE_IDS = {
    "Astral rune": 9075,
    "Nature rune": 561,
    "Earth rune": 557,
}

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
    **MISC_ITEMS
}
