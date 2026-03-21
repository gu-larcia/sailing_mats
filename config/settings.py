"""Application settings."""

APP_VERSION = "5.1"
APP_TITLE = "OSRS Market Tracker"
APP_SUBTITLE = "Sailing Materials & Beyond"
APP_ICON = "https://oldschool.runescape.wiki/images/Sailing_icon.png"

# Cache TTLs (seconds)
CACHE_TTL_PRICES = 60
CACHE_TTL_MAPPING = 300
CACHE_TTL_CHAINS = 3600

DEFAULT_CONFIG = {
    "quantity": 1,
    "plank_method": "Sawmill",
    "self_collected": False,
    "ancient_furnace": False,
    "show_gp_hr": False,
    "bank_location": "Medium (Typical)",
    "use_stamina": True,
    "has_imcando_hammer": False,
    "has_amys_saw": False,
    "has_plank_sack": False,
    "has_smithing_outfit": False,
    "use_earth_staff": False,
    "use_sawmill_vouchers": False,
    "has_coal_bag": False,
}

# Maps URL param names to config keys
URL_PARAMS = {
    "plank_method": "plank_method",
    "self_collected": "self_collected",
    "ancient_furnace": "ancient_furnace",
    "show_gp_hr": "show_gp_hr",
    "bank_location": "bank_location",
    "use_stamina": "use_stamina",
    "imcando_hammer": "has_imcando_hammer",
    "amys_saw": "has_amys_saw",
    "plank_sack": "has_plank_sack",
    "smithing_outfit": "has_smithing_outfit",
    "quantity": "quantity",
    "sawmill_vouchers": "use_sawmill_vouchers",
    "coal_bag": "has_coal_bag",
}

# Item groups that can be tracked (extensible)
ITEM_GROUPS = {
    "sailing": "Sailing Materials",
    "logs": "Logs",
    "planks": "Planks",
    "hull_parts": "Hull Parts",
    "large_hull_parts": "Large Hull Parts",
    "hull_repair_kits": "Hull Repair Kits",
    "ores": "Ores",
    "bars": "Bars",
    "keel_parts": "Keel Parts",
    "large_keel_parts": "Large Keel Parts",
    "nails": "Nails",
    "cannonballs": "Cannonballs",
    "bar_smelting": "Bar Smelting",
    "nails_from_ore": "Nails (from Ore)",
    "keel_parts_from_ore": "Keel Parts (from Ore)",
    "cannonballs_from_ore": "Cannonballs (from Ore)",
    "large_keel_from_bar": "Large Keel Parts (from Bar)",
    "large_keel_from_ore": "Large Keel Parts (from Ore)",
    "hull_parts_from_log": "Hull Parts (from Log)",
    "large_hull_from_log": "Large Hull Parts (from Log)",
    "repair_kits_from_log": "Repair Kits (from Log)",
    "unstrung_bows": "Unstrung Bows",
    "strung_bows": "Strung Bows",
    "arrows": "Arrows",
    "darts": "Darts",
    "bows_from_log": "Bows (from Log)",
    "crossbow_stocks": "Crossbow Stocks",
    "crossbow_limbs": "Crossbow Limbs",
    "crossbows_u": "Crossbows (u)",
    "crossbows": "Crossbows",
    "crossbows_from_log": "Crossbows (from Log)",
    "bolts_unf": "Bolts (unf)",
    "bolts": "Bolts",
    "bolts_from_ore": "Bolts (from Ore)",
    "javelin_heads": "Javelin Heads",
    "javelins": "Javelins",
    "javelins_from_ore": "Javelins (from Ore)",
    "arrows_from_bar": "Arrows (from Bar)",
    "arrows_from_ore": "Arrows (from Ore)",
    "darts_from_bar": "Darts (from Bar)",
    "darts_from_ore": "Darts (from Ore)",
    "bolts_from_bar": "Bolts (from Bar)",
    "javelins_from_bar": "Javelins (from Bar)",
    "crossbow_limbs_from_ore": "Crossbow Limbs (from Ore)",
}
