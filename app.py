"""
OSRS Sailing Materials Tracker
Version 4.5
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="OSRS Sailing Tracker",
    page_icon="https://oldschool.runescape.wiki/images/Sailing_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

OSRS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --parchment: #f4e4bc;
    --parchment-dark: #e8d5a3;
    --parchment-light: #faf3e0;
    --driftwood: #8b7355;
    --driftwood-dark: #5c4d3a;
    --driftwood-light: #a08b6d;
    --gold: #ffd700;
    --gold-dark: #d4af37;
    --gold-light: #ffec80;
    --ocean-dark: #1a3a4a;
    --ocean: #2d5a6b;
    --ocean-light: #3d7a8c;
    --copper: #b87333;
    --bronze: #cd7f32;
    --rune-blue: #5dade2;
    --dragon-red: #c0392b;
}

.stApp {
    background: linear-gradient(180deg, #1a2a3a 0%, #0d1a24 50%, #1a2a3a 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border-right: 4px solid var(--driftwood);
}

[data-testid="stSidebar"] * {
    color: var(--driftwood-dark) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--driftwood-dark) !important;
}

.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.stApp h1 {
    border-bottom: 3px solid var(--gold-dark);
    padding-bottom: 10px;
}

.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border-radius: 8px 8px 0 0;
    padding: 5px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    color: var(--parchment) !important;
    background: transparent;
    border-radius: 6px 6px 0 0;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--gold-dark) 0%, var(--copper) 100%) !important;
    color: var(--driftwood-dark) !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: linear-gradient(180deg, rgba(244,228,188,0.1) 0%, rgba(244,228,188,0.05) 100%);
    border: 2px solid var(--driftwood);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
}

[data-testid="stMetric"] label {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment) !important;
    font-size: 1.1rem !important;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'Crimson Text', serif !important;
}

[data-testid="stDataFrame"] {
    border: 3px solid var(--driftwood);
    border-radius: 8px;
    overflow: visible;
}

.stButton > button {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--gold) 0%, var(--gold-dark) 100%);
    color: var(--driftwood-dark) !important;
    border: 2px solid var(--copper);
    border-radius: 6px;
    font-weight: 600;
    box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(180deg, var(--gold-light) 0%, var(--gold) 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

[data-testid="stForm"] {
    background: linear-gradient(180deg, rgba(139,115,85,0.2) 0%, rgba(92,77,58,0.2) 100%);
    border: 2px solid var(--driftwood);
    border-radius: 8px;
    padding: 15px;
}

.stSelectbox > div > div {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
}

.stSelectbox > div > div > div {
    color: var(--driftwood-dark) !important;
}

.stSelectbox input {
    caret-color: transparent !important;
    pointer-events: none !important;
}

.stSelectbox > div > div {
    cursor: pointer !important;
}

[data-baseweb="select"] > div,
[data-baseweb="popover"] > div,
[role="listbox"],
[role="option"] {
    background: var(--parchment-light) !important;
    color: var(--driftwood-dark) !important;
}

[role="option"]:hover {
    background: var(--parchment-dark) !important;
}

.stSelectbox label {
    color: var(--parchment) !important;
}

[data-testid="stSidebar"] .stSelectbox label {
    color: var(--driftwood-dark) !important;
}

.stCheckbox label, .stToggle label {
    font-family: 'Crimson Text', serif !important;
}

.streamlit-expanderHeader {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 6px;
    color: var(--gold) !important;
}

.stLinkButton > a {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--ocean) 0%, var(--ocean-dark) 100%);
    color: var(--parchment) !important;
    border: 2px solid var(--ocean-light);
}

.stCaption {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment-dark) !important;
    font-style: italic;
}

.stSpinner > div {
    border-color: var(--gold) !important;
}

[data-testid="stToast"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border: 2px solid var(--gold-dark);
    color: var(--driftwood-dark);
    font-family: 'Crimson Text', serif;
}

hr {
    border-color: var(--driftwood) !important;
}

[data-testid="stSidebar"] input {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
    color: var(--driftwood-dark) !important;
}

.stAlert {
    font-family: 'Crimson Text', serif;
    border-radius: 6px;
}

.item-card {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.item-card img {
    width: 36px;
    height: 36px;
    image-rendering: pixelated;
}

.item-card .item-name {
    color: var(--parchment);
    font-family: 'Cinzel', serif;
    font-size: 0.95rem;
}

.item-card .item-profit {
    color: var(--gold);
    font-family: 'Crimson Text', serif;
    font-weight: 600;
}

.best-item-display {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}

.best-item-display img {
    width: 48px;
    height: 48px;
    image-rendering: pixelated;
    margin-bottom: 8px;
}

.best-item-display .label {
    color: var(--gold);
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    margin-bottom: 4px;
}

.best-item-display .value {
    color: var(--parchment);
    font-family: 'Crimson Text', serif;
    font-size: 1rem;
    word-wrap: break-word;
}

[data-testid="stDataFrame"] {
    overflow-x: auto !important;
    overflow-y: visible !important;
    -webkit-overflow-scrolling: touch;
    width: 100% !important;
}

[data-testid="stDataFrame"] > div {
    overflow-x: auto !important;
    min-width: 100%;
}

[data-testid="stDataFrame"] iframe {
    min-width: 100%;
}

.stDataFrame, .dataframe-container {
    overflow-x: auto !important;
    max-width: 100%;
    display: block;
}

[data-testid="stDataFrame"] table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
}

[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {
    overflow-x: auto !important;
    max-width: 100% !important;
}

@media screen and (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] {
        min-width: 250px;
    }
    
    [data-testid="stDataFrame"] {
        font-size: 0.85rem;
    }
    
    [data-testid="stDataFrame"]::after {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: 30px;
        background: linear-gradient(to right, transparent, rgba(26,42,58,0.8));
        pointer-events: none;
        opacity: 0.7;
    }
    
    [data-testid="stMetric"] {
        padding: 10px;
    }
    
    .js-plotly-plot, .plotly {
        max-width: 100% !important;
        overflow-x: auto;
    }
    
    .js-plotly-plot .plotly .modebar {
        transform: scale(0.8);
        transform-origin: top right;
    }
    
    .js-plotly-plot .plotly svg text {
        font-size: 90% !important;
    }
    
    .js-plotly-plot .legend {
        max-width: 100%;
        overflow-x: auto;
    }
    
    .stButton > button {
        min-height: 44px;
        padding: 10px 16px;
    }
    
    .stSelectbox, .stNumberInput, .stTextInput {
        min-height: 44px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex-shrink: 0;
        padding: 8px 12px;
    }
    
    .stApp h1 {
        font-size: 1.5rem !important;
    }
    
    .stApp h2 {
        font-size: 1.25rem !important;
    }
    
    .stApp h3 {
        font-size: 1.1rem !important;
    }
    
    .best-item-display {
        padding: 10px;
    }
    
    .best-item-display img {
        width: 32px;
        height: 32px;
    }
    
    [data-testid="stDataFrame"]::before {
        content: 'scroll horizontally';
        display: block;
        text-align: center;
        font-size: 0.7rem;
        color: var(--gold-dark);
        padding: 4px;
        opacity: 0.7;
    }
}

@media screen and (max-width: 480px) {
    [data-testid="stDataFrame"] {
        font-size: 0.75rem;
    }
    
    [data-testid="stMetric"] label {
        font-size: 0.8rem !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1rem !important;
    }
}

[data-testid="stDataFrame"]::-webkit-scrollbar {
    height: 8px;
}

[data-testid="stDataFrame"]::-webkit-scrollbar-track {
    background: var(--driftwood-dark);
    border-radius: 4px;
}

[data-testid="stDataFrame"]::-webkit-scrollbar-thumb {
    background: var(--gold-dark);
    border-radius: 4px;
}

[data-testid="stDataFrame"]::-webkit-scrollbar-thumb:hover {
    background: var(--gold);
}
</style>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.setAttribute('autocomplete', 'off');
    });
});
const observer = new MutationObserver(function(mutations) {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.setAttribute('autocomplete', 'off');
    });
});
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""

st.markdown(OSRS_CSS, unsafe_allow_html=True)

API_BASE = "https://prices.runescape.wiki/api/v1/osrs"

METAL_COLORS = {
    'bronze': '#CD7F32',
    'iron': '#5C5C5C',
    'steel': '#71797E',
    'black': '#1C1C1C',
    'mithril': '#284B63',
    'adamant': '#2E8B57',
    'rune': '#00CED1',
    'dragon': '#DC143C',
}

WOOD_COLORS = {
    'wooden': '#DEB887',
    'oak': '#C19A6B',
    'willow': '#A8C090',
    'teak': '#8B7355',
    'maple': '#C9A66B',
    'mahogany': '#6B4423',
    'yew': '#8B4513',
    'magic': '#4B0082',
    'redwood': '#A52A2A',
    'camphor': '#2E8B57',
    'ironwood': '#00CED1',
    'rosewood': '#DC143C',
}

CATEGORY_COLORS = {
    'Planks': '#C19A6B',
    'Hull Parts': '#8B7355',
    'Large Hull Parts': '#6B4423',
    'Hull Repair Kits': '#DAA520',
    'Keel Parts': '#71797E',
    'Large Keel Parts': '#5F9EA0',
    'Nails': '#CD7F32',
    'Cannonballs': '#5C5C5C',
    'Other': '#7f8c8d',
}


def get_item_tier_color(item_name: str, profit: float = 0) -> str:
    name_lower = item_name.lower()
    
    if 'dragon' in name_lower:
        return METAL_COLORS['dragon']
    elif 'rune ' in name_lower or 'rune_' in name_lower or 'runite' in name_lower:
        return METAL_COLORS['rune']
    elif 'adamant' in name_lower:
        return METAL_COLORS['adamant']
    elif 'mithril' in name_lower:
        return METAL_COLORS['mithril']
    elif 'black' in name_lower and ('nail' in name_lower or 'keel' in name_lower):
        return METAL_COLORS['black']
    elif 'steel' in name_lower:
        return METAL_COLORS['steel']
    elif 'iron ' in name_lower or 'iron_' in name_lower or name_lower.startswith('iron'):
        if 'ironwood' not in name_lower:
            return METAL_COLORS['iron']
    elif 'bronze' in name_lower:
        return METAL_COLORS['bronze']
    
    if 'rosewood' in name_lower:
        return WOOD_COLORS['rosewood']
    elif 'ironwood' in name_lower:
        return WOOD_COLORS['ironwood']
    elif 'camphor' in name_lower:
        return WOOD_COLORS['camphor']
    elif 'mahogany' in name_lower:
        return WOOD_COLORS['mahogany']
    elif 'teak' in name_lower:
        return WOOD_COLORS['teak']
    elif 'oak' in name_lower:
        return WOOD_COLORS['oak']
    elif 'wooden' in name_lower or name_lower == 'plank' or name_lower.endswith(' plank'):
        if not any(wood in name_lower for wood in ['oak', 'teak', 'mahogany', 'camphor', 'ironwood', 'rosewood']):
            return WOOD_COLORS['wooden']
    
    return '#d4af37' if profit >= 0 else '#c0392b'


def get_tier_from_name(item_name: str) -> str:
    name_lower = item_name.lower()
    
    for tier in ['dragon', 'rune', 'adamant', 'mithril', 'steel', 'iron', 'bronze']:
        if tier in name_lower and not (tier == 'iron' and 'ironwood' in name_lower):
            return tier.capitalize()
    
    for tier in ['rosewood', 'ironwood', 'camphor', 'mahogany', 'teak', 'oak', 'wooden']:
        if tier in name_lower:
            return tier.capitalize()
    
    return "Other"


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
    31916: "Dragon cannonball",
}

AMMO_MOULDS = {
    4: "Ammo mould",
    27012: "Double ammo mould",
}

MISC_ITEMS = {
    1941: "Swamp paste",
    25580: "Plank sack",
}

SAWMILL_COSTS = {
    "Plank": 100,
    "Oak plank": 250,
    "Teak plank": 500,
    "Mahogany plank": 1500,
    "Camphor plank": 2500,
    "Ironwood plank": 5000,
    "Rosewood plank": 7500,
}

PLANK_MAKE_COSTS = {
    "Plank": 70,
    "Oak plank": 175,
    "Teak plank": 350,
    "Mahogany plank": 1050,
    "Camphor plank": 1750,
    "Ironwood plank": 3500,
    "Rosewood plank": 5250,
}

RUNE_IDS = {
    "Astral rune": 9075,
    "Nature rune": 561,
    "Earth rune": 557,
}

PLANK_SACK_CAPACITY = 28


@dataclass
class ActivityTiming:
    ticks_per_action: int
    items_per_action: int
    materials_per_action: int
    needs_hammer: bool
    needs_saw: bool
    other_tool_slots: int
    activity_name: str
    is_smithing: bool = False
    uses_planks: bool = False
    notes: str = ""


@dataclass
class BankLocation:
    name: str
    bank_time: float
    travel_time: float
    has_anvil: bool
    has_furnace: bool
    has_shipwright: bool
    has_sawmill: bool
    requirements: str
    stamina_dependent: bool
    
    @property
    def total_overhead(self) -> float:
        return self.bank_time + self.travel_time


BANK_LOCATIONS = {
    "Deepfin Point": BankLocation(
        name="Deepfin Point",
        bank_time=3.0,
        travel_time=4.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=False,
        requirements="67 Sailing",
        stamina_dependent=False
    ),
    "Prifddinas": BankLocation(
        name="Prifddinas",
        bank_time=4.0,
        travel_time=4.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=True,
        requirements="Song of the Elves",
        stamina_dependent=False
    ),
    "Edgeville Furnace": BankLocation(
        name="Edgeville Furnace",
        bank_time=4.0,
        travel_time=6.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="None",
        stamina_dependent=False
    ),
    "Varrock West Anvil": BankLocation(
        name="Varrock West Anvil",
        bank_time=4.0,
        travel_time=8.0,
        has_anvil=True,
        has_furnace=False,
        has_shipwright=False,
        has_sawmill=False,
        requirements="None",
        stamina_dependent=False
    ),
    "Port Phasmatys": BankLocation(
        name="Port Phasmatys",
        bank_time=5.0,
        travel_time=10.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="Priest in Peril",
        stamina_dependent=False
    ),
    "Neitiznot": BankLocation(
        name="Neitiznot",
        bank_time=4.0,
        travel_time=8.0,
        has_anvil=True,
        has_furnace=False,
        has_shipwright=False,
        has_sawmill=False,
        requirements="The Fremennik Isles (partial)",
        stamina_dependent=False
    ),
    "Al Kharid Furnace": BankLocation(
        name="Al Kharid Furnace",
        bank_time=5.0,
        travel_time=12.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="None (10gp gate or Prince Ali Rescue)",
        stamina_dependent=False
    ),
    "Shilo Village": BankLocation(
        name="Shilo Village",
        bank_time=5.0,
        travel_time=10.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="Shilo Village quest",
        stamina_dependent=False
    ),
    "WC Guild Sawmill": BankLocation(
        name="WC Guild Sawmill",
        bank_time=4.0,
        travel_time=8.0,
        has_anvil=False,
        has_furnace=False,
        has_shipwright=False,
        has_sawmill=True,
        requirements="60 Woodcutting",
        stamina_dependent=False
    ),
    "Fast (Optimal)": BankLocation(
        name="Fast (Optimal)",
        bank_time=4.0,
        travel_time=4.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=True,
        requirements="Best available setup",
        stamina_dependent=False
    ),
    "Medium (Typical)": BankLocation(
        name="Medium (Typical)",
        bank_time=5.0,
        travel_time=10.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=True,
        requirements="Typical efficient banking",
        stamina_dependent=False
    ),
    "Slow (Suboptimal)": BankLocation(
        name="Slow (Suboptimal)",
        bank_time=6.0,
        travel_time=19.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=True,
        requirements="Suboptimal setup",
        stamina_dependent=True
    ),
}

SMITHING_OUTFIT_TICK_SAVE_CHANCE = 0.15

ACTIVITY_TIMINGS = {
    "Cannonballs_Single": ActivityTiming(
        ticks_per_action=9,
        items_per_action=4,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=1,
        activity_name="Cannonball Smelting (Single)",
        is_smithing=True,
        uses_planks=False,
        notes="Regular ammo mould: 1 bar per 4 cannonballs per 9 ticks."
    ),
    "Cannonballs_Double": ActivityTiming(
        ticks_per_action=9,
        items_per_action=8,
        materials_per_action=2,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=1,
        activity_name="Cannonball Smelting (Double)",
        is_smithing=True,
        uses_planks=False,
        notes="Double ammo mould: 2 bars per 8 cannonballs per 9 ticks."
    ),
    "Keel Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Keel Parts Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="5 bars per part."
    ),
    "Dragon Keel Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=2,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Dragon Keel Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="2 sheets per part. Requires 92 Smithing."
    ),
    "Large Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Keel Assembly",
        is_smithing=True,
        uses_planks=False,
        notes="5 regular parts per large part."
    ),
    "Large Dragon Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=2,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Dragon Keel Assembly",
        is_smithing=True,
        uses_planks=False,
        notes="2 dragon keel parts per large part."
    ),
    "Hull Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Hull Parts Crafting",
        is_smithing=False,
        uses_planks=True,
        notes="5 planks per part."
    ),
    "Large Hull Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Large Hull Assembly",
        is_smithing=False,
        uses_planks=False,
        notes="5 regular parts per large part."
    ),
    "Nails": ActivityTiming(
        ticks_per_action=4,
        items_per_action=15,
        materials_per_action=1,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Nail Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="15 nails per bar."
    ),
    "Planks_Sawmill": ActivityTiming(
        ticks_per_action=1,
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Sawmill Conversion",
        is_smithing=False,
        uses_planks=False,
        notes="Time dominated by travel. Uses coin pouch."
    ),
    "Planks_PlankMake": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=3,
        activity_name="Plank Make Spell",
        is_smithing=False,
        uses_planks=False,
        notes="3 ticks per cast. Earth staff reduces rune slots needed."
    ),
}


def calculate_gp_per_hour(
    profit_per_item: float,
    category: str,
    chain_name: str,
    config: Dict
) -> Optional[Dict]:
    timing_key = None
    is_double_mould_chain = "(Double)" in chain_name
    
    if category == "Cannonballs":
        if is_double_mould_chain:
            timing_key = "Cannonballs_Double"
        else:
            timing_key = "Cannonballs_Single"
    elif category == "Keel Parts":
        if "dragon" in chain_name.lower():
            timing_key = "Dragon Keel Parts"
        else:
            timing_key = "Keel Parts"
    elif category == "Large Keel Parts":
        if "dragon" in chain_name.lower():
            timing_key = "Large Dragon Keel Parts"
        else:
            timing_key = "Large Keel Parts"
    elif category == "Hull Parts":
        timing_key = "Hull Parts"
    elif category == "Large Hull Parts":
        timing_key = "Large Hull Parts"
    elif category == "Nails":
        timing_key = "Nails"
    elif category == "Planks":
        if "Plank Make" in config.get("plank_method", "Sawmill"):
            timing_key = "Planks_PlankMake"
        else:
            timing_key = "Planks_Sawmill"
    
    if not timing_key or timing_key not in ACTIVITY_TIMINGS:
        return None
    
    timing = ACTIVITY_TIMINGS[timing_key]
    
    has_imcando_hammer = config.get("has_imcando_hammer", False)
    has_amys_saw = config.get("has_amys_saw", False)
    has_smithing_outfit = config.get("has_smithing_outfit", False)
    has_plank_sack = config.get("has_plank_sack", False)
    use_stamina = config.get("use_stamina", True)
    
    bank_location_name = config.get("bank_location", "Medium (Typical)")
    bank_location = BANK_LOCATIONS.get(bank_location_name, BANK_LOCATIONS["Medium (Typical)"])
    
    effective_ticks = timing.ticks_per_action
    if has_smithing_outfit and timing.is_smithing:
        effective_ticks = timing.ticks_per_action - (SMITHING_OUTFIT_TICK_SAVE_CHANCE * 1)
    
    tool_slots_used = timing.other_tool_slots
    
    if timing.needs_hammer:
        if not has_imcando_hammer:
            tool_slots_used += 1
    
    if timing.needs_saw:
        if not has_amys_saw:
            tool_slots_used += 1
    
    plank_sack_bonus = 0
    if has_plank_sack and timing.uses_planks:
        tool_slots_used += 1
        plank_sack_bonus = PLANK_SACK_CAPACITY
    
    base_inventory = 28
    effective_inventory = base_inventory - tool_slots_used
    
    if timing_key == "Planks_PlankMake" and config.get("use_earth_staff", False):
        effective_inventory += 1
    
    items_per_action = timing.items_per_action
    materials_per_action = timing.materials_per_action
    
    materials_per_trip = effective_inventory
    
    if has_plank_sack and timing.uses_planks:
        materials_per_trip = effective_inventory + plank_sack_bonus
    
    actions_per_trip = materials_per_trip // materials_per_action
    
    items_per_trip = actions_per_trip * items_per_action
    
    if items_per_trip <= 0:
        return None
    
    ticks_per_trip = actions_per_trip * effective_ticks
    craft_time_seconds = ticks_per_trip * 0.6
    
    trip_overhead = bank_location.total_overhead
    
    if bank_location.stamina_dependent and use_stamina:
        trip_overhead = bank_location.bank_time + (bank_location.travel_time * 0.7)
    
    seconds_per_trip = craft_time_seconds + trip_overhead
    
    if timing_key == "Planks_Sawmill":
        sawmill_travel = config.get("sawmill_travel_time", bank_location.total_overhead)
        seconds_per_trip = sawmill_travel
        items_per_trip = effective_inventory
    
    ancient_furnace_active = False
    if config.get("ancient_furnace", False) and timing.is_smithing:
        craft_time_seconds = craft_time_seconds / 2
        seconds_per_trip = craft_time_seconds + trip_overhead
        ancient_furnace_active = True
    
    trips_per_hour = 3600.0 / seconds_per_trip
    
    items_per_hour = trips_per_hour * items_per_trip
    
    gp_per_hour = items_per_hour * profit_per_item
    
    tool_notes = []
    if timing.needs_hammer:
        tool_notes.append(f"Hammer: {'equipped' if has_imcando_hammer else 'inventory'}")
    if timing.needs_saw:
        tool_notes.append(f"Saw: {'equipped' if has_amys_saw else 'inventory'}")
    if has_plank_sack and timing.uses_planks:
        tool_notes.append(f"Plank sack: +{plank_sack_bonus} planks")
    
    bonus_notes = []
    if has_smithing_outfit and timing.is_smithing:
        bonus_notes.append("Smithing outfit: -15% avg ticks")
    if ancient_furnace_active:
        bonus_notes.append("Ancient Furnace: 2x speed")
    if is_double_mould_chain:
        bonus_notes.append("Double mould: 2 bars/action")
    if has_plank_sack and timing.uses_planks:
        bonus_notes.append(f"Plank sack: +{plank_sack_bonus} capacity")
    
    return {
        "gp_per_hour": gp_per_hour,
        "items_per_hour": items_per_hour,
        "trips_per_hour": trips_per_hour,
        "items_per_trip": items_per_trip,
        "materials_per_trip": materials_per_trip,
        "effective_inventory": effective_inventory,
        "seconds_per_trip": seconds_per_trip,
        "timing_key": timing_key,
        "timing": timing,
        "notes": timing.notes,
        "tool_notes": tool_notes,
        "bonus_notes": bonus_notes,
        "tool_slots_saved": (1 if timing.needs_hammer and has_imcando_hammer else 0) + 
                           (1 if timing.needs_saw and has_amys_saw else 0),
        "bank_location": bank_location.name,
        "bank_requirements": bank_location.requirements,
        "effective_ticks": effective_ticks,
        "is_double_mould": is_double_mould_chain,
        "plank_sack_active": has_plank_sack and timing.uses_planks,
    }


ALL_ITEMS = {
    **ALL_LOGS, **ALL_PLANKS, **HULL_PARTS, **LARGE_HULL_PARTS,
    **HULL_REPAIR_KITS, **ALL_ORES, **ALL_BARS, **KEEL_PARTS,
    **LARGE_KEEL_PARTS, **ALL_NAILS, **ALL_CANNONBALLS, **AMMO_MOULDS,
    **MISC_ITEMS
}


def get_wiki_image_url(item_name: str) -> str:
    formatted_name = item_name.replace(" ", "_").replace("'", "%27")
    return f"https://oldschool.runescape.wiki/images/{formatted_name}.png"


def get_item_icon_url(item_name: str) -> str:
    name_fixes = {
        "Plank": "Plank",
        "Logs": "Logs",
    }
    
    fixed_name = name_fixes.get(item_name, item_name)
    return get_wiki_image_url(fixed_name)


def get_clean_item_name(chain_name: str) -> str:
    clean = chain_name.replace(" processing", "").replace(" smithing", "")
    clean = clean.replace(" (Regular)", "").replace(" (Double)", "")
    return clean


def get_output_item_name(chain_name: str) -> str:
    clean = get_clean_item_name(chain_name)
    return clean


class OSRSWikiConnection:
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'OSRS-Sailing-Tracker/4.5 (Streamlit App)'
        })
    
    def fetch_mapping(self) -> Dict:
        response = self._session.get(f"{self.base_url}/mapping")
        response.raise_for_status()
        items = response.json()
        return {item['id']: item for item in items}
    
    def fetch_prices(self) -> Dict:
        response = self._session.get(f"{self.base_url}/latest")
        response.raise_for_status()
        return response.json().get('data', {})


@st.cache_resource
def get_api_connection() -> OSRSWikiConnection:
    return OSRSWikiConnection()


@st.cache_data(ttl=300, show_spinner=False)
def fetch_item_mapping(_conn: OSRSWikiConnection) -> Dict:
    return _conn.fetch_mapping()


@st.cache_data(ttl=60, show_spinner=False)
def fetch_latest_prices(_conn: OSRSWikiConnection) -> Dict:
    return _conn.fetch_prices()


@st.cache_resource
def get_id_lookup(_item_mapping_hash: str, item_mapping: Dict) -> 'ItemIDLookup':
    return ItemIDLookup(item_mapping)


class ItemIDLookup:
    def __init__(self, item_mapping: Dict):
        self.item_mapping = item_mapping
        self.name_to_id_cache = {}
        
        for item_id, item_data in item_mapping.items():
            if isinstance(item_data, dict) and 'name' in item_data:
                self.name_to_id_cache[item_data['name'].lower()] = item_id
    
    def find_id_by_name(self, item_name: str) -> Optional[int]:
        search_name = item_name.lower()
        
        if search_name in self.name_to_id_cache:
            return self.name_to_id_cache[search_name]
        
        for name, item_id in self.name_to_id_cache.items():
            if search_name in name or name in search_name:
                return item_id
        
        return None
    
    def get_or_find_id(self, item_id: Optional[int], item_name: str) -> Optional[int]:
        if item_id:
            return item_id
        
        found_id = self.find_id_by_name(item_name)
        if found_id:
            ALL_ITEMS[found_id] = item_name
        return found_id


@dataclass
class ChainStep:
    item_id: Optional[int]
    item_name: str
    quantity: float = 1
    is_self_obtained: bool = False
    processing_method: Optional[str] = None
    custom_cost: Optional[float] = None


@dataclass
class ProcessingChain:
    name: str
    category: str
    steps: List[ChainStep] = field(default_factory=list)
    special_ratio: Optional[Dict] = field(default_factory=dict)
    
    def get_output_item_name(self) -> str:
        if self.steps:
            return self.steps[-1].item_name
        return get_clean_item_name(self.name)
    
    def calculate(self, prices: Dict, config: Dict, id_lookup: ItemIDLookup) -> Dict:
        results = {
            "chain_name": self.name,
            "category": self.category,
            "steps": [],
            "raw_material_cost": 0,
            "processing_costs": 0,
            "total_input_cost": 0,
            "output_value": 0,
            "ge_tax": 0,
            "net_profit": 0,
            "roi": 0,
            "profit_per_item": 0,
            "missing_prices": [],
            "output_item_name": self.get_output_item_name()
        }
        
        if not self.steps:
            results["error"] = "No steps in chain"
            return results
        
        final_quantity = config.get("quantity", 1)
        
        if self.special_ratio and "dragon" in self.name.lower():
            ratio = self.special_ratio.get("conversion_ratio", 5)
        else:
            ratio = 5
        
        num_steps = len(self.steps)
        needed = [0.0] * num_steps
        needed[-1] = final_quantity

        for idx in range(num_steps - 2, -1, -1):
            prev = self.steps[idx]
            nxt = self.steps[idx + 1]
            if getattr(nxt, 'quantity', 0) == 0:
                needed[idx] = needed[idx + 1] * getattr(prev, 'quantity', 1)
            else:
                needed[idx] = needed[idx + 1] * (getattr(prev, 'quantity', 1) / getattr(nxt, 'quantity', 1))

        for i, step in enumerate(self.steps):
            resolved_id = id_lookup.get_or_find_id(step.item_id, step.item_name)

            if not resolved_id:
                results["missing_prices"].append(step.item_name)
                continue

            price_data = prices.get(str(resolved_id), {})

            if not price_data:
                results["missing_prices"].append(step.item_name)

            step_qty = needed[i]
            is_output = (i == len(self.steps) - 1)
            is_input = (i == 0)

            if is_output:
                unit_price = price_data.get("low", 0) if price_data else 0
                total_value = unit_price * step_qty
                results["output_value"] = total_value
            else:
                is_free = step.is_self_obtained or config.get("self_collected", False)
                unit_price = price_data.get("high", 0) if price_data and not is_free else 0
                total_value = unit_price * step_qty

                results["raw_material_cost"] += total_value

            processing_cost = 0
            process_notes = ""

            if step.processing_method:
                processing_cost, process_notes = self._calculate_processing_cost(
                    step, step_qty, prices, config, id_lookup
                )
                results["processing_costs"] += processing_cost

            results["steps"].append({
                "name": step.item_name,
                "quantity": step_qty,
                "unit_price": unit_price,
                "total_value": total_value,
                "is_self_obtained": step.is_self_obtained or config.get("self_collected", False),
                "processing_cost": processing_cost,
                "processing_notes": process_notes,
                "step_type": "Output" if is_output else ("Input" if is_input else "Intermediate")
            })
        
        results["total_input_cost"] = results["raw_material_cost"] + results["processing_costs"]
        
        if results["output_value"] >= 50:
            results["ge_tax"] = min(results["output_value"] * 0.02, 5_000_000)
        
        results["net_profit"] = results["output_value"] - results["total_input_cost"] - results["ge_tax"]
        results["profit_per_item"] = results["net_profit"] / final_quantity if final_quantity > 0 else 0
        
        if results["total_input_cost"] > 0:
            results["roi"] = (results["net_profit"] / results["total_input_cost"]) * 100
        elif results["raw_material_cost"] == 0:
            results["roi"] = float('inf')
        
        return results
    
    def _calculate_processing_cost(self, step: ChainStep, quantity: float, 
                                  prices: Dict, config: Dict, id_lookup: ItemIDLookup) -> Tuple[float, str]:
        if step.custom_cost is not None:
            return step.custom_cost * quantity, f"Custom: {step.custom_cost} gp each"
        
        if step.processing_method == "Sawmill":
            if step.item_name in SAWMILL_COSTS:
                cost = SAWMILL_COSTS[step.item_name] * quantity
                return cost, f"Sawmill: {SAWMILL_COSTS[step.item_name]} gp each"
        
        elif step.processing_method == "Plank Make":
            if step.item_name in PLANK_MAKE_COSTS:
                base_cost = PLANK_MAKE_COSTS[step.item_name] * quantity
                
                astral_price = prices.get(str(RUNE_IDS["Astral rune"]), {}).get("high", 0)
                nature_price = prices.get(str(RUNE_IDS["Nature rune"]), {}).get("high", 0)
                
                rune_cost = (astral_price * 2 + nature_price) * quantity
                
                if not config.get("use_earth_staff", False):
                    earth_price = prices.get(str(RUNE_IDS["Earth rune"]), {}).get("high", 0)
                    rune_cost += earth_price * 15 * quantity
                    notes = f"Plank Make: {PLANK_MAKE_COSTS[step.item_name]} + runes"
                else:
                    notes = f"Plank Make (Earth staff): {PLANK_MAKE_COSTS[step.item_name]} + runes"
                
                return base_cost + rune_cost, notes
        
        elif step.processing_method == "Smithing":
            return 0, "Smithing (no cost)"
        
        elif step.processing_method == "Dragon Forge":
            return 0, "Dragon Forge (no cost, 92 Smithing req)"
        
        return 0, ""


@st.cache_data(ttl=3600)
def generate_all_chains() -> Dict[str, List[ProcessingChain]]:
    chains = {
        "Planks": [],
        "Hull Parts": [],
        "Large Hull Parts": [],
        "Hull Repair Kits": [],
        "Keel Parts": [],
        "Large Keel Parts": [],
        "Nails": [],
        "Cannonballs": [],
    }
    
    plank_mappings = [
        (1511, "Logs", 960, "Plank"),
        (1521, "Oak logs", 8778, "Oak plank"),
        (6333, "Teak logs", 8780, "Teak plank"),
        (6332, "Mahogany logs", 8782, "Mahogany plank"),
        (32904, "Camphor logs", 31432, "Camphor plank"),
        (32907, "Ironwood logs", 31435, "Ironwood plank"),
        (32910, "Rosewood logs", 31438, "Rosewood plank"),
    ]
    
    for log_id, log_name, plank_id, plank_name in plank_mappings:
        chain = ProcessingChain(
            name=f"{plank_name} processing",
            category="Planks"
        )
        chain.steps = [
            ChainStep(log_id, log_name, 1),
            ChainStep(plank_id, plank_name, 1, processing_method="Sawmill")
        ]
        chains["Planks"].append(chain)
    
    hull_mappings = [
        (960, "Plank", 32041, "Wooden hull parts"),
        (8778, "Oak plank", 32044, "Oak hull parts"),
        (8780, "Teak plank", 32047, "Teak hull parts"),
        (8782, "Mahogany plank", 32050, "Mahogany hull parts"),
        (31432, "Camphor plank", 32053, "Camphor hull parts"),
        (31435, "Ironwood plank", 32056, "Ironwood hull parts"),
        (31438, "Rosewood plank", 32059, "Rosewood hull parts"),
    ]
    
    for plank_id, plank_name, hull_id, hull_name in hull_mappings:
        chain = ProcessingChain(
            name=hull_name,
            category="Hull Parts"
        )
        chain.steps = [
            ChainStep(plank_id, plank_name, 5),
            ChainStep(hull_id, hull_name, 1)
        ]
        chains["Hull Parts"].append(chain)
    
    large_hull_mappings = [
        (32041, "Wooden hull parts", 32062, "Large wooden hull parts"),
        (32044, "Oak hull parts", 32065, "Large oak hull parts"),
        (32047, "Teak hull parts", 32068, "Large teak hull parts"),
        (32050, "Mahogany hull parts", 32071, "Large mahogany hull parts"),
        (32053, "Camphor hull parts", 32074, "Large camphor hull parts"),
        (32056, "Ironwood hull parts", 32077, "Large ironwood hull parts"),
        (32059, "Rosewood hull parts", 32080, "Large rosewood hull parts"),
    ]
    
    for hull_id, hull_name, large_id, large_name in large_hull_mappings:
        chain = ProcessingChain(
            name=large_name,
            category="Large Hull Parts"
        )
        chain.steps = [
            ChainStep(hull_id, hull_name, 5),
            ChainStep(large_id, large_name, 1)
        ]
        chains["Large Hull Parts"].append(chain)
    
    repair_kit_mappings = [
        (960, "Plank", 4819, "Bronze nails", 5, 2, 10, 2, 31964, "Repair kit"),
        (8778, "Oak plank", 4820, "Iron nails", 5, 2, 10, 2, 31967, "Oak repair kit"),
        (8780, "Teak plank", 1539, "Steel nails", 5, 2, 10, 2, 31970, "Teak repair kit"),
        (8782, "Mahogany plank", 4822, "Mithril nails", 5, 2, 10, 2, 31973, "Mahogany repair kit"),
        (31432, "Camphor plank", 4823, "Adamantite nails", 5, 2, 10, 2, 31976, "Camphor repair kit"),
        (31435, "Ironwood plank", 4824, "Rune nails", 5, 1, 10, 3, 31979, "Ironwood repair kit"),
        (31438, "Rosewood plank", 31406, "Dragon nails", 5, 1, 5, 3, 31982, "Rosewood repair kit"),
    ]
    
    for plank_id, plank_name, nail_id, nail_name, paste_qty, plank_qty, nail_qty, output_qty, kit_id, kit_name in repair_kit_mappings:
        chain = ProcessingChain(
            name=kit_name,
            category="Hull Repair Kits"
        )
        chain.steps = [
            ChainStep(plank_id, plank_name, plank_qty),
            ChainStep(nail_id, nail_name, nail_qty),
            ChainStep(1941, "Swamp paste", paste_qty),
            ChainStep(kit_id, kit_name, output_qty)
        ]
        chains["Hull Repair Kits"].append(chain)
    
    keel_mappings = [
        (2349, "Bronze bar", 31999, "Bronze keel parts", 5),
        (2351, "Iron bar", 32002, "Iron keel parts", 5),
        (2353, "Steel bar", 32005, "Steel keel parts", 5),
        (2359, "Mithril bar", 32008, "Mithril keel parts", 5),
        (2361, "Adamantite bar", 32011, "Adamant keel parts", 5),
        (2363, "Runite bar", 32014, "Rune keel parts", 5),
        (31996, "Dragon metal sheet", 32017, "Dragon keel parts", 2),
    ]
    
    for bar_id, bar_name, keel_id, keel_name, qty in keel_mappings:
        chain = ProcessingChain(
            name=keel_name,
            category="Keel Parts"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, qty),
            ChainStep(keel_id, keel_name, 1)
        ]
        chains["Keel Parts"].append(chain)
    
    large_keel_mappings = [
        (31999, "Bronze keel parts", 32020, "Large bronze keel parts", 5),
        (32002, "Iron keel parts", 32023, "Large iron keel parts", 5),
        (32005, "Steel keel parts", 32026, "Large steel keel parts", 5),
        (32008, "Mithril keel parts", 32029, "Large mithril keel parts", 5),
        (32011, "Adamant keel parts", 32032, "Large adamant keel parts", 5),
        (32014, "Rune keel parts", 32035, "Large rune keel parts", 5),
        (32017, "Dragon keel parts", 32038, "Large dragon keel parts", 2),
    ]
    
    for keel_id, keel_name, large_id, large_name, qty in large_keel_mappings:
        chain = ProcessingChain(
            name=large_name,
            category="Large Keel Parts"
        )
        chain.steps = [
            ChainStep(keel_id, keel_name, qty),
            ChainStep(large_id, large_name, 1)
        ]
        if qty == 2:
            chain.special_ratio = {"conversion_ratio": 2}
        chains["Large Keel Parts"].append(chain)
    
    nail_mappings = [
        (2349, "Bronze bar", 4819, "Bronze nails"),
        (2351, "Iron bar", 4820, "Iron nails"),
        (2353, "Steel bar", 1539, "Steel nails"),
        (2359, "Mithril bar", 4822, "Mithril nails"),
        (2361, "Adamantite bar", 4823, "Adamantite nails"),
        (2363, "Runite bar", 4824, "Rune nails"),
        (31996, "Dragon metal sheet", 31406, "Dragon nails"),
    ]
    
    for bar_id, bar_name, nail_id, nail_name in nail_mappings:
        chain = ProcessingChain(
            name=f"{nail_name} smithing",
            category="Nails"
        )
        processing = "Dragon Forge" if "Dragon" in nail_name else "Smithing"
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(nail_id, nail_name, 15, processing_method=processing)
        ]
        chains["Nails"].append(chain)
    
    cannonball_mappings = [
        (2349, "Bronze bar", 31906, "Bronze cannonball"),
        (2351, "Iron bar", 31908, "Iron cannonball"),
        (2353, "Steel bar", 2, "Steel cannonball"),
        (2359, "Mithril bar", 31910, "Mithril cannonball"),
        (2361, "Adamantite bar", 31912, "Adamant cannonball"),
        (2363, "Runite bar", 31914, "Rune cannonball"),
    ]
    
    for bar_id, bar_name, ball_id, ball_name in cannonball_mappings:
        chain = ProcessingChain(
            name=f"{ball_name} (Regular)",
            category="Cannonballs"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(ball_id, ball_name, 4)
        ]
        chains["Cannonballs"].append(chain)
        
        chain_double = ProcessingChain(
            name=f"{ball_name} (Double)",
            category="Cannonballs"
        )
        chain_double.steps = [
            ChainStep(bar_id, bar_name, 2),
            ChainStep(ball_id, ball_name, 8)
        ]
        chains["Cannonballs"].append(chain_double)
    
    return chains


def format_gp(value: float) -> str:
    if value == float('inf'):
        return "Inf"
    
    is_negative = value < 0
    value = abs(value)
    
    if value >= 1_000_000:
        formatted = f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        formatted = f"{value/1_000:.1f}K"
    else:
        formatted = f"{int(value):,}"
    
    return f"-{formatted}" if is_negative else formatted


def render_item_with_icon(item_name: str, profit: Optional[float] = None, show_profit: bool = True) -> str:
    icon_url = get_item_icon_url(item_name)
    profit_html = ""
    if show_profit and profit is not None:
        profit_color = "#d4af37" if profit >= 0 else "#c0392b"
        profit_html = f'<span style="color: {profit_color}; font-weight: 600;">{format_gp(profit)}</span>'
    
    return f"""
    <div style="display: flex; align-items: center; gap: 10px; padding: 8px; 
                background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
                border: 2px solid #d4af37; border-radius: 8px; margin: 4px 0;">
        <img src="{icon_url}" style="width: 32px; height: 32px; image-rendering: pixelated;" 
             onerror="this.style.display='none'">
        <div style="flex: 1;">
            <div style="color: #f4e4bc; font-family: 'Cinzel', serif; font-size: 0.9rem;">{item_name}</div>
            {profit_html}
        </div>
    </div>
    """


def render_best_item_card(label: str, item_name: str, value: str) -> str:
    icon_url = get_item_icon_url(get_clean_item_name(item_name))
    return f"""
    <div style="background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
                border: 2px solid #d4af37; border-radius: 10px; padding: 15px;
                text-align: center; height: 100%;">
        <div style="color: #ffd700; font-family: 'Cinzel', serif; font-size: 0.85rem; margin-bottom: 8px;">
            {label}
        </div>
        <img src="{icon_url}" style="width: 40px; height: 40px; image-rendering: pixelated; margin-bottom: 8px;"
             onerror="this.style.display='none'">
        <div style="color: #f4e4bc; font-family: 'Crimson Text', serif; font-size: 0.95rem; 
                    word-wrap: break-word; line-height: 1.3;">
            {item_name}
        </div>
        <div style="color: #d4af37; font-family: 'Crimson Text', serif; font-size: 1rem; 
                    font-weight: 600; margin-top: 4px;">
            {value}
        </div>
    </div>
    """


def create_profit_chart(results: List[Dict], top_n: int = 10) -> go.Figure:
    sorted_results = sorted(results, key=lambda x: x.get("_profit_raw", 0), reverse=True)[:top_n]
    
    items = [r["Item"] for r in sorted_results]
    profits = [r["_profit_raw"] for r in sorted_results]
    categories = [r.get("Category", "Unknown") for r in sorted_results]
    
    display_names = [get_clean_item_name(name) for name in items]
    tiers = [get_tier_from_name(name) for name in items]
    colors = [get_item_tier_color(items[i], profits[i]) for i in range(len(items))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=profits,
            y=display_names,
            orientation='h',
            marker_color=colors,
            marker_line_color='#1a2a3a',
            marker_line_width=1.5,
            text=[format_gp(p) for p in profits],
            textposition='outside',
            textfont=dict(color='#f4e4bc', size=10),
            name='Profit',
            customdata=list(zip(categories, tiers)),
            hovertemplate='<b>%{y}</b><br>Category: %{customdata[0]}<br>Tier: %{customdata[1]}<br>Profit: %{x:,.0f} GP<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Top Profitable Chains",
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text=f"Top {len(sorted_results)} by profit - colored by tier",
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title="Net Profit (GP)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f'
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color='#f4e4bc', size=9),
            autorange="reversed"
        ),
        height=max(380, top_n * 36),
        margin=dict(l=140, r=80, t=60, b=45),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False
    )
    
    return fig


def create_category_pie(results: List[Dict]) -> go.Figure:
    category_profits = {}
    category_counts = {}
    for r in results:
        cat = r.get("Category", "Unknown")
        profit = max(0, r.get("_profit_raw", 0))
        category_profits[cat] = category_profits.get(cat, 0) + profit
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    sorted_cats = sorted(category_profits.items(), key=lambda x: x[1], reverse=True)
    total_profit = sum(category_profits.values())
    
    main_cats = []
    other_total = 0
    other_count = 0
    threshold = total_profit * 0.02
    
    for cat, profit in sorted_cats:
        if profit >= threshold:
            main_cats.append((cat, profit, category_counts[cat]))
        else:
            other_total += profit
            other_count += category_counts.get(cat, 0)
    
    if other_total > 0:
        main_cats.append(("Other", other_total, other_count))
    
    labels = [c[0] for c in main_cats]
    values = [c[1] for c in main_cats]
    counts = [c[2] for c in main_cats]
    
    colors = [CATEGORY_COLORS.get(label, '#8e44ad') for label in labels]
    
    hover_text = [
        f"<b>{label}</b><br>"
        f"Total Profit: {format_gp(val)}<br>"
        f"Chains: {cnt}<br>"
        f"Share: {val/total_profit*100:.1f}%"
        for label, val, cnt in zip(labels, values, counts)
    ]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(color='#f4e4bc', size=10),
            hovertext=hover_text,
            hoverinfo='text',
            marker=dict(
                colors=colors,
                line=dict(color='#1a2a3a', width=2)
            ),
            pull=[0.03 if i == 0 else 0 for i in range(len(labels))],
            insidetextorientation='horizontal',
            sort=False
        )
    ])
    
    fig.add_annotation(
        text=f"<b>Total</b><br>{format_gp(total_profit)}",
        x=0.5, y=0.5,
        font=dict(color='#ffd700', size=12),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text="Profit by Category",
            font=dict(color='#ffd700', size=16)
        ),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        uniformtext=dict(minsize=8, mode='hide')
    )
    
    return fig


def create_profit_histogram(profits: List[float], results: List[Dict] = None, per_item: bool = False) -> go.Figure:
    profits_arr = np.array(profits)
    median_val = np.median(profits_arr)
    q1 = np.percentile(profits_arr, 25)
    q3 = np.percentile(profits_arr, 75)
    iqr = q3 - q1
    
    unit_label = "GP/item" if per_item else "GP"
    
    lower_fence = q1 - 3 * iqr
    upper_fence = q3 + 3 * iqr
    
    main_data = profits_arr[(profits_arr >= lower_fence) & (profits_arr <= upper_fence)]
    outliers = profits_arr[(profits_arr < lower_fence) | (profits_arr > upper_fence)]
    
    has_extreme_outliers = len(outliers) > 0 and (
        len(main_data) >= len(profits_arr) * 0.75
    )
    
    if has_extreme_outliers and len(main_data) > 0:
        hist_data = main_data
        outlier_note = f"{len(outliers)} extreme outlier(s) excluded"
    else:
        hist_data = profits_arr
        outlier_note = None
    
    profitable = hist_data[hist_data > 0]
    unprofitable = hist_data[hist_data <= 0]
    
    if len(hist_data) > 1:
        hist_min, hist_max = hist_data.min(), hist_data.max()
        hist_range = hist_max - hist_min
        
        target_bins = 20
        bin_size = hist_range / target_bins if hist_range > 0 else 1000
        
        if bin_size > 0:
            magnitude = 10 ** np.floor(np.log10(max(abs(bin_size), 1)))
            bin_size = np.ceil(bin_size / magnitude) * magnitude
        bin_size = max(bin_size, 100)
    else:
        bin_size = 10000
    
    fig = go.Figure()
    
    if len(profitable) > 0:
        fig.add_trace(
            go.Histogram(
                x=profitable,
                name=f'Profitable ({len(profitable)})',
                marker_color='#d4af37',
                marker_line_color='#b8860b',
                marker_line_width=1,
                opacity=0.9,
                xbins=dict(size=bin_size),
                hovertemplate=f'<b>Profitable Chains</b><br>Range: %{{x:,.0f}} {unit_label}<br>Count: %{{y}}<extra></extra>'
            )
        )
    
    if len(unprofitable) > 0:
        fig.add_trace(
            go.Histogram(
                x=unprofitable,
                name=f'Unprofitable ({len(unprofitable)})',
                marker_color='#c0392b',
                marker_line_color='#922b21',
                marker_line_width=1,
                opacity=0.9,
                xbins=dict(size=bin_size),
                hovertemplate=f'<b>Unprofitable Chains</b><br>Range: %{{x:,.0f}} {unit_label}<br>Count: %{{y}}<extra></extra>'
            )
        )
    
    fig.add_vline(
        x=0, 
        line_dash="solid", 
        line_color="rgba(244,228,188,0.5)",
        line_width=2,
        annotation_text="Break-even",
        annotation_position="top",
        annotation_font=dict(color='#f4e4bc', size=10)
    )
    
    if not has_extreme_outliers or (lower_fence <= median_val <= upper_fence):
        fig.add_vline(
            x=median_val,
            line_dash="dot",
            line_color="#5dade2",
            line_width=2,
            annotation_text=f"Median: {format_gp(median_val)}",
            annotation_position="top right",
            annotation_font=dict(color='#5dade2', size=10)
        )
    
    title_text = "Profit Distribution"
    subtitle_parts = [f"Showing {len(hist_data)} chains"]
    if outlier_note:
        subtitle_parts.append(outlier_note)
    subtitle_text = " - ".join(subtitle_parts)
    
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text=subtitle_text,
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title=f"Net Profit ({unit_label})",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f',
            zeroline=True,
            zerolinecolor='rgba(244,228,188,0.3)',
            zerolinewidth=1
        ),
        yaxis=dict(
            title="Count",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)'
        ),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        barmode='overlay',
        bargap=0.1,
        legend=dict(
            font=dict(color='#f4e4bc', size=9),
            bgcolor='rgba(92,77,58,0.85)',
            bordercolor='#5c4d3a',
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            itemsizing='constant'
        ),
        margin=dict(l=55, r=25, t=70, b=50)
    )
    
    stats_lines = [
        "<b>Stats</b>",
        f"Med: {format_gp(median_val)}",
        f"Q1: {format_gp(q1)}",
        f"Q3: {format_gp(q3)}",
    ]
    
    fig.add_annotation(
        x=0.98,
        y=0.95,
        xref='paper',
        yref='paper',
        text="<br>".join(stats_lines),
        showarrow=False,
        font=dict(color='#f4e4bc', size=9),
        align='right',
        bgcolor='rgba(92,77,58,0.9)',
        bordercolor='#d4af37',
        borderwidth=1,
        borderpad=5
    )
    
    return fig


def create_category_comparison(results: List[Dict]) -> go.Figure:
    category_stats = {}
    for r in results:
        cat = r.get("Category", "Unknown")
        profit = r.get("_profit_raw", 0)
        if cat not in category_stats:
            category_stats[cat] = {"profits": [], "count": 0}
        category_stats[cat]["profits"].append(profit)
        category_stats[cat]["count"] += 1
    
    sorted_categories = sorted(
        category_stats.items(),
        key=lambda x: max(x[1]["profits"]),
        reverse=True
    )
    
    categories = [c[0] for c in sorted_categories]
    stats = [c[1] for c in sorted_categories]
    
    avg_profits = [np.mean(s["profits"]) for s in stats]
    max_profits = [max(s["profits"]) for s in stats]
    median_profits = [np.median(s["profits"]) for s in stats]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Best Profit',
        x=categories,
        y=max_profits,
        marker_color='#d4af37',
        marker_line_color='#b8860b',
        marker_line_width=1.5,
        text=[format_gp(v) for v in max_profits],
        textposition='outside',
        textfont=dict(color='#f4e4bc', size=9),
        hovertemplate='<b>%{x}</b><br>Best: %{y:,.0f} GP<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Median Profit',
        x=categories,
        y=median_profits,
        marker_color='#5dade2',
        marker_line_color='#3498db',
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Median: %{y:,.0f} GP<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Average Profit',
        x=categories,
        y=avg_profits,
        marker_color='#1abc9c',
        marker_line_color='#16a085',
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Avg: %{y:,.0f} GP<extra></extra>'
    ))
    
    fig.add_hline(
        y=0,
        line_dash="solid",
        line_color="rgba(244,228,188,0.3)",
        line_width=1
    )
    
    fig.update_layout(
        title=dict(
            text="Category Performance",
            font=dict(color='#ffd700', size=16)
        ),
        xaxis=dict(
            title="",
            tickfont=dict(color='#f4e4bc', size=9),
            tickangle=45
        ),
        yaxis=dict(
            title="Profit (GP)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f',
            zeroline=True,
            zerolinecolor='rgba(244,228,188,0.3)'
        ),
        barmode='group',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        legend=dict(
            font=dict(color='#f4e4bc', size=9),
            bgcolor='rgba(92,77,58,0.85)',
            bordercolor='#5c4d3a',
            borderwidth=1,
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            itemsizing='constant'
        ),
        margin=dict(l=55, r=15, t=70, b=100),
        bargap=0.15,
        bargroupgap=0.08
    )
    
    return fig


def create_roi_scatter(results: List[Dict]) -> go.Figure:
    data = [r for r in results if r.get("ROI %") is not None and r.get("ROI %") != float('inf')]
    
    if not data:
        return None
    
    categories_data = {}
    for r in data:
        cat = r.get("Category", "Unknown")
        if cat not in categories_data:
            categories_data[cat] = {"profits": [], "rois": [], "names": []}
        categories_data[cat]["profits"].append(r["_profit_raw"])
        categories_data[cat]["rois"].append(r["ROI %"])
        categories_data[cat]["names"].append(get_clean_item_name(r["Item"]))
    
    fallback_colors = ['#8e44ad', '#e74c3c', '#9b59b6', '#34495e']
    
    fig = go.Figure()
    
    for i, (cat, cat_data) in enumerate(categories_data.items()):
        color = CATEGORY_COLORS.get(cat, fallback_colors[i % len(fallback_colors)])
        
        fig.add_trace(go.Scatter(
            x=cat_data["profits"],
            y=cat_data["rois"],
            mode='markers',
            name=cat,
            marker=dict(
                size=11,
                color=color,
                line=dict(color='#1a2a3a', width=1.5),
                opacity=0.85
            ),
            text=cat_data["names"],
            hovertemplate=(
                '<b>%{text}</b><br>'
                f'<span style="color:{color}">*</span> {cat}<br>'
                'Profit: %{x:,.0f} GP<br>'
                'ROI: %{y:.1f}%'
                '<extra></extra>'
            )
        ))
    
    all_profits = [r["_profit_raw"] for r in data]
    all_rois = [r["ROI %"] for r in data]
    
    notable_indices = set()
    
    sorted_by_profit = sorted(range(len(data)), key=lambda i: all_profits[i], reverse=True)
    for i in sorted_by_profit[:2]:
        notable_indices.add(i)
    
    sorted_by_roi = sorted(range(len(data)), key=lambda i: all_rois[i], reverse=True)
    for i in sorted_by_roi[:2]:
        if len(notable_indices) < 4:
            notable_indices.add(i)
    
    for idx in notable_indices:
        item_name = get_clean_item_name(data[idx]["Item"])
        display_name = item_name[:15] + "..." if len(item_name) > 15 else item_name
        
        fig.add_annotation(
            x=all_profits[idx],
            y=all_rois[idx],
            text=display_name,
            showarrow=True,
            arrowhead=2,
            arrowsize=0.8,
            arrowwidth=1,
            arrowcolor='#f4e4bc',
            font=dict(color='#f4e4bc', size=8),
            bgcolor='rgba(26,42,58,0.85)',
            bordercolor='#5c4d3a',
            borderwidth=1,
            borderpad=2,
            ax=25,
            ay=-20
        )
    
    min_profit, max_profit = min(all_profits), max(all_profits)
    min_roi, max_roi = min(all_rois), max(all_rois)
    
    if min_profit < 0 < max_profit:
        fig.add_vline(
            x=0,
            line_dash="dash",
            line_color="rgba(244,228,188,0.4)",
            line_width=1
        )
    
    if min_roi < 0 < max_roi:
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="rgba(244,228,188,0.4)",
            line_width=1
        )
    
    fig.update_layout(
        title=dict(
            text="ROI vs Profit Analysis",
            font=dict(color='#ffd700', size=16),
            subtitle=dict(
                text="Higher and further right = better investment",
                font=dict(color='#a08b6d', size=11)
            )
        ),
        xaxis=dict(
            title="Net Profit (GP)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f',
            zeroline=True,
            zerolinecolor='rgba(244,228,188,0.3)'
        ),
        yaxis=dict(
            title="ROI (%)",
            title_font=dict(color='#f4e4bc', size=11),
            tickfont=dict(color='#f4e4bc', size=9),
            gridcolor='rgba(139,115,85,0.25)',
            ticksuffix='%',
            zeroline=True,
            zerolinecolor='rgba(244,228,188,0.3)'
        ),
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        legend=dict(
            title=dict(
                text='Category',
                font=dict(color='#ffd700', size=10)
            ),
            font=dict(color='#f4e4bc', size=9),
            bgcolor='rgba(92,77,58,0.85)',
            bordercolor='#5c4d3a',
            borderwidth=1,
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            itemsizing='constant',
            itemwidth=30
        ),
        margin=dict(l=55, r=20, t=60, b=90)
    )
    
    return fig


def main():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("OSRS Sailing Materials Tracker")
        st.caption("*\"For the crafty sailor!\"*")
    with col2:
        st.link_button(
            "OSRS Wiki",
            "https://oldschool.runescape.wiki/w/Sailing",
            use_container_width=True
        )
    
    conn = get_api_connection()
    
    with st.spinner("Loading market data..."):
        item_mapping = fetch_item_mapping(conn)
        prices = fetch_latest_prices(conn)
        mapping_hash = str(hash(frozenset(item_mapping.keys())))
        id_lookup = get_id_lookup(mapping_hash, item_mapping)
        all_chains = generate_all_chains()
    
    params = st.query_params
    
    with st.sidebar:
        st.header("Configuration")
        
        with st.form("config_form"):
            st.subheader("Processing Options")
            
            plank_method = st.selectbox(
                "Plank Method",
                ["Sawmill", "Plank Make", "Plank Make (Earth Staff)"],
                index=["Sawmill", "Plank Make", "Plank Make (Earth Staff)"].index(
                    params.get("plank_method", "Sawmill")
                ) if params.get("plank_method") in ["Sawmill", "Plank Make", "Plank Make (Earth Staff)"] else 0
            )
            
            self_collected = st.toggle(
                "Self-Collected Materials",
                value=params.get("self_collected", "false") == "true",
                help="Sets material cost to 0"
            )
            
            ancient_furnace = st.toggle(
                "Ancient Furnace",
                value=params.get("ancient_furnace", "false") == "true",
                help="Halves smithing time (87 Sailing)"
            )
            
            st.divider()
            
            st.subheader("GP/hr Calculation")
            
            show_gp_hr = st.toggle(
                "Show GP/hr",
                value=params.get("show_gp_hr", "false") == "true",
                help="Calculate and display gold per hour estimates"
            )
            
            if show_gp_hr:
                bank_location_options = list(BANK_LOCATIONS.keys())
                default_location = params.get("bank_location", "Medium (Typical)")
                if default_location not in bank_location_options:
                    default_location = "Medium (Typical)"
                
                bank_location = st.selectbox(
                    "Bank Location",
                    bank_location_options,
                    index=bank_location_options.index(default_location),
                    help="Select your banking location"
                )
                
                selected_bank = BANK_LOCATIONS[bank_location]
                st.caption(f"*{selected_bank.total_overhead:.0f}s overhead | Req: {selected_bank.requirements}*")
                
                use_stamina = True
                if selected_bank.stamina_dependent:
                    use_stamina = st.toggle(
                        "Using Stamina Potions",
                        value=params.get("use_stamina", "true") == "true",
                        help="Reduces travel time by ~30%"
                    )
                
                st.caption("**Equipment**")
                
                has_imcando_hammer = st.toggle(
                    "Imcando Hammer",
                    value=params.get("imcando_hammer", "false") == "true",
                    help="Equippable hammer (Below Ice Mountain)"
                )
                
                has_amys_saw = st.toggle(
                    "Amy's Saw",
                    value=params.get("amys_saw", "false") == "true",
                    help="Equippable saw (Sailing reward)"
                )
                
                has_plank_sack = st.toggle(
                    "Plank Sack",
                    value=params.get("plank_sack", "false") == "true",
                    help="Holds 28 extra planks (Mahogany Homes)"
                )
                
                has_smithing_outfit = st.toggle(
                    "Smiths' Uniform",
                    value=params.get("smithing_outfit", "false") == "true",
                    help="15% chance to save 1 tick (Giants' Foundry)"
                )
                
            else:
                bank_location = params.get("bank_location", "Medium (Typical)")
                use_stamina = params.get("use_stamina", "true") == "true"
                has_imcando_hammer = params.get("imcando_hammer", "false") == "true"
                has_amys_saw = params.get("amys_saw", "false") == "true"
                has_plank_sack = params.get("plank_sack", "false") == "true"
                has_smithing_outfit = params.get("smithing_outfit", "false") == "true"
            
            st.divider()
            
            quantity = st.number_input(
                "Calculate for quantity:",
                min_value=1,
                max_value=100000,
                value=int(params.get("quantity", 1)),
                step=1
            )
            
            submitted = st.form_submit_button("Apply Settings", use_container_width=True)
            
            if submitted:
                st.query_params["plank_method"] = plank_method
                st.query_params["self_collected"] = str(self_collected).lower()
                st.query_params["ancient_furnace"] = str(ancient_furnace).lower()
                st.query_params["show_gp_hr"] = str(show_gp_hr).lower()
                st.query_params["bank_location"] = bank_location
                st.query_params["use_stamina"] = str(use_stamina).lower()
                st.query_params["imcando_hammer"] = str(has_imcando_hammer).lower()
                st.query_params["amys_saw"] = str(has_amys_saw).lower()
                st.query_params["plank_sack"] = str(has_plank_sack).lower()
                st.query_params["smithing_outfit"] = str(has_smithing_outfit).lower()
                st.query_params["quantity"] = str(quantity)
                st.toast("Settings applied!")
        
        st.divider()
        
        with st.container():
            st.subheader("Stats")
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                st.metric("Items", len(ALL_ITEMS))
            with stat_col2:
                st.metric("Prices", len(prices))
        
        if st.button("Refresh Prices", use_container_width=True):
            st.cache_data.clear()
            st.toast("Prices refreshed!")
            st.rerun()
        
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    use_earth_staff = "Earth Staff" in plank_method
    show_gp_hr = params.get("show_gp_hr", "false") == "true"
    config = {
        "quantity": quantity,
        "use_earth_staff": use_earth_staff,
        "self_collected": self_collected,
        "ancient_furnace": ancient_furnace,
        "plank_method": plank_method,
        "show_gp_hr": show_gp_hr,
        "bank_location": params.get("bank_location", "Medium (Typical)"),
        "use_stamina": params.get("use_stamina", "true") == "true",
        "has_imcando_hammer": params.get("imcando_hammer", "false") == "true",
        "has_amys_saw": params.get("amys_saw", "false") == "true",
        "has_plank_sack": params.get("plank_sack", "false") == "true",
        "has_smithing_outfit": params.get("smithing_outfit", "false") == "true",
    }
    
    tabs = st.tabs([
        "All Chains", 
        "Search Items", 
        "Sailing Items",
        "Best Profits",
        "Analytics"
    ])
    
    with tabs[0]:
        st.header("All Processing Chains")
        
        category = st.selectbox(
            "Select Category",
            list(all_chains.keys()),
            key="chain_category"
        )
        
        chains = all_chains[category]
        show_gp_hr = config.get("show_gp_hr", False)
        
        if chains:
            results = []
            for chain in chains:
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    profit = result["net_profit"]
                    profit_per_item = result["profit_per_item"]
                    output_name = result.get("output_item_name", chain.name)
                    
                    row = {
                        "Icon": get_item_icon_url(output_name),
                        "Item": chain.name,
                        "Input Cost": result["raw_material_cost"],
                        "Process Cost": result["processing_costs"],
                        "Total Cost": result["total_input_cost"],
                        "Output": result["output_value"],
                        "Tax": result["ge_tax"],
                        "Net Profit": profit,
                        "Per Item": profit_per_item,
                        "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                        "_profit_raw": profit,
                        "_profitable": profit > 0,
                        "_output_name": output_name
                    }
                    
                    if show_gp_hr:
                        gp_hr_data = calculate_gp_per_hour(
                            profit_per_item, category, chain.name, config
                        )
                        if gp_hr_data:
                            row["GP/hr"] = gp_hr_data["gp_per_hour"]
                            row["Items/hr"] = gp_hr_data["items_per_hour"]
                            row["_gp_hr_raw"] = gp_hr_data["gp_per_hour"]
                        else:
                            row["GP/hr"] = None
                            row["Items/hr"] = None
                            row["_gp_hr_raw"] = 0
                    
                    results.append(row)
            
            if results:
                df = pd.DataFrame(results)
                
                if show_gp_hr and "GP/hr" in df.columns:
                    df = df.sort_values("_gp_hr_raw", ascending=False, na_position='last')
                else:
                    df = df.sort_values("_profit_raw", ascending=False)
                
                column_config = {
                    "Icon": st.column_config.ImageColumn("Icon", width="small"),
                    "Item": st.column_config.TextColumn("Item", width="medium"),
                    "Input Cost": st.column_config.NumberColumn("Input Cost", format="%.0f gp"),
                    "Process Cost": st.column_config.NumberColumn("Process Cost", format="%.0f gp"),
                    "Total Cost": st.column_config.NumberColumn("Total Cost", format="%.0f gp"),
                    "Output": st.column_config.NumberColumn("Output Value", format="%.0f gp"),
                    "Tax": st.column_config.NumberColumn("GE Tax", format="%.0f gp"),
                    "Net Profit": st.column_config.NumberColumn("Net Profit", format="%.0f gp"),
                    "Per Item": st.column_config.NumberColumn("Per Item", format="%.1f gp"),
                    "ROI %": st.column_config.ProgressColumn("ROI %", format="%.1f%%", min_value=-100, max_value=100),
                    "_profit_raw": None,
                    "_profitable": None,
                    "_output_name": None
                }
                
                if show_gp_hr:
                    column_config["GP/hr"] = st.column_config.NumberColumn("GP/hr", format="%.0f")
                    column_config["Items/hr"] = st.column_config.NumberColumn("Items/hr", format="%.0f")
                    column_config["_gp_hr_raw"] = None
                
                st.dataframe(df, use_container_width=True, hide_index=True, column_config=column_config)
                
                profitable = sum(1 for r in results if r["_profit_raw"] > 0)
                best_profit = max(results, key=lambda x: x["_profit_raw"])
                total_profit = sum(r["_profit_raw"] for r in results if r["_profit_raw"] > 0)
                
                if show_gp_hr:
                    gp_hr_results = [r for r in results if r.get("_gp_hr_raw", 0) > 0]
                    best_gp_hr = max(gp_hr_results, key=lambda x: x.get("_gp_hr_raw", 0)) if gp_hr_results else None
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Profitable Chains", f"{profitable}/{len(results)}", delta=f"{(profitable/len(results)*100):.0f}%")
                    with col2:
                        if best_gp_hr:
                            st.markdown(render_best_item_card("Best GP/hr", get_clean_item_name(best_gp_hr["Item"]), format_gp(best_gp_hr["_gp_hr_raw"]) + "/hr"), unsafe_allow_html=True)
                    with col3:
                        st.markdown(render_best_item_card("Best Profit", get_clean_item_name(best_profit["Item"]), format_gp(best_profit["Net Profit"])), unsafe_allow_html=True)
                    with col4:
                        st.metric("Total Potential", format_gp(total_profit))
                else:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Profitable Chains", f"{profitable}/{len(results)}", delta=f"{(profitable/len(results)*100):.0f}%")
                    with col2:
                        st.markdown(render_best_item_card("Best Item", get_clean_item_name(best_profit["Item"]), format_gp(best_profit["Net Profit"])), unsafe_allow_html=True)
                    with col3:
                        st.metric("Best Profit", format_gp(best_profit["Net Profit"]), delta="per batch")
                    with col4:
                        st.metric("Total Potential", format_gp(total_profit))
                
                with st.expander("View Chain Details", expanded=False):
                    selected_item = st.selectbox("Select item for details", [r["Item"] for r in results])
                    
                    for chain in chains:
                        if chain.name == selected_item:
                            result = chain.calculate(prices, config, id_lookup)
                            
                            output_name = result.get("output_item_name", chain.name)
                            icon_url = get_item_icon_url(output_name)
                            st.markdown(f"""
                            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                                <img src="{icon_url}" style="width: 48px; height: 48px; image-rendering: pixelated;" onerror="this.style.display='none'">
                                <h3 style="margin: 0; color: #ffd700;">Chain: {chain.name}</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if config.get("self_collected", False):
                                st.info("Materials marked as self-collected (0 GP cost)")
                            
                            for i, step in enumerate(result["steps"]):
                                step_type = step["step_type"]
                                step_icon_url = get_item_icon_url(step['name'])
                                
                                if step_type == "Output":
                                    icon = "[OUT]"
                                    bg_color = "rgba(212,175,55,0.2)"
                                elif step_type == "Input":
                                    icon = "[IN]"
                                    bg_color = "rgba(93,173,226,0.2)"
                                else:
                                    icon = "[>]"
                                    bg_color = "rgba(139,115,85,0.2)"
                                
                                self_note = " (self-collected)" if step.get("is_self_obtained") and step_type != "Output" else ""
                                
                                st.markdown(f"""
                                <div style="display: flex; align-items: center; gap: 12px; padding: 12px;
                                            background: {bg_color}; border-radius: 8px; margin: 8px 0;
                                            border: 1px solid #5c4d3a;">
                                    <img src="{step_icon_url}" style="width: 36px; height: 36px; image-rendering: pixelated;" onerror="this.style.display='none'">
                                    <div style="flex: 1;">
                                        <div style="color: #ffd700; font-weight: 600;">{icon} Step {i+1}: {step['name']}{self_note}</div>
                                        <div style="color: #f4e4bc; font-size: 0.9rem;">
                                            Qty: {step['quantity']:,.0f} | Unit: {format_gp(step['unit_price'])} | Total: {format_gp(step['total_value'])}
                                            {f" | {step['processing_notes']}" if step['processing_notes'] else ""}
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            if result["missing_prices"]:
                                st.warning(f"Missing prices for: {', '.join(result['missing_prices'])}")
                            
                            if show_gp_hr:
                                gp_hr_data = calculate_gp_per_hour(result["profit_per_item"], category, chain.name, config)
                                if gp_hr_data:
                                    st.markdown("---")
                                    st.markdown("##### GP/hr Breakdown")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        tool_info = gp_hr_data.get("tool_notes", [])
                                        tool_status = " | ".join(tool_info) if tool_info else "None needed"
                                        
                                        st.markdown(f"""
                                        <div style="background: rgba(93,173,226,0.15); padding: 12px; border-radius: 8px; border: 1px solid #5c4d3a;">
                                            <div style="color: #5dade2; font-weight: 600; margin-bottom: 8px;">Efficiency</div>
                                            <div style="color: #f4e4bc; font-size: 0.9rem; line-height: 1.6;">
                                                <strong>Location:</strong> {gp_hr_data['bank_location']}<br>
                                                <strong>Inventory:</strong> {gp_hr_data['effective_inventory']} slots<br>
                                                <strong>Materials/trip:</strong> {gp_hr_data['materials_per_trip']:,.0f}<br>
                                                <strong>Items/trip:</strong> {gp_hr_data['items_per_trip']:,.0f}<br>
                                                <strong>Seconds/trip:</strong> {gp_hr_data['seconds_per_trip']:.1f}s<br>
                                                <strong>Ticks/action:</strong> {gp_hr_data['effective_ticks']:.2f}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col2:
                                        bonus_notes = gp_hr_data.get('bonus_notes', [])
                                        bonuses = " | ".join(bonus_notes) if bonus_notes else "None"
                                        
                                        st.markdown(f"""
                                        <div style="background: rgba(212,175,55,0.15); padding: 12px; border-radius: 8px; border: 1px solid #5c4d3a;">
                                            <div style="color: #d4af37; font-weight: 600; margin-bottom: 8px;">Output</div>
                                            <div style="color: #f4e4bc; font-size: 0.9rem; line-height: 1.6;">
                                                <strong>Items/hr:</strong> {gp_hr_data['items_per_hour']:,.0f}<br>
                                                <strong>GP/hr:</strong> {format_gp(gp_hr_data['gp_per_hour'])}<br>
                                                <strong>Trips/hr:</strong> {gp_hr_data['trips_per_hour']:.1f}<br>
                                                <strong>Tools:</strong> {tool_status}<br>
                                                <strong>Bonuses:</strong> {bonuses}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    if gp_hr_data.get("notes"):
                                        st.caption(f"*{gp_hr_data['notes']}*")
                            
                            break
    
    with tabs[1]:
        st.header("Item Database Search")
        
        search = st.text_input("Search items by name:", placeholder="Try 'rosewood', 'dragon', or 'hull'...", key="item_search")
        
        if search:
            with st.spinner("Searching..."):
                local_matches = [(id, name) for id, name in ALL_ITEMS.items() if search.lower() in name.lower()]
                api_matches = [(id, item['name']) for id, item in item_mapping.items() if search.lower() in item['name'].lower()][:50]
                
                if local_matches or api_matches:
                    data = []
                    all_matches = {id: name for id, name in local_matches + api_matches}
                    
                    for item_id, item_name in list(all_matches.items())[:100]:
                        price = prices.get(str(item_id))
                        is_sailing = item_id in ALL_ITEMS
                        
                        if price:
                            margin = price['low'] - price['high']
                            roi = (margin/price['high']*100) if price['high'] > 0 else 0
                            data.append({
                                'Icon': get_item_icon_url(item_name),
                                'ID': item_id,
                                'Name': item_name,
                                'Sailing': is_sailing,
                                'Buy': price['high'],
                                'Sell': price['low'],
                                'Margin': margin,
                                'ROI %': roi
                            })
                        else:
                            data.append({
                                'Icon': get_item_icon_url(item_name),
                                'ID': item_id,
                                'Name': item_name,
                                'Sailing': is_sailing,
                                'Buy': None,
                                'Sell': None,
                                'Margin': None,
                                'ROI %': None
                            })
                    
                    df = pd.DataFrame(data)
                    
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Icon": st.column_config.ImageColumn("Icon", width="small"),
                            "ID": st.column_config.NumberColumn("ID", format="%d"),
                            "Name": st.column_config.TextColumn("Name", width="medium"),
                            "Sailing": st.column_config.CheckboxColumn("Sailing"),
                            "Buy": st.column_config.NumberColumn("Buy Price", format="%d gp"),
                            "Sell": st.column_config.NumberColumn("Sell Price", format="%d gp"),
                            "Margin": st.column_config.NumberColumn("Margin", format="%d gp"),
                            "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%")
                        }
                    )
                    
                    st.caption(f"Found {len(data)} items matching '{search}'")
                else:
                    st.info(f"No items found matching '{search}'")
    
    with tabs[2]:
        st.header("Sailing-Specific Items")
        
        sailing_categories = {
            "Woods": [32904, 32907, 32910, 31432, 31435, 31438],
            "Hull Parts": list(HULL_PARTS.keys()) + list(LARGE_HULL_PARTS.keys()),
            "Hull Repair Kits": list(HULL_REPAIR_KITS.keys()),
            "Keel Parts": list(KEEL_PARTS.keys()) + list(LARGE_KEEL_PARTS.keys()),
            "Metals": [31716, 31719, 32889, 32892, 31996],
            "Dragon Items": [31406, 32017, 32038, 31916],
            "Ship Cannonballs": [31906, 31908, 2, 31910, 31912, 31914, 31916],
        }
        
        selected_cat = st.selectbox("Category", list(sailing_categories.keys()), key="sailing_category")
        
        item_ids = sailing_categories[selected_cat]
        
        data = []
        for item_id in item_ids:
            item_name = ALL_ITEMS.get(item_id, f"Unknown ({item_id})")
            price = prices.get(str(item_id))
            
            if price:
                margin = price['low'] - price['high']
                data.append({
                    'Icon': get_item_icon_url(item_name),
                    'ID': item_id,
                    'Name': item_name,
                    'Buy': price['high'],
                    'Sell': price['low'],
                    'Margin': margin,
                    'ROI %': (margin/price['high']*100) if price['high'] > 0 else 0,
                    'Status': True
                })
            else:
                data.append({
                    'Icon': get_item_icon_url(item_name),
                    'ID': item_id,
                    'Name': item_name,
                    'Buy': None,
                    'Sell': None,
                    'Margin': None,
                    'ROI %': None,
                    'Status': False
                })
        
        if data:
            df = pd.DataFrame(data)
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Icon": st.column_config.ImageColumn("Icon", width="small"),
                    "ID": st.column_config.NumberColumn("ID", format="%d"),
                    "Name": st.column_config.TextColumn("Name", width="medium"),
                    "Buy": st.column_config.NumberColumn("Buy Price", format="%d gp"),
                    "Sell": st.column_config.NumberColumn("Sell Price", format="%d gp"),
                    "Margin": st.column_config.NumberColumn("Margin", format="%d gp"),
                    "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                    "Status": st.column_config.CheckboxColumn("Active")
                }
            )
            
            active = sum(1 for d in data if d['Status'])
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Items with Prices", f"{active}/{len(data)}")
            with col2:
                if active > 0:
                    avg_margin = sum(d['Margin'] for d in data if d['Margin']) / active
                    st.metric("Avg Margin", format_gp(avg_margin))
    
    with tabs[3]:
        st.header("Most Profitable Chains")
        
        all_results = []
        
        with st.spinner("Calculating all chains..."):
            for category, chains in all_chains.items():
                for chain in chains:
                    result = chain.calculate(prices, config, id_lookup)
                    if "error" not in result:
                        output_name = result.get("output_item_name", chain.name)
                        all_results.append({
                            "Icon": get_item_icon_url(output_name),
                            "Category": category,
                            "Item": chain.name,
                            "Profit": result["net_profit"],
                            "Per Item": result["profit_per_item"],
                            "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                            "_profit_raw": result["net_profit"],
                            "_output_name": output_name
                        })
        
        if all_results:
            col1, col2 = st.columns(2)
            with col1:
                show_profitable_only = st.toggle("Show profitable only", value=True)
            with col2:
                top_n = st.slider("Show top N", 5, 50, 20)
            
            filtered_results = all_results
            if show_profitable_only:
                filtered_results = [r for r in all_results if r["_profit_raw"] > 0]
            
            filtered_results.sort(key=lambda x: x["_profit_raw"], reverse=True)
            top_results = filtered_results[:top_n]
            
            if top_results:
                df = pd.DataFrame(top_results)
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Icon": st.column_config.ImageColumn("Icon", width="small"),
                        "Category": st.column_config.TextColumn("Category"),
                        "Item": st.column_config.TextColumn("Item", width="medium"),
                        "Profit": st.column_config.NumberColumn("Net Profit", format="%.0f gp"),
                        "Per Item": st.column_config.NumberColumn("Per Item", format="%.1f gp"),
                        "ROI %": st.column_config.ProgressColumn("ROI %", format="%.1f%%", min_value=-100, max_value=100),
                        "_profit_raw": None,
                        "_output_name": None
                    }
                )
                
                st.subheader("Best in Each Category")
                
                category_bests = {}
                for result in all_results:
                    cat = result["Category"]
                    if result["_profit_raw"] > 0:
                        if cat not in category_bests or result["_profit_raw"] > category_bests[cat]["_profit_raw"]:
                            category_bests[cat] = result
                
                if category_bests:
                    best_data = []
                    for cat, best in category_bests.items():
                        best_data.append({
                            "Icon": best["Icon"],
                            "Category": cat,
                            "Best Item": get_clean_item_name(best['Item']),
                            "Profit": best['_profit_raw']
                        })
                    
                    best_df = pd.DataFrame(best_data)
                    best_df = best_df.sort_values("Profit", ascending=False)
                    
                    st.dataframe(
                        best_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Icon": st.column_config.ImageColumn("Icon", width="small"),
                            "Category": st.column_config.TextColumn("Category", width="medium"),
                            "Best Item": st.column_config.TextColumn("Best Item", width="large"),
                            "Profit": st.column_config.NumberColumn("Profit", format="%.0f gp")
                        }
                    )
            else:
                st.warning("No profitable chains found with current settings.")
    
    with tabs[4]:
        st.header("Profit Analytics")
        
        st.markdown("##### Analysis Filters")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            exclude_dragon = st.toggle("Exclude Dragon Items", value=True, help="Dragon items are extreme outliers")
        with filter_col2:
            use_per_item = st.toggle("Show Per-Item Profit", value=False)
        with filter_col3:
            filter_outliers = st.toggle("Filter Statistical Outliers", value=False, help="Remove values beyond 1.5x IQR")
        
        all_results_for_charts = []
        quantity = config.get("quantity", 1)
        
        for category, chains in all_chains.items():
            for chain in chains:
                if exclude_dragon and "dragon" in chain.name.lower():
                    continue
                    
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    profit = result["net_profit"]
                    if use_per_item and quantity > 0:
                        profit = profit / quantity
                    
                    all_results_for_charts.append({
                        "Category": category,
                        "Item": chain.name,
                        "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                        "_profit_raw": profit
                    })
        
        if filter_outliers and len(all_results_for_charts) > 4:
            profits = [r["_profit_raw"] for r in all_results_for_charts]
            q1 = np.percentile(profits, 25)
            q3 = np.percentile(profits, 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            original_count = len(all_results_for_charts)
            all_results_for_charts = [r for r in all_results_for_charts if lower_bound <= r["_profit_raw"] <= upper_bound]
            filtered_count = original_count - len(all_results_for_charts)
            if filtered_count > 0:
                st.caption(f"*{filtered_count} statistical outliers hidden*")
        
        if all_results_for_charts:
            profitable_results = [r for r in all_results_for_charts if r["_profit_raw"] > 0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                if profitable_results:
                    fig = create_profit_chart(profitable_results, top_n=10)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_category_comparison(all_results_for_charts)
                st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = create_roi_scatter(all_results_for_charts)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough ROI data for scatter plot")
            
            with col2:
                if profitable_results:
                    fig = create_category_pie(profitable_results)
                    st.plotly_chart(fig, use_container_width=True)
            
            profit_label = "Per-Item Profit" if use_per_item else f"Batch Profit (qty: {quantity})"
            st.subheader(f"Distribution Analysis as {profit_label}")
            profits = [r["_profit_raw"] for r in all_results_for_charts]
            fig = create_profit_histogram(profits, per_item=use_per_item)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Voyage Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Chains", len(all_results_for_charts))
            with col2:
                profitable_count = sum(1 for p in profits if p > 0)
                st.metric("Profitable", f"{profitable_count} ({profitable_count/len(profits)*100:.0f}%)")
            with col3:
                avg_profit = sum(profits) / len(profits)
                st.metric("Avg Profit", format_gp(avg_profit))
            with col4:
                max_profit = max(profits)
                st.metric("Best Profit", format_gp(max_profit))


if __name__ == "__main__":
    main()
