"""OSRS tier colors."""

# Metal tiers (match in-game appearance)
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

# Wood tiers (Sailing woods mapped to metal equivalents)
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
    'camphor': '#2E8B57',
    'ironwood': '#00CED1',
    'rosewood': '#DC143C',
}

CATEGORY_COLORS = {
    'Planks': '#C19A6B',
    'Hull Parts': '#8B7355',
    'Large Hull Parts': '#6B4423',
    'Hull Repair Kits': '#DAA520',
    'Keel Parts': '#71797E',
    'Large Keel Parts': '#5F9EA0',
    'Nails': '#CD7F32',
    'Cannonballs': '#5C5C5C',
    'Bar Smelting': '#B87333',
    'Nails (from Ore)': '#DAA520',
    'Keel Parts (from Ore)': '#5F9EA0',
    'Cannonballs (from Ore)': '#8B8682',
    'Large Keel Parts (from Bar)': '#4682B4',
    'Large Keel Parts (from Ore)': '#2F4F4F',
    'Hull Parts (from Log)': '#A0522D',
    'Large Hull Parts (from Log)': '#8B4513',
    'Repair Kits (from Log)': '#B8860B',
    'Unstrung Bows': '#8B7355',
    'Strung Bows': '#6B8E23',
    'Arrows': '#228B22',
    'Darts': '#2E8B57',
    'Bows (from Log)': '#556B2F',
    'Other': '#7f8c8d',
}

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
    """Return tier color based on item name. Falls back to gold/red by profit."""
    name_lower = item_name.lower()
    
    # Metal tiers
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
    
    # Amethyst tier
    if 'amethyst' in name_lower:
        return '#9966CC'

    # Wood tiers
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
    elif 'magic' in name_lower:
        return WOOD_COLORS['magic']
    elif 'yew' in name_lower:
        return WOOD_COLORS['yew']
    elif 'maple' in name_lower:
        return WOOD_COLORS['maple']
    elif 'willow' in name_lower:
        return WOOD_COLORS['willow']
    elif 'oak' in name_lower:
        return WOOD_COLORS['oak']
    elif 'wooden' in name_lower or name_lower == 'plank' or name_lower.endswith(' plank'):
        if not any(wood in name_lower for wood in ['oak', 'teak', 'mahogany', 'camphor', 'ironwood', 'rosewood']):
            return WOOD_COLORS['wooden']
    
    return CHART_COLORS['gold'] if profit >= 0 else CHART_COLORS['dragon_red']


def get_tier_from_name(item_name: str) -> str:
    """Extract tier name from item name."""
    name_lower = item_name.lower()
    
    for tier in ['dragon', 'rune', 'adamant', 'mithril', 'steel', 'iron', 'bronze', 'gold', 'silver']:
        if tier in name_lower and not (tier == 'iron' and 'ironwood' in name_lower):
            return tier.capitalize()
    
    for tier in ['rosewood', 'ironwood', 'camphor', 'mahogany', 'magic', 'yew', 'maple', 'willow', 'teak', 'oak', 'wooden']:
        if tier in name_lower:
            return tier.capitalize()
    
    return "Other"
