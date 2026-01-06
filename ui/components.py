"""
Reusable UI components for rendering items and cards.
"""

from typing import Optional

try:
    from ..utils import format_gp, get_item_icon_url, get_clean_item_name
except ImportError:
    from utils import format_gp, get_item_icon_url, get_clean_item_name


def render_item_with_icon(item_name: str, profit: Optional[float] = None, show_profit: bool = True) -> str:
    """
    Render an item with its icon and optional profit display.
    
    Args:
        item_name: Name of the item
        profit: Optional profit value to display
        show_profit: Whether to show the profit
        
    Returns:
        HTML string for the item card
    """
    icon_url = get_item_icon_url(item_name)
    profit_html = ""
    
    if show_profit and profit is not None:
        profit_color = "#d4af37" if profit >= 0 else "#c0392b"
        profit_html = f'<span style="color: {profit_color}; font-weight: 600;">{format_gp(profit)}</span>'
    
    return f"""
    <div style="display: flex; align-items: center; gap: 10px; padding: 8px; 
                background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
                border: 2px solid #d4af37; border-radius: 8px; margin: 4px 0;">
        <img src="{icon_url}" style="width: 32px; height: 32px; image-rendering: pixelated;" 
             onerror="this.style.display='none'">
        <div style="flex: 1;">
            <div style="color: #f4e4bc; font-family: 'Cinzel', serif; font-size: 0.9rem;">{item_name}</div>
            {profit_html}
        </div>
    </div>
    """


def render_best_item_card(label: str, item_name: str, value: str) -> str:
    """
    Render a card showing the best item in a category.
    
    Args:
        label: Label for the card (e.g., "Best Profit")
        item_name: Name of the item
        value: Value to display (e.g., formatted GP)
        
    Returns:
        HTML string for the card
    """
    icon_url = get_item_icon_url(get_clean_item_name(item_name))
    
    return f"""
    <div style="background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
                border: 2px solid #d4af37; border-radius: 10px; padding: 15px;
                text-align: center; height: 100%;">
        <div style="color: #ffd700; font-family: 'Cinzel', serif; font-size: 0.85rem; margin-bottom: 8px;">
            {label}
        </div>
        <img src="{icon_url}" style="width: 40px; height: 40px; image-rendering: pixelated; margin-bottom: 8px;"
             onerror="this.style.display='none'">
        <div style="color: #f4e4bc; font-family: 'Crimson Text', serif; font-size: 0.95rem; 
                    word-wrap: break-word; line-height: 1.3;">
            {item_name}
        </div>
        <div style="color: #d4af37; font-family: 'Crimson Text', serif; font-size: 1rem; 
                    font-weight: 600; margin-top: 4px;">
            {value}
        </div>
    </div>
    """


def render_step_indicator(step_type: str) -> str:
    """
    Render a step type indicator for processing chains.
    
    Args:
        step_type: One of "Input", "Intermediate", "Output"
        
    Returns:
        Styled indicator string
    """
    indicators = {
        "Input": "[IN]",
        "Intermediate": "[>]",
        "Output": "[OUT]",
    }
    return indicators.get(step_type, "[?]")
