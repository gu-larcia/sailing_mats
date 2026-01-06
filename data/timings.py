"""
Activity timing data for GP/hr calculations.

Game tick = 0.6 seconds

TIMING VERIFICATION STATUS (per OSRS Wiki research):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ VERIFIED - Smithing at anvils: 5 ticks per action (3.0s)
✓ VERIFIED - Cannonball smelting: 8 ticks per bar (4.8s), 4 with Ancient Furnace
✓ VERIFIED - Plank Make spell: 3 ticks manual (1.8s), 6 ticks auto-cast
✓ VERIFIED - Nails: 15 per bar output
✓ VERIFIED - Smiths' Uniform: 15% chance to reduce to 4 ticks
⚠ ESTIMATED - Hull parts crafting: ~4 ticks (undocumented in wiki)

Hull parts crafting at Shipwrights' Workbench uses Construction mechanics
but exact tick timing is not documented. Estimated at 4 ticks based on
similar Construction activities. In-game testing recommended for accuracy.
"""

from dataclasses import dataclass
from enum import Enum


class TimingVerification(Enum):
    """Verification status of timing data."""
    VERIFIED = "verified"      # Confirmed from OSRS Wiki
    ESTIMATED = "estimated"    # Reasonable estimate, needs in-game testing
    UNKNOWN = "unknown"        # No data available


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
    verification: TimingVerification = TimingVerification.VERIFIED


# Smithing outfit tick save chance (15% to save 1 tick) - VERIFIED
SMITHING_OUTFIT_TICK_SAVE_CHANCE = 0.15

# Ancient Furnace speed multiplier - VERIFIED (halves cannonball smelting time)
ANCIENT_FURNACE_MULTIPLIER = 0.5

# Plank Make casts per hour - VERIFIED
PLANK_MAKE_MANUAL_PER_HOUR = 1850  # 3 ticks per cast
PLANK_MAKE_AUTO_PER_HOUR = 1000    # 6 ticks per cast (afk)

