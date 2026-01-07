"""
Activity timing data for GP/hr calculations.

1 tick = 0.6 seconds

Sources:
- Smithing: https://oldschool.runescape.wiki/w/Smithing
- Cannonballs: https://oldschool.runescape.wiki/w/Cannonball
- Plank Make: https://oldschool.runescape.wiki/w/Plank_Make
"""

from dataclasses import dataclass


@dataclass
class ActivityTiming:
    """Timing data for a processing activity."""
    ticks_per_action: int
    items_per_action: int
    materials_per_action: int
    needs_hammer: bool
    needs_saw: bool
    other_tool_slots: int
    activity_name: str
    is_smithing: bool = False
    uses_planks: bool = False
    notes: str = ""


# Smiths' Uniform: 15% chance to save 1 tick
SMITHING_OUTFIT_TICK_SAVE_CHANCE = 0.15

ACTIVITY_TIMINGS = {
    "Cannonballs_Single": ActivityTiming(
        ticks_per_action=9,
        items_per_action=4,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=1,
        activity_name="Cannonball Smelting (Single)",
        is_smithing=True,
        notes="1 bar → 4 cannonballs"
    ),
    
    "Cannonballs_Double": ActivityTiming(
        ticks_per_action=9,
        items_per_action=8,
        materials_per_action=2,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=1,
        activity_name="Cannonball Smelting (Double)",
        is_smithing=True,
        notes="2 bars → 8 cannonballs"
    ),
    
    "Keel Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Keel Parts Smithing",
        is_smithing=True,
        notes="5 bars → 1 part"
    ),
    
    "Dragon Keel Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=2,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Dragon Keel Smithing",
        is_smithing=True,
        notes="2 sheets → 1 part. Requires 92 Smithing."
    ),
    
    "Large Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Keel Assembly",
        is_smithing=True,
        notes="5 parts → 1 large"
    ),
    
    "Large Dragon Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=2,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Dragon Keel Assembly",
        is_smithing=True,
        notes="2 dragon parts → 1 large"
    ),
    
    "Hull Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Hull Parts Crafting",
        is_smithing=False,
        uses_planks=True,
        notes="5 planks → 1 part"
    ),
    
    "Large Hull Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Large Hull Assembly",
        is_smithing=False,
        notes="5 parts → 1 large"
    ),
    
    "Nails": ActivityTiming(
        ticks_per_action=4,
        items_per_action=15,
        materials_per_action=1,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Nail Smithing",
        is_smithing=True,
        notes="1 bar → 15 nails"
    ),
    
    "Planks_Sawmill": ActivityTiming(
        ticks_per_action=1,
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Sawmill Conversion",
        is_smithing=False,
        notes="Travel-dominated. Uses coin pouch."
    ),
    
    "Planks_PlankMake": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=3,  # Rune slots (2 with Earth staff)
        activity_name="Plank Make Spell",
        is_smithing=False,
        notes="Earth staff reduces rune slots."
    ),
}
