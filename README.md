# OSRS Sailing Materials Tracker v4.7

Streamlit dashboard for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices.

## Features

### Core
- Real-time GE prices from OSRS Wiki API
- Processing chain profitability analysis
- GP/hr estimates with equipment bonuses
- OSRS-themed Plotly visualizations

### Processing Chains
- **Planks**: 7 wood tiers (Normal → Rosewood)
- **Hull Parts**: All wood tiers, regular and large
- **Hull Repair Kits**: All tiers with material requirements
- **Keel Parts**: All metal tiers including Dragon
- **Nails**: All metal tiers (15 per bar)
- **Cannonballs**: All metal tiers (single and double mould)

### v4.7 Additions
- **Yarns**: Linen (12 Crafting), Hemp (39), Cotton (73) via spinning wheel
- **Bolts**: Linen, Canvas, Cotton via loom (2 yarn → 1 bolt)
- **Full Textile Chains**: Raw material → yarn → bolt complete paths
- **Coral Products**: Anti-odour salt, Super fishing/hunter potions, Armadyl brew, Haemostatic dressing

### Equipment Support
- Imcando Hammer (equippable, saves inventory slot)
- Amy's Saw (500 Carpenter points)
- Plank Sack (+28 plank capacity)
- Smiths' Uniform (15% tick save)
- Ancient Furnace (2x smithing speed, 87 Sailing)

## Project Structure

```
osrs_sailing/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── config/               
│   └── settings.py        # App constants, cache TTLs
├── data/                 
│   ├── items.py           # Item ID dictionaries (21 new in v4.7)
│   ├── costs.py           # Sawmill/Plank Make costs
│   ├── timings.py         # Activity tick timings
│   └── locations.py       # Bank location data
├── models/               
│   ├── dataclasses.py     # ChainStep, ProcessingChain
│   └── chains.py          # Chain generation (4 new categories)
├── services/             
│   ├── api.py             # OSRS Wiki API client
│   ├── lookup.py          # Item ID lookup service
│   └── calculations.py    # GP/hr calculations
├── ui/                   
│   ├── styles.py          # OSRS-themed CSS
│   ├── components.py      # Reusable UI components
│   └── charts.py          # Plotly chart functions
└── utils/                
    ├── formatting.py      # GP formatting, name cleaning
    └── colors.py          # Tier colors (textile/coral added)
```

## Installation

```bash
cd osrs_sailing
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
streamlit run app.py
```

## New Item IDs (v4.7)

### Textile Seeds
| Item | ID |
|------|-----|
| Flax seed | 31541 |
| Hemp seed | 31543 |
| Cotton seed | 31545 |

### Raw Textiles
| Item | ID |
|------|-----|
| Flax | 1779 |
| Hemp | 31457 |
| Cotton boll | 31460 |

### Yarns
| Item | ID |
|------|-----|
| Linen yarn | 31463 |
| Hemp yarn | 31466 |
| Cotton yarn | 31469 |

### Bolts
| Item | ID |
|------|-----|
| Bolt of linen | 31472 |
| Bolt of canvas | 31475 |
| Bolt of cotton | 31478 |

### Coral Frags
| Item | ID |
|------|-----|
| Elkhorn frag | 31511 |
| Pillar frag | 31513 |
| Umbral frag | 31515 |

### Coral
| Item | ID |
|------|-----|
| Elkhorn coral | 31481 |
| Pillar coral | 31484 |
| Umbral coral | 31487 |

### Coral Products
| Item | ID |
|------|-----|
| Anti-odour salt | 31712 |
| Haemostatic dressing (1) | 31599 |
| Super fishing potion (3) | 31605 |
| Super hunter potion (4) | 31626 |
| Armadyl brew (4) | 31650 |

## Processing Ratios

### Textiles
| Activity | Ratio | Ticks |
|----------|-------|-------|
| Spinning wheel | 1 raw → 1 yarn | 3 |
| Loom | 2 yarn → 1 bolt | 4 |

### Coral Products
| Product | Recipe |
|---------|--------|
| Anti-odour salt (15) | 1 Elkhorn coral + 5 Crab paste |
| Super fishing potion | Pillar coral + Haddock eye |
| Super hunter potion | Pillar coral + Crab paste |
| Armadyl brew | Umbral coral + Rainbow crab paste |
| Haemostatic dressing | Elkhorn coral + Squid paste + Cotton yarn |

## API

Base URL: `https://prices.runescape.wiki/api/v1/osrs`

| Endpoint | TTL | Purpose |
|----------|-----|---------|
| /mapping | 300s | Item metadata |
| /latest | 60s | Current prices |

## Changelog

### v4.7 - Textile & Coral Update
- Added 21 new tradeable items from Sailing skill update
- New categories: Yarns, Bolts, Full Textile Chains, Coral Products
- Textile processing timings (spinning wheel, loom)
- Coral product recipes (potions, anti-odour salt)
- New "Textiles & Coral" tab in UI
- Extended color system for textile/coral tiers

### v4.6 - Modular Architecture
- Refactored into modular package structure
- Separated concerns: data, models, services, UI

### v4.5 - GP/hr Update
- GP/hr calculations with equipment support
- Bank location presets
- Ancient Furnace support

## License

MIT License
