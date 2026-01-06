"""
Processing costs.

Sources:
- https://oldschool.runescape.wiki/w/Sawmill
- https://oldschool.runescape.wiki/w/Plank_Make
"""

# GP paid to sawmill operator
SAWMILL_COSTS = {
    "Plank": 100,
    "Oak plank": 250,
    "Teak plank": 500,
    "Mahogany plank": 1500,
    "Camphor plank": 2500,
    "Ironwood plank": 5000,
    "Rosewood plank": 7500,
}

# GP component of Plank Make spell (runes separate)
PLANK_MAKE_COSTS = {
    "Plank": 70,
    "Oak plank": 175,
    "Teak plank": 350,
    "Mahogany plank": 1050,
    "Camphor plank": 1750,
    "Ironwood plank": 3500,
    "Rosewood plank": 5250,
}

PLANK_SACK_CAPACITY = 28

# GE tax: 2%, capped at 5M, only on sales >= 50gp
GE_TAX_RATE = 0.02
GE_TAX_CAP = 5_000_000
GE_TAX_THRESHOLD = 50
