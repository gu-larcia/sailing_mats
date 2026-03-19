"""OSRS Market Tracker v5.1 — Sailing Materials & Beyond"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict

from config import (
    APP_TITLE, APP_SUBTITLE, APP_ICON, APP_VERSION,
    CACHE_TTL_PRICES, CACHE_TTL_MAPPING, CACHE_TTL_CHAINS,
    ITEM_GROUPS,
)
from data import ALL_ITEMS, BANK_LOCATIONS
from data.items import (
    ALL_LOGS, ALL_PLANKS, HULL_PARTS, LARGE_HULL_PARTS,
    HULL_REPAIR_KITS, ALL_ORES, ALL_BARS, KEEL_PARTS,
    LARGE_KEEL_PARTS, ALL_NAILS, ALL_CANNONBALLS,
)
from models import generate_all_chains
from services import OSRSWikiConnection, ItemIDLookup, calculate_gp_per_hour, OSRSDataCache
from ui import (
    OSRS_CSS,
    render_best_item_card,
    render_live_stat,
    create_profit_chart,
    create_category_pie,
    create_profit_histogram,
    create_roi_scatter,
    create_category_comparison,
    create_tier_category_heatmap,
    create_cost_waterfall,
    create_multi_waterfall,
)
from utils import format_gp, get_clean_item_name, get_item_icon_url

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(OSRS_CSS, unsafe_allow_html=True)


# Caching layer

@st.cache_resource
def get_api_connection() -> OSRSWikiConnection:
    return OSRSWikiConnection(user_agent=f"OSRS-Market-Tracker/{APP_VERSION}")


@st.cache_data(ttl=CACHE_TTL_MAPPING, show_spinner=False)
def fetch_item_mapping(_conn: OSRSWikiConnection) -> Dict:
    return _conn.fetch_mapping()


@st.cache_data(ttl=CACHE_TTL_PRICES, show_spinner=False)
def fetch_latest_prices(_conn: OSRSWikiConnection) -> Dict:
    return _conn.fetch_prices()


@st.cache_resource
def get_id_lookup(_mapping_hash: str, item_mapping: Dict) -> ItemIDLookup:
    return ItemIDLookup(item_mapping)


@st.cache_data(ttl=CACHE_TTL_CHAINS)
def get_all_chains() -> Dict:
    return generate_all_chains()


@st.cache_resource
def get_data_cache() -> OSRSDataCache:
    """Create the in-memory SQLite cache (persists across reruns)."""
    return OSRSDataCache()


def sync_cache(cache: OSRSDataCache, item_mapping: Dict, prices: Dict):
    """Load API data into the SQLite cache and register tracked item groups."""
    if cache.is_loaded:
        cache.load_prices(prices)
        return

    cache.load_item_mapping(item_mapping)
    cache.load_prices(prices)

    # Register item groups for extensibility
    group_data = {
        "logs": ALL_LOGS,
        "planks": ALL_PLANKS,
        "hull_parts": HULL_PARTS,
        "large_hull_parts": LARGE_HULL_PARTS,
        "hull_repair_kits": HULL_REPAIR_KITS,
        "ores": ALL_ORES,
        "bars": ALL_BARS,
        "keel_parts": KEEL_PARTS,
        "large_keel_parts": LARGE_KEEL_PARTS,
        "nails": ALL_NAILS,
        "cannonballs": ALL_CANNONBALLS,
        "sailing": ALL_ITEMS,
    }

    for group_key, items in group_data.items():
        cache.load_tracked_items(items, group_key)

    cache.is_loaded = True


def main():
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(APP_TITLE)
        st.caption(f"*{APP_SUBTITLE} — v{APP_VERSION}*")
    with col2:
        st.link_button(
            "OSRS Wiki",
            "https://oldschool.runescape.wiki/w/Sailing",
            use_container_width=True
        )

    conn = get_api_connection()

    try:
        with st.spinner("Loading market data..."):
            item_mapping = fetch_item_mapping(conn)
            prices = fetch_latest_prices(conn)
            mapping_hash = str(hash(frozenset(item_mapping.keys())))
            id_lookup = get_id_lookup(mapping_hash, item_mapping)
            all_chains = get_all_chains()
            data_cache = get_data_cache()
            sync_cache(data_cache, item_mapping, prices)
    except Exception as e:
        st.error(f"Failed to load market data from OSRS Wiki API: {e}")
        st.info("The API may be temporarily unavailable. Try refreshing in a few moments.")
        st.stop()

    # Live stats bar
    stats = data_cache.get_stats()
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.markdown(render_live_stat("Items Loaded", f"{stats['total_items']:,}"), unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(render_live_stat("Active Prices", f"{stats['prices_loaded']:,}"), unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(render_live_stat("Tracked Items", f"{stats['tracked_items']:,}"), unsafe_allow_html=True)
    with stat_cols[3]:
        st.markdown(render_live_stat("Item Groups", f"{stats['tracked_groups']}"), unsafe_allow_html=True)

    params = st.query_params

    # Sidebar
    with st.sidebar:
        st.header("Configuration")

        with st.form("config_form"):
            st.subheader("Processing Options")

            plank_options = ["Sawmill", "Plank Make", "Plank Make (Earth Staff)"]
            plank_method = st.radio(
                "Plank Method",
                plank_options,
                index=plank_options.index(
                    params.get("plank_method", "Sawmill")
                ) if params.get("plank_method") in plank_options else 0,
                horizontal=True,
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

            use_sawmill_vouchers = st.toggle(
                "Sawmill Vouchers",
                value=params.get("sawmill_vouchers", "false") == "true",
                help="Use GE-bought vouchers instead of GP for Sawmill/Plank Make"
            )

            st.divider()

            st.subheader("GP/hr Calculation")

            show_gp_hr = st.toggle(
                "Show GP/hr",
                value=params.get("show_gp_hr", "false") == "true",
                help="Show gold per hour estimates"
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
                    help="Banking location"
                )

                selected_bank = BANK_LOCATIONS[bank_location]
                st.caption(f"*{selected_bank.total_overhead:.0f}s overhead | Req: {selected_bank.requirements}*")

                use_stamina = True
                if selected_bank.stamina_dependent:
                    use_stamina = st.toggle(
                        "Using Stamina Potions",
                        value=params.get("use_stamina", "true") == "true",
                        help="~30% travel time reduction"
                    )

                st.caption("**Equipment**")

                has_imcando_hammer = st.toggle(
                    "Imcando Hammer",
                    value=params.get("imcando_hammer", "false") == "true",
                    help="Equipped hammer (Below Ice Mountain)"
                )

                has_amys_saw = st.toggle(
                    "Amy's Saw",
                    value=params.get("amys_saw", "false") == "true",
                    help="Equipped saw (Sailing reward)"
                )

                has_plank_sack = st.toggle(
                    "Plank Sack",
                    value=params.get("plank_sack", "false") == "true",
                    help="+28 planks (Mahogany Homes)"
                )

                has_smithing_outfit = st.toggle(
                    "Smiths' Uniform",
                    value=params.get("smithing_outfit", "false") == "true",
                    help="15% tick save (Giants' Foundry)"
                )

                has_coal_bag = st.toggle(
                    "Coal Bag",
                    value=params.get("coal_bag", "false") == "true",
                    help="+27 coal capacity (Motherlode Mine)"
                )
            else:
                bank_location = params.get("bank_location", "Medium (Typical)")
                use_stamina = params.get("use_stamina", "true") == "true"
                has_imcando_hammer = params.get("imcando_hammer", "false") == "true"
                has_amys_saw = params.get("amys_saw", "false") == "true"
                has_plank_sack = params.get("plank_sack", "false") == "true"
                has_smithing_outfit = params.get("smithing_outfit", "false") == "true"
                has_coal_bag = params.get("coal_bag", "false") == "true"

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
                st.query_params["coal_bag"] = str(has_coal_bag).lower()
                st.query_params["sawmill_vouchers"] = str(use_sawmill_vouchers).lower()
                st.query_params["quantity"] = str(quantity)
                st.toast("Settings applied!")

        st.divider()

        if st.button("Refresh Prices", use_container_width=True):
            st.cache_data.clear()
            st.toast("Prices refreshed!")
            st.rerun()

        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

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
        "has_coal_bag": params.get("coal_bag", "false") == "true",
        "use_sawmill_vouchers": params.get("sawmill_vouchers", "false") == "true",
    }

    tabs = st.tabs([
        "All Chains",
        "Search Items",
        "Tracked Items",
        "Best Profits",
        "Analytics"
    ])

    # Tab 1: All Chains
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

    # Tab 2: Search Items (powered by SQLite cache)
    with tabs[1]:
        st.header("Search Items")
        st.caption("*Search the full OSRS item database*")

        search_col1, search_col2, search_col3 = st.columns([3, 1, 1])
        with search_col1:
            search_term = st.text_input("Search by name", key="item_search", placeholder="e.g. Dragon, Rune, Plank...")
        with search_col2:
            members_filter = st.selectbox("Members", ["All", "Members", "F2P"], key="members_filter")
        with search_col3:
            price_filter = st.toggle("Has price only", value=True, key="price_filter")

        if search_term:
            members_only = None
            if members_filter == "Members":
                members_only = True
            elif members_filter == "F2P":
                members_only = False

            matching_items = data_cache.search_items(
                query=search_term,
                members_only=members_only,
                has_price=price_filter,
                limit=50,
            )
            total_count = data_cache.search_items_count(
                query=search_term,
                members_only=members_only,
                has_price=price_filter,
            )

            if matching_items:
                df_data = []
                for item in matching_items:
                    buy = item["buy_price"]
                    sell = item["sell_price"]
                    df_data.append({
                        "Icon": get_item_icon_url(item["name"]),
                        "ID": item["item_id"],
                        "Name": item["name"],
                        "Buy": buy,
                        "Sell": sell,
                        "Margin": buy - sell if buy and sell else 0,
                        "ROI %": ((sell - buy) / buy * 100) if buy > 0 else 0,
                        "Members": bool(item.get("members", 0)),
                    })

                st.dataframe(
                    pd.DataFrame(df_data),
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
                        "Members": st.column_config.CheckboxColumn("P2P"),
                    }
                )
                st.caption(f"Showing {len(matching_items)} of {total_count} results")
            else:
                st.info("No items found.")

    # Tab 3: Tracked Items (by group, using SQLite cache)
    with tabs[2]:
        st.header("Tracked Items")

        available_groups = data_cache.get_tracked_groups()
        group_labels = {k: v for k, v in ITEM_GROUPS.items() if k in available_groups}
        group_labels["all"] = "All Tracked Items"

        selected_group_label = st.selectbox(
            "Item Group",
            list(group_labels.values()),
            key="tracked_group",
        )

        # Reverse lookup key from label
        selected_group_key = "all"
        for k, v in group_labels.items():
            if v == selected_group_label:
                selected_group_key = k
                break

        tracked = data_cache.get_tracked_items(selected_group_key)

        if tracked:
            data = []
            for item in tracked:
                data.append({
                    "Icon": get_item_icon_url(item["name"]),
                    "ID": item["item_id"],
                    "Name": item["name"],
                    "Group": ITEM_GROUPS.get(item.get("item_group", ""), item.get("item_group", "")),
                    "Buy": item["buy_price"],
                    "Sell": item["sell_price"],
                    "Margin": item["margin"],
                    "ROI %": ((item["sell_price"] - item["buy_price"]) / item["buy_price"] * 100) if item["buy_price"] > 0 else 0,
                    "Active": bool(item["buy_price"] or item["sell_price"])
                })

            df = pd.DataFrame(data)

            col_config = {
                "Icon": st.column_config.ImageColumn("Icon", width="small"),
                "ID": st.column_config.NumberColumn("ID", format="%d"),
                "Name": st.column_config.TextColumn("Name", width="medium"),
                "Buy": st.column_config.NumberColumn("Buy Price", format="%d gp"),
                "Sell": st.column_config.NumberColumn("Sell Price", format="%d gp"),
                "Margin": st.column_config.NumberColumn("Margin", format="%d gp"),
                "ROI %": st.column_config.NumberColumn("ROI", format="%.1f%%"),
                "Active": st.column_config.CheckboxColumn("Active"),
            }

            # Hide group column when viewing a specific group
            if selected_group_key != "all":
                col_config["Group"] = None

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config=col_config,
            )

            active = sum(1 for d in data if d['Active'])
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Items with Prices", f"{active}/{len(data)}")
            with col2:
                if active > 0:
                    avg_margin = sum(d['Margin'] for d in data if d['Margin']) / active
                    st.metric("Avg Margin", format_gp(avg_margin))
            with col3:
                st.metric("Item Group", selected_group_label)

    # Tab 4: Best Profits
    with tabs[3]:
        st.header("Most Profitable Chains")

        all_results = []

        with st.spinner("Calculating..."):
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

    # Tab 5: Analytics
    with tabs[4]:
        st.header("Profit Analytics")

        st.markdown("##### Filters")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            exclude_dragon = st.toggle("Exclude Dragon Items", value=True, help="Dragon items are extreme outliers")
        with filter_col2:
            use_per_item = st.toggle("Show Per-Item Profit", value=False)
        with filter_col3:
            filter_outliers = st.toggle("Filter Outliers", value=False, help="Remove values beyond 1.5x IQR")

        # Collect rich data for all charts (including cost breakdown fields)
        all_results_for_charts = []
        all_raw_results = {}  # chain name -> full calculate() result for waterfall
        quantity_val = config.get("quantity", 1)

        for cat, cat_chains in all_chains.items():
            for chain in cat_chains:
                if exclude_dragon and "dragon" in chain.name.lower():
                    continue

                result = chain.calculate(prices, config, id_lookup)
                if "error" not in result:
                    profit = result["net_profit"]
                    display_profit = profit / quantity_val if (use_per_item and quantity_val > 0) else profit

                    all_results_for_charts.append({
                        "Category": cat,
                        "Item": chain.name,
                        "ROI %": result['roi'] if result['roi'] != float('inf') else None,
                        "_profit_raw": display_profit,
                        "_raw_cost": result["raw_material_cost"],
                        "_proc_cost": result["processing_costs"],
                        "_tax": result["ge_tax"],
                        "_output": result["output_value"],
                    })

                    all_raw_results[chain.name] = result

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
                st.caption(f"*{filtered_count} outliers hidden*")

        if all_results_for_charts:
            profitable_results = [r for r in all_results_for_charts if r["_profit_raw"] > 0]

            # Top Profits + Category Comparison
            col1, col2 = st.columns(2)

            with col1:
                if profitable_results:
                    fig = create_profit_chart(profitable_results, top_n=10)
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = create_category_comparison(all_results_for_charts)
                st.plotly_chart(fig, use_container_width=True)

            # Tier x Category Heatmap
            st.subheader("Tier × Category Analysis")
            heatmap_fig = create_tier_category_heatmap(all_results_for_charts)
            if heatmap_fig:
                st.plotly_chart(heatmap_fig, use_container_width=True)
            else:
                st.info("Not enough tier data for heatmap")

            # Cost Breakdown Waterfall
            st.subheader("Cost Breakdown")

            chain_names = sorted(all_raw_results.keys())
            selected_chain = st.selectbox(
                "Select chain to inspect",
                chain_names,
                key="waterfall_chain",
            )

            if selected_chain and selected_chain in all_raw_results:
                wf_result = all_raw_results[selected_chain]
                fig = create_cost_waterfall(wf_result, selected_chain)
                st.plotly_chart(fig, use_container_width=True)

            # Multi-chain cost comparison
            st.markdown("##### Cost Structure Comparison")
            comparison_n = st.slider("Compare top N chains", 3, 10, 5, key="comparison_n")
            fig = create_multi_waterfall(all_results_for_charts, top_n=comparison_n)
            st.plotly_chart(fig, use_container_width=True)

            # ROI + Category Pie
            col1, col2 = st.columns(2)

            with col1:
                fig = create_roi_scatter(all_results_for_charts)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough ROI data")

            with col2:
                if profitable_results:
                    fig = create_category_pie(profitable_results)
                    st.plotly_chart(fig, use_container_width=True)

            # Histogram
            profit_label = "Per-Item Profit" if use_per_item else f"Batch Profit (qty: {quantity_val})"
            st.subheader(f"Distribution: {profit_label}")
            profits = [r["_profit_raw"] for r in all_results_for_charts]
            fig = create_profit_histogram(profits, per_item=use_per_item)
            st.plotly_chart(fig, use_container_width=True)

            # Summary Metrics
            st.subheader("Summary")
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
