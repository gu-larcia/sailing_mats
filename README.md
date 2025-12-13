# OSRS Sailing Materials Tracker v4.3 - Enhanced Analytics

A comprehensive Streamlit application for tracking Old School RuneScape Sailing skill materials with real-time Grand Exchange prices, complete processing chain calculations, and **gold per hour estimates**.

## What's New in v4.3

This version significantly improves the **Analytics tab** with better chart design, proper legends, and more insightful visualizations.

### Enhanced Analytics Charts
- **ROI vs Profit Scatter**: Now has a proper category legend that exports correctly, annotations for notable items, and quadrant reference lines
- **Distribution Analysis**: Combines box plot + histogram, shows profitable vs unprofitable chains separately, includes statistical annotations (median, quartiles)
- **Category Comparison**: Now shows Best/Median/Average profits, sorted by performance, with value labels
- **Pie Chart**: Consistent category colors across all charts, center total annotation, chain count in hover
- **Consistent Color Scheme**: All charts use the same category-to-color mapping for easy cross-referencing

### Visual Polish
- Subtitles on key charts explaining what they show
- Better axis formatting for GP values  
- Improved hover templates with more context
- Annotations highlighting top performers
- Cleaner grid lines and borders

## What's New in v4.2

This version adds **proper GP/hr calculations** with separate toggles for the Imcando Hammer and Crystal Saw, so you can see exactly how your tool unlocks affect your profits.

### GP/hr System
- **Per-activity calculations**: Each crafting activity (hull parts, keel parts, nails, cannonballs, planks) has its own timing data based on game ticks
- **Tool-aware inventory**: The system accounts for which tools you need and whether you have the equipped versions
- **Bank speed presets**: Fast (8s), Medium (15s), Slow (25s) to match your setup
- **Ancient Furnace support**: Halves smithing time when enabled

### Equipped Tools (Separate Toggles)
- **Imcando Hammer**: Saves 1 inventory slot for smithing activities (keel parts, nails). Obtained from Below Ice Mountain quest.
- **Crystal Saw**: Saves 1 inventory slot for hull crafting. Obtained from Eyes of Glouphrie quest.
- **Both together**: Hull parts need both tools - each one you have equipped saves a slot (up to 2 total)
- **Defaults to OFF**: These are meaningful unlocks, not assumed

### Enhanced Chain Details
- When GP/hr is enabled, the chain details expander shows a full breakdown:
  - Effective inventory slots
  - Items per trip
  - Seconds per trip
  - Trips per hour
  - Tool status (equipped vs inventory)
  - Slots saved by equipped tools

### URL Parameters
New shareable parameters:
```
?imcando_hammer=true&crystal_saw=true&show_gp_hr=true&bank_speed=Fast
```

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

### GP/hr Calculation Model
The GP/hr system calculates hourly profit based on:

```
1. Effective Inventory = 28 - tool_slots - other_slots
   - Hammer: 1 slot (saved if Imcando Hammer equipped)
   - Saw: 1 slot (saved if Crystal Saw equipped)
   - Ammo mould: 1 slot (not equippable)
   
2. Items per Trip = floor(Effective Inventory / materials_per_craft) Ã— output_per_craft

3. Time per Trip = (actions Ã— ticks Ã— 0.6s) + bank_time
   - Ancient Furnace halves the crafting portion for smithing

4. Trips per Hour = 3600 / Time per Trip

5. GP per Hour = Trips per Hour Ã— Items per Trip Ã— Profit per Item
```

### Activity Timing Data
| Activity | Ticks/Action | Materials | Output | Tools Needed |
|----------|--------------|-----------|--------|--------------|
| Hull Parts | 4 | 5 planks | 1 | Hammer + Saw |
| Large Hull Parts | 3 | 5 hull parts | 1 | Hammer + Saw |
| Keel Parts | 4 | 5 bars | 1 | Hammer |
| Dragon Keel Parts | 4 | 2 sheets | 1 | Hammer |
| Nails | 4 | 1 bar | 15 | Hammer |
| Cannonballs | 9 | 1 bar | 4 (or 8) | Mould |
| Sawmill Planks | ~1 | 1 log | 1 | None |
| Plank Make | 3 | 1 log | 1 | Runes |

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

### v4.3 (Enhanced Analytics Edition)
- **ROI vs Profit scatter redesign**: Separate traces per category for proper legend support on export
- **Automatic item annotations**: Top profit and ROI items are labeled on the scatter plot
- **Distribution histogram overhaul**: Box plot + histogram combo showing profitable/unprofitable split
- **Statistical annotations**: Median, Q1, Q3 stats displayed in an info box
- **Smart binning**: Histogram bin sizes adapt to data range automatically
- **Category comparison upgrade**: Now shows Best/Median/Average with sorted categories
- **Consistent color mapping**: All charts use same category colors for cross-reference
- **Pie chart improvements**: Center total display, chain counts in hover, consistent colors
- **Chart subtitles**: Added explanatory subtitles to key visualizations
- **Quadrant reference lines**: ROI scatter shows 0% profit/ROI reference lines when applicable

### v4.2 (GP/hr with Equipped Tools)
- **GP/hr calculations**: Full gold-per-hour estimates for all craftable items
- **Imcando Hammer toggle**: Separate setting for equipped hammer (saves 1 slot on smithing)
- **Crystal Saw toggle**: Separate setting for equipped saw (saves 1 slot on hull crafting)
- **Tool defaults OFF**: These are unlocks players earn, not assumed equipment
- **Ancient Furnace integration**: Properly halves smithing time in GP/hr calculations
- **Bank speed presets**: Fast/Medium/Slow banking options
- **Chain details GP/hr breakdown**: Shows full efficiency stats when expanded
- **Activity timing data**: Each activity type has accurate tick-based timing
- **URL shareable tool settings**: `?imcando_hammer=true&crystal_saw=true`

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
