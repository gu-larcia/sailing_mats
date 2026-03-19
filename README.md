# OSRS Market Tracker v5.0

Streamlit dashboard for OSRS item tracking with live Grand Exchange prices. Currently focused on Sailing skill materials with architecture designed to expand to all tradable items.

*"Sailing Materials & Beyond"*

## Features

- Live GE prices from OSRS Wiki API
- In-memory SQLite cache for fast item search and filtering
- Profit/loss calculations for all processing chains
- GP/hr estimates with equipment modifiers
- Dark OSRS-themed UI inspired by osrsplayercount.com
- Extensible item group tracking system
- Plotly charts with dark theme

### Supported Processing Chains

- **Planks**: Normal through Rosewood (7 tiers)
- **Hull Parts**: All wood tiers, regular and large
- **Hull Repair Kits**: All tiers
- **Keel Parts**: All metal tiers including Dragon, regular and large
- **Nails**: All metal tiers (15 per bar)
- **Cannonballs**: All metal tiers, single and double mould

### Equipment Support

- **Imcando Hammer**: Equipped hammer, saves inventory slot
- **Amy's Saw**: Equipped saw (500 Carpenter points)
- **Plank Sack**: +28 plank capacity
- **Smiths' Uniform**: 15% tick save chance
- **Ancient Furnace**: 2x smithing speed (87 Sailing)

## Project Structure

```
osrs_market_tracker/
├── app.py                 # Main application
├── requirements.txt
├── config/                # App settings, item groups
├── data/                  # Item IDs, costs, timings, locations
├── models/                # ProcessingChain, ChainStep
├── services/              # API client, lookups, calculations, SQLite cache
│   └── cache.py           # In-memory SQLite data cache
├── ui/                    # Dark OSRS styles, components, charts
└── utils/                 # Formatting, colors
```

## Installation

```bash
cd osrs_market_tracker
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Open http://localhost:8501
2. Configure processing options in sidebar
3. Browse tabs for different views

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

### v5.0

- Dark OSRS theme (inspired by osrsplayercount.com)
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
