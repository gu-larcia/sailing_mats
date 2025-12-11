"""
OSRS Sailing Materials Tracker
Main Streamlit Application - Improved Processing Chain Logic
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
from dataclasses import dataclass, field

# Page config
st.set_page_config(
    page_title="OSRS Sailing Tracker",
    page_icon="⚓",
    layout="wide"
)

# Constants
API_BASE = "https://prices.runescape.wiki/api/v1/osrs"

# Common item IDs (that we know exist)
COMMON_ITEMS = {
    # Logs
    1511: "Logs",
    1521: "Oak logs", 
    6333: "Teak logs",
    6332: "Mahogany logs",
    1515: "Yew logs",
    1513: "Magic logs",
    
    # Planks  
    960: "Plank",
    8778: "Oak plank",
    8780: "Teak plank", 
    8782: "Mahogany plank",
    
    # Bars
    2349: "Bronze bar",
    2351: "Iron bar",
    2353: "Steel bar",
    2359: "Mithril bar",
    2361: "Adamantite bar",
    2363: "Runite bar",
    
    # Nails
    4819: "Bronze nails",
    4820: "Iron nails",
    1539: "Steel nails",
    4822: "Mithril nails",
    4823: "Adamantite nails",
    4824: "Rune nails",
    
    # Runes (for Plank Make)
    9075: "Astral rune",
    561: "Nature rune",
    557: "Earth rune",
    
    # Tools/Staves
    6562: "Mud battlestaff",
    1381: "Staff of air",
    1385: "Staff of earth"
}

# Processing costs by method
PLANK_COSTS = {
    "Sawmill": {
        960: 100,    # Regular plank
        8778: 250,   # Oak plank
        8780: 500,   # Teak plank
        8782: 1500,  # Mahogany plank
    },
    "Plank Make (No staff)": {
        960: 70,     # Regular plank
        8778: 175,   # Oak plank  
        8780: 350,   # Teak plank
        8782: 1050,  # Mahogany plank
    },
    "Plank Make (Earth staff)": {
        960: 70,     # Regular plank
        8778: 175,   # Oak plank
        8780: 350,   # Teak plank
        8782: 1050,  # Mahogany plank
    },
    "Butler": {
        960: 100,    # Regular plank
        8778: 250,   # Oak plank
        8780: 500,   # Teak plank
        8782: 1500,  # Mahogany plank
    }
}

@dataclass
class ProcessingStep:
    """Represents a single step in a processing chain"""
    item_id: int
    item_name: str
    quantity_per_output: int = 1  # How many of this item needed per output
    processing_method: str = "None"
    processing_cost_override: Optional[float] = None

@dataclass  
class ProcessingChain:
    """Complete processing chain with calculations"""
    name: str
    steps: List[ProcessingStep] = field(default_factory=list)
    
    def calculate(self, prices: Dict, final_quantity: int = 1, 
                 plank_method: str = "Sawmill", use_earth_staff: bool = False) -> Dict:
        """
        Calculate the full chain costs working backwards from final product
        """
        if not self.steps or len(self.steps) < 2:
            return {"error": "Need at least 2 steps in chain"}
        
        results = {
            "final_product": self.steps[-1].item_name,
            "final_quantity": final_quantity,
            "steps_breakdown": [],
            "total_input_cost": 0,
            "total_output_value": 0,
            "total_processing_cost": 0,
            "ge_tax": 0,
            "net_profit": 0,
            "roi": 0,
            "materials_summary": {}
        }
        
        # Work backwards through the chain
        current_quantity = final_quantity
        
        for i in range(len(self.steps) - 1, -1, -1):
            step = self.steps[i]
            price_data = prices.get(str(step.item_id))
            
            if not price_data:
                results["steps_breakdown"].append({
                    "item": step.item_name,
                    "quantity": current_quantity * step.quantity_per_output,
                    "error": "No price data"
                })
                continue
            
            step_qty = current_quantity * step.quantity_per_output
            
            # Determine price (buy for inputs, sell for output)
            if i == len(self.steps) - 1:  # Final product
                unit_price = price_data.get("low", 0)  # Sell price
                step_total = unit_price * step_qty
                results["total_output_value"] = step_total
                step_type = "Output"
            else:
                unit_price = price_data.get("high", 0)  # Buy price  
                step_total = unit_price * step_qty
                if i == 0:  # First input
                    results["total_input_cost"] = step_total
                    results["materials_summary"][step.item_name] = step_qty
                step_type = "Input" if i == 0 else "Intermediate"
            
            # Calculate processing cost for this step
            processing_cost = 0
            processing_notes = ""
            
            if step.processing_cost_override is not None:
                processing_cost = step.processing_cost_override * current_quantity
                processing_notes = f"Custom cost: {step.processing_cost_override} gp each"
            elif step.processing_method == "Plank Make":
                # Calculate Plank Make costs
                if step.item_id in PLANK_COSTS["Plank Make (Earth staff)"]:
                    base_cost = PLANK_COSTS["Plank Make (Earth staff)"][step.item_id]
                    processing_cost = base_cost * current_quantity
                    
                    # Add rune costs
                    astral_price = prices.get(str(9075), {}).get("high", 0)
                    nature_price = prices.get(str(561), {}).get("high", 0)
                    rune_cost = (astral_price * 2 + nature_price) * current_quantity
                    
                    if not use_earth_staff:
                        earth_price = prices.get(str(557), {}).get("high", 0)
                        rune_cost += earth_price * 15 * current_quantity
                        processing_notes = f"Plank Make: {base_cost} gp + runes"
                    else:
                        processing_notes = f"Plank Make (Earth staff): {base_cost} gp + runes"
                    
                    processing_cost += rune_cost
                    
            elif step.processing_method == "Sawmill":
                if step.item_id in PLANK_COSTS["Sawmill"]:
                    sawmill_cost = PLANK_COSTS["Sawmill"][step.item_id]
                    processing_cost = sawmill_cost * current_quantity
                    processing_notes = f"Sawmill: {sawmill_cost} gp each"
            
            results["total_processing_cost"] += processing_cost
            
            # Add to breakdown
            results["steps_breakdown"].append({
                "step": i + 1,
                "type": step_type,
                "item": step.item_name,
                "quantity": step_qty,
                "unit_price": unit_price,
                "total_value": step_total,
                "processing_cost": processing_cost,
                "processing_notes": processing_notes
            })
            
            # Set quantity for next iteration (going backwards)
            if i > 0:
                current_quantity = step_qty
        
        # Calculate final values
        if results["total_output_value"] >= 50:
            results["ge_tax"] = min(results["total_output_value"] * 0.02, 5000000)
        
        total_cost = results["total_input_cost"] + results["total_processing_cost"] + results["ge_tax"]
        results["net_profit"] = results["total_output_value"] - total_cost
        
        if results["total_input_cost"] > 0:
            results["roi"] = (results["net_profit"] / results["total_input_cost"]) * 100
        
        # Reverse the steps for display (show in logical order)
        results["steps_breakdown"].reverse()
        
        return results

class OSRSApiClient:
    """Client for interacting with OSRS Wiki API"""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def fetch_item_mapping():
        """Fetch all item mappings from API"""
        try:
            response = requests.get(f"{API_BASE}/mapping")
            response.raise_for_status()
            items = response.json()
            return {item['id']: item for item in items}
        except Exception as e:
            st.error(f"Failed to fetch item mapping: {e}")
            return {}
    
    @staticmethod
    @st.cache_data(ttl=60)
    def fetch_latest_prices():
        """Fetch latest prices from API"""
        try:
            response = requests.get(f"{API_BASE}/latest")
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except Exception as e:
            st.error(f"Failed to fetch prices: {e}")
            return {}

def format_gp(value: float) -> str:
    """Format gold pieces value"""
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"{value/1_000:.0f}K"
    else:
        return f"{int(value):,}"

def get_preset_chains() -> List[ProcessingChain]:
    """Get preset processing chains"""
    chains = []
    
    # Oak processing
    oak_chain = ProcessingChain("Oak Processing (Logs → Planks → Hull Parts)")
    oak_chain.steps = [
        ProcessingStep(1521, "Oak logs", 1),
        ProcessingStep(8778, "Oak plank", 1, "Sawmill"),
        # ProcessingStep(31636, "Oak hull parts", 5),  # If we find the real ID
    ]
    chains.append(oak_chain)
    
    # Teak processing  
    teak_chain = ProcessingChain("Teak Processing (Logs → Planks)")
    teak_chain.steps = [
        ProcessingStep(6333, "Teak logs", 1),
        ProcessingStep(8780, "Teak plank", 1, "Sawmill"),
    ]
    chains.append(teak_chain)
    
    # Mahogany processing
    mahogany_chain = ProcessingChain("Mahogany Processing (Logs → Planks)")
    mahogany_chain.steps = [
        ProcessingStep(6332, "Mahogany logs", 1),
        ProcessingStep(8782, "Mahogany plank", 1, "Sawmill"),
    ]
    chains.append(mahogany_chain)
    
    return chains

def main():
    st.title("⚓ OSRS Sailing Materials Tracker")
    
    # Initialize session state
    if 'custom_chains' not in st.session_state:
        st.session_state.custom_chains = []
    if 'current_chain' not in st.session_state:
        st.session_state.current_chain = ProcessingChain("New Chain")
    
    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Plank Processing Method")
        plank_method = st.selectbox(
            "Method:",
            ["Sawmill", "Plank Make", "Butler", "Custom"]
        )
        
        use_earth_staff = False
        if plank_method == "Plank Make":
            use_earth_staff = st.checkbox("Using Earth/Mud Staff?")
            st.info("Earth staff removes 15 earth rune cost per plank")
        
        st.divider()
        
        if st.button("🔄 Refresh Prices"):
            st.cache_data.clear()
            st.rerun()
    
    # Load data
    with st.spinner("Loading data..."):
        item_mapping = OSRSApiClient.fetch_item_mapping()
        prices = OSRSApiClient.fetch_latest_prices()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🔄 Processing Chains", "📊 Quick Lookup", "🔍 Item Search"])
    
    with tab1:
        st.header("Processing Chain Calculator")
        
        # Choose between preset and custom
        chain_mode = st.radio("Chain Mode:", ["Use Preset", "Build Custom"], horizontal=True)
        
        if chain_mode == "Use Preset":
            preset_chains = get_preset_chains()
            selected_preset = st.selectbox(
                "Select Preset Chain:",
                preset_chains,
                format_func=lambda x: x.name
            )
            
            if selected_preset:
                st.session_state.current_chain = selected_preset
        
        else:  # Build Custom
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Build Chain")
                
                chain_name = st.text_input("Chain Name", value=st.session_state.current_chain.name)
                st.session_state.current_chain.name = chain_name
                
                st.write("**Add Steps (in order)**")
                st.info("Add items from raw material to final product")
                
                # Quick add common items
                st.write("Quick Add:")
                quick_cols = st.columns(2)
                with quick_cols[0]:
                    if st.button("+ Oak logs", use_container_width=True):
                        st.session_state.current_chain.steps.append(
                            ProcessingStep(1521, "Oak logs", 1)
                        )
                        st.rerun()
                    if st.button("+ Teak logs", use_container_width=True):
                        st.session_state.current_chain.steps.append(
                            ProcessingStep(6333, "Teak logs", 1)
                        )
                        st.rerun()
                
                with quick_cols[1]:
                    if st.button("+ Oak plank", use_container_width=True):
                        st.session_state.current_chain.steps.append(
                            ProcessingStep(8778, "Oak plank", 1, "Sawmill")
                        )
                        st.rerun()
                    if st.button("+ Teak plank", use_container_width=True):
                        st.session_state.current_chain.steps.append(
                            ProcessingStep(8780, "Teak plank", 1, "Sawmill")
                        )
                        st.rerun()
                
                st.divider()
                
                # Custom item add
                search_term = st.text_input("Search item to add:")
                if search_term:
                    matches = [(id, item['name']) for id, item in item_mapping.items() 
                              if search_term.lower() in item['name'].lower()][:10]
                    
                    if matches:
                        selected = st.selectbox(
                            "Select:",
                            matches,
                            format_func=lambda x: f"{x[1]} (ID: {x[0]})"
                        )
                        
                        qty_needed = st.number_input(
                            "Quantity needed per output:", 
                            min_value=1, 
                            value=1
                        )
                        
                        proc_method = st.selectbox(
                            "Processing method:",
                            ["None", "Sawmill", "Plank Make", "Custom"]
                        )
                        
                        custom_cost = None
                        if proc_method == "Custom":
                            custom_cost = st.number_input(
                                "Cost per item (gp):", 
                                min_value=0, 
                                value=0
                            )
                        
                        if st.button("Add to Chain"):
                            st.session_state.current_chain.steps.append(
                                ProcessingStep(
                                    selected[0], 
                                    selected[1], 
                                    qty_needed,
                                    proc_method,
                                    custom_cost
                                )
                            )
                            st.rerun()
                
                # Show current chain
                if st.session_state.current_chain.steps:
                    st.divider()
                    st.write("**Current Chain:**")
                    for i, step in enumerate(st.session_state.current_chain.steps):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.write(f"{i+1}. {step.item_name}")
                            if step.quantity_per_output > 1:
                                st.caption(f"   Qty: {step.quantity_per_output}")
                            if step.processing_method != "None":
                                st.caption(f"   Process: {step.processing_method}")
                        with col_b:
                            if st.button("❌", key=f"del_{i}"):
                                del st.session_state.current_chain.steps[i]
                                st.rerun()
                    
                    if st.button("🗑️ Clear All"):
                        st.session_state.current_chain.steps = []
                        st.rerun()
            
            with col2:
                st.subheader("Analysis")
                
                if len(st.session_state.current_chain.steps) >= 2:
                    quantity = st.number_input(
                        "Calculate for quantity:",
                        min_value=1,
                        value=1,
                        step=1
                    )
                    
                    # Calculate
                    results = st.session_state.current_chain.calculate(
                        prices, 
                        quantity,
                        plank_method,
                        use_earth_staff
                    )
                    
                    if "error" in results:
                        st.error(results["error"])
                    else:
                        # Metrics
                        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                        
                        with col_m1:
                            st.metric(
                                "Input Cost",
                                f"{format_gp(results['total_input_cost'])} gp"
                            )
                        
                        with col_m2:
                            st.metric(
                                "Output Value",
                                f"{format_gp(results['total_output_value'])} gp"
                            )
                        
                        with col_m3:
                            color = "🟢" if results['net_profit'] > 0 else "🔴"
                            st.metric(
                                f"{color} Net Profit",
                                f"{format_gp(results['net_profit'])} gp",
                                delta=f"{results['roi']:.1f}% ROI"
                            )
                        
                        with col_m4:
                            st.metric(
                                "GE Tax (2%)",
                                f"{format_gp(results['ge_tax'])} gp"
                            )
                        
                        # Processing cost breakdown
                        if results['total_processing_cost'] > 0:
                            st.info(f"Total Processing Cost: {format_gp(results['total_processing_cost'])} gp")
                        
                        # Materials needed
                        if results['materials_summary']:
                            st.divider()
                            st.write("**Materials Required:**")
                            for mat, qty in results['materials_summary'].items():
                                st.write(f"• {mat}: {qty:,}")
                        
                        # Detailed breakdown
                        st.divider()
                        st.write("**Step-by-Step Breakdown:**")
                        
                        breakdown_data = []
                        for step in results['steps_breakdown']:
                            if 'error' not in step:
                                breakdown_data.append({
                                    'Step': step['step'],
                                    'Type': step['type'],
                                    'Item': step['item'],
                                    'Quantity': f"{step['quantity']:,}",
                                    'Unit Price': f"{format_gp(step['unit_price'])} gp",
                                    'Total Value': f"{format_gp(step['total_value'])} gp",
                                    'Processing': f"{format_gp(step['processing_cost'])} gp" if step['processing_cost'] > 0 else "-",
                                    'Notes': step['processing_notes'] if step['processing_notes'] else ""
                                })
                        
                        if breakdown_data:
                            df = pd.DataFrame(breakdown_data)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        # Summary
                        st.divider()
                        st.write("**Summary:**")
                        summary_data = {
                            'Input Cost': f"{format_gp(results['total_input_cost'])} gp",
                            'Processing Cost': f"{format_gp(results['total_processing_cost'])} gp",
                            'GE Tax': f"{format_gp(results['ge_tax'])} gp",
                            'Total Cost': f"{format_gp(results['total_input_cost'] + results['total_processing_cost'] + results['ge_tax'])} gp",
                            'Output Value': f"{format_gp(results['total_output_value'])} gp",
                            'Net Profit': f"{format_gp(results['net_profit'])} gp",
                            'ROI': f"{results['roi']:.1f}%",
                            'Profit per Item': f"{format_gp(results['net_profit'] / quantity)} gp"
                        }
                        
                        for key, value in summary_data.items():
                            st.write(f"**{key}:** {value}")
                
                else:
                    st.info("Add at least 2 items to see analysis")
    
    with tab2:
        st.header("Quick Price Lookup")
        
        # Common items prices
        st.subheader("Common Items")
        
        common_data = []
        for item_id, item_name in COMMON_ITEMS.items():
            price = prices.get(str(item_id))
            if price:
                margin = price['low'] - price['high']
                common_data.append({
                    'Item': item_name,
                    'Buy': f"{format_gp(price['high'])} gp",
                    'Sell': f"{format_gp(price['low'])} gp",
                    'Margin': f"{format_gp(margin)} gp",
                    'ROI': f"{(margin/price['high']*100):.1f}%" if price['high'] > 0 else "0%"
                })
        
        if common_data:
            df = pd.DataFrame(common_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.header("Item Search")
        
        search = st.text_input("Search by name:")
        
        if search:
            results = [(id, item) for id, item in item_mapping.items()
                      if search.lower() in item['name'].lower()][:50]
            
            if results:
                st.write(f"Found {len(results)} items")
                
                data = []
                for item_id, item in results:
                    price = prices.get(str(item_id))
                    data.append({
                        'ID': item_id,
                        'Name': item['name'],
                        'Has Price': '✓' if price else '✗',
                        'Buy': f"{format_gp(price['high'])} gp" if price else 'N/A',
                        'Sell': f"{format_gp(price['low'])} gp" if price else 'N/A'
                    })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
