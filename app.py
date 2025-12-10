"""
OSRS Sailing Materials Tracker
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Tuple
import time

# Page config
st.set_page_config(
    page_title="OSRS Sailing Tracker",
    page_icon="⚓",
    layout="wide"
)

# Constants
API_BASE = "https://prices.runescape.wiki/api/v1/osrs"
CACHE_DURATION = 60  # seconds

# Initialize session state
if 'price_cache' not in st.session_state:
    st.session_state.price_cache = {}
    st.session_state.cache_timestamp = None
    st.session_state.item_mapping = {}
    st.session_state.processing_chains = []
    st.session_state.watchlist = []

class OSRSApiClient:
    """Client for interacting with OSRS Wiki API"""
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_item_mapping():
        """Fetch all item mappings from API"""
        try:
            response = requests.get(f"{API_BASE}/mapping")
            response.raise_for_status()
            items = response.json()
            # Convert to dict for easier lookup
            return {item['id']: item for item in items}
        except Exception as e:
            st.error(f"Failed to fetch item mapping: {e}")
            return {}
    
    @staticmethod
    @st.cache_data(ttl=60)  # Cache for 1 minute
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
    
    @staticmethod
    def get_item_price(item_id: int, prices: Dict) -> Optional[Dict]:
        """Get price for specific item"""
        return prices.get(str(item_id))

class ProcessingChain:
    """Handles processing chain calculations"""
    
    def __init__(self, name: str = "New Chain"):
        self.name = name
        self.steps = []
    
    def add_step(self, item_id: int, item_name: str, 
                 input_qty: float = 1, output_qty: float = 1, 
                 processing_cost: float = 0):
        """Add a step to the processing chain"""
        self.steps.append({
            'item_id': item_id,
            'item_name': item_name,
            'input_qty': input_qty,
            'output_qty': output_qty,
            'processing_cost': processing_cost
        })
    
    def calculate(self, prices: Dict, final_quantity: int = 1) -> Dict:
        """Calculate the full processing chain costs and profits"""
        if not self.steps:
            return {}
        
        results = {
            'steps': [],
            'total_input_cost': 0,
            'total_output_value': 0,
            'total_processing_cost': 0,
            'net_profit': 0,
            'roi': 0,
            'materials_needed': {}
        }
        
        # Work backwards from final quantity
        current_qty = final_quantity
        
        for i, step in enumerate(reversed(self.steps)):
            price_data = OSRSApiClient.get_item_price(step['item_id'], prices)
            
            if not price_data:
                st.warning(f"No price data for {step['item_name']}")
                continue
            
            # Calculate quantities needed
            if i == 0:  # Final product
                qty_needed = current_qty
                step_value = price_data.get('low', 0) * qty_needed
                results['total_output_value'] = step_value
            else:
                # Calculate how many inputs needed
                prev_step = self.steps[-i]  # The step that produces this
                qty_needed = current_qty * (step['input_qty'] / prev_step['output_qty'])
                
                if i == len(self.steps) - 1:  # First input
                    step_cost = price_data.get('high', 0) * qty_needed
                    results['total_input_cost'] += step_cost
                    results['materials_needed'][step['item_name']] = qty_needed
            
            results['total_processing_cost'] += step['processing_cost'] * qty_needed
            
            results['steps'].append({
                'name': step['item_name'],
                'quantity': qty_needed,
                'unit_price': price_data.get('high', 0) if i > 0 else price_data.get('low', 0),
                'total_value': price_data.get('high', 0) * qty_needed if i > 0 else price_data.get('low', 0) * qty_needed
            })
            
            current_qty = qty_needed
        
        # Calculate final metrics
        ge_tax = results['total_output_value'] * 0.02 if results['total_output_value'] > 50 else 0
        results['ge_tax'] = min(ge_tax, 5000000)
        results['net_profit'] = results['total_output_value'] - results['total_input_cost'] - results['total_processing_cost'] - results['ge_tax']
        
        if results['total_input_cost'] > 0:
            results['roi'] = (results['net_profit'] / results['total_input_cost']) * 100
        
        return results

def format_gp(value: float) -> str:
    """Format gold pieces value"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K"
    else:
        return f"{value:.0f}"

