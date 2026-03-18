"""UI components for items and cards — dark OSRS theme."""

from typing import Optional

try:
    from ..utils import format_gp, get_item_icon_url, get_clean_item_name
except ImportError:
    from utils import format_gp, get_item_icon_url, get_clean_item_name


def render_item_with_icon(item_name: str, profit: Optional[float] = None, show_profit: bool = True) -> str:
    """Render item with icon and optional profit. Returns HTML."""
    icon_url = get_item_icon_url(item_name)
    profit_html = ""

    if show_profit and profit is not None:
        profit_color = "#00ff00" if profit >= 0 else "#c0392b"
        profit_html = f'<span style="color: {profit_color}; font-weight: 600; text-shadow: 1px 1px 0 #000;">{format_gp(profit)}</span>'

    return f"""
    <div style="display: flex; align-items: center; gap: 10px; padding: 8px;
                background: #3a3124;
                border: 2px solid #5a4a2a; border-radius: 8px; margin: 4px 0;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);">
        <img src="{icon_url}" style="width: 32px; height: 32px; image-rendering: pixelated;"
             onerror="this.style.display='none'">
        <div style="flex: 1;">
            <div style="color: #ffff00; font-family: 'RuneScape', 'Cinzel', serif; font-size: 0.9rem; text-shadow: 1px 1px 0 #000;">{item_name}</div>
            {profit_html}
        </div>
    </div>
    """


def render_best_item_card(label: str, item_name: str, value: str) -> str:
    """Render highlight card. Returns HTML."""
    icon_url = get_item_icon_url(get_clean_item_name(item_name))

    return f"""
    <div style="background: #3a3124;
                border: 2px solid #5a4a2a; border-radius: 10px; padding: 15px;
                text-align: center; height: 100%;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);">
        <div style="color: #ff981f; font-family: 'RuneScape', 'Cinzel', serif; font-size: 0.85rem; margin-bottom: 8px; text-shadow: 1px 1px 0 #000;">
            {label}
        </div>
        <img src="{icon_url}" style="width: 40px; height: 40px; image-rendering: pixelated; margin-bottom: 8px;"
             onerror="this.style.display='none'">
        <div style="color: #ffff00; font-family: 'RuneScape', 'Crimson Text', serif; font-size: 0.95rem;
                    word-wrap: break-word; line-height: 1.3; text-shadow: 1px 1px 0 #000;">
            {item_name}
        </div>
        <div style="color: #00ff00; font-family: 'RuneScape', 'Crimson Text', serif; font-size: 1rem;
                    font-weight: 600; margin-top: 4px; text-shadow: 1px 1px 0 #000;">
            {value}
        </div>
    </div>
    """


def render_live_stat(label: str, value: str, sub: str = "") -> str:
    """Render a live stat card (new component for header stats)."""
    sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="live-stat">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {sub_html}
    </div>
    """


def render_step_indicator(step_type: str) -> str:
    """Return step type indicator string."""
    indicators = {
        "Input": "[IN]",
        "Intermediate": "[>]",
        "Output": "[OUT]",
    }
    return indicators.get(step_type, "[?]")
