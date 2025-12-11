"""
OSRS Sailing Materials Tracker
Version 3.0
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import json
from dataclasses import dataclass, field
import time

# Page config
st.set_page_config(
    page_title="OSRS Sailing Tracker",
    page_icon="⚓",
    layout="wide"
)

# Constants
API_BASE = "https://prices.runescape.wiki/api/v1/osrs"

# ===============
#  ITEM DATABASE
# ===============

# ALL LOGS (including new Sailing woods)
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
    32902: "Jatoba logs",  # Quest item only, cannot be planked
    32904: "Camphor logs",
    32907: "Ironwood logs",
    32910: "Rosewood logs",
}

# ALL PLANKS (including Sailing planks)
ALL_PLANKS = {
    960: "Plank",
    8778: "Oak plank",
    8780: "Teak plank",
    8782: "Mahogany plank",
    19787: "Redwood plank",
    # Sailing planks
    31432: "Camphor plank",
    31435: "Ironwood plank",
    31438: "Rosewood plank",
    # Note: No Jatoba plank exists
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
    32017: "Dragon keel parts",  # Drop only
}

# LARGE KEEL PARTS (5 regular each, except dragon which is 2:1)
LARGE_KEEL_PARTS = {
    32020: "Large bronze keel parts",
    32023: "Large iron keel parts",
    32026: "Large steel keel parts",
    32029: "Large mithril keel parts",
    32032: "Large adamant keel parts",
    32035: "Large rune keel parts",
    32038: "Large dragon keel parts",  # Only needs 2 regular dragon keel parts
}

# ALL NAILS (15 per bar via Smithing)
ALL_NAILS = {
    4819: "Bronze nails",
    4820: "Iron nails",
    4821: "Black nails",  # Drop only
    1539: "Steel nails",
    4822: "Mithril nails",
    4823: "Adamantite nails",
    4824: "Rune nails",
    31406: "Dragon nails",  # 92 Smithing, Dragon Forge only
}

# ALL CANNONBALLS
ALL_CANNONBALLS = {
    2: "Steel cannonball",
    21728: "Granite cannonball",
    # Sailing cannonballs
    31906: "Bronze cannonball",
    31908: "Iron cannonball",
    31910: "Mithril cannonball",
    31912: "Adamant cannonball",
    31914: "Rune cannonball",
    31916: "Dragon cannonball",  # Drop only
}

# Ammo moulds
AMMO_MOULDS = {
    4: "Ammo mould",  # 1 bar → 4 cannonballs
    27012: "Double ammo mould",  # 2 bars → 8 cannonballs (2x speed)
}

# Processing costs by wood type
SAWMILL_COSTS = {
    "Plank": 100,
    "Oak plank": 250,
    "Teak plank": 500,
    "Mahogany plank": 1500,
    "Redwood plank": 2000,
    "Camphor plank": 2500,
    "Ironwood plank": 5000,
    "Rosewood plank": 7500,
}

PLANK_MAKE_COSTS = {
    "Plank": 70,
    "Oak plank": 175,
    "Teak plank": 350,
    "Mahogany plank": 1050,
    "Redwood plank": 1400,
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

class ItemIDLookup:
    """Dynamic item ID lookup system"""
    
    def __init__(self, item_mapping: Dict):
        self.item_mapping = item_mapping
        self.name_to_id_cache = {}
        
        # Reverse lookup
        for item_id, item_data in item_mapping.items():
            if isinstance(item_data, dict) and 'name' in item_data:
                self.name_to_id_cache[item_data['name'].lower()] = item_id
    
    def find_id_by_name(self, item_name: str) -> Optional[int]:
        """Find item ID by searching for name"""
        search_name = item_name.lower()
        
        # Direct match
        if search_name in self.name_to_id_cache:
            return self.name_to_id_cache[search_name]
        
        # Partial match
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
            st.info(f"Auto-discovered ID for '{item_name}': {found_id}")
            # Update our database
            ALL_ITEMS[found_id] = item_name
        return found_id

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
    special_ratio: Optional[Dict] = field(default_factory=dict)  # For dragon keel 2:1 ratio etc
    
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
        
        # Handle special ratios (e.g., dragon keel parts 2:1 instead of 5:1)
        if self.special_ratio and "dragon" in self.name.lower():
            ratio = self.special_ratio.get("conversion_ratio", 5)
        else:
            ratio = 5  # Default ratio for most items
        
        # Handle double ammo mould for cannonballs
        if self.category == "Cannonballs" and len(self.steps) >= 2:
            if config.get("double_ammo_mould", False):
                # Double ammo mould makes 8 cannonballs from 1 bar
                if self.steps[-1].item_name.endswith("cannonball"):
                    self.steps[-1].quantity = 8
            else:
                # Regular mould makes 4 cannonballs from 1 bar
                if self.steps[-1].item_name.endswith("cannonball"):
                    self.steps[-1].quantity = 4
        
        current_multiplier = final_quantity
        
        # Process each step
        for i, step in enumerate(self.steps):
            # Try to resolve item ID if missing
            resolved_id = id_lookup.get_or_find_id(step.item_id, step.item_name)
            
            if not resolved_id:
                results["missing_prices"].append(step.item_name)
                continue
            
            price_data = prices.get(str(resolved_id), {})
            
            if not price_data:
                results["missing_prices"].append(step.item_name)
            
            # Calculate quantity needed
            step_qty = current_multiplier * step.quantity
            
            # Determine step type
            is_output = (i == len(self.steps) - 1)
            is_input = (i == 0)
            
            # Get price
            if is_output:
                unit_price = price_data.get("low", 0) if price_data else 0
                total_value = unit_price * step_qty
                results["output_value"] = total_value
            else:
                unit_price = price_data.get("high", 0) if price_data and not step.is_self_obtained else 0
                total_value = unit_price * step_qty
                
                if is_input:
                    results["raw_material_cost"] = total_value
            
            # Calculate processing cost
            processing_cost = 0
            process_notes = ""
            
            if step.processing_method:
                processing_cost, process_notes = self._calculate_processing_cost(
                    step, step_qty, prices, config, id_lookup
                )
                results["processing_costs"] += processing_cost
            
            # Add to breakdown
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
            
            # Update multiplier
            if not is_output:
                current_multiplier = step_qty
        
        # Calculate totals
        results["total_input_cost"] = results["raw_material_cost"] + results["processing_costs"]
        
        # GE Tax (2%, max 5M)
        if results["output_value"] >= 50:
            results["ge_tax"] = min(results["output_value"] * 0.02, 5_000_000)
        
        results["net_profit"] = results["output_value"] - results["total_input_cost"] - results["ge_tax"]
        results["profit_per_item"] = results["net_profit"] / final_quantity if final_quantity > 0 else 0
        
        # ROI
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
                
                # Add rune costs
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
    
    # PLANK CHAINS (Log → Plank)
    plank_mappings = [
        (1511, "Logs", 960, "Plank"),
        (1521, "Oak logs", 8778, "Oak plank"),
        (6333, "Teak logs", 8780, "Teak plank"),
        (6332, "Mahogany logs", 8782, "Mahogany plank"),
        (19669, "Redwood logs", 19787, "Redwood plank"),
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
    
    # HULL PARTS CHAINS (5 Planks → 1 Hull Part)
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
    
    # LARGE HULL PARTS (5 Hull Parts → 1 Large)
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
            ChainStep(hull_id, hull_name, 5),  # 5 regular per large
            ChainStep(large_id, large_name, 1)
        ]
        chains["Large Hull Parts"].append(chain)
    
    # KEEL PARTS (5 Bars → 1 Keel Part, except dragon)
    keel_mappings = [
        (2349, "Bronze bar", 31999, "Bronze keel parts", 5),
        (2351, "Iron bar", 32002, "Iron keel parts", 5),
        (2353, "Steel bar", 32005, "Steel keel parts", 5),
        (2359, "Mithril bar", 32008, "Mithril keel parts", 5),
        (2361, "Adamantite bar", 32011, "Adamant keel parts", 5),
        (2363, "Runite bar", 32014, "Rune keel parts", 5),
        (31996, "Dragon metal sheet", 32017, "Dragon keel parts", 1),  # Special case
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
    
    # LARGE KEEL PARTS (5 Regular → 1 Large, except dragon 2:1)
    large_keel_mappings = [
        (31999, "Bronze keel parts", 32020, "Large bronze keel parts", 5),
        (32002, "Iron keel parts", 32023, "Large iron keel parts", 5),
        (32005, "Steel keel parts", 32026, "Large steel keel parts", 5),
        (32008, "Mithril keel parts", 32029, "Large mithril keel parts", 5),
        (32011, "Adamant keel parts", 32032, "Large adamant keel parts", 5),
        (32014, "Rune keel parts", 32035, "Large rune keel parts", 5),
        (32017, "Dragon keel parts", 32038, "Large dragon keel parts", 2),  # Special 2:1 ratio
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
    
    # NAIL CHAINS (1 Bar → 15 Nails)
    nail_mappings = [
        (2349, "Bronze bar", 4819, "Bronze nails"),
        (2351, "Iron bar", 4820, "Iron nails"),
        (2353, "Steel bar", 1539, "Steel nails"),
        (2359, "Mithril bar", 4822, "Mithril nails"),
        (2361, "Adamantite bar", 4823, "Adamantite nails"),
        (2363, "Runite bar", 4824, "Rune nails"),
        (31996, "Dragon metal sheet", 31406, "Dragon nails"),  # Dragon Forge only
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
        # Regular mould version
        chain = ProcessingChain(
            name=f"{ball_name} (Regular)",
            category="Cannonballs"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(ball_id, ball_name, 4)  # 4 per bar with regular mould
        ]
        chains["Cannonballs"].append(chain)
        
        # Double mould version
        chain_double = ProcessingChain(
            name=f"{ball_name} (Double)",
            category="Cannonballs"
        )
        chain_double.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(ball_id, ball_name, 8)  # 8 per bar with double mould
        ]
        chains["Cannonballs"].append(chain_double)
    
    # Granite cannonballs (special case)
    granite_chain = ProcessingChain(
        name="Granite cannonballs",
        category="Cannonballs"
    )
    granite_chain.steps = [
        ChainStep(2, "Steel cannonball", 1),
        ChainStep(21952, "Granite dust", 1),
        ChainStep(21728, "Granite cannonball", 1)
    ]
    chains["Cannonballs"].append(granite_chain)
    
    return chains

class OSRSApiClient:
    """Client for OSRS Wiki API"""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def fetch_item_mapping():
        """Fetch all item mappings"""
        try:
            response = requests.get(f"{API_BASE}/mapping")
            response.raise_for_status()
            items = response.json()
            return {item['id']: item for item in items}
        except Exception as e:
            st.error(f"Failed to fetch items: {e}")
            return {}
    
    @staticmethod
    @st.cache_data(ttl=60)
    def fetch_latest_prices():
        """Fetch latest prices"""
        try:
            response = requests.get(f"{API_BASE}/latest")
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except Exception as e:
            st.error(f"Failed to fetch prices: {e}")
            return {}

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

def main():
    st.title("⚓ OSRS Sailing Materials Tracker")
    st.caption("For the crafty sailor!")
    
    # Initialize session state
    if 'all_chains' not in st.session_state:
        st.session_state.all_chains = generate_all_chains()
    
    # Load data
    with st.spinner("Loading prices..."):
        item_mapping = OSRSApiClient.fetch_item_mapping()
        prices = OSRSApiClient.fetch_latest_prices()
        id_lookup = ItemIDLookup(item_mapping)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("Processing Options")
        
        plank_method = st.selectbox(
            "Plank Method",
            ["Sawmill", "Plank Make", "Plank Make (Earth Staff)"]
        )
        use_earth_staff = "Earth Staff" in plank_method
        
        use_double_mould = st.checkbox(
            "Double Ammo Mould",
            help="Makes 8 cannonballs per bar (requires 2,000 Foundry rep)"
        )
        
        ancient_furnace = st.checkbox(
            "Ancient Furnace",
            help="Halves smithing time (87 Sailing req)"
        )
        
        st.divider()
        
        quantity = st.number_input(
            "Calculate for quantity:",
            min_value=1,
            value=100,
            step=10
        )
        
        st.divider()
        
        # Show stats
        st.metric("Items in Database", len(ALL_ITEMS))
        st.metric("Items with Prices", len(prices))
        
        if st.button("🔄 Refresh Prices"):
            st.cache_data.clear()
            st.rerun()
    
    # Main tabs
    tabs = st.tabs([
        "📊 All Chains", 
        "🔍 Search Items", 
        "⚓ Sailing Items",
        "📈 Best Profits"
    ])
    
    # Tab 1: All Processing Chains
    with tabs[0]:
        st.header("All Processing Chains")
        
        # Category selector
        category = st.selectbox(
            "Select Category",
            list(st.session_state.all_chains.keys())
        )
        
        chains = st.session_state.all_chains[category]
        
        if chains:
            # Calculate all chains
            config = {
                "quantity": quantity,
                "use_earth_staff": use_earth_staff,
                "double_ammo_mould": use_double_mould,
                "ancient_furnace": ancient_furnace
            }
            
            results = []
            for chain in chains:
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    results.append({
                        "Item": chain.name,
                        "Input Cost": format_gp(result["raw_material_cost"]),
                        "Process Cost": format_gp(result["processing_costs"]),
                        "Total Cost": format_gp(result["total_input_cost"]),
                        "Output": format_gp(result["output_value"]),
                        "Tax": format_gp(result["ge_tax"]),
                        "Net Profit": format_gp(result["net_profit"]),
                        "Per Item": format_gp(result["profit_per_item"]),
                        "ROI %": f"{result['roi']:.1f}%" if result['roi'] != float('inf') else "∞",
                        "_profit_raw": result["net_profit"]  # Hidden column for sorting
                    })
            
            if results:
                df = pd.DataFrame(results)
                
                # Sort by profit
                df = df.sort_values("_profit_raw", ascending=False)
                display_df = df.drop(columns=["_profit_raw"])
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Net Profit": st.column_config.TextColumn(
                            help="Profit after all costs and GE tax"
                        ),
                        "ROI %": st.column_config.TextColumn(
                            help="Return on Investment percentage"
                        )
                    }
                )
                
                # Summary metrics
                profitable = sum(1 for r in results if r["_profit_raw"] > 0)
                best_profit = max(results, key=lambda x: x["_profit_raw"])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Profitable", f"{profitable}/{len(results)}")
                with col2:
                    st.metric("Best Item", best_profit["Item"])
                with col3:
                    st.metric("Best Profit", best_profit["Net Profit"])
    
    # Tab 2: Item Search
    with tabs[1]:
        st.header("Item Database Search")
        
        search = st.text_input("Search items by name:")
        
        if search:
            # Search in our database first
            local_matches = [
                (id, name) for id, name in ALL_ITEMS.items()
                if search.lower() in name.lower()
            ]
            
            # Also search API
            api_matches = [
                (id, item['name']) for id, item in item_mapping.items()
                if search.lower() in item['name'].lower()
            ][:50]
            
            if local_matches or api_matches:
                data = []
                
                # Combine results
                all_matches = {id: name for id, name in local_matches + api_matches}
                
                for item_id, item_name in list(all_matches.items())[:100]:
                    price = prices.get(str(item_id))
                    
                    is_sailing = item_id in ALL_ITEMS
                    
                    if price:
                        margin = price['low'] - price['high']
                        data.append({
                            'ID': item_id,
                            'Name': item_name,
                            'Sailing': '⚓' if is_sailing else '',
                            'Buy': format_gp(price['high']),
                            'Sell': format_gp(price['low']),
                            'Margin': format_gp(margin),
                            'ROI %': f"{(margin/price['high']*100):.1f}%" if price['high'] > 0 else "0%"
                        })
                    else:
                        data.append({
                            'ID': item_id,
                            'Name': item_name,
                            'Sailing': '⚓' if is_sailing else '',
                            'Buy': 'No data',
                            'Sell': 'No data',
                            'Margin': '-',
                            'ROI %': '-'
                        })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
    
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
        
        selected_cat = st.selectbox("Category", list(sailing_categories.keys()))
        
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
                    'Buy': format_gp(price['high']),
                    'Sell': format_gp(price['low']),
                    'Margin': format_gp(margin),
                    'ROI %': f"{(margin/price['high']*100):.1f}%" if price['high'] > 0 else "0%",
                    'Status': '✅ Active'
                })
            else:
                data.append({
                    'ID': item_id,
                    'Name': item_name,
                    'Buy': 'No data',
                    'Sell': 'No data',
                    'Margin': '-',
                    'ROI %': '-',
                    'Status': '❌ No prices'
                })
        
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Tab 4: Best Profits
    with tabs[3]:
        st.header("Most Profitable Chains")
        
        # Calculate all chains
        config = {
            "quantity": quantity,
            "use_earth_staff": use_earth_staff,
            "double_ammo_mould": use_double_mould,
            "ancient_furnace": ancient_furnace
        }
        
        all_results = []
        
        for category, chains in st.session_state.all_chains.items():
            for chain in chains:
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result and result["net_profit"] > 0:
                    all_results.append({
                        "Category": category,
                        "Item": chain.name,
                        "Profit": format_gp(result["net_profit"]),
                        "Per Item": format_gp(result["profit_per_item"]),
                        "ROI %": f"{result['roi']:.1f}%" if result['roi'] != float('inf') else "∞",
                        "_profit_raw": result["net_profit"]
                    })
        
        if all_results:
            # Sort by profit
            all_results.sort(key=lambda x: x["_profit_raw"], reverse=True)
            
            # Show top 20
            top_results = all_results[:20]
            
            df = pd.DataFrame(top_results)
            display_df = df.drop(columns=["_profit_raw"])
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Best by category
            st.subheader("Best in Each Category")
            
            category_bests = {}
            for result in all_results:
                cat = result["Category"]
                if cat not in category_bests or result["_profit_raw"] > category_bests[cat]["_profit_raw"]:
                    category_bests[cat] = result
            
            for cat, best in category_bests.items():
                st.write(f"**{cat}:** {best['Item']} - {best['Profit']} profit")

if __name__ == "__main__":
    main()
