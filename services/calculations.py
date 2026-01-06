"""
GP/hr calculation service for processing activities.

Calculates gold per hour estimates based on:
- Activity timing (ticks per action)
- Bank location overhead
- Equipment bonuses (Imcando Hammer, Amy's Saw, etc.)
- Ancient Furnace (2x smithing speed)
"""

from typing import Dict, Optional

try:
    from ..data import (
        ACTIVITY_TIMINGS,
        BANK_LOCATIONS,
        PLANK_SACK_CAPACITY,
        SMITHING_OUTFIT_TICK_SAVE_CHANCE,
    )
except ImportError:
    from data import (
        ACTIVITY_TIMINGS,
        BANK_LOCATIONS,
        PLANK_SACK_CAPACITY,
        SMITHING_OUTFIT_TICK_SAVE_CHANCE,
    )


def calculate_gp_per_hour(
    profit_per_item: float,
    category: str,
    chain_name: str,
    config: Dict
) -> Optional[Dict]:
    """
    Calculate GP/hr for a processing activity.
    
    Args:
        profit_per_item: Profit per single item produced
        category: Processing category (e.g., "Cannonballs", "Hull Parts")
        chain_name: Name of the processing chain
        config: User configuration dict with equipment/location settings
        
    Returns:
        Dict with GP/hr data, or None if activity timing not found:
        {
            'gp_per_hour': float,
            'items_per_hour': float,
            'trips_per_hour': float,
            'items_per_trip': int,
            'materials_per_trip': int,
            'effective_inventory': int,
            'seconds_per_trip': float,
            'timing_key': str,
            'timing': ActivityTiming,
            'notes': str,
            'tool_notes': list,
            'bonus_notes': list,
            'tool_slots_saved': int,
            'bank_location': str,
            'bank_requirements': str,
            'effective_ticks': float,
            'is_double_mould': bool,
            'plank_sack_active': bool,
        }
    """
    # Determine which activity timing to use
    timing_key = _get_timing_key(category, chain_name, config)
    
    if not timing_key or timing_key not in ACTIVITY_TIMINGS:
        return None
    
    timing = ACTIVITY_TIMINGS[timing_key]
    is_double_mould_chain = "(Double)" in chain_name
    
    # Get equipment settings
    has_imcando_hammer = config.get("has_imcando_hammer", False)
    has_amys_saw = config.get("has_amys_saw", False)
    has_smithing_outfit = config.get("has_smithing_outfit", False)
    has_plank_sack = config.get("has_plank_sack", False)
    use_stamina = config.get("use_stamina", True)
    
    # Get bank location
    bank_location_name = config.get("bank_location", "Medium (Typical)")
    bank_location = BANK_LOCATIONS.get(bank_location_name, BANK_LOCATIONS["Medium (Typical)"])
    
    # Calculate effective ticks (with smithing outfit bonus)
    effective_ticks = timing.ticks_per_action
    if has_smithing_outfit and timing.is_smithing:
        effective_ticks = timing.ticks_per_action - (SMITHING_OUTFIT_TICK_SAVE_CHANCE * 1)
    
    # Calculate tool slots used
    tool_slots_used = timing.other_tool_slots
    
    if timing.needs_hammer and not has_imcando_hammer:
        tool_slots_used += 1
    
    if timing.needs_saw and not has_amys_saw:
        tool_slots_used += 1
    
    # Plank sack bonus
    plank_sack_bonus = 0
    if has_plank_sack and timing.uses_planks:
        tool_slots_used += 1  # Sack takes a slot
        plank_sack_bonus = PLANK_SACK_CAPACITY
    
    # Calculate effective inventory
    base_inventory = 28
    effective_inventory = base_inventory - tool_slots_used
    
    # Earth staff saves a rune slot for Plank Make
    if timing_key == "Planks_PlankMake" and config.get("use_earth_staff", False):
        effective_inventory += 1
    
    # Calculate materials and items per trip
    items_per_action = timing.items_per_action
    materials_per_action = timing.materials_per_action
    
    materials_per_trip = effective_inventory
    
    if has_plank_sack and timing.uses_planks:
        materials_per_trip = effective_inventory + plank_sack_bonus
    
    actions_per_trip = materials_per_trip // materials_per_action
    items_per_trip = actions_per_trip * items_per_action
    
    if items_per_trip <= 0:
        return None
    
    # Calculate time per trip
    ticks_per_trip = actions_per_trip * effective_ticks
    craft_time_seconds = ticks_per_trip * 0.6  # 1 tick = 0.6 seconds
    
    # Bank overhead
    trip_overhead = bank_location.total_overhead
    
    if bank_location.stamina_dependent and use_stamina:
        trip_overhead = bank_location.bank_time + (bank_location.travel_time * 0.7)
    
    seconds_per_trip = craft_time_seconds + trip_overhead
    
    # Special handling for sawmill (dominated by travel)
    if timing_key == "Planks_Sawmill":
        sawmill_travel = config.get("sawmill_travel_time", bank_location.total_overhead)
        seconds_per_trip = sawmill_travel
        items_per_trip = effective_inventory
    
    # Ancient Furnace bonus (2x speed for smithing)
    ancient_furnace_active = False
    if config.get("ancient_furnace", False) and timing.is_smithing:
        craft_time_seconds = craft_time_seconds / 2
        seconds_per_trip = craft_time_seconds + trip_overhead
        ancient_furnace_active = True
    
    # Calculate hourly rates
    trips_per_hour = 3600.0 / seconds_per_trip
    items_per_hour = trips_per_hour * items_per_trip
    gp_per_hour = items_per_hour * profit_per_item
    
    # Build notes
    tool_notes = []
    if timing.needs_hammer:
        tool_notes.append(f"Hammer: {'equipped' if has_imcando_hammer else 'inventory'}")
    if timing.needs_saw:
        tool_notes.append(f"Saw: {'equipped' if has_amys_saw else 'inventory'}")
    if has_plank_sack and timing.uses_planks:
        tool_notes.append(f"Plank sack: +{plank_sack_bonus} planks")
    
    bonus_notes = []
    if has_smithing_outfit and timing.is_smithing:
        bonus_notes.append("Smithing outfit: -15% avg ticks")
    if ancient_furnace_active:
        bonus_notes.append("Ancient Furnace: 2x speed")
    if is_double_mould_chain:
        bonus_notes.append("Double mould: 2 bars/action")
    if has_plank_sack and timing.uses_planks:
        bonus_notes.append(f"Plank sack: +{plank_sack_bonus} capacity")
    
    return {
        "gp_per_hour": gp_per_hour,
        "items_per_hour": items_per_hour,
        "trips_per_hour": trips_per_hour,
        "items_per_trip": items_per_trip,
        "materials_per_trip": materials_per_trip,
        "effective_inventory": effective_inventory,
        "seconds_per_trip": seconds_per_trip,
        "timing_key": timing_key,
        "timing": timing,
        "notes": timing.notes,
        "tool_notes": tool_notes,
        "bonus_notes": bonus_notes,
        "tool_slots_saved": (1 if timing.needs_hammer and has_imcando_hammer else 0) + 
                           (1 if timing.needs_saw and has_amys_saw else 0),
        "bank_location": bank_location.name,
        "bank_requirements": bank_location.requirements,
        "effective_ticks": effective_ticks,
        "is_double_mould": is_double_mould_chain,
        "plank_sack_active": has_plank_sack and timing.uses_planks,
    }


def _get_timing_key(category: str, chain_name: str, config: Dict) -> Optional[str]:
    """Determine the activity timing key based on category and chain name."""
    is_double_mould = "(Double)" in chain_name
    
    if category == "Cannonballs":
        return "Cannonballs_Double" if is_double_mould else "Cannonballs_Single"
    
    elif category == "Keel Parts":
        if "dragon" in chain_name.lower():
            return "Dragon Keel Parts"
        return "Keel Parts"
    
    elif category == "Large Keel Parts":
        if "dragon" in chain_name.lower():
            return "Large Dragon Keel Parts"
        return "Large Keel Parts"
    
    elif category == "Hull Parts":
        return "Hull Parts"
    
    elif category == "Large Hull Parts":
        return "Large Hull Parts"
    
    elif category == "Nails":
        return "Nails"
    
    elif category == "Planks":
        plank_method = config.get("plank_method", "Sawmill")
        if "Plank Make" in plank_method:
            return "Planks_PlankMake"
        return "Planks_Sawmill"
    
    return None
