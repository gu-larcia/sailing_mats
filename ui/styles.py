"""Dark OSRS-themed CSS for Streamlit — inspired by osrsplayercount.com."""

OSRS_CSS = """
<style>
@font-face {
    font-family: 'RuneScape';
    src: url('https://raw.githubusercontent.com/runelite/runelite/master/runelite-client/src/main/resources/net/runelite/client/ui/runescape.ttf') format('truetype');
    font-display: swap;
}

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --bg-primary: #1b1b1b;
    --bg-secondary: #2b2b2b;
    --bg-card: #3a3124;
    --bg-card-dark: #2e2720;
    --border-primary: #383023;
    --border-gold: #5a4a2a;
    --text-yellow: #ffff00;
    --text-orange: #ff981f;
    --text-green: #00ff00;
    --text-lime: #90c040;
    --text-gray: #aaaaaa;
    --text-light: #d4c5a0;
    --text-white: #e8dcc8;
    --gold: #ffd700;
    --gold-dark: #d4af37;
    --copper: #b87333;
    --dragon-red: #c0392b;
    --rune-blue: #5dade2;
    --shadow: rgba(0, 0, 0, 0.6);
}

/* ===== App Background ===== */
.stApp {
    background: var(--bg-primary);
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2e2720 0%, #1e1a15 100%);
    border-right: 3px solid var(--border-gold);
}

[data-testid="stSidebar"] * {
    color: var(--text-light) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    color: var(--text-orange) !important;
    text-shadow: 1px 1px 0 #000;
}

[data-testid="stSidebar"] input {
    background: var(--bg-secondary) !important;
    border: 2px solid var(--border-gold) !important;
    color: var(--text-light) !important;
}

[data-testid="stSidebar"] .stSelectbox label {
    color: var(--text-light) !important;
}

/* ===== Headers ===== */
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    color: var(--text-yellow) !important;
    text-shadow: 1px 1px 0 #000, 2px 2px 4px rgba(0,0,0,0.5);
}

.stApp h1 {
    border-bottom: 3px solid var(--border-gold);
    padding-bottom: 10px;
}

/* ===== Tabs ===== */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card-dark);
    border-radius: 8px 8px 0 0;
    padding: 5px;
    gap: 4px;
    border: 1px solid var(--border-gold);
    border-bottom: none;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    color: var(--text-light) !important;
    background: transparent;
    border-radius: 6px 6px 0 0;
    padding: 10px 20px;
    text-shadow: 1px 1px 0 #000;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, var(--border-gold) 0%, var(--bg-card) 100%) !important;
    color: var(--text-yellow) !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: var(--bg-secondary);
    border: 2px solid var(--border-gold);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 20px;
}

/* ===== Metrics ===== */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 2px solid var(--border-gold);
    border-radius: 10px;
    padding: 15px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.4), 0 2px 4px var(--shadow);
}

[data-testid="stMetric"] label {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    color: var(--text-orange) !important;
    text-shadow: 1px 1px 0 #000;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'RuneScape', 'Crimson Text', serif !important;
    color: var(--text-green) !important;
    font-size: 1.1rem !important;
    text-shadow: 1px 1px 0 #000;
}

[data-testid="stMetric"] [data-testid="stMetricDelta"] svg {
    display: none;
}

/* ===== DataFrames ===== */
[data-testid="stDataFrame"] {
    border: 3px solid var(--border-gold);
    border-radius: 8px;
    overflow-x: auto !important;
    overflow-y: visible !important;
}

/* ===== Buttons ===== */
.stButton > button {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-card-dark) 100%);
    color: var(--text-orange) !important;
    border: 2px solid var(--border-gold);
    border-radius: 6px;
    font-weight: 600;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 2px 4px var(--shadow);
    transition: all 0.2s ease;
    text-shadow: 1px 1px 0 #000;
}

.stButton > button:hover {
    background: linear-gradient(180deg, var(--border-gold) 0%, var(--bg-card) 100%);
    color: var(--text-yellow) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px var(--shadow);
}

/* ===== Forms ===== */
[data-testid="stForm"] {
    background: linear-gradient(180deg, rgba(58,49,36,0.3) 0%, rgba(46,39,32,0.3) 100%);
    border: 2px solid var(--border-gold);
    border-radius: 8px;
    padding: 15px;
}

/* ===== Select boxes ===== */
.stSelectbox > div > div {
    background: var(--bg-secondary) !important;
    border: 2px solid var(--border-gold) !important;
}

.stSelectbox > div > div > div {
    color: var(--text-light) !important;
}

.stSelectbox label {
    color: var(--text-light) !important;
}

/* ===== Radio buttons ===== */
.stRadio label {
    color: var(--text-light) !important;
}

.stRadio [data-baseweb="radio"] label {
    color: var(--text-light) !important;
    font-family: 'Crimson Text', serif !important;
}

/* ===== Expanders ===== */
.streamlit-expanderHeader {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    background: var(--bg-card-dark);
    border: 2px solid var(--border-gold);
    border-radius: 6px;
    color: var(--text-orange) !important;
    text-shadow: 1px 1px 0 #000;
}

/* ===== Link Buttons ===== */
.stLinkButton > a {
    font-family: 'RuneScape', 'Cinzel', serif !important;
    background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-card-dark) 100%);
    color: var(--text-lime) !important;
    border: 2px solid var(--border-gold);
    text-shadow: 1px 1px 0 #000;
}

/* ===== Captions & Alerts ===== */
.stCaption {
    font-family: 'Crimson Text', serif !important;
    color: var(--text-gray) !important;
    font-style: italic;
}

.stAlert {
    font-family: 'Crimson Text', serif;
    border-radius: 6px;
}

/* ===== Toasts ===== */
[data-testid="stToast"] {
    background: var(--bg-card);
    border: 2px solid var(--border-gold);
    color: var(--text-light);
    font-family: 'Crimson Text', serif;
    text-shadow: 1px 1px 0 #000;
}

hr {
    border-color: var(--border-gold) !important;
}

.stSpinner > div {
    border-color: var(--text-orange) !important;
}

/* ===== Custom Item Cards ===== */
.item-card {
    background: var(--bg-card);
    border: 2px solid var(--border-gold);
    border-radius: 10px;
    padding: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
}

.item-card img {
    width: 36px;
    height: 36px;
    image-rendering: pixelated;
}

.item-card .item-name {
    color: var(--text-yellow);
    font-family: 'RuneScape', 'Cinzel', serif;
    font-size: 0.95rem;
    text-shadow: 1px 1px 0 #000;
}

.item-card .item-profit {
    color: var(--text-green);
    font-family: 'RuneScape', 'Crimson Text', serif;
    font-weight: 600;
    text-shadow: 1px 1px 0 #000;
}

.best-item-display {
    background: var(--bg-card);
    border: 2px solid var(--border-gold);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.best-item-display img {
    width: 48px;
    height: 48px;
    image-rendering: pixelated;
    margin-bottom: 8px;
}

.best-item-display .label {
    color: var(--text-orange);
    font-family: 'RuneScape', 'Cinzel', serif;
    font-size: 0.85rem;
    margin-bottom: 4px;
    text-shadow: 1px 1px 0 #000;
}

.best-item-display .value {
    color: var(--text-yellow);
    font-family: 'RuneScape', 'Crimson Text', serif;
    font-size: 1rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    text-shadow: 1px 1px 0 #000;
    max-width: 100%;
}

/* ===== Live Stats Header ===== */
.live-stat {
    background: var(--bg-card);
    border: 2px solid var(--border-gold);
    border-radius: 8px;
    padding: 12px 16px;
    text-align: center;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
}

.live-stat .stat-label {
    color: var(--text-orange);
    font-family: 'RuneScape', 'Cinzel', serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-shadow: 1px 1px 0 #000;
}

.live-stat .stat-value {
    color: var(--text-green);
    font-family: 'RuneScape', 'Cinzel', serif;
    font-size: 1.4rem;
    text-shadow: 1px 1px 0 #000;
}

.live-stat .stat-sub {
    color: var(--text-gray);
    font-family: 'Crimson Text', serif;
    font-size: 0.75rem;
}

/* ===== Responsive ===== */
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

    [data-testid="stDataFrame"]::before {
        content: 'scroll horizontally';
        display: block;
        text-align: center;
        font-size: 0.7rem;
        color: var(--text-gray);
        padding: 4px;
        opacity: 0.7;
    }
}

@media screen and (max-width: 480px) {
    [data-testid="stDataFrame"] {
        font-size: 0.75rem;
    }

    [data-testid="stMetric"] label {
        font-size: 0.8rem !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1rem !important;
    }
}

/* Responsive font scaling for ultra-wide */
@media screen and (min-width: 1921px) {
    .stApp {
        font-size: calc(16px + 0.5vw);
    }
}

/* ===== Scrollbars ===== */
[data-testid="stDataFrame"]::-webkit-scrollbar {
    height: 8px;
}

[data-testid="stDataFrame"]::-webkit-scrollbar-track {
    background: var(--bg-card-dark);
    border-radius: 4px;
}

[data-testid="stDataFrame"]::-webkit-scrollbar-thumb {
    background: var(--border-gold);
    border-radius: 4px;
}

[data-testid="stDataFrame"]::-webkit-scrollbar-thumb:hover {
    background: var(--gold-dark);
}
</style>

<script>
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
