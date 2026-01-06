"""GP and item name formatting."""


def format_gp(value: float) -> str:
    """Format GP value with K/M suffix."""
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
    """Remove processing suffixes from chain name."""
    clean = chain_name.replace(" processing", "").replace(" smithing", "")
    clean = clean.replace(" (Regular)", "").replace(" (Double)", "")
    return clean


def get_output_item_name(chain_name: str) -> str:
    """Alias for get_clean_item_name."""
    return get_clean_item_name(chain_name)


def get_wiki_image_url(item_name: str) -> str:
    """Generate OSRS Wiki image URL for item."""
    formatted_name = item_name.replace(" ", "_").replace("'", "%27")
    return f"https://oldschool.runescape.wiki/images/{formatted_name}.png"


def get_item_icon_url(item_name: str) -> str:
    """Get icon URL with name corrections for special cases."""
    name_fixes = {
        "Plank": "Plank",
        "Logs": "Logs",
    }
    
    fixed_name = name_fixes.get(item_name, item_name)
    return get_wiki_image_url(fixed_name)
