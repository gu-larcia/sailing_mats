"""
OSRS Sailing Materials Tracker
Version 4.0 - Enhanced Streamlit Edition
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="OSRS Sailing Tracker",
    page_icon="https://oldschool.runescape.wiki/images/Sailing_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============
#  OSRS THEME CSS
# ===============

OSRS_CSS = """
<style>
/* Import OSRS-style fonts */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* Root variables for OSRS theme */
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

/* Main app background - dark ocean theme */
.stApp {
    background: linear-gradient(180deg, #1a2a3a 0%, #0d1a24 50%, #1a2a3a 100%);
}

/* Sidebar styling - parchment look */
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

/* Main content headers */
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.stApp h1 {
    border-bottom: 3px solid var(--gold-dark);
    padding-bottom: 10px;
}

/* Tabs styling */
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

/* Metrics styling - gold coin look */
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
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'Crimson Text', serif !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border: 3px solid var(--driftwood);
    border-radius: 8px;
    overflow: hidden;
}

/* Buttons - wooden/gold style */
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

/* Form styling */
[data-testid="stForm"] {
    background: linear-gradient(180deg, rgba(139,115,85,0.2) 0%, rgba(92,77,58,0.2) 100%);
    border: 2px solid var(--driftwood);
    border-radius: 8px;
    padding: 15px;
}

/* Selectbox styling */
.stSelectbox > div > div {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
}

.stSelectbox > div > div > div {
    color: var(--driftwood-dark) !important;
}

/* Selectbox dropdown menu */
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

/* Main content selectbox text */
.stSelectbox label {
    color: var(--parchment) !important;
}

/* Toggle styling */
.stCheckbox label, .stToggle label {
    font-family: 'Crimson Text', serif !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 6px;
    color: var(--gold) !important;
}

/* Link button */
.stLinkButton > a {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--ocean) 0%, var(--ocean-dark) 100%);
    color: var(--parchment) !important;
    border: 2px solid var(--ocean-light);
}

/* Caption text */
.stCaption {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment-dark) !important;
    font-style: italic;
}

/* Spinner */
.stSpinner > div {
    border-color: var(--gold) !important;
}

/* Toast notifications */
[data-testid="stToast"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border: 2px solid var(--gold-dark);
    color: var(--driftwood-dark);
    font-family: 'Crimson Text', serif;
}

/* Divider */
hr {
    border-color: var(--driftwood) !important;
}

/* Number input in sidebar */
[data-testid="stSidebar"] input {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
    color: var(--driftwood-dark) !important;
}