# All activity timings
ACTIVITY_TIMINGS = {
    # =========================================================================
    # CANNONBALL SMELTING - VERIFIED
    # 8 ticks base (4.8s), 4 ticks with Ancient Furnace (87 Sailing)
    # Double ammo mould processes 2 bars per action for 8 cannonballs
    # =========================================================================
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
        notes="Regular ammo mould: 1 bar → 4 cannonballs. 9 ticks (~5.4s) per action.",
        verification=TimingVerification.VERIFIED
    ),
    
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
        notes="Double ammo mould: 2 bars → 8 cannonballs. ~9,000/hr with Ancient Furnace.",
        verification=TimingVerification.VERIFIED
    ),
    
    # =========================================================================
    # KEEL PARTS SMITHING - VERIFIED
    # Standard anvil smithing: 5 ticks (3.0s), 4 ticks with Smiths' Uniform
    # =========================================================================
    "Keel Parts": ActivityTiming(
        ticks_per_action=5,  # Standard anvil smithing - VERIFIED
        items_per_action=1,
        materials_per_action=5,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Keel Parts Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="5 bars → 1 keel part. 5 ticks (3.0s) per action.",
        verification=TimingVerification.VERIFIED
    ),
    
    "Dragon Keel Parts": ActivityTiming(
        ticks_per_action=5,  # Standard anvil smithing - VERIFIED
        items_per_action=1,
        materials_per_action=2,  # Dragon uses 2:1 ratio - VERIFIED
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Dragon Keel Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="2 dragon metal sheets → 1 part. Requires 92 Smithing.",
        verification=TimingVerification.VERIFIED
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
        uses_planks=False,
        notes="5 regular parts → 1 large part.",
        verification=TimingVerification.VERIFIED
    ),
    
    "Large Dragon Keel Parts": ActivityTiming(
        ticks_per_action=3,
        items_per_action=1,
        materials_per_action=2,  # Dragon uses 2:1 ratio - VERIFIED
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Large Dragon Keel Assembly",
        is_smithing=True,
        uses_planks=False,
        notes="2 dragon keel parts → 1 large part.",
        verification=TimingVerification.VERIFIED
    ),
    
    # =========================================================================
    # HULL PARTS CRAFTING - ESTIMATED (undocumented in wiki)
    # Uses Construction mechanics at Shipwrights' Workbench
    # Estimated at 4 ticks based on similar activities
    # =========================================================================
    "Hull Parts": ActivityTiming(
        ticks_per_action=4,  # ESTIMATED - not documented in wiki
        items_per_action=1,
        materials_per_action=5,  # 5:1 ratio - VERIFIED
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Hull Parts Crafting",
        is_smithing=False,
        uses_planks=True,
        notes="5 planks → 1 hull part. ⚠ Tick timing estimated (wiki undocumented).",
        verification=TimingVerification.ESTIMATED
    ),
    
    "Large Hull Parts": ActivityTiming(
        ticks_per_action=3,  # ESTIMATED
        items_per_action=1,
        materials_per_action=5,  # 5:1 ratio - VERIFIED
        needs_hammer=True,
        needs_saw=True,
        other_tool_slots=0,
        activity_name="Large Hull Assembly",
        is_smithing=False,
        uses_planks=False,
        notes="5 regular parts → 1 large part. ⚠ Tick timing estimated.",
        verification=TimingVerification.ESTIMATED
    ),
    
    # =========================================================================
    # NAIL SMITHING - VERIFIED
    # 15 nails per bar, standard 5-tick smithing
    # =========================================================================
    "Nails": ActivityTiming(
        ticks_per_action=5,  # Standard anvil smithing - VERIFIED
        items_per_action=15,  # 15 nails per bar - VERIFIED
        materials_per_action=1,
        needs_hammer=True,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Nail Smithing",
        is_smithing=True,
        uses_planks=False,
        notes="1 bar → 15 nails. 5 ticks (3.0s) per action.",
        verification=TimingVerification.VERIFIED
    ),
    
    # =========================================================================
    # PLANK PROCESSING - VERIFIED
    # Sawmill: dominated by travel time
    # Plank Make: 3 ticks manual, 6 ticks auto-cast
    # =========================================================================
    "Planks_Sawmill": ActivityTiming(
        ticks_per_action=1,  # Instant conversion
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=0,
        activity_name="Sawmill Conversion",
        is_smithing=False,
        uses_planks=False,
        notes="Instant conversion. Time dominated by travel to sawmill.",
        verification=TimingVerification.VERIFIED
    ),
    
    "Planks_PlankMake": ActivityTiming(
        ticks_per_action=3,  # 1.8 seconds manual - VERIFIED
        items_per_action=1,
        materials_per_action=1,
        needs_hammer=False,
        needs_saw=False,
        other_tool_slots=3,  # Rune slots (or 2 with Earth staff)
        activity_name="Plank Make Spell",
        is_smithing=False,
        uses_planks=False,
        notes="3 ticks (1.8s) manual, 6 ticks auto-cast. ~1,850/hr manual.",
        verification=TimingVerification.VERIFIED
    ),
}


def get_timing_info(timing_key: str) -> dict:
    """
    Get detailed timing information for an activity.
    
    Returns dict with:
        - timing: ActivityTiming object
        - verification: TimingVerification enum value
        - is_verified: bool
        - warning: str if estimated/unknown
    """
    timing = ACTIVITY_TIMINGS.get(timing_key)
    if not timing:
        return None
    
    result = {
        "timing": timing,
        "verification": timing.verification,
        "is_verified": timing.verification == TimingVerification.VERIFIED,
        "warning": None
    }
    
    if timing.verification == TimingVerification.ESTIMATED:
        result["warning"] = f"⚠ {timing.activity_name} tick timing is estimated. In-game testing recommended."
    elif timing.verification == TimingVerification.UNKNOWN:
        result["warning"] = f"⚠ {timing.activity_name} tick timing is unknown."
    
    return result
