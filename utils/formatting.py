"""
Formatting utilities for GP values and item names.
"""


def format_gp(value: float) -> str:
    """
    Format a gold piece value with appropriate suffix (K/M).
    
    Examples:
        format_gp(1500) -> "1.5K"
        format_gp(2500000) -> "2.50M"
        format_gp(-500) -> "-500"
    """
    if value == float('inf'):
        return "Inf"
    
    is_negative = value < 0
    value = abs(value)
    
    if value >= 1_000_000:
        formatted = f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        formatted = f"{value/1_000:.1f}K"
    else:
        formatted = f"{int(value):,}"
    
    return f"-{formatted}" if is_negative else formatted


def get_clean_item_name(chain_name: str) -> str:
    """
    Clean a processing chain name to get the base item name.
    Removes suffixes like " processing", " smithing", "(Regular)", "(Double)".
    """
    clean = chain_name.replace(" processing", "").replace(" smithing", "")
    clean = clean.replace(" (Regular)", "").replace(" (Double)", "")
    return clean


def get_output_item_name(chain_name: str) -> str:
    """Get the output item name from a chain name."""
    return get_clean_item_name(chain_name)


def get_wiki_image_url(item_name: str) -> str:
    """
    Generate the OSRS Wiki image URL for an item.
    
    Example:
        get_wiki_image_url("Bronze bar") -> "https://oldschool.runescape.wiki/images/Bronze_bar.png"
    """
    formatted_name = item_name.replace(" ", "_").replace("'", "%27")
    return f"https://oldschool.runescape.wiki/images/{formatted_name}.png"


def get_item_icon_url(item_name: str) -> str:
    """
    Get the icon URL for an item, with name fixes for special cases.
    """
    # Some items have different wiki image names
    name_fixes = {
        "Plank": "Plank",
        "Logs": "Logs",
    }
    
    fixed_name = name_fixes.get(item_name, item_name)
    return get_wiki_image_url(fixed_name)