/* Warning/Info boxes */
.stAlert {
    font-family: 'Crimson Text', serif;
    border-radius: 6px;
}
</style>
"""

# Apply OSRS theme
st.markdown(OSRS_CSS, unsafe_allow_html=True)

# Constants
API_BASE = "https://prices.runescape.wiki/api/v1/osrs"

# ===============
#  ITEM DATABASE
# ===============

# ALL LOGS
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
    # Sailing-specific woods
    32902: "Jatoba logs",
    32904: "Camphor logs",
    32907: "Ironwood logs",
    32910: "Rosewood logs",
}

# ALL PLANKS
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

# HULL PARTS (Regular - 5 planks each)
HULL_PARTS = {
    32041: "Wooden hull parts",
    32044: "Oak hull parts",
    32047: "Teak hull parts",
    32050: "Mahogany hull parts",
    32053: "Camphor hull parts",
    32056: "Ironwood hull parts",
    32059: "Rosewood hull parts",
}

# LARGE HULL PARTS (5 regular hull parts each = 25 planks)
LARGE_HULL_PARTS = {
    32062: "Large wooden hull parts",
    32065: "Large oak hull parts",
    32068: "Large teak hull parts",
    32071: "Large mahogany hull parts",
    32074: "Large camphor hull parts",
    32077: "Large ironwood hull parts",
    32080: "Large rosewood hull parts",
}

# HULL REPAIR KITS
HULL_REPAIR_KITS = {
    31964: "Repair kit",
    31967: "Oak repair kit",
    31970: "Teak repair kit",
    31973: "Mahogany repair kit",
    31976: "Camphor repair kit",
    31979: "Ironwood repair kit",
    31982: "Rosewood repair kit",
}

# ALL ORES
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
    # Additional ores
    1436: "Rune essence",
    1440: "Pure essence",
}

# ALL BARS
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

# KEEL PARTS (Regular - 5 bars each, except dragon)
KEEL_PARTS = {
    31999: "Bronze keel parts",
    32002: "Iron keel parts",
    32005: "Steel keel parts",
    32008: "Mithril keel parts",
    32011: "Adamant keel parts",
    32014: "Rune keel parts",
    32017: "Dragon keel parts",
}

# LARGE KEEL PARTS (5 regular each, except dragon which is 2:1)
LARGE_KEEL_PARTS = {
    32020: "Large bronze keel parts",
    32023: "Large iron keel parts",
    32026: "Large steel keel parts",
    32029: "Large mithril keel parts",
    32032: "Large adamant keel parts",
    32035: "Large rune keel parts",
    32038: "Large dragon keel parts",
}

# ALL NAILS (15 per bar via Smithing)
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

# ALL CANNONBALLS
ALL_CANNONBALLS = {
    2: "Steel cannonball",
    # Sailing cannonballs
    31906: "Bronze cannonball",
    31908: "Iron cannonball",
    31910: "Mithril cannonball",
    31912: "Adamant cannonball",
    31914: "Rune cannonball",
    31916: "Dragon cannonball",
}

# Ammo moulds
AMMO_MOULDS = {
    4: "Ammo mould",
    27012: "Double ammo mould",
}

# Processing costs by wood type
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

# Rune IDs for Plank Make
RUNE_IDS = {
    "Astral rune": 9075,
    "Nature rune": 561,
    "Earth rune": 557,
}

# Combine all items for easy lookup
ALL_ITEMS = {
    **ALL_LOGS, **ALL_PLANKS, **HULL_PARTS, **LARGE_HULL_PARTS,
    **HULL_REPAIR_KITS, **ALL_ORES, **ALL_BARS, **KEEL_PARTS,
    **LARGE_KEEL_PARTS, **ALL_NAILS, **ALL_CANNONBALLS, **AMMO_MOULDS
}


# ===============
#  API CONNECTION
# ===============

class OSRSWikiConnection:
    """Custom connection class for OSRS Wiki API"""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'OSRS-Sailing-Tracker/4.0 (Streamlit App)'
        })
    
    def fetch_mapping(self) -> Dict:
        """Fetch item mappings"""
        response = self._session.get(f"{self.base_url}/mapping")
        response.raise_for_status()
        items = response.json()
        return {item['id']: item for item in items}
    
    def fetch_prices(self) -> Dict:
        """Fetch latest prices"""
        response = self._session.get(f"{self.base_url}/latest")
        response.raise_for_status()
        return response.json().get('data', {})


@st.cache_resource
def get_api_connection() -> OSRSWikiConnection:
    """Get cached API connection instance"""
    return OSRSWikiConnection()


@st.cache_data(ttl=300, show_spinner=False)
def fetch_item_mapping(_conn: OSRSWikiConnection) -> Dict:
    """Fetch all item mappings with caching"""
    return _conn.fetch_mapping()


@st.cache_data(ttl=60, show_spinner=False)
def fetch_latest_prices(_conn: OSRSWikiConnection) -> Dict:
    """Fetch latest prices with caching"""
    return _conn.fetch_prices()


# ===============
#  ITEM LOOKUP
# ===============

@st.cache_resource
def get_id_lookup(_item_mapping_hash: str, item_mapping: Dict) -> 'ItemIDLookup':
    """Get cached ItemIDLookup instance"""
    return ItemIDLookup(item_mapping)


class ItemIDLookup:
    """Dynamic item ID lookup system"""
    
    def __init__(self, item_mapping: Dict):
        self.item_mapping = item_mapping
        self.name_to_id_cache = {}
        
        for item_id, item_data in item_mapping.items():
            if isinstance(item_data, dict) and 'name' in item_data:
                self.name_to_id_cache[item_data['name'].lower()] = item_id
    
    def find_id_by_name(self, item_name: str) -> Optional[int]:
        """Find item ID by searching for name"""
        search_name = item_name.lower()
        
        if search_name in self.name_to_id_cache:
            return self.name_to_id_cache[search_name]
        
        for name, item_id in self.name_to_id_cache.items():
            if search_name in name or name in search_name:
                return item_id
        
        return None
    
    def get_or_find_id(self, item_id: Optional[int], item_name: str) -> Optional[int]:
        """Get existing ID or find it by name"""
        if item_id:
            return item_id
        
        found_id = self.find_id_by_name(item_name)
        if found_id:
            ALL_ITEMS[found_id] = item_name
        return found_id


# ===============
#  PROCESSING CHAINS
# ===============

@dataclass
class ChainStep:
    """Single step in processing chain"""
    item_id: Optional[int]
    item_name: str
    quantity: float = 1
    is_self_obtained: bool = False
    processing_method: Optional[str] = None
    custom_cost: Optional[float] = None


@dataclass
class ProcessingChain:
    """Complete processing chain"""
    name: str
    category: str
    steps: List[ChainStep] = field(default_factory=list)
    special_ratio: Optional[Dict] = field(default_factory=dict)
    
    def calculate(self, prices: Dict, config: Dict, id_lookup: ItemIDLookup) -> Dict:
        """Calculate chain profitability"""
        
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
            "missing_prices": []
        }
        
        if not self.steps:
            results["error"] = "No steps in chain"
            return results
        
        final_quantity = config.get("quantity", 1)
        
        if self.special_ratio and "dragon" in self.name.lower():
            ratio = self.special_ratio.get("conversion_ratio", 5)
        else:
            ratio = 5
        
        if self.category == "Cannonballs" and len(self.steps) >= 2:
            input_step = self.steps[0]
            output_step = self.steps[-1]

            if config.get("double_ammo_mould", False):
                if output_step.item_name.endswith("cannonball"):
                    output_step.quantity = 8
                    input_step.quantity = 2
            else:
                if output_step.item_name.endswith("cannonball"):
                    output_step.quantity = 4
                    input_step.quantity = 1
        
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
                unit_price = price_data.get("high", 0) if price_data and not step.is_self_obtained else 0
                total_value = unit_price * step_qty

                if is_input:
                    results["raw_material_cost"] = total_value

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
                "is_self_obtained": step.is_self_obtained,
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
        """Calculate processing cost for a step"""
        
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
    """Generate all systematic processing chains"""
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
    
    # PLANK CHAINS
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
    
    # HULL PARTS CHAINS
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
    
    # LARGE HULL PARTS
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
    
    # KEEL PARTS (5 bars each, except dragon which needs 2 sheets)
    keel_mappings = [
        (2349, "Bronze bar", 31999, "Bronze keel parts", 5),
        (2351, "Iron bar", 32002, "Iron keel parts", 5),
        (2353, "Steel bar", 32005, "Steel keel parts", 5),
        (2359, "Mithril bar", 32008, "Mithril keel parts", 5),
        (2361, "Adamantite bar", 32011, "Adamant keel parts", 5),
        (2363, "Runite bar", 32014, "Rune keel parts", 5),
        (31996, "Dragon metal sheet", 32017, "Dragon keel parts", 2),  # 2 sheets per 1 keel part
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
    
    # LARGE KEEL PARTS
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
    
    # NAIL CHAINS
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
    
    # CANNONBALL CHAINS
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


# ===============
#  UTILITIES
# ===============

def format_gp(value: float) -> str:
    """Format GP values"""
    if value == float('inf'):
        return "∞"
    
    is_negative = value < 0
    value = abs(value)
    
    if value >= 1_000_000:
        formatted = f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        formatted = f"{value/1_000:.1f}K"
    else:
        formatted = f"{int(value):,}"
    
    return f"-{formatted}" if is_negative else formatted


def create_profit_chart(results: List[Dict], top_n: int = 10) -> go.Figure:
    """Create a bar chart of top profits with OSRS theming"""
    sorted_results = sorted(results, key=lambda x: x.get("_profit_raw", 0), reverse=True)[:top_n]
    
    items = [r["Item"] for r in sorted_results]
    profits = [r["_profit_raw"] for r in sorted_results]
    
    # OSRS-themed colors: gold for profit, dragon red for loss
    colors = ['#d4af37' if p > 0 else '#c0392b' for p in profits]
    
    fig = go.Figure(data=[
        go.Bar(
            x=profits,
            y=items,
            orientation='h',
            marker_color=colors,
            marker_line_color='#5c4d3a',
            marker_line_width=2,
            text=[format_gp(p) for p in profits],
            textposition='outside',
            textfont=dict(color='#f4e4bc', size=12)
        )
    ])
    
    fig.update_layout(
        title="Top Profitable Chains",
        title_font_color='#ffd700',
        title_font_size=18,
        xaxis_title="Net Profit (GP)",
        xaxis_title_font_color='#f4e4bc',
        xaxis_tickfont_color='#f4e4bc',
        xaxis_gridcolor='rgba(139,115,85,0.3)',
        yaxis_title="",
        yaxis_tickfont_color='#f4e4bc',
        yaxis_autorange="reversed",
        height=400,
        margin=dict(l=200, r=80, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False
    )
    
    return fig


def create_category_pie(results: List[Dict]) -> go.Figure:
    """Create a pie chart of profits by category with OSRS theming"""
    category_profits = {}
    for r in results:
        cat = r.get("Category", "Unknown")
        profit = max(0, r.get("_profit_raw", 0))
        category_profits[cat] = category_profits.get(cat, 0) + profit
    
    # Sort by profit and separate small slices
    sorted_cats = sorted(category_profits.items(), key=lambda x: x[1], reverse=True)
    total_profit = sum(category_profits.values())
    
    # Group categories under 2% into "Other"
    main_cats = []
    other_total = 0
    threshold = total_profit * 0.02
    
    for cat, profit in sorted_cats:
        if profit >= threshold:
            main_cats.append((cat, profit))
        else:
            other_total += profit
    
    if other_total > 0:
        main_cats.append(("Other", other_total))
    
    labels = [c[0] for c in main_cats]
    values = [c[1] for c in main_cats]
    
    # OSRS-themed color palette
    osrs_colors = [
        '#d4af37',  # Gold
        '#cd7f32',  # Bronze
        '#5dade2',  # Rune blue
        '#c0392b',  # Dragon red
        '#27ae60',  # Nature green
        '#8e44ad',  # Magic purple
        '#f39c12',  # Orange/copper
        '#1abc9c',  # Teal
        '#7f8c8d',  # Gray (for Other)
    ]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(color='#f4e4bc', size=12),
            marker=dict(
                colors=osrs_colors[:len(labels)],
                line=dict(color='#5c4d3a', width=2)
            ),
            pull=[0.05 if i == 0 else 0 for i in range(len(labels))]  # Pull out largest slice slightly
        )
    ])
    
    fig.update_layout(
        title="Profit by Category",
        title_font_color='#ffd700',
        title_font_size=18,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        legend_font_color='#f4e4bc',
        legend_bgcolor='rgba(92,77,58,0.5)',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=20, r=120, t=50, b=20)
    )
    
    return fig


def create_profit_histogram(profits: List[float]) -> go.Figure:
    """Create a histogram of profit distribution"""
    fig = go.Figure(data=[
        go.Histogram(
            x=profits,
            nbinsx=30,
            marker_color='#d4af37',
            marker_line_color='#5c4d3a',
            marker_line_width=1
        )
    ])
    
    fig.update_layout(
        title="Profit Distribution",
        title_font_color='#ffd700',
        title_font_size=18,
        xaxis_title="Net Profit (GP)",
        xaxis_title_font_color='#f4e4bc',
        xaxis_tickfont_color='#f4e4bc',
        xaxis_gridcolor='rgba(139,115,85,0.3)',
        yaxis_title="Number of Chains",
        yaxis_title_font_color='#f4e4bc',
        yaxis_tickfont_color='#f4e4bc',
        yaxis_gridcolor='rgba(139,115,85,0.3)',
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)'
    )
    
    return fig


def create_category_comparison(results: List[Dict]) -> go.Figure:
    """Create a grouped bar chart comparing categories"""
    category_stats = {}
    for r in results:
        cat = r.get("Category", "Unknown")
        profit = r.get("_profit_raw", 0)
        if cat not in category_stats:
            category_stats[cat] = {"profits": [], "count": 0}
        category_stats[cat]["profits"].append(profit)
        category_stats[cat]["count"] += 1
    
    categories = list(category_stats.keys())
    avg_profits = [sum(category_stats[c]["profits"]) / len(category_stats[c]["profits"]) for c in categories]
    max_profits = [max(category_stats[c]["profits"]) for c in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Average Profit',
        x=categories,
        y=avg_profits,
        marker_color='#5dade2',
        marker_line_color='#5c4d3a',
        marker_line_width=2
    ))
    
    fig.add_trace(go.Bar(
        name='Best Profit',
        x=categories,
        y=max_profits,
        marker_color='#d4af37',
        marker_line_color='#5c4d3a',
        marker_line_width=2
    ))
    
    fig.update_layout(
        title="Category Comparison",
        title_font_color='#ffd700',
        title_font_size=18,
        xaxis_title="",
        xaxis_tickfont_color='#f4e4bc',
        xaxis_tickangle=45,
        yaxis_title="Profit (GP)",
        yaxis_title_font_color='#f4e4bc',
        yaxis_tickfont_color='#f4e4bc',
        yaxis_gridcolor='rgba(139,115,85,0.3)',
        barmode='group',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        legend_font_color='#f4e4bc',
        legend_bgcolor='rgba(92,77,58,0.5)'
    )
    
    return fig


def create_roi_scatter(results: List[Dict]) -> go.Figure:
    """Create a scatter plot of ROI vs Profit"""
    data = [r for r in results if r.get("ROI %") is not None and r.get("ROI %") != float('inf')]
    
    if not data:
        return None
    
    profits = [r["_profit_raw"] for r in data]
    rois = [r["ROI %"] for r in data]
    names = [r["Item"] for r in data]
    categories = [r.get("Category", "Unknown") for r in data]
    
    # Color by category
    unique_cats = list(set(categories))
    osrs_colors = ['#d4af37', '#cd7f32', '#5dade2', '#c0392b', '#27ae60', '#8e44ad', '#f39c12', '#1abc9c']
    cat_colors = {cat: osrs_colors[i % len(osrs_colors)] for i, cat in enumerate(unique_cats)}
    colors = [cat_colors[c] for c in categories]
    
    fig = go.Figure(data=[
        go.Scatter(
            x=profits,
            y=rois,
            mode='markers',
            marker=dict(
                size=12,
                color=colors,
                line=dict(color='#5c4d3a', width=1)
            ),
            text=names,
            hovertemplate='<b>%{text}</b><br>Profit: %{x:,.0f} GP<br>ROI: %{y:.1f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="ROI vs Profit Analysis",
        title_font_color='#ffd700',
        title_font_size=18,
        xaxis_title="Net Profit (GP)",
        xaxis_title_font_color='#f4e4bc',
        xaxis_tickfont_color='#f4e4bc',
        xaxis_gridcolor='rgba(139,115,85,0.3)',
        yaxis_title="ROI (%)",
        yaxis_title_font_color='#f4e4bc',
        yaxis_tickfont_color='#f4e4bc',
        yaxis_gridcolor='rgba(139,115,85,0.3)',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)'
    )
    
    return fig


# ===============
#  MAIN APP
# ===============

def main():
    # Header with OSRS styling
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
    
    # Initialize connection and load data
    conn = get_api_connection()
    
    with st.spinner("Loading market data..."):
        item_mapping = fetch_item_mapping(conn)
        prices = fetch_latest_prices(conn)
        mapping_hash = str(hash(frozenset(item_mapping.keys())))
        id_lookup = get_id_lookup(mapping_hash, item_mapping)
        all_chains = generate_all_chains()
    
    # Sync with URL parameters
    params = st.query_params
    
    # Sidebar configuration with form
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
            
            use_double_mould = st.toggle(
                "Double Ammo Mould",
                value=params.get("double_mould", "false") == "true",
                help="Makes 8 cannonballs per 2 bars (requires 2,000 Foundry rep)"
            )
            
            ancient_furnace = st.toggle(
                "Ancient Furnace",
                value=params.get("ancient_furnace", "false") == "true",
                help="Halves smithing time (87 Sailing req)"
            )
            
            st.divider()
            
            quantity = st.number_input(
                "Calculate for quantity:",
                min_value=1,
                max_value=100000,
                value=int(params.get("quantity", 100)),
                step=10
            )
            
            submitted = st.form_submit_button("Apply Settings", use_container_width=True)
            
            if submitted:
                st.query_params["plank_method"] = plank_method
                st.query_params["double_mould"] = str(use_double_mould).lower()
                st.query_params["ancient_furnace"] = str(ancient_furnace).lower()
                st.query_params["quantity"] = str(quantity)
                st.toast("Settings applied!")
        
        st.divider()
        
        # Stats display
        with st.container():
            st.subheader("Stats")
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                st.metric("Items", len(ALL_ITEMS))
            with stat_col2:
                st.metric("Prices", len(prices))
        
        # Refresh button
        if st.button("Refresh Prices", use_container_width=True):
            st.cache_data.clear()
            st.toast("Prices refreshed!")
            st.rerun()
        
        # Last update time
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Prepare config
    use_earth_staff = "Earth Staff" in plank_method
    config = {
        "quantity": quantity,
        "use_earth_staff": use_earth_staff,
        "double_ammo_mould": use_double_mould,
        "ancient_furnace": ancient_furnace
    }
    
    # Main tabs
    tabs = st.tabs([
        "All Chains", 
        "Search Items", 
        "Sailing Items",
        "Best Profits",
        "Analytics"
    ])
    
    # Tab 1: All Processing Chains
    with tabs[0]:
        st.header("All Processing Chains")
        
        category = st.selectbox(
            "Select Category",
            list(all_chains.keys()),
            key="chain_category"
        )
        
        chains = all_chains[category]
        
        if chains:
            results = []
            for chain in chains:
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    profit = result["net_profit"]
                    results.append({
                        "Item": chain.name,
                        "Input Cost": result["raw_material_cost"],
                        "Process Cost": result["processing_costs"],
                        "Total Cost": result["total_input_cost"],
                        "Output": result["output_value"],
                        "Tax": result["ge_tax"],
                        "Net Profit": profit,
                        "Per Item": result["profit_per_item"],
                        "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                        "_profit_raw": profit,
                        "_profitable": profit > 0
                    })
            
            if results:
                df = pd.DataFrame(results)
                df = df.sort_values("_profit_raw", ascending=False)
                
                # Display with enhanced column config
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Item": st.column_config.TextColumn("Item", width="medium"),
                        "Input Cost": st.column_config.NumberColumn(
                            "Input Cost",
                            format="%.0f gp"
                        ),
                        "Process Cost": st.column_config.NumberColumn(
                            "Process Cost",
                            format="%.0f gp"
                        ),
                        "Total Cost": st.column_config.NumberColumn(
                            "Total Cost",
                            format="%.0f gp"
                        ),
                        "Output": st.column_config.NumberColumn(
                            "Output Value",
                            format="%.0f gp"
                        ),
                        "Tax": st.column_config.NumberColumn(
                            "GE Tax",
                            format="%.0f gp"
                        ),
                        "Net Profit": st.column_config.NumberColumn(
                            "Net Profit",
                            format="%.0f gp",
                            help="Profit after all costs and GE tax"
                        ),
                        "Per Item": st.column_config.NumberColumn(
                            "Per Item",
                            format="%.1f gp"
                        ),
                        "ROI %": st.column_config.ProgressColumn(
                            "ROI %",
                            format="%.1f%%",
                            min_value=-100,
                            max_value=100,
                            help="Return on Investment percentage"
                        ),
                        "_profit_raw": None,
                        "_profitable": None
                    }
                )
                
                # Summary metrics
                profitable = sum(1 for r in results if r["_profit_raw"] > 0)
                best_profit = max(results, key=lambda x: x["_profit_raw"])
                total_profit = sum(r["_profit_raw"] for r in results if r["_profit_raw"] > 0)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        "Profitable Chains",
                        f"{profitable}/{len(results)}",
                        delta=f"{(profitable/len(results)*100):.0f}%"
                    )
                with col2:
                    st.metric("Best Item", best_profit["Item"])
                with col3:
                    st.metric(
                        "Best Profit",
                        format_gp(best_profit["Net Profit"]),
                        delta="per batch"
                    )
                with col4:
                    st.metric("Total Potential", format_gp(total_profit))
                
                # Expandable details
                with st.expander("View Chain Details", expanded=False):
                    selected_item = st.selectbox(
                        "Select item for details",
                        [r["Item"] for r in results]
                    )
                    
                    # Find the chain
                    for chain in chains:
                        if chain.name == selected_item:
                            result = chain.calculate(prices, config, id_lookup)
                            
                            st.subheader(f"Chain: {chain.name}")
                            
                            for i, step in enumerate(result["steps"]):
                                step_type = step["step_type"]
                                icon = "[OUT]" if step_type == "Output" else ("[IN]" if step_type == "Input" else "[...]")
                                
                                st.markdown(f"""
                                **{icon} Step {i+1}: {step['name']}**
                                - Quantity: {step['quantity']:,.0f}
                                - Unit Price: {format_gp(step['unit_price'])}
                                - Total Value: {format_gp(step['total_value'])}
                                - Processing: {step['processing_notes'] or 'None'}
                                """)
                            
                            if result["missing_prices"]:
                                st.warning(f"Missing prices for: {', '.join(result['missing_prices'])}")
                            break
    
    # Tab 2: Item Search
    with tabs[1]:
        st.header("Item Database Search")
        
        search = st.text_input(
            "Search items by name:",
            placeholder="Try 'rosewood', 'dragon', or 'hull'...",
            key="item_search"
        )
        
        if search:
            with st.spinner("Searching..."):
                local_matches = [
                    (id, name) for id, name in ALL_ITEMS.items()
                    if search.lower() in name.lower()
                ]
                
                api_matches = [
                    (id, item['name']) for id, item in item_mapping.items()
                    if search.lower() in item['name'].lower()
                ][:50]
                
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
                            "ID": st.column_config.NumberColumn("ID", format="%d"),
                            "Name": st.column_config.TextColumn("Name", width="medium"),
                            "Sailing": st.column_config.CheckboxColumn("Sailing", help="Sailing item"),
                            "Buy": st.column_config.NumberColumn("Buy Price", format="%d gp"),
                            "Sell": st.column_config.NumberColumn("Sell Price", format="%d gp"),
                            "Margin": st.column_config.NumberColumn("Margin", format="%d gp"),
                            "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%")
                        }
                    )
                    
                    st.caption(f"Found {len(data)} items matching '{search}'")
                else:
                    st.info(f"No items found matching '{search}'")
    
    # Tab 3: Sailing-specific items
    with tabs[2]:
        st.header("Sailing-Specific Items")
        
        sailing_categories = {
            "New Woods": [32902, 32904, 32907, 32910, 31432, 31435, 31438],
            "Hull Parts": list(HULL_PARTS.keys()) + list(LARGE_HULL_PARTS.keys()),
            "Hull Repair Kits": list(HULL_REPAIR_KITS.keys()),
            "Keel Parts": list(KEEL_PARTS.keys()) + list(LARGE_KEEL_PARTS.keys()),
            "New Metals": [31716, 31719, 32889, 32892, 31996],
            "Dragon Items": [31406, 32017, 32038, 31916],
            "Ship Cannonballs": [31906, 31908, 31910, 31912, 31914, 31916],
        }
        
        selected_cat = st.selectbox(
            "Category",
            list(sailing_categories.keys()),
            key="sailing_category"
        )
        
        item_ids = sailing_categories[selected_cat]
        
        data = []
        for item_id in item_ids:
            item_name = ALL_ITEMS.get(item_id, f"Unknown ({item_id})")
            price = prices.get(str(item_id))
            
            if price:
                margin = price['low'] - price['high']
                data.append({
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
                    "ID": st.column_config.NumberColumn("ID", format="%d"),
                    "Name": st.column_config.TextColumn("Name", width="medium"),
                    "Buy": st.column_config.NumberColumn("Buy Price", format="%d gp"),
                    "Sell": st.column_config.NumberColumn("Sell Price", format="%d gp"),
                    "Margin": st.column_config.NumberColumn("Margin", format="%d gp"),
                    "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                    "Status": st.column_config.CheckboxColumn("Active", help="Has GE prices")
                }
            )
            
            # Category stats
            active = sum(1 for d in data if d['Status'])
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Items with Prices", f"{active}/{len(data)}")
            with col2:
                if active > 0:
                    avg_margin = sum(d['Margin'] for d in data if d['Margin']) / active
                    st.metric("Avg Margin", format_gp(avg_margin))
    
    # Tab 4: Best Profits
    with tabs[3]:
        st.header("Most Profitable Chains")
        
        all_results = []
        
        with st.spinner("Calculating all chains..."):
            for category, chains in all_chains.items():
                for chain in chains:
                    result = chain.calculate(prices, config, id_lookup)
                    if "error" not in result:
                        all_results.append({
                            "Category": category,
                            "Item": chain.name,
                            "Profit": result["net_profit"],
                            "Per Item": result["profit_per_item"],
                            "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                            "_profit_raw": result["net_profit"]
                        })
        
        if all_results:
            # Filter controls
            col1, col2 = st.columns(2)
            with col1:
                show_profitable_only = st.toggle("Show profitable only", value=True)
            with col2:
                top_n = st.slider("Show top N", 5, 50, 20)
            
            filtered_results = all_results
            if show_profitable_only:
                filtered_results = [r for r in all_results if r["_profit_raw"] > 0]
            
            # Sort and limit
            filtered_results.sort(key=lambda x: x["_profit_raw"], reverse=True)
            top_results = filtered_results[:top_n]
            
            if top_results:
                df = pd.DataFrame(top_results)
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Category": st.column_config.TextColumn("Category"),
                        "Item": st.column_config.TextColumn("Item", width="medium"),
                        "Profit": st.column_config.NumberColumn(
                            "Net Profit",
                            format="%.0f gp"
                        ),
                        "Per Item": st.column_config.NumberColumn(
                            "Per Item",
                            format="%.1f gp"
                        ),
                        "ROI %": st.column_config.ProgressColumn(
                            "ROI %",
                            format="%.1f%%",
                            min_value=-100,
                            max_value=100
                        ),
                        "_profit_raw": None
                    }
                )
                
                # Best by category
                st.subheader("Best in Each Category")
                
                category_bests = {}
                for result in all_results:
                    cat = result["Category"]
                    if result["_profit_raw"] > 0:
                        if cat not in category_bests or result["_profit_raw"] > category_bests[cat]["_profit_raw"]:
                            category_bests[cat] = result
                
                if category_bests:
                    # Use a cleaner table format instead of cramped metrics
                    best_data = []
                    for cat, best in category_bests.items():
                        best_data.append({
                            "Category": cat,
                            "Best Item": best['Item'].replace(' processing', '').replace(' smithing', ''),
                            "Profit": best['_profit_raw']
                        })
                    
                    best_df = pd.DataFrame(best_data)
                    best_df = best_df.sort_values("Profit", ascending=False)
                    
                    st.dataframe(
                        best_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Category": st.column_config.TextColumn("Category", width="medium"),
                            "Best Item": st.column_config.TextColumn("Best Item", width="large"),
                            "Profit": st.column_config.NumberColumn("Profit", format="%.0f gp")
                        }
                    )
            else:
                st.warning("No profitable chains found with current settings.")
    
    # Tab 5: Analytics
    with tabs[4]:
        st.header("Profit Analytics")
        
        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            exclude_dragon = st.toggle(
                "Exclude Dragon Items",
                value=False,
                help="Dragon items are outliers with very high profits - exclude them to see other trends more clearly"
            )
        
        # Calculate all for charts
        all_results_for_charts = []
        for category, chains in all_chains.items():
            for chain in chains:
                # Skip dragon items if filter is on
                if exclude_dragon and "dragon" in chain.name.lower():
                    continue
                    
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    all_results_for_charts.append({
                        "Category": category,
                        "Item": chain.name,
                        "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                        "_profit_raw": result["net_profit"]
                    })
        
        if all_results_for_charts:
            profitable_results = [r for r in all_results_for_charts if r["_profit_raw"] > 0]
            
            # Row 1: Top profits and category comparison (better use of space)
            col1, col2 = st.columns(2)
            
            with col1:
                if profitable_results:
                    fig = create_profit_chart(profitable_results, top_n=10)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = create_category_comparison(all_results_for_charts)
                st.plotly_chart(fig, use_container_width=True)
            
            # Row 2: ROI scatter and pie chart
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
            
            # Row 3: Profit distribution histogram
            st.subheader("Distribution Analysis")
            profits = [r["_profit_raw"] for r in all_results_for_charts]
            fig = create_profit_histogram(profits)
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary stats
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
