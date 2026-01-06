# OSRS Sailing Materials Tracker v4.6

A comprehensive Streamlit dashboard for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices.

![OSRS Sailing](https://oldschool.runescape.wiki/images/Sailing_icon.png)

## Features

### Core Functionality
- **Real-time GE Prices**: Fetches live prices from the OSRS Wiki API
- **Processing Chain Analysis**: Calculates profit/loss for all material processing chains
- **GP/hr Estimates**: Detailed time-based profitability calculations
- **Interactive Charts**: Plotly visualizations with OSRS-themed styling

### Supported Processing Chains
- **Planks**: 7 wood tiers (Normal → Rosewood)
- **Hull Parts**: All wood tiers, regular and large
- **Hull Repair Kits**: All tiers with proper material requirements
- **Keel Parts**: All metal tiers including Dragon (regular and large)
- **Nails**: All metal tiers (15 per bar)
- **Cannonballs**: All metal tiers (regular and double mould)

### Equipment Support
- **Imcando Hammer**: Equippable hammer (saves inventory slot)
- **Amy's Saw**: Equippable saw (500 Carpenter points)
- **Plank Sack**: +28 plank capacity
- **Smiths' Uniform**: 15% tick save chance
- **Ancient Furnace**: 2x smithing speed (87 Sailing)

## Project Structure

```
osrs_sailing_tracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── __init__.py           # Package metadata
│
├── config/               # Application configuration
│   ├── __init__.py
│   └── settings.py       # App constants, defaults, URL params
│
├── data/                 # Static data and constants
│   ├── __init__.py
│   ├── items.py          # Item ID dictionaries
│   ├── costs.py          # Sawmill/Plank Make costs
│   ├── timings.py        # Activity timing data
│   └── locations.py      # Bank location data
│
├── models/               # Core data models
│   ├── __init__.py
│   ├── dataclasses.py    # ChainStep, ProcessingChain
│   └── chains.py         # Chain generation functions
│
├── services/             # Business logic and API
│   ├── __init__.py
│   ├── api.py            # OSRS Wiki API client
│   ├── lookup.py         # Item ID lookup service
│   └── calculations.py   # GP/hr calculations
│
├── ui/                   # User interface components
│   ├── __init__.py
│   ├── styles.py         # OSRS-themed CSS
│   ├── components.py     # Reusable UI components
│   └── charts.py         # Plotly chart functions
│
├── utils/                # Utility functions
│   ├── __init__.py
│   ├── formatting.py     # GP formatting, name cleaning
│   └── colors.py         # Tier colors, category colors
│
└── pages/                # (Reserved for future tab modules)
    └── __init__.py
```

## Installation

```bash
# Clone or download the project
cd osrs_sailing_tracker

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Usage

### Basic Usage
1. Open the app in your browser (default: http://localhost:8501)
2. Use the sidebar to configure processing options
3. Navigate tabs to explore different views

### Configuration Options
- **Plank Method**: Sawmill, Plank Make, or Plank Make with Earth Staff
- **Self-Collected**: Set material costs to zero
- **Ancient Furnace**: Enable 2x smithing speed
- **GP/hr Mode**: Show time-based profitability

### URL Parameters
Settings persist via URL parameters for sharing:
```
?plank_method=Sawmill&self_collected=false&show_gp_hr=true&quantity=100
```

## API Reference

### OSRS Wiki Prices API
- Base URL: `https://prices.runescape.wiki/api/v1/osrs`
- No API key required
- Requires User-Agent header
- Endpoints used:
  - `/mapping` - Item metadata
  - `/latest` - Current prices

### Caching Strategy
- Prices: 60 seconds TTL
- Item mappings: 5 minutes TTL
- Chain definitions: 1 hour TTL

## Game Mechanics Reference

### Crafting Ratios (Verified)
| Activity | Input | Output |
|----------|-------|--------|
| Hull Parts | 5 planks | 1 part |
| Large Hull Parts | 5 parts | 1 large part |
| Keel Parts | 5 bars | 1 part |
| Dragon Keel Parts | 2 sheets | 1 part |
| Nails | 1 bar | 15 nails |
| Cannonballs | 1 bar | 4 balls |
| Cannonballs (Double) | 2 bars | 8 balls |

### Tick Timings
| Activity | Base Ticks | With Bonus |
|----------|------------|------------|
| Smithing | 5 ticks | 4 (Smiths' Uniform avg) |
| Cannonballs | 9 ticks | 4.5 (Ancient Furnace) |
| Plank Make | 3 ticks | - |

## Changelog

### v4.6 - Modular Architecture
- Complete refactor into modular package structure
- Separated concerns: data, models, services, UI
- Improved code organization and maintainability
- Added comprehensive documentation
- All original functionality preserved

### v4.5 - GP/hr Update
- Added GP/hr calculations with equipment support
- Bank location presets
- Ancient Furnace support
- Mobile-responsive improvements

### v4.0 - Sailing Launch
- Initial release for Sailing skill (Nov 19, 2025)
- All Sailing materials and processing chains
- Real-time GE price integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - See LICENSE file for details.

## Credits

- **OSRS Wiki Team**: For the excellent Prices API
- **Jagex**: For Old School RuneScape
- **Streamlit**: For the amazing framework

---

*"For the crafty sailor!"* ⛵
