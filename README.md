# OSRS Sailing Materials Tracker v4.6

Streamlit dashboard for Sailing skill materials with live Grand Exchange prices.

*"For the crafty sailor!"*

## Features

- Live GE prices from OSRS Wiki API
- Profit/loss calculations for all processing chains
- GP/hr estimates with equipment modifiers
- Plotly charts

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
osrs_sailing_tracker/
├── app.py                 # Main application
├── requirements.txt
├── config/                # App settings
├── data/                  # Item IDs, costs, timings, locations
├── models/                # ProcessingChain, ChainStep
├── services/              # API client, lookups, calculations
├── ui/                    # Styles, components, charts
└── utils/                 # Formatting, colors
```

## Installation

```bash
cd osrs_sailing_tracker
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Open http://localhost:8501
2. Configure processing options in sidebar
3. Browse tabs for different views

### URL Parameters

Settings persist via URL:
```
?plank_method=Sawmill&self_collected=false&show_gp_hr=true&quantity=100
```

## API

### OSRS Wiki Prices API

- Base: `https://prices.runescape.wiki/api/v1/osrs`
- No API key required
- Requires User-Agent header
- Endpoints: `/mapping`, `/latest`

### Cache TTLs

- Prices: 60s
- Item mappings: 5min
- Chain definitions: 1hr

## Game Mechanics

### Crafting Ratios

| Activity | Input | Output |
|----------|-------|--------|
| Hull Parts | 5 planks | 1 part |
| Large Hull Parts | 5 parts | 1 large |
| Keel Parts | 5 bars | 1 part |
| Dragon Keel Parts | 2 sheets | 1 part |
| Nails | 1 bar | 15 nails |
| Cannonballs | 1 bar | 4 balls |
| Cannonballs (Double) | 2 bars | 8 balls |

### Tick Timings

| Activity | Base | With Bonus |
|----------|------|------------|
| Smithing | 5 ticks | ~4.25 (Smiths' Uniform) |
| Cannonballs | 9 ticks | ~4.5 (Ancient Furnace) |
| Plank Make | 3 ticks | - |

## Changelog

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
