"""
OSRS-themed CSS styles for Streamlit.

Theme inspired by:
- Parchment sidebar (like in-game interfaces)
- Ocean-dark background (nautical theme for Sailing)
- Gold accents on headers and buttons
- Cinzel & Crimson Text fonts for medieval RPG feel
"""

OSRS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --parchment: #f4e4bc;
    --parchment-dark: #e8d5a3;
    --parchment-light: #faf3e0;
    --driftwood: #8b7355;
    --driftwood-dark: #5c4d3a;
    --driftwood-light: #a08b6d;
    --gold: #ffd700;
    --gold-dark: #d4af37;
    --gold-light: #ffec80;
    --ocean-dark: #1a3a4a;
    --ocean: #2d5a6b;
    --ocean-light: #3d7a8c;
    --copper: #b87333;
    --bronze: #cd7f32;
    --rune-blue: #5dade2;
    --dragon-red: #c0392b;
}

/* Main app background */
.stApp {
    background: linear-gradient(180deg, #1a2a3a 0%, #0d1a24 50%, #1a2a3a 100%);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border-right: 4px solid var(--driftwood);
}

[data-testid="stSidebar"] * {
    color: var(--driftwood-dark) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--driftwood-dark) !important;
}

/* Headers */
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.stApp h1 {
    border-bottom: 3px solid var(--gold-dark);
    padding-bottom: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border-radius: 8px 8px 0 0;
    padding: 5px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    color: var(--parchment) !important;
    background: transparent;
    border-radius: 6px 6px 0 0;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--gold-dark) 0%, var(--copper) 100%) !important;
    color: var(--driftwood-dark) !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: linear-gradient(180deg, rgba(244,228,188,0.1) 0%, rgba(244,228,188,0.05) 100%);
    border: 2px solid var(--driftwood);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
}

[data-testid="stMetric"] label {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment) !important;
    font-size: 1.1rem !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border: 3px solid var(--driftwood);
    border-radius: 8px;
    overflow-x: auto !important;
    overflow-y: visible !important;
}

/* Buttons */
.stButton > button {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--gold) 0%, var(--gold-dark) 100%);
    color: var(--driftwood-dark) !important;
    border: 2px solid var(--copper);
    border-radius: 6px;
    font-weight: 600;
    box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(180deg, var(--gold-light) 0%, var(--gold) 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

/* Forms */
[data-testid="stForm"] {
    background: linear-gradient(180deg, rgba(139,115,85,0.2) 0%, rgba(92,77,58,0.2) 100%);
    border: 2px solid var(--driftwood);
    border-radius: 8px;
    padding: 15px;
}

/* Select boxes */
.stSelectbox > div > div {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
}

.stSelectbox > div > div > div {
    color: var(--driftwood-dark) !important;
}

.stSelectbox label {
    color: var(--parchment) !important;
}

[data-testid="stSidebar"] .stSelectbox label {
    color: var(--driftwood-dark) !important;
}

/* Inputs */
[data-testid="stSidebar"] input {
    background: var(--parchment-light) !important;
    border: 2px solid var(--driftwood) !important;
    color: var(--driftwood-dark) !important;
}

/* Expanders */
.streamlit-expanderHeader {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--driftwood) 0%, var(--driftwood-dark) 100%);
    border: 2px solid var(--gold-dark);
    border-radius: 6px;
    color: var(--gold) !important;
}

/* Link buttons */
.stLinkButton > a {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--ocean) 0%, var(--ocean-dark) 100%);
    color: var(--parchment) !important;
    border: 2px solid var(--ocean-light);
}

/* Captions */
.stCaption {
    font-family: 'Crimson Text', serif !important;
    color: var(--parchment-dark) !important;
    font-style: italic;
}

/* Alerts */
.stAlert {
    font-family: 'Crimson Text', serif;
    border-radius: 6px;
}

/* Toasts */
[data-testid="stToast"] {
    background: linear-gradient(180deg, var(--parchment) 0%, var(--parchment-dark) 100%);
    border: 2px solid var(--gold-dark);
    color: var(--driftwood-dark);
    font-family: 'Crimson Text', serif;
}

/* Dividers */
hr {
    border-color: var(--driftwood) !important;
}

/* Spinners */
.stSpinner > div {
    border-color: var(--gold) !important;
}

/* Timing warning style - NEW for estimated timing indicators */
.timing-warning {
    background: linear-gradient(145deg, #5c4d3a 0%, #3d3228 100%);
    border: 2px solid #b8860b;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 4px 0;
    color: #ffd700;
    font-size: 0.85rem;
}

.timing-verified {
    background: linear-gradient(145deg, #2E8B57 0%, #1d5c38 100%);
    border: 2px solid #3CB371;
    border-radius: 6px;
    padding: 4px 8px;
    color: #90EE90;
    font-size: 0.75rem;
    display: inline-block;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
    .stApp {
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] {
        min-width: 250px;
    }
    
    [data-testid="stDataFrame"] {
        font-size: 0.85rem;
    }
    
    [data-testid="stMetric"] {
        padding: 10px;
    }
    
    .js-plotly-plot, .plotly {
        max-width: 100% !important;
        overflow-x: auto;
    }
    
    .stButton > button {
        min-height: 44px;
        padding: 10px 16px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex-shrink: 0;
        padding: 8px 12px;
    }
    
    .stApp h1 { font-size: 1.5rem !important; }
    .stApp h2 { font-size: 1.25rem !important; }
    .stApp h3 { font-size: 1.1rem !important; }
}
</style>

<script>
// Disable autocomplete on all inputs
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => input.setAttribute('autocomplete', 'off'));
});

const observer = new MutationObserver(function(mutations) {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => input.setAttribute('autocomplete', 'off'));
});
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""
