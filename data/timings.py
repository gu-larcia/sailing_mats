"""
Activity timing data for GP/hr calculations.

Game tick = 0.6 seconds

Verified timings from OSRS Wiki:
- Smithing: 5 ticks per action (can be 4 with Smiths' Uniform)
- Cannonballs: 8 ticks per bar (4 with Ancient Furnace)
- Plank Make: 3 ticks per cast (manual), 6 ticks (auto)
- Nails: 15 per bar output

Hull parts crafting timing is undocumented in wiki - estimated at 4 ticks.
"""

from dataclasses import dataclass


@dataclass
class ActivityTiming:
    """Timing data for a crafting/smithing activity."""
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


# Smithing outfit tick save chance (15% to save 1 tick)
SMITHING_OUTFIT_TICK_SAVE_CHANCE = 0.15

# All activity timings
ACTIVITY_TIMINGS = {
    # Cannonball smelting - 8 ticks (4.8s) per bar, 4 balls output
    "Cannonballs_Single": ActivityTiming(
        ticks_per_action=9,  # Slightly longer due to animation
        items_per_action=4,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=1,  # Ammo mould
        activity_name="Cannonball Smelting (Single)",
        is_smithing=True,
        uses_planks=False,
        notes="Regular ammo mould: 1 bar per 4 cannonballs per 9 ticks."
    ),
    
    # Double ammo mould - processes 2 bars at once
    "Cannonballs_Double": ActivityTiming(
        ticks_per_action=9,
        items_per_action=8,
        materials_per_action=2,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=1,  # Double ammo mould
        activity_name="Cannonball Smelting (Double)",
        is_smithing=True,
        uses_planks=False,
        notes="Double ammo mould: 2 bars per 8 cannonballs per 9 ticks."
    ),
    
    # Keel parts - 5 bars per part
    "Keel Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Keel Parts Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="5 bars per part."
    ),
    
    # Dragon keel parts - special 2:1 ratio
    "Dragon Keel Parts": ActivityTiming(
        ticks_per_action=4,
        items_per_action=1,
        materials_per_action=2,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Dragon Keel Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="2 dragon metal sheets per part. Requires 92 Smithing."
    ),
    
    # Large keel parts - 5 regular parts per large
    "Large Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Keel Assembly",
        is_smithing=True,
        uses_planks=False,
        notes="5 regular parts per large part."
    ),
    
    # Large dragon keel parts - 2:1 ratio
    "Large Dragon Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=2,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Dragon Keel Assembly",
        is_smithing=True,
        uses_planks=False,
        notes="2 dragon keel parts per large part."
    ),
    
    # Hull parts - 5 planks per part (estimated 4 ticks)
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
        notes="5 planks per part."
    ),
    
    # Large hull parts - 5 regular parts per large
    "Large Hull Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Large Hull Assembly",
        is_smithing=False,
        uses_planks=False,
        notes="5 regular parts per large part."
    ),
    
    # Nails - 15 per bar
    "Nails": ActivityTiming(
        ticks_per_action=4,
        items_per_action=15,
        materials_per_action=1,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Nail Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="15 nails per bar."
    ),
    
    # Sawmill - dominated by travel time
    "Planks_Sawmill": ActivityTiming(
        ticks_per_action=1,
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Sawmill Conversion",
        is_smithing=False,
        uses_planks=False,
        notes="Time dominated by travel. Uses coin pouch."
    ),
    
    # Plank Make spell - 3 ticks per cast
    "Planks_PlankMake": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=3,  # Rune slots (or 2 with Earth staff)
        activity_name="Plank Make Spell",
        is_smithing=False,
        uses_planks=False,
        notes="3 ticks per cast. Earth staff reduces rune slots needed."
    ),
}
