"""Application settings."""

APP_VERSION = "4.6"
APP_TITLE = "OSRS Sailing Materials Tracker"
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
}
