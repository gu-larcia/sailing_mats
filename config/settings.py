"""
Application configuration and constants.
"""

# App metadata
APP_VERSION = "4.7"  # Bumped for research-based improvements
APP_TITLE = "OSRS Sailing Materials Tracker"
APP_ICON = "https://oldschool.runescape.wiki/images/Sailing_icon.png"

# Cache TTLs (in seconds)
# Research confirmed: don't poll faster than 5-minute data refresh
CACHE_TTL_PRICES = 60       # Price data refreshes every minute
CACHE_TTL_MAPPING = 300     # Item mappings refresh every 5 minutes
CACHE_TTL_CHAINS = 3600     # Chain definitions refresh every hour

# Default configuration values
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

# URL parameter mappings
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

# API Configuration
API_USER_AGENT = "OSRS-Sailing-Tracker/4.7 (Streamlit App)"
API_POLL_INTERVAL = 300  # 5 minutes minimum between refreshes (per research)
