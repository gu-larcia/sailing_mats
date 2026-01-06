"""
Processing chain generation for all Sailing materials.

Generates all possible processing chains for:
- Planks (log -> plank)
- Hull Parts (plank -> hull parts)
- Large Hull Parts (hull parts -> large hull parts)
- Hull Repair Kits (planks + nails + swamp paste -> kit)
- Keel Parts (bar -> keel parts)
- Large Keel Parts (keel parts -> large keel parts)
- Nails (bar -> nails)
- Cannonballs (bar -> cannonballs)

RATIOS VERIFIED FROM RESEARCH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Hull/Keel parts: 5:1 standard ratio
✓ Dragon items: 2:1 ratio (dragon metal sheets)
✓ Nails: 15 per bar
✓ Cannonballs: 4 per bar (8 with double mould)
✓ Repair kits: 2 planks + 10 nails + 5 swamp paste → 2 kits
"""

from typing import Dict, List
from .dataclasses import ProcessingChain, ChainStep


def generate_all_chains() -> Dict[str, List[ProcessingChain]]:
    """
    Generate all processing chains for Sailing materials.
    
    Returns:
        Dict mapping category name to list of ProcessingChain objects
    """
    chains = {
        "Planks": [],
        "Hull Parts": [],
        "Large Hull Parts": [],
        "Hull Repair Kits": [],
        "Keel Parts": [],
        "Large Keel Parts": [],
        "Nails": [],
        "Cannonballs": [],
    }
    
    # ========================================================================
    # PLANKS (log -> plank via Sawmill or Plank Make)
    # ========================================================================
    plank_mappings = [
        (1511, "Logs", 960, "Plank"),
        (1521, "Oak logs", 8778, "Oak plank"),
        (6333, "Teak logs", 8780, "Teak plank"),
        (6332, "Mahogany logs", 8782, "Mahogany plank"),
        (32904, "Camphor logs", 31432, "Camphor plank"),
        (32907, "Ironwood logs", 31435, "Ironwood plank"),
        (32910, "Rosewood logs", 31438, "Rosewood plank"),
    ]
    
    for log_id, log_name, plank_id, plank_name in plank_mappings:
        chain = ProcessingChain(
            name=f"{plank_name} processing",
            category="Planks"
        )
        chain.steps = [
            ChainStep(log_id, log_name, 1),
            ChainStep(plank_id, plank_name, 1, processing_method="Sawmill")
        ]
        chains["Planks"].append(chain)
    
    # ========================================================================
    # HULL PARTS (5 planks -> 1 hull part) - VERIFIED 5:1 ratio
    # ========================================================================
    hull_mappings = [
        (960, "Plank", 32041, "Wooden hull parts"),
        (8778, "Oak plank", 32044, "Oak hull parts"),
        (8780, "Teak plank", 32047, "Teak hull parts"),
        (8782, "Mahogany plank", 32050, "Mahogany hull parts"),
        (31432, "Camphor plank", 32053, "Camphor hull parts"),
        (31435, "Ironwood plank", 32056, "Ironwood hull parts"),
        (31438, "Rosewood plank", 32059, "Rosewood hull parts"),
    ]
    
    for plank_id, plank_name, hull_id, hull_name in hull_mappings:
        chain = ProcessingChain(
            name=hull_name,
            category="Hull Parts"
        )
        chain.steps = [
            ChainStep(plank_id, plank_name, 5),  # 5:1 ratio - VERIFIED
            ChainStep(hull_id, hull_name, 1)
        ]
        chains["Hull Parts"].append(chain)
    
    # ========================================================================
    # LARGE HULL PARTS (5 hull parts -> 1 large hull part) - VERIFIED 5:1
    # ========================================================================
    large_hull_mappings = [
        (32041, "Wooden hull parts", 32062, "Large wooden hull parts"),
        (32044, "Oak hull parts", 32065, "Large oak hull parts"),
        (32047, "Teak hull parts", 32068, "Large teak hull parts"),
        (32050, "Mahogany hull parts", 32071, "Large mahogany hull parts"),
        (32053, "Camphor hull parts", 32074, "Large camphor hull parts"),
        (32056, "Ironwood hull parts", 32077, "Large ironwood hull parts"),
        (32059, "Rosewood hull parts", 32080, "Large rosewood hull parts"),
    ]
    
    for hull_id, hull_name, large_id, large_name in large_hull_mappings:
        chain = ProcessingChain(
            name=large_name,
            category="Large Hull Parts"
        )
        chain.steps = [
            ChainStep(hull_id, hull_name, 5),  # 5:1 ratio - VERIFIED
            ChainStep(large_id, large_name, 1)
        ]
        chains["Large Hull Parts"].append(chain)
    
    # ========================================================================
    # HULL REPAIR KITS (planks + nails + swamp paste -> kits)
    # VERIFIED from research:
    # - Basic: 2 planks + 10 bronze nails + 5 swamp paste → 2 kits
    # - Higher tiers require Shipwrights' Workbench
    # ========================================================================
    repair_kit_mappings = [
        # (plank_id, plank_name, nail_id, nail_name, paste_qty, plank_qty, nail_qty, output_qty, kit_id, kit_name)
        (960, "Plank", 4819, "Bronze nails", 5, 2, 10, 2, 31964, "Repair kit"),
        (8778, "Oak plank", 4820, "Iron nails", 5, 2, 10, 2, 31967, "Oak repair kit"),
        (8780, "Teak plank", 1539, "Steel nails", 5, 2, 10, 2, 31970, "Teak repair kit"),
        (8782, "Mahogany plank", 4822, "Mithril nails", 5, 2, 10, 2, 31973, "Mahogany repair kit"),
        (31432, "Camphor plank", 4823, "Adamantite nails", 5, 2, 10, 2, 31976, "Camphor repair kit"),
        (31435, "Ironwood plank", 4824, "Rune nails", 5, 1, 10, 3, 31979, "Ironwood repair kit"),
        (31438, "Rosewood plank", 31406, "Dragon nails", 5, 1, 5, 3, 31982, "Rosewood repair kit"),
    ]
    
    for plank_id, plank_name, nail_id, nail_name, paste_qty, plank_qty, nail_qty, output_qty, kit_id, kit_name in repair_kit_mappings:
        chain = ProcessingChain(
            name=kit_name,
            category="Hull Repair Kits"
        )
        chain.steps = [
            ChainStep(plank_id, plank_name, plank_qty),
            ChainStep(nail_id, nail_name, nail_qty),
            ChainStep(1941, "Swamp paste", paste_qty),
            ChainStep(kit_id, kit_name, output_qty)
        ]
        chains["Hull Repair Kits"].append(chain)
    
    # ========================================================================
    # KEEL PARTS (5 bars -> 1 keel part) - VERIFIED
    # Dragon: 2 sheets -> 1 part (VERIFIED 2:1 ratio)
    # ========================================================================
    keel_mappings = [
        # (bar_id, bar_name, keel_id, keel_name, input_qty)
        (2349, "Bronze bar", 31999, "Bronze keel parts", 5),
        (2351, "Iron bar", 32002, "Iron keel parts", 5),
        (2353, "Steel bar", 32005, "Steel keel parts", 5),
        (2359, "Mithril bar", 32008, "Mithril keel parts", 5),
        (2361, "Adamantite bar", 32011, "Adamant keel parts", 5),
        (2363, "Runite bar", 32014, "Rune keel parts", 5),
        (31996, "Dragon metal sheet", 32017, "Dragon keel parts", 2),  # 2:1 ratio - VERIFIED
    ]
    
    for bar_id, bar_name, keel_id, keel_name, qty in keel_mappings:
        chain = ProcessingChain(
            name=keel_name,
            category="Keel Parts"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, qty),
            ChainStep(keel_id, keel_name, 1)
        ]
        chains["Keel Parts"].append(chain)
    
    # ========================================================================
    # LARGE KEEL PARTS (5 parts -> 1 large) - VERIFIED
    # Dragon: 2 -> 1 (VERIFIED 2:1 ratio)
    # ========================================================================
    large_keel_mappings = [
        (31999, "Bronze keel parts", 32020, "Large bronze keel parts", 5),
        (32002, "Iron keel parts", 32023, "Large iron keel parts", 5),
        (32005, "Steel keel parts", 32026, "Large steel keel parts", 5),
        (32008, "Mithril keel parts", 32029, "Large mithril keel parts", 5),
        (32011, "Adamant keel parts", 32032, "Large adamant keel parts", 5),
        (32014, "Rune keel parts", 32035, "Large rune keel parts", 5),
        (32017, "Dragon keel parts", 32038, "Large dragon keel parts", 2),  # 2:1 - VERIFIED
    ]
    
    for keel_id, keel_name, large_id, large_name, qty in large_keel_mappings:
        chain = ProcessingChain(
            name=large_name,
            category="Large Keel Parts"
        )
        chain.steps = [
            ChainStep(keel_id, keel_name, qty),
            ChainStep(large_id, large_name, 1)
        ]
        if qty == 2:
            chain.special_ratio = {"conversion_ratio": 2}
        chains["Large Keel Parts"].append(chain)
    
    # ========================================================================
    # NAILS (1 bar -> 15 nails) - VERIFIED 15:1 ratio
    # ========================================================================
    nail_mappings = [
        (2349, "Bronze bar", 4819, "Bronze nails"),
        (2351, "Iron bar", 4820, "Iron nails"),
        (2353, "Steel bar", 1539, "Steel nails"),
        (2359, "Mithril bar", 4822, "Mithril nails"),
        (2361, "Adamantite bar", 4823, "Adamantite nails"),
        (2363, "Runite bar", 4824, "Rune nails"),
        (31996, "Dragon metal sheet", 31406, "Dragon nails"),
    ]
    
    for bar_id, bar_name, nail_id, nail_name in nail_mappings:
        chain = ProcessingChain(
            name=f"{nail_name} smithing",
            category="Nails"
        )
        processing = "Dragon Forge" if "Dragon" in nail_name else "Smithing"
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(nail_id, nail_name, 15, processing_method=processing)  # 15:1 - VERIFIED
        ]
        chains["Nails"].append(chain)
    
    # ========================================================================
    # CANNONBALLS (1 bar -> 4 balls) - VERIFIED
    # Double mould: 2 bars -> 8 balls (same time as single)
    # Note: Dragon cannonballs are drop-only and cannot be smithed
    # ========================================================================
    cannonball_mappings = [
        (2349, "Bronze bar", 31906, "Bronze cannonball"),
        (2351, "Iron bar", 31908, "Iron cannonball"),
        (2353, "Steel bar", 2, "Steel cannonball"),
        (2359, "Mithril bar", 31910, "Mithril cannonball"),
        (2361, "Adamantite bar", 31912, "Adamant cannonball"),
        (2363, "Runite bar", 31914, "Rune cannonball"),
    ]
    
    for bar_id, bar_name, ball_id, ball_name in cannonball_mappings:
        # Regular ammo mould (1 bar -> 4 balls) - VERIFIED
        chain = ProcessingChain(
            name=f"{ball_name} (Regular)",
            category="Cannonballs"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(ball_id, ball_name, 4)  # 4:1 - VERIFIED
        ]
        chains["Cannonballs"].append(chain)
        
        # Double ammo mould (2 bars -> 8 balls per action) - VERIFIED
        chain_double = ProcessingChain(
            name=f"{ball_name} (Double)",
            category="Cannonballs"
        )
        chain_double.steps = [
            ChainStep(bar_id, bar_name, 2),
            ChainStep(ball_id, ball_name, 8)  # 8:2 (same as 4:1) - VERIFIED
        ]
        chains["Cannonballs"].append(chain_double)
    
    return chains
