# OSRS Market Tracker v5.1

Streamlit dashboard for OSRS item tracking with live Grand Exchange prices. Currently focused on Sailing skill materials with architecture designed to expand to all tradable items.

*"Sailing Materials & Beyond"*

## Features

- Live GE prices from OSRS Wiki API
- In-memory SQLite cache for fast item search and filtering
- Profit/loss calculations for all processing chains
- GP/hr estimates with equipment modifiers
- Dark OSRS-themed UI
- Extensible item group tracking system
- Plotly charts with dark theme

### Supported Processing Chains

**Single-step chains** (buy input, process, sell output):

- **Planks**: Normal through Rosewood (7 tiers). Sawmill, Plank Make, and Sawmill Voucher cost methods.
- **Hull Parts**: All wood tiers, regular and large
- **Hull Repair Kits**: All tiers
- **Keel Parts**: All metal tiers including Dragon, regular and large
- **Nails**: All metal tiers (15 per bar)
- **Cannonballs**: All metal tiers, single and double mould
- **Bar Smelting**: All standard bars via regular Furnace and Blast Furnace (half coal)

**Extended chains** (buy raw materials, produce intermediates, sell final product):

- **Hull Parts (from Log)**: Log -> Plank -> Hull Parts
- **Large Hull Parts (from Log)**: Log -> Plank -> Hull Part -> Large Hull Part (25 logs per large part)
- **Repair Kits (from Log)**: Log -> Plank + GE nails + paste -> Kit
- **Nails (from Ore)**: Ore -> Bar (Furnace/BF) -> Nails
- **Keel Parts (from Ore)**: Ore -> Bar (Furnace/BF) -> Keel Parts
- **Cannonballs (from Ore)**: Ore -> Bar (Furnace/BF) -> Cannonballs
- **Large Keel Parts (from Bar)**: 25 GE-bought bars -> 5 Keel Parts -> 1 Large Keel Part
- **Large Keel Parts (from Ore)**: Ore -> Bar (Furnace/BF) -> Keel -> Large Keel (full pipeline)

Extended chains mark intermediate products as self-obtained so they are costed from raw materials rather than GE buy price.

### Equipment Support

- **Imcando Hammer**: Equipped hammer, saves inventory slot
- **Amy's Saw**: Equipped saw (500 Carpenter points)
- **Plank Sack**: +28 plank capacity
- **Smiths' Uniform**: 15% tick save chance
- **Ancient Furnace**: 2x smithing speed (87 Sailing)
- **Coal Bag**: +27 coal capacity (Blast Furnace)

## Project Structure

```
sailing_mats/
├── app.py                 # Main application
├── requirements.txt
├── config/                # App settings, item groups
├── data/                  # Item IDs, costs, timings, locations
├── models/                # ProcessingChain, ChainStep, chain generation
├── services/              # API client, lookups, calculations, SQLite cache
├── ui/                    # Dark OSRS styles, components, charts
└── utils/                 # Formatting, colors
```

## Installation

```bash
cd sailing_mats
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
streamlit run app.py
```

### Tabs

- **All Chains**: Browse processing chains by category
- **Search Items**: Search the full OSRS item database (SQLite-powered)
- **Tracked Items**: View items by group (logs, bars, planks, etc.)
- **Best Profits**: Top profitable chains sorted
- **Analytics**: Charts and profit distribution

### URL Parameters

Settings persist via URL:
```
?plank_method=Sawmill&self_collected=false&show_gp_hr=true&quantity=100
```

## Architecture

### SQLite Cache Layer

The app uses an in-memory SQLite database (`:memory:`) cached within Streamlit's `@st.cache_resource` for fast queryable access to item data and prices. Tables include:

- `items`: Full OSRS item catalog from Wiki API
- `prices`: Latest buy/sell prices
- `tracked_items`: Items organized into named groups

This enables SQL-powered search, filtering, and aggregation without requiring a persistent local database.

### Item Groups

Items are organized into extensible groups defined in `config/settings.py`. New groups can be added by registering them in `ITEM_GROUPS` and loading their items into the cache.

### Processing Chain Model

Chains are defined in `models/chains.py` using `ProcessingChain` and `ChainStep` dataclasses. Each chain is a list of steps where the last step is the output (sold at GE sell price) and all preceding steps are inputs (bought at GE buy price). Multi-input recipes (e.g. plank + nails + paste) are supported.

**Extended chains** compose multiple processing stages by marking intermediate products with `is_self_obtained=True`. The backward quantity calculation propagates ratios through the step list to determine how many raw materials are needed for one unit of final output. Step quantities must be pre-scaled so these ratios resolve correctly (see `chains.py` for examples).

The `plank_method` and `use_sawmill_vouchers` config options are evaluated at calculation time in `_calculate_processing_cost`, not at chain creation time. This means the same chain definition works regardless of which plank method the user selects.

## API

### OSRS Wiki Prices API

- Base: `https://prices.runescape.wiki/api/v1/osrs`
- No API key required
- Requires User-Agent header
- Endpoints: `/mapping`, `/latest`, `/5m`, `/1h`

### Cache TTLs

- Prices: 60s
- Item mappings: 5min
- Chain definitions: 1hr

## Changelog

### v5.1

- Blast Furnace support (half coal smelting for all standard bars)
- Sawmill Voucher support (replaces GP cost for Sawmill and Plank Make)
- Extended processing chains composing multiple steps (ore to final product, log to final product)
- Coal Bag equipment toggle for Blast Furnace GP/hr
- Fixed plank_method config not affecting processing cost calculation
- Comment formatting cleanup

### v5.0

- Dark OSRS theme
- RuneScape font from RuneLite
- In-memory SQLite cache for item data
- Extensible item group tracking
- Rebranded from "Sailing Materials Tracker" to "Market Tracker"
- Redesigned search with filters (members, price availability)
- Tracked Items tab with group selector
- Live stats header bar
- Rethemed Plotly charts for dark aesthetic

### v4.6

- Refactored to modular package structure
- Separated data, models, services, UI

### v4.5

- Added GP/hr calculations
- Bank location presets
- Ancient Furnace support

### v4.0

- Initial release for Sailing skill (Nov 19, 2025)

## License

MIT