def main():
    st.title("⚓ OSRS Sailing Materials Tracker")
    
    # Sidebar for data refresh
    with st.sidebar:
        st.header("Data Management")
        
        if st.button("🔄 Refresh All Data"):
            st.cache_data.clear()
            st.session_state.price_cache = {}
            st.session_state.cache_timestamp = None
            st.rerun()
        
        # Show last update time
        if st.session_state.cache_timestamp:
            time_diff = datetime.now() - st.session_state.cache_timestamp
            st.info(f"Last updated: {time_diff.seconds}s ago")
        
        st.divider()
        
        # Quick stats
        st.header("Quick Stats")
        prices = OSRSApiClient.fetch_latest_prices()
        st.metric("Items with Prices", len(prices))
        st.metric("GE Tax Rate", "2%")
    
    # Load data
    with st.spinner("Loading item data..."):
        item_mapping = OSRSApiClient.fetch_item_mapping()
        prices = OSRSApiClient.fetch_latest_prices()
        st.session_state.cache_timestamp = datetime.now()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Processing Chains", "📊 Price Lookup", "📋 Watchlist", "🔍 Item Search"])
    
    # Tab 1: Processing Chains
    with tab1:
        st.header("Processing Chain Calculator")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Build Your Chain")
            
            # Chain name
            chain_name = st.text_input("Chain Name", value="New Processing Chain")
            
            # Add steps
            st.write("**Add Processing Steps**")
            
            # Item selector
            search_term = st.text_input("Search for item")
            if search_term:
                matching_items = [
                    (id, item['name']) 
                    for id, item in item_mapping.items() 
                    if search_term.lower() in item['name'].lower()
                ][:20]  # Limit to 20 results
                
                if matching_items:
                    selected = st.selectbox(
                        "Select Item",
                        matching_items,
                        format_func=lambda x: f"{x[1]} (ID: {x[0]})"
                    )
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        input_qty = st.number_input("Input Qty", min_value=1, value=1)
                    with col_b:
                        output_qty = st.number_input("Output Qty", min_value=1, value=1)
                    
                    processing_cost = st.number_input("Processing Cost (GP)", min_value=0, value=0)
                    
                    if st.button("➕ Add Step"):
                        if 'current_chain' not in st.session_state:
                            st.session_state.current_chain = ProcessingChain(chain_name)
                        
                        st.session_state.current_chain.add_step(
                            selected[0], selected[1], 
                            input_qty, output_qty, 
                            processing_cost
                        )
                        st.success(f"Added {selected[1]} to chain")
                        st.rerun()
            
            # Show current chain
            if 'current_chain' in st.session_state and st.session_state.current_chain.steps:
                st.divider()
                st.write("**Current Chain Steps:**")
                for i, step in enumerate(st.session_state.current_chain.steps):
                    st.write(f"{i+1}. {step['item_name']} ({step['input_qty']} → {step['output_qty']})")
                
                if st.button("🗑️ Clear Chain"):
                    del st.session_state.current_chain
                    st.rerun()
        
        with col2:
            st.subheader("Chain Analysis")
            
            if 'current_chain' in st.session_state and st.session_state.current_chain.steps:
                # Quantity selector
                final_qty = st.number_input(
                    "Calculate for quantity:", 
                    min_value=1, 
                    value=1, 
                    step=1
                )
                
                # Calculate results
                results = st.session_state.current_chain.calculate(prices, final_qty)
                
                if results:
                    # Display metrics
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
                        st.metric(
                            "Net Profit", 
                            f"{format_gp(results['net_profit'])} gp",
                            delta=f"{results['roi']:.1f}% ROI"
                        )
                    
                    with col_m4:
                        st.metric(
                            "GE Tax", 
                            f"{format_gp(results['ge_tax'])} gp"
                        )
                    
                    # Materials needed
                    st.divider()
                    st.write("**Materials Required:**")
                    for material, qty in results['materials_needed'].items():
                        st.write(f"• {material}: {qty:.0f}")
                    
                    # Detailed breakdown
                    st.divider()
                    st.write("**Step-by-Step Breakdown:**")
                    
                    steps_df = pd.DataFrame(results['steps'])
                    if not steps_df.empty:
                        steps_df['unit_price'] = steps_df['unit_price'].apply(lambda x: f"{format_gp(x)} gp")
                        steps_df['total_value'] = steps_df['total_value'].apply(lambda x: f"{format_gp(x)} gp")
                        st.dataframe(steps_df, use_container_width=True)
            else:
                st.info("Build a processing chain on the left to see analysis")
    
    # Tab 2: Price Lookup
    with tab2:
        st.header("Live Price Lookup")
        
        # Search
        search = st.text_input("Search items by name")
        
        if search:
            # Filter items
            filtered_items = {
                id: item for id, item in item_mapping.items()
                if search.lower() in item['name'].lower()
            }[:100]  # Limit to 100 results
            
            if filtered_items:
                # Create dataframe
                data = []
                for item_id, item in filtered_items.items():
                    price = OSRSApiClient.get_item_price(item_id, prices)
                    
                    data.append({
                        'ID': item_id,
                        'Name': item['name'],
                        'Buy Price': format_gp(price['high']) + ' gp' if price else 'N/A',
                        'Sell Price': format_gp(price['low']) + ' gp' if price else 'N/A',
                        'Margin': format_gp(price['low'] - price['high']) + ' gp' if price else 'N/A',
                        'ROI %': f"{((price['low'] - price['high']) / price['high'] * 100):.1f}%" if price and price['high'] > 0 else 'N/A'
                    })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No items found")
    
    # Tab 3: Watchlist
    with tab3:
        st.header("Watchlist")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Add Items")
            
            # Item search for watchlist
            watch_search = st.text_input("Search to add to watchlist", key="watch_search")
            
            if watch_search:
                matching = [
                    (id, item['name']) 
                    for id, item in item_mapping.items() 
                    if watch_search.lower() in item['name'].lower()
                ][:10]
                
                if matching:
                    selected_watch = st.selectbox(
                        "Select item to watch",
                        matching,
                        format_func=lambda x: f"{x[1]} (ID: {x[0]})",
                        key="watch_select"
                    )
                    
                    if st.button("Add to Watchlist"):
                        if selected_watch not in st.session_state.watchlist:
                            st.session_state.watchlist.append(selected_watch)
                            st.success(f"Added {selected_watch[1]} to watchlist")
                            st.rerun()
            
            if st.button("Clear Watchlist"):
                st.session_state.watchlist = []
                st.rerun()
        
        with col2:
            st.subheader("Watched Items")
            
            if st.session_state.watchlist:
                watch_data = []
                for item_id, item_name in st.session_state.watchlist:
                    price = OSRSApiClient.get_item_price(item_id, prices)
                    
                    if price:
                        margin = price['low'] - price['high']
                        watch_data.append({
                            'Name': item_name,
                            'Buy': format_gp(price['high']) + ' gp',
                            'Sell': format_gp(price['low']) + ' gp',
                            'Margin': format_gp(margin) + ' gp',
                            'ROI': f"{(margin / price['high'] * 100):.1f}%" if price['high'] > 0 else '0%'
                        })
                    else:
                        watch_data.append({
                            'Name': item_name,
                            'Buy': 'N/A',
                            'Sell': 'N/A',
                            'Margin': 'N/A',
                            'ROI': 'N/A'
                        })
                
                watch_df = pd.DataFrame(watch_data)
                st.dataframe(watch_df, use_container_width=True)
            else:
                st.info("No items in watchlist. Add some items to track their prices!")
    
    # Tab 4: Item Search
    with tab4:
        st.header("Item Database Search")
        
        col1, col2 = st.columns(2)
        
        with col1:
            search_name = st.text_input("Search by name", key="db_search")
        
        with col2:
            search_id = st.number_input("Search by ID", min_value=0, value=0, key="id_search")
        
        if search_name or search_id > 0:
            if search_id > 0:
                # Search by ID
                if search_id in item_mapping:
                    item = item_mapping[search_id]
                    price = OSRSApiClient.get_item_price(search_id, prices)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {item['name']}")
                        st.write(f"**ID:** {search_id}")
                        if 'examine' in item:
                            st.write(f"**Examine:** {item['examine']}")
                        if 'highalch' in item:
                            st.write(f"**High Alch:** {item['highalch']} gp")
                    
                    with col2:
                        if price:
                            st.write(f"**Buy Price:** {format_gp(price['high'])} gp")
                            st.write(f"**Sell Price:** {format_gp(price['low'])} gp")
                            st.write(f"**Margin:** {format_gp(price['low'] - price['high'])} gp")
                        else:
                            st.warning("No price data available")
                else:
                    st.error(f"Item ID {search_id} not found")
            
            elif search_name:
                # Search by name
                results = [
                    (id, item) for id, item in item_mapping.items()
                    if search_name.lower() in item['name'].lower()
                ][:50]
                
                if results:
                    st.write(f"Found {len(results)} items (showing max 50)")
                    
                    data = []
                    for item_id, item in results:
                        price = OSRSApiClient.get_item_price(item_id, prices)
                        data.append({
                            'ID': item_id,
                            'Name': item['name'],
                            'Has Price': '✓' if price else '✗',
                            'Buy': format_gp(price['high']) + ' gp' if price else 'N/A',
                            'Sell': format_gp(price['low']) + ' gp' if price else 'N/A'
                        })
                    
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No items found")

if __name__ == "__main__":
    main()
