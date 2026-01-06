# OSRS Sailing Materials Tracker v4.7

A comprehensive Streamlit dashboard for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices.

![OSRS Sailing](https://oldschool.runescape.wiki/images/Sailing_icon.png)

## What's New in v4.7 (Research-Optimized)

This version implements improvements based on comprehensive research of the OSRS Wiki API and game mechanics:

### ✅ API Best Practices
- **Single `/latest` call** for all ~3,700 items (no per-item loops)
- **Custom User-Agent** header (default user-agents are blocked)
- **5-minute minimum poll interval** respected
- **Optional osrs-prices package support** for cleaner code

### ✅ Verified Game Mechanics
- All crafting ratios confirmed against OSRS Wiki
- Timing verification system distinguishes wiki-verified vs estimated data
- Equipment effects documented and implemented correctly

### ✅ Timing Data Transparency
- Wiki-verified timings marked with ✓
- Estimated timings display warnings to users
- Hull parts crafting timing noted as undocumented

---

## Features

### Core Functionality
- **Real-time GE Prices**: Fetches live prices from the OSRS Wiki API
- **Processing Chain Analysis**: Calculates profit/loss for all material processing chains
- **GP/hr Estimates**: Detailed time-based profitability calculations
- **Interactive Charts**: Plotly visualizations with OSRS-themed styling
- **Timing Verification**: Clear indication of verified vs estimated timing data

### Supported Processing Chains

| Category | Ratio | Status |
|----------|-------|--------|
| Planks (7 tiers) | 1 log → 1 plank | ✅ Verified |
| Hull Parts | 5 planks → 1 part | ✅ Verified |
| Large Hull Parts | 5 parts → 1 large | ✅ Verified |
| Keel Parts | 5 bars → 1 part | ✅ Verified |
| Dragon Keel Parts | 2 sheets → 1 part | ✅ Verified |
| Large Keel Parts | 5/2 parts → 1 large | ✅ Verified |
| Nails | 1 bar → 15 nails | ✅ Verified |
| Cannonballs | 1 bar → 4 balls | ✅ Verified |
| Cannonballs (Double) | 2 bars → 8 balls | ✅ Verified |

### Equipment Support

| Equipment | Effect | Source |
|-----------|--------|--------|
| Imcando Hammer | Equippable hammer, saves inventory slot | Ruins of Camdozaal |
| Amy's Saw | Equippable saw, works in weapon/off-hand | 500 Carpenter points |
| Plank Sack | +28 plank capacity | Mahogany Homes |
| Smiths' Uniform | 15% chance to save 1 tick | Giants' Foundry |
| Ancient Furnace | 2x cannonball speed (87 Sailing) | Grimstone island |

---

## Timing Data Reference

### ✅ Wiki-Verified Timings

| Activity | Ticks | Time | Notes |
|----------|-------|------|-------|
| Anvil smithing | 5 | 3.0s | Reduced to ~4 with Smiths' Uniform |
| Cannonball smelting | 8 | 4.8s | Halved by Ancient Furnace |
| Plank Make (manual) | 3 | 1.8s | ~1,850 casts/hour |
| Plank Make (auto) | 6 | 3.6s | ~1,000 casts/hour |
| Nail output | - | - | 15 per bar |

### ⚠️ Estimated Timings

| Activity | Estimated Ticks | Notes |
|----------|-----------------|-------|
| Hull parts crafting | ~4 | Undocumented in wiki, needs in-game testing |
| Large hull assembly | ~3 | Undocumented in wiki |

---

## Installation

```bash
# Clone or download the project
git clone https://github.com/yourname/osrs-sailing-tracker.git
cd osrs-sailing-tracker

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Optional: Install osrs-prices for cleaner API access
pip install osrs-prices

# Run the application
streamlit run app.py
```

---

## Project Structure

```
osrs_sailing_tracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
├── config/                # Application configuration
│   ├── __init__.py
│   └── settings.py        # Version, cache TTLs, defaults
│
├── data/                  # Static data and constants
│   ├── __init__.py
│   ├── items.py           # Item IDs (verified against /mapping)
│   ├── costs.py           # Sawmill/Plank Make costs
│   ├── timings.py         # Activity timings with verification status
│   └── locations.py       # Bank location data
│
├── models/                # Core data models
│   ├── __init__.py
│   ├── dataclasses.py     # ChainStep, ProcessingChain
│   └── chains.py          # Chain generation (verified ratios)
│
├── services/              # Business logic and API
│   ├── __init__.py
│   ├── api.py             # Wiki API + Weird Gloop + optional packages
│   ├── lookup.py          # Item ID lookup with Sailing filtering
│   └── calculations.py    # GP/hr with timing verification
│
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── styles.py          # OSRS-themed CSS
│   ├── components.py      # Cards, badges, timing warnings
│   └── charts.py          # Plotly visualizations
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── formatting.py      # GP formatting, name cleaning
│   └── colors.py          # Tier colors (metal/wood/category)
│
└── pages/                 # Reserved for future multi-page support
    └── __init__.py
```

---

## API Reference

### Primary API: OSRS Wiki Prices

```
Base URL: https://prices.runescape.wiki/api/v1/osrs
```

| Endpoint | Purpose | Notes |
|----------|---------|-------|
| `/mapping` | Item metadata | IDs, names, buy limits, alch values |
| `/latest` | Current prices | High/low for all ~3,700 items |
| `/5m` | 5-min averages | Includes volume data |
| `/1h` | 1-hour averages | Includes volume data |
| `/timeseries` | Historical | Up to 365 data points |

**Requirements:**
- Custom User-Agent header (python-requests blocked)
- No API key needed
- Don't poll faster than 5-minute refresh

### Historical API: Weird Gloop

```
Base URL: https://api.weirdgloop.org/exchange/history/osrs
```

Provides 90-day and full history with official GE prices (not RuneLite data).

### Optional Python Packages

| Package | Version | Notes |
|---------|---------|-------|
| osrs-prices | 0.1.0+ | Purpose-built for Wiki API |
| rswiki-wrapper | 0.0.6+ | Wraps both APIs |
| osrsreboxed | 2.3.33+ | Item database (27+ properties) |

---

## URL Parameters

Share configurations via URL:

```
?plank_method=Sawmill
&self_collected=false
&ancient_furnace=true
&show_gp_hr=true
&bank_location=Deepfin+Point
&imcando_hammer=true
&amys_saw=true
&plank_sack=true
&smithing_outfit=true
&quantity=100
```

---

## Known Limitations

1. **Hull parts timing**: Crafting tick rate at Shipwrights' Workbench is undocumented in the wiki. The application uses an estimate of ~4 ticks based on similar Construction activities. In-game testing recommended for precise GP/hr calculations.

2. **Sailing item IDs**: Python packages don't yet have native Sailing support (skill launched Nov 19, 2025). Item IDs are queried directly from `/mapping` and maintained in `data/items.py`.

3. **Dragon cannonballs**: Cannot be smithed (drop-only), not included in processing chains.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow existing code style
4. Verify data against OSRS Wiki where possible
5. Mark any estimated/unverified data clearly
6. Submit a pull request

---

## Changelog

### v4.7 - Research-Optimized Architecture
- Implemented timing verification system (wiki-verified vs estimated)
- Added new Sailing item IDs (helms: 32151-32153, cannons: 32203+, keel pieces: 32189-32190)
- Enhanced API service with best practices (single /latest call, proper User-Agent)
- Added optional osrs-prices package support
- Added Weird Gloop historical API integration
- Improved user transparency for estimated timing data
- Updated documentation with research findings

### v4.6 - Modular Architecture
- Refactored into modular package structure
- Separated concerns: data, models, services, UI
- Added comprehensive type hints and documentation

### Previous versions
- See commit history for earlier changes

---

## Credits

- **OSRS Wiki Team**: For the excellent Prices API and documentation
- **RuneLite**: For real-time price data
- **Jagex**: For Old School RuneScape
- **Streamlit**: For the web framework

---

## License

MIT License - See LICENSE file for details.

---

*"For the crafty sailor!"* ⛵
