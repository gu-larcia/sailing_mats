# OSRS Sailing Materials Tracker

A Streamlit-based web application for tracking Old School RuneScape (OSRS) item prices and calculating processing chain profitability.

## Features

### 🔄 Processing Chain Calculator (Main Feature)
- Build custom processing chains with any items
- Define input/output quantities at each step
- Add processing costs (e.g., sawmill fees)
- Calculate total costs, profits, and ROI
- See materials required for any quantity

### 📊 Live Price Lookup
- Real-time prices from OSRS Wiki API
- Search any item by name
- View buy/sell prices and margins
- Calculate ROI percentages

### 📋 Watchlist
- Track specific items you care about
- Quick view of prices and margins
- Persistent across sessions

### 🔍 Item Database Search
- Search by item name or ID
- View detailed item information
- Check price availability

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/osrs-sailing-tracker.git
cd osrs-sailing-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. Push this code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and branch
5. Set the main file path to `app.py`
6. Click Deploy!

Your app will be available at:
`https://yourusername-osrs-sailing-tracker-app-xxxxx.streamlit.app`

## Usage

### Building a Processing Chain

1. Go to the "Processing Chains" tab
2. Search for your starting material (e.g., "Oak logs")
3. Add each processing step in order:
   - Set input/output quantities (e.g., 5 planks → 1 hull part)
   - Add any processing costs
4. View the complete analysis with profits and ROI

### Example: Oak Wood Processing
1. Add "Oak logs" (Input: 1, Output: 1)
2. Add "Oak plank" (Input: 1, Output: 1, Cost: 250gp)
3. Add "Oak hull parts" (Input: 5, Output: 1)
4. Enter quantity to calculate total costs and profits

## API Information

This app uses the OSRS Wiki Real-time Prices API:
- Base URL: `https://prices.runescape.wiki/api/v1/osrs`
- No authentication required
- 5-minute price updates
- Cached for performance

## Tech Stack

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Requests**: API calls
- **Python 3.8+**: Core language

## Contributing

Feel free to submit issues or pull requests to improve the tracker!

## License

MIT License - Use freely for any purpose

## Disclaimer

This is a fan-made tool. Old School RuneScape is a trademark of Jagex Ltd.
