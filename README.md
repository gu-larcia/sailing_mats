# OSRS Sailing Materials Tracker - Final Version

A comprehensive Streamlit application for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices and complete processing chain calculations.

## 🎯 Features

### Complete Item Coverage (Released November 19, 2025)
- **All 7 wood tiers**: Regular through Rosewood
- **Hull parts**: IDs 32041-32080 (regular and large)
- **Keel parts**: IDs 31999-32038 (bronze through dragon)
- **Hull repair kits**: IDs 31964-31982 (all wood tiers)
- **New metals**: Lead ore/bars, Nickel ore, Cupronickel bars
- **Dragon tier items**: Dragon nails (31406), Dragon keel parts (32017)
- **Ship cannonballs**: Bronze through Dragon (31906-31916)

### Smart Processing Chains
- **Automatic calculations** for all material conversions
- **Special ratios**: Dragon keel parts use 2:1 (not 5:1)
- **Double ammo mould support**: 8 cannonballs per bar
- **Ancient Furnace**: 4x production speed
- **Multiple plank methods**: Sawmill, Plank Make, Earth Staff variants

### Dynamic Item ID Lookup
- Automatically discovers missing item IDs from API
- Self-populates database when new items are found
- Fallback to name-based searching

### Real-time Price Analysis
- Live GE prices (60-second cache)
- Profit/loss calculations with 2% GE tax
- ROI percentages
- Best profit finder across all categories

## 📋 Complete Item Database

### Hull Parts Processing
```
5 Planks → 1 Hull Part
5 Hull Parts → 1 Large Hull Part
Total: 25 planks per Large Hull Part
```

### Keel Parts Processing
```
5 Bars → 1 Keel Part (standard metals)
1 Dragon Metal Sheet → 1 Dragon Keel Part
5 Keel Parts → 1 Large Keel Part
2 Dragon Keel Parts → 1 Large Dragon Keel Part (special!)
```

### Sawmill Costs (New Woods)
- Camphor: 2,500 gp
- Ironwood: 5,000 gp
- Rosewood: 7,500 gp

### Cannonball Production
- Regular mould: 1 bar → 4 cannonballs
- Double mould: 2 bars → 8 cannonballs (2x speed)
- Ancient Furnace: Halves production time

## 🚀 Installation

### Local Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/osrs-sailing-tracker.git
cd osrs-sailing-tracker

# Install dependencies
pip install -r requirements_final.txt

# Run the app
streamlit run app_final.py
```

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file to `app_final.py`
5. Deploy!

## 📊 Usage Examples

### Finding Profitable Chains
1. Go to "Best Profits" tab
2. Set your quantity (e.g., 1000)
3. Configure processing options:
   - Sawmill vs Plank Make
   - Double ammo mould (yes/no)
   - Ancient Furnace access
4. View top 20 most profitable items

### Sailing-Specific Items
1. Go to "Sailing Items" tab
2. Browse categories:
   - New Woods (Camphor, Ironwood, Rosewood)
   - Hull Parts (Regular and Large)
   - Dragon Items (Nails, Keel parts)
3. Check current prices and availability

### Custom Comparisons
1. Select any processing chain
2. Toggle different methods:
   - Self-obtained materials (infinite ROI)
   - Different processing methods
3. Compare profit margins

## 🔧 Technical Details

### API Integration
- Base URL: `https://prices.runescape.wiki/api/v1/osrs`
- Endpoints: `/mapping` (items), `/latest` (prices)
- Cache: 60 seconds for prices, 5 minutes for mappings

### Item ID Ranges
- Hull Parts: 32041-32080
- Keel Parts: 31999-32038
- Repair Kits: 31964-31982
- New Planks: 31432-31438
- New Logs: 32902-32910
- Ship Cannonballs: 31906-31916

### Special Mechanics
- Dragon keel parts: 2:1 ratio (not 5:1 like others)
- Jatoba logs: Quest-only, cannot be planked
- Dragon items: Require Dragon Forge (Ancient Cavern)
- Double ammo mould: 2,000 Foundry Reputation required

## 📈 Profit Optimization Tips

1. **Rosewood Processing**: Highest tier = highest margins
2. **Dragon Items**: Limited supply = premium prices
3. **Double Ammo Mould**: Essential for cannonball profits
4. **Self-Obtained**: Cutting your own logs = infinite ROI
5. **Bulk Processing**: Higher quantities reduce per-item costs

## 🐛 Known Issues

- Some Sailing items may not have stable prices yet
- Dragon cannonballs are drop-only (cannot be smithed)
- Jatoba logs cannot be processed into planks

## 📝 License

MIT License - Free for all OSRS players

## 🙏 Credits

- OSRS Wiki for item data and API
- Jagex for creating the Sailing skill
- Anthropic for development assistance

---

*Sailing skill released November 19, 2025 - All item IDs current as of December 2025*
