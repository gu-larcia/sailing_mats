# OSRS Sailing Materials Tracker v4.1 - Item Thumbnails Edition

A comprehensive Streamlit application for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices and complete processing chain calculations.

## What's New in v4.1

This version adds **item thumbnails** throughout the application and fixes several visual polish issues based on user feedback.

### Item Thumbnails
- **Data tables**: All item tables now show OSRS Wiki icons in the first column
- **Best item cards**: Custom HTML cards display item icons alongside names and profits
- **Chain details**: Each step in a processing chain shows the relevant item icon
- **Category tables**: Icons appear in Best Profits, Sailing Items, and Search results

### Visual Fixes
- **Fixed truncated text**: "Best Item" display now uses a custom card layout that wraps long names properly instead of cutting them off
- **Fixed pie chart labels**: Category labels now appear outside the chart to prevent overlap with the legend
- **Cleaner chart layouts**: Removed redundant legends where labels are already visible
- **Better hover states**: All charts show item names and values on hover

### Technical Improvements
- New `get_item_icon_url()` function with common naming fixes
- New `render_best_item_card()` for custom HTML item displays
- `ProcessingChain.get_output_item_name()` method for better icon matching
- Icon column uses `st.column_config.ImageColumn` with graceful fallback

## OSRS Visual Theme (from v4.0)
- **Parchment sidebar** with driftwood borders
- **Ocean-dark main background** evoking the high seas
- **Gold accents** on headers, buttons, and metrics
- **Cinzel & Crimson Text fonts** for that medieval RPG feel
- **OSRS-colored charts**: Gold for profits, Dragon red for losses, Rune blue for comparisons

## Streamlit Features Utilized

| Feature | Usage | Benefit |
|---------|-------|---------|
| `st.column_config.ImageColumn` | Item icons in tables | Visual item identification |
| `st.status()` | Data loading feedback | Clear progress indication |
| `st.toast()` | Settings/refresh notifications | Non-intrusive alerts |
| `st.form()` | Grouped sidebar inputs | Prevents constant reruns |
| `st.toggle()` | Modern boolean switches | Cleaner UI than checkboxes |
| `st.query_params` | URL state persistence | Shareable configurations |
| `st.cache_resource` | Singleton class caching | Better memory efficiency |
| `st.link_button()` | External Wiki links | Easy navigation |
| `st.expander()` | Collapsible chain details | Cleaner interface |
| `st.plotly_chart()` | Interactive visualizations | Profit analysis charts |
| `st.spinner()` | Search loading states | Better UX feedback |
| `st.metric()` | Summary statistics | At-a-glance insights |

## Features

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

## Installation

### Local Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/osrs-sailing-tracker.git
cd osrs-sailing-tracker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file to `app.py`
5. Deploy!

## Usage

### Configuration (Sidebar)
1. **Plank Method**: Choose between Sawmill, Plank Make, or Plank Make with Earth Staff
2. **Self-Collected Materials**: Toggle to set raw material costs to 0 (for ironmen or self-gatherers)
3. **Double Ammo Mould**: Toggle for 2x cannonball production
4. **Ancient Furnace**: Toggle for faster smithing
5. **Quantity**: Set batch size for calculations
6. Click "Apply Settings" to update calculations

### Tabs Overview

#### All Chains
- Browse processing chains by category
- **NEW**: Item icons in table rows
- View detailed cost breakdowns with step icons
- Expand for step-by-step chain analysis

#### Search Items
- Search any item by name
- **NEW**: Item thumbnails in search results
- See buy/sell prices and margins
- Identify Sailing-specific items

#### Sailing Items
- Browse Sailing-specific categories
- **NEW**: Visual item icons
- Quick access to sailing content
- Monitor item availability

#### Best Profits
- Top 20 most profitable chains with icons
- Filter by profitable only
- Best item per category with visual thumbnails

#### Analytics
- Visual profit comparisons
- **FIXED**: Category pie chart with outside labels
- Category profit distribution
- Profit histogram
- Summary statistics

## Technical Details

### API Integration
- Base URL: `https://prices.runescape.wiki/api/v1/osrs`
- Endpoints: `/mapping` (items), `/latest` (prices)
- Cache: 60 seconds for prices, 5 minutes for mappings

### Item Icons
Icons are fetched from the OSRS Wiki using the pattern:
```
https://oldschool.runescape.wiki/images/{Item_Name}.png
```

The app includes fallback handling for items with different image names than their in-game names.

### Caching Strategy
```python
@st.cache_resource  # For singleton instances (API connection, ID lookup)
@st.cache_data(ttl=60)  # For price data (60s refresh)
@st.cache_data(ttl=300)  # For item mappings (5min refresh)
@st.cache_data(ttl=3600)  # For chain generation (1hr, static data)
```

### URL-Shareable Settings
Share your configuration with others via URL parameters:
```
https://your-app.streamlit.app/?plank_method=Sawmill&double_mould=true&quantity=1000
```

## Profit Optimization Tips

1. **Rosewood Processing**: Highest tier = highest margins
2. **Dragon Items**: Limited supply = premium prices
3. **Double Ammo Mould**: Essential for cannonball profits
4. **Self-Obtained**: Cutting your own logs = infinite ROI
5. **Bulk Processing**: Higher quantities reduce per-item costs

## Known Issues

- Some Sailing items may not have stable prices yet
- Dragon cannonballs are drop-only (cannot be smithed)
- Jatoba logs cannot be processed into planks
- Some item icons may not load if the Wiki image name differs from the item name

## Changelog

### v4.1 (Item Thumbnails Edition)
- **Item icons**: Added OSRS Wiki thumbnails throughout all data tables
- **Fixed truncated text**: Best Item display now uses custom HTML cards that wrap text properly
- **Fixed pie chart**: Labels moved outside chart, removed redundant legend
- **Chain details icons**: Each processing step shows its item icon
- **Better icon matching**: `get_output_item_name()` method for accurate icon URLs
- **Graceful fallbacks**: Icons that fail to load are hidden cleanly
- **Custom HTML cards**: `render_best_item_card()` for rich item displays
- **Improved hover info**: Charts show clean item names without suffixes

### v4.0 (Enhanced Streamlit Edition)
- **OSRS Visual Theme**: Parchment sidebar, ocean background, gold accents
- **Custom fonts**: Cinzel (headers) and Crimson Text (body)
- **New charts**: Category comparison bars, ROI vs Profit scatter plot
- **OSRS-themed chart colors**: Gold, bronze, rune blue, dragon red
- **Dragon Filter**: Toggle to exclude dragon item outliers from analytics
- **Improved Pie Chart**: Small slices grouped into "Other" for clarity
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

### v3.1 (Original)
- Basic Streamlit implementation
- Core processing chain calculations
- Real-time GE price fetching

## License

MIT License - Free for all OSRS players

## Credits

- OSRS Wiki for item data, API, and item icons
- Jagex for creating the Sailing skill
- Streamlit for the amazing framework
- Clan feedback for v4.1 improvements

---

*Sailing skill released November 19, 2025 - All item IDs current as of December 2025*
