"""
OSRS-authentic color system for material tiers.
Colors match in-game metal and wood tiers.
"""

# Metal tier colors (matches in-game appearance)
METAL_COLORS = {
    'bronze': '#CD7F32',
    'iron': '#5C5C5C',
    'steel': '#71797E',
    'black': '#1C1C1C',
    'mithril': '#284B63',
    'adamant': '#2E8B57',
    'rune': '#00CED1',
    'dragon': '#DC143C',
}

# Wood tier colors (Sailing woods matched to metal equivalents)
WOOD_COLORS = {
    'wooden': '#DEB887',
    'oak': '#C19A6B',
    'willow': '#A8C090',
    'teak': '#8B7355',
    'maple': '#C9A66B',
    'mahogany': '#6B4423',
    'yew': '#8B4513',
    'magic': '#4B0082',
    'redwood': '#A52A2A',
    'camphor': '#2E8B57',    # Adamant equivalent
    'ironwood': '#00CED1',   # Rune equivalent
    'rosewood': '#DC143C',   # Dragon equivalent
}

# Category colors for charts
CATEGORY_COLORS = {
    'Planks': '#C19A6B',
    'Hull Parts': '#8B7355',
    'Large Hull Parts': '#6B4423',
    'Hull Repair Kits': '#DAA520',
    'Keel Parts': '#71797E',
    'Large Keel Parts': '#5F9EA0',
    'Nails': '#CD7F32',
    'Cannonballs': '#5C5C5C',
    'Other': '#7f8c8d',
}

# Chart theme colors
CHART_COLORS = {
    'gold': '#d4af37',
    'gold_dark': '#b8860b',
    'dragon_red': '#c0392b',
    'dragon_red_dark': '#922b21',
    'rune_blue': '#5dade2',
    'parchment': '#f4e4bc',
    'ocean_dark': '#1a2a3a',
    'driftwood': '#8b7355',
}


def get_item_tier_color(item_name: str, profit: float = 0) -> str:
    """
    Get the appropriate OSRS tier color for an item based on its name.
    Falls back to gold/red based on profit if no tier match.
    """
    name_lower = item_name.lower()
    
    # Check metal tiers first
    if 'dragon' in name_lower:
        return METAL_COLORS['dragon']
    elif 'rune ' in name_lower or 'rune_' in name_lower or 'runite' in name_lower:
        return METAL_COLORS['rune']
    elif 'adamant' in name_lower:
        return METAL_COLORS['adamant']
    elif 'mithril' in name_lower:
        return METAL_COLORS['mithril']
    elif 'black' in name_lower and ('nail' in name_lower or 'keel' in name_lower):
        return METAL_COLORS['black']
    elif 'steel' in name_lower:
        return METAL_COLORS['steel']
    elif 'iron ' in name_lower or 'iron_' in name_lower or name_lower.startswith('iron'):
        if 'ironwood' not in name_lower:
            return METAL_COLORS['iron']
    elif 'bronze' in name_lower:
        return METAL_COLORS['bronze']
    
    # Check wood tiers
    if 'rosewood' in name_lower:
        return WOOD_COLORS['rosewood']
    elif 'ironwood' in name_lower:
        return WOOD_COLORS['ironwood']
    elif 'camphor' in name_lower:
        return WOOD_COLORS['camphor']
    elif 'mahogany' in name_lower:
        return WOOD_COLORS['mahogany']
    elif 'teak' in name_lower:
        return WOOD_COLORS['teak']
    elif 'oak' in name_lower:
        return WOOD_COLORS['oak']
    elif 'wooden' in name_lower or name_lower == 'plank' or name_lower.endswith(' plank'):
        if not any(wood in name_lower for wood in ['oak', 'teak', 'mahogany', 'camphor', 'ironwood', 'rosewood']):
            return WOOD_COLORS['wooden']
    
    # Default based on profit
    return CHART_COLORS['gold'] if profit >= 0 else CHART_COLORS['dragon_red']


def get_tier_from_name(item_name: str) -> str:
    """Extract the tier name from an item name for display/grouping."""
    name_lower = item_name.lower()
    
    # Check metals
    for tier in ['dragon', 'rune', 'adamant', 'mithril', 'steel', 'iron', 'bronze']:
        if tier in name_lower and not (tier == 'iron' and 'ironwood' in name_lower):
            return tier.capitalize()
    
    # Check woods
    for tier in ['rosewood', 'ironwood', 'camphor', 'mahogany', 'teak', 'oak', 'wooden']:
        if tier in name_lower:
            return tier.capitalize()
    
    return "Other"
