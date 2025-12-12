# OSRS Sailing Materials Tracker v4.0 - Enhanced Streamlit Edition

A comprehensive Streamlit application for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices and complete processing chain calculations.

## 🆕 What's New in v4.0

This version takes full advantage of Streamlit's built-in modules for a better user experience, plus a complete **OSRS-themed visual overhaul**!

### 🎨 OSRS Visual Theme
- **Parchment sidebar** with driftwood borders
- **Ocean-dark main background** evoking the high seas
- **Gold accents** on headers, buttons, and metrics
- **Cinzel & Crimson Text fonts** for that medieval RPG feel
- **OSRS-colored charts**: Gold for profits, Dragon red for losses, Rune blue for comparisons

### Streamlit Features Now Utilized

| Feature | Usage | Benefit |
|---------|-------|---------|
| `st.status()` | Data loading feedback | Clear progress indication |
| `st.toast()` | Settings/refresh notifications | Non-intrusive alerts |
| `st.form()` | Grouped sidebar inputs | Prevents constant reruns |
| `st.toggle()` | Modern boolean switches | Cleaner UI than checkboxes |
| `st.query_params` | URL state persistence | Shareable configurations |
| `st.cache_resource` | Singleton class caching | Better memory efficiency |
| `st.link_button()` | External Wiki links | Easy navigation |
| `st.expander()` | Collapsible chain details | Cleaner interface |
| `st.column_config` | Enhanced table formatting | Progress bars, number formatting |
| `st.plotly_chart()` | Interactive visualizations | Profit analysis charts |
| `st.spinner()` | Search loading states | Better UX feedback |
| `st.metric()` | Summary statistics | At-a-glance insights |

### New Analytics Tab
- **Profit Bar Charts**: Visual comparison of top profitable chains
- **Category Pie Chart**: Distribution of profits by category (small slices grouped into "Other")
- **Category Comparison**: Average vs Best profit per category
- **ROI vs Profit Scatter**: Find high-ROI opportunities
- **Profit Histogram**: Overall profit distribution
- **Dragon Filter**: Toggle to exclude dragon items and see non-outlier trends
- **Voyage Summary**: Comprehensive overview

### Improved Data Tables
- Number formatting with GP units
- Progress bars for ROI percentages
- Checkbox columns for status indicators
- Sortable columns with proper data types

### URL-Shareable Settings
Share your configuration with others via URL parameters:
```
https://your-app.streamlit.app/?plank_method=Sawmill&double_mould=true&quantity=1000
```

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

### Real-time Price Analysis
- Live GE prices (60-second cache)
- Profit/loss calculations with 2% GE tax
- ROI percentages with visual progress bars
- Best profit finder across all categories

## 🚀 Installation

### Local Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/osrs-sailing-tracker.git
cd osrs-sailing-tracker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_improved.py
```

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file to `app_improved.py`
5. Deploy!

## 📊 Usage

### Configuration (Sidebar)
1. **Plank Method**: Choose between Sawmill, Plank Make, or Plank Make with Earth Staff
2. **Double Ammo Mould**: Toggle for 2x cannonball production
3. **Ancient Furnace**: Toggle for faster smithing
4. **Quantity**: Set batch size for calculations
5. Click "Apply Settings" to update calculations

### Tabs Overview

#### 📊 All Chains
- Browse processing chains by category
- View detailed cost breakdowns
- Expand for step-by-step chain analysis

#### 🔍 Search Items
- Search any item by name
- See buy/sell prices and margins
- Identify Sailing-specific items (⚓ marker)

#### ⚓ Sailing Items
- Browse Sailing-specific categories
- Quick access to new content items
- Monitor item availability

#### 📈 Best Profits
- Top 20 most profitable chains
- Filter by profitable only
- Best item per category highlights

#### 📉 Analytics
- Visual profit comparisons
- Category profit distribution
- Profit histogram
- Summary statistics

## 🔧 Technical Details

### API Integration
- Base URL: `https://prices.runescape.wiki/api/v1/osrs`
- Endpoints: `/mapping` (items), `/latest` (prices)
- Cache: 60 seconds for prices, 5 minutes for mappings

### Caching Strategy
```python
@st.cache_resource  # For singleton instances (API connection, ID lookup)
@st.cache_data(ttl=60)  # For price data (60s refresh)
@st.cache_data(ttl=300)  # For item mappings (5min refresh)
@st.cache_data(ttl=3600)  # For chain generation (1hr, static data)
```

### State Management
- `st.query_params` for URL-shareable configuration
- `st.form()` for batched input handling
- Efficient reruns with targeted caching

## 📈 Profit Optimization Tips

1. **Rosewood Processing**: Highest tier = highest margins
2. **Dragon Items**: Limited supply = premium prices
3. **Double Ammo Mould**: Essential for cannonball profits
4. **Self-Obtained**: Cutting your own logs = infinite ROI
5. **Bulk Processing**: Higher quantities reduce per-item costs

## 🛠 Known Issues

- Some Sailing items may not have stable prices yet
- Dragon cannonballs are drop-only (cannot be smithed)
- Jatoba logs cannot be processed into planks

## 📝 Changelog

### v4.0 (Enhanced Streamlit Edition)
- **OSRS Visual Theme**: Parchment sidebar, ocean background, gold accents
- **Custom fonts**: Cinzel (headers) and Crimson Text (body)
- **New charts**: Category comparison bars, ROI vs Profit scatter plot
- **OSRS-themed chart colors**: Gold, bronze, rune blue, dragon red
- **Dragon Filter**: Toggle to exclude dragon item outliers from analytics
- **Improved Pie Chart**: Small slices grouped into "Other" for clarity
- **No Emojis**: Clean professional look using OSRS Wiki icon for page
- Added `st.toast()` for notifications
- Added `st.form()` for grouped inputs
- Added `st.toggle()` for modern switches
- Added `st.query_params` for URL sharing
- Added `st.cache_resource` for class instances
- Added `st.link_button()` for Wiki links
- Added `st.expander()` for chain details
- Added Plotly charts for analytics
- Added Analytics tab with visualizations
- Improved table formatting with `st.column_config`
- Added progress bars for ROI display
- Fixed "Best in Category" display - now uses table format instead of cramped metrics
- Fixed dropdown contrast issues (dark text on light background)

### v3.1 (Original)
- Basic Streamlit implementation
- Core processing chain calculations
- Real-time GE price fetching

## 📄 License

MIT License - Free for all OSRS players

## 🙏 Credits

- OSRS Wiki for item data and API
- Jagex for creating the Sailing skill
- Streamlit for the amazing framework

---

*Sailing skill released November 19, 2025 - All item IDs current as of December 2025*
