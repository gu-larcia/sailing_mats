"""
OSRS Sailing Materials Tracker
Version 4.6 - Modular Architecture

A comprehensive Streamlit application for tracking Old School RuneScape 
Sailing skill materials with real-time Grand Exchange prices.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict

# Local imports
from config import APP_TITLE, APP_ICON, CACHE_TTL_PRICES, CACHE_TTL_MAPPING, CACHE_TTL_CHAINS
from data import ALL_ITEMS, BANK_LOCATIONS
from models import generate_all_chains
from services import OSRSWikiConnection, ItemIDLookup, calculate_gp_per_hour
from ui import (
    OSRS_CSS,
    render_best_item_card,
    create_profit_chart,
    create_category_pie,
    create_profit_histogram,
    create_roi_scatter,
    create_category_comparison,
)
from utils import format_gp, get_clean_item_name, get_item_icon_url

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(OSRS_CSS, unsafe_allow_html=True)


# =============================================================================
# CACHED RESOURCES
# =============================================================================

@st.cache_resource
def get_api_connection() -> OSRSWikiConnection:
    """Get a singleton API connection."""
    return OSRSWikiConnection()


@st.cache_data(ttl=CACHE_TTL_MAPPING, show_spinner=False)
def fetch_item_mapping(_conn: OSRSWikiConnection) -> Dict:
    """Fetch and cache item mappings."""
    return _conn.fetch_mapping()


@st.cache_data(ttl=CACHE_TTL_PRICES, show_spinner=False)
def fetch_latest_prices(_conn: OSRSWikiConnection) -> Dict:
    """Fetch and cache latest prices."""
    return _conn.fetch_prices()


@st.cache_resource
def get_id_lookup(_mapping_hash: str, item_mapping: Dict) -> ItemIDLookup:
    """Get a cached ItemIDLookup instance."""
    return ItemIDLookup(item_mapping)


@st.cache_data(ttl=CACHE_TTL_CHAINS)
def get_all_chains() -> Dict:
    """Get all processing chains (cached for 1 hour)."""
    return generate_all_chains()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(APP_TITLE)
        st.caption("*\"For the crafty sailor!\"*")
    with col2:
        st.link_button(
            "OSRS Wiki",
            "https://oldschool.runescape.wiki/w/Sailing",
            use_container_width=True
        )
    
    # Load data
    conn = get_api_connection()
    
    with st.spinner("Loading market data..."):
        item_mapping = fetch_item_mapping(conn)
        prices = fetch_latest_prices(conn)
        mapping_hash = str(hash(frozenset(item_mapping.keys())))
        id_lookup = get_id_lookup(mapping_hash, item_mapping)
        all_chains = get_all_chains()
    
    # Get URL parameters
    params = st.query_params
    
    # ==========================================================================
    # SIDEBAR CONFIGURATION
    # ==========================================================================
    
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
        
        # Stats
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
    
    # Build config dict
    use_earth_staff = "Earth Staff" in plank_method
    show_gp_hr_active = params.get("show_gp_hr", "false") == "true"
    
    config = {
        "quantity": quantity,
        "use_earth_staff": use_earth_staff,
        "self_collected": self_collected,
        "ancient_furnace": ancient_furnace,
        "plank_method": plank_method,
        "show_gp_hr": show_gp_hr_active,
        "bank_location": params.get("bank_location", "Medium (Typical)"),
        "use_stamina": params.get("use_stamina", "true") == "true",
        "has_imcando_hammer": params.get("imcando_hammer", "false") == "true",
        "has_amys_saw": params.get("amys_saw", "false") == "true",
        "has_plank_sack": params.get("plank_sack", "false") == "true",
        "has_smithing_outfit": params.get("smithing_outfit", "false") == "true",
    }
    
    # ==========================================================================
    # MAIN TABS
    # ==========================================================================
    
    tabs = st.tabs([
        "All Chains", 
        "Search Items", 
        "Sailing Items",
        "Best Profits",
        "Analytics"
    ])
    
    # --------------------------------------------------------------------------
    # TAB 1: ALL CHAINS
    # --------------------------------------------------------------------------
    with tabs[0]:
        st.header("All Processing Chains")
        
        category = st.selectbox(
            "Select Category",
            list(all_chains.keys()),
            key="chain_category"
        )
        
        chains = all_chains[category]
        show_gp_hr_display = config.get("show_gp_hr", False)
        
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
                    
                    if show_gp_hr_display:
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
                
                if show_gp_hr_display and "GP/hr" in df.columns:
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
                
                if show_gp_hr_display:
                    column_config["GP/hr"] = st.column_config.NumberColumn("GP/hr", format="%.0f")
                    column_config["Items/hr"] = st.column_config.NumberColumn("Items/hr", format="%.0f")
                    column_config["_gp_hr_raw"] = None
                
                st.dataframe(df, use_container_width=True, hide_index=True, column_config=column_config)
                
                # Summary stats
                profitable = sum(1 for r in results if r["_profit_raw"] > 0)
                best_profit = max(results, key=lambda x: x["_profit_raw"])
                total_profit = sum(r["_profit_raw"] for r in results if r["_profit_raw"] > 0)
                
                if show_gp_hr_display:
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
                        st.markdown(render_best_item_card("Best Profit", get_clean_item_name(best_profit["Item"]), format_gp(best_profit["Net Profit"])), unsafe_allow_html=True)
                    with col3:
                        st.metric("Total Potential", format_gp(total_profit))
                    with col4:
                        if best_profit["ROI %"]:
                            st.metric("Best ROI", f"{best_profit['ROI %']:.1f}%")
    
    # --------------------------------------------------------------------------
    # TAB 2: SEARCH ITEMS
    # --------------------------------------------------------------------------
    with tabs[1]:
        st.header("Search Items")
        
        search_term = st.text_input("Search by name or ID", key="item_search")
        
        if search_term:
            search_lower = search_term.lower()
            matching_items = []
            
            for item_id, item_data in item_mapping.items():
                if isinstance(item_data, dict):
                    name = item_data.get('name', '')
                    if search_lower in name.lower() or search_term == str(item_id):
                        price_data = prices.get(str(item_id), {})
                        matching_items.append({
                            "Icon": get_item_icon_url(name),
                            "ID": item_id,
                            "Name": name,
                            "Buy": price_data.get("high", 0),
                            "Sell": price_data.get("low", 0),
                            "Margin": price_data.get("high", 0) - price_data.get("low", 0) if price_data else 0,
                            "ROI %": ((price_data.get("low", 0) - price_data.get("high", 0)) / price_data.get("high", 1) * 100) if price_data.get("high", 0) else 0,
                            "Status": bool(price_data)
                        })
            
            if matching_items:
                st.dataframe(
                    pd.DataFrame(matching_items[:50]),
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
                st.caption(f"Showing {min(50, len(matching_items))} of {len(matching_items)} results")
            else:
                st.info("No items found matching your search.")
    
    # --------------------------------------------------------------------------
    # TAB 3: SAILING ITEMS
    # --------------------------------------------------------------------------
    with tabs[2]:
        st.header("Sailing Items")
        
        data = []
        for item_id, name in ALL_ITEMS.items():
            price_data = prices.get(str(item_id), {})
            data.append({
                "Icon": get_item_icon_url(name),
                "ID": item_id,
                "Name": name,
                "Buy": price_data.get("high", 0),
                "Sell": price_data.get("low", 0),
                "Margin": price_data.get("high", 0) - price_data.get("low", 0) if price_data else 0,
                "ROI %": ((price_data.get("low", 0) - price_data.get("high", 0)) / price_data.get("high", 1) * 100) if price_data.get("high", 0) else 0,
                "Status": bool(price_data)
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
    
    # --------------------------------------------------------------------------
    # TAB 4: BEST PROFITS
    # --------------------------------------------------------------------------
    with tabs[3]:
        st.header("Most Profitable Chains")
        
        all_results = []
        
        with st.spinner("Calculating all chains..."):
            for cat, cat_chains in all_chains.items():
                for chain in cat_chains:
                    result = chain.calculate(prices, config, id_lookup)
                    if "error" not in result:
                        output_name = result.get("output_item_name", chain.name)
                        all_results.append({
                            "Icon": get_item_icon_url(output_name),
                            "Category": cat,
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
            else:
                st.warning("No profitable chains found with current settings.")
    
    # --------------------------------------------------------------------------
    # TAB 5: ANALYTICS
    # --------------------------------------------------------------------------
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
        quantity_val = config.get("quantity", 1)
        
        for cat, cat_chains in all_chains.items():
            for chain in cat_chains:
                if exclude_dragon and "dragon" in chain.name.lower():
                    continue
                    
                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    profit = result["net_profit"]
                    if use_per_item and quantity_val > 0:
                        profit = profit / quantity_val
                    
                    all_results_for_charts.append({
                        "Category": cat,
                        "Item": chain.name,
                        "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                        "_profit_raw": profit
                    })
        
        if filter_outliers and len(all_results_for_charts) > 4:
            profits_list = [r["_profit_raw"] for r in all_results_for_charts]
            q1 = np.percentile(profits_list, 25)
            q3 = np.percentile(profits_list, 75)
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
            
            # Distribution histogram
            profit_label = "Per-Item Profit" if use_per_item else f"Batch Profit (qty: {quantity_val})"
            st.subheader(f"Distribution Analysis as {profit_label}")
            profits = [r["_profit_raw"] for r in all_results_for_charts]
            fig = create_profit_histogram(profits, per_item=use_per_item)
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
