"""Processing chain generation."""

from typing import Dict, List
from .dataclasses import ProcessingChain, ChainStep


def generate_all_chains() -> Dict[str, List[ProcessingChain]]:
    """Generate all processing chains. Returns category -> chain list."""
    chains = {
        "Planks": [],
        "Hull Parts": [],
        "Large Hull Parts": [],
        "Hull Repair Kits": [],
        "Keel Parts": [],
        "Large Keel Parts": [],
        "Nails": [],
        "Cannonballs": [],
        "Bar Smelting": [],
        "Unstrung Bows": [],
        "Strung Bows": [],
        "Arrows": [],
        "Darts": [],
    }
    
    # Planks: log -> plank
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
    
    # Hull Parts: 5 planks -> 1 part
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
            ChainStep(plank_id, plank_name, 5),
            ChainStep(hull_id, hull_name, 1)
        ]
        chains["Hull Parts"].append(chain)
    
    # Large Hull Parts: 5 parts -> 1 large
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
            ChainStep(hull_id, hull_name, 5),
            ChainStep(large_id, large_name, 1)
        ]
        chains["Large Hull Parts"].append(chain)
    
    # Hull Repair Kits: planks + nails + swamp paste -> kits
    # (plank_id, plank_name, nail_id, nail_name, paste_qty, plank_qty, nail_qty, output_qty, kit_id, kit_name)
    repair_kit_mappings = [
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
    
    # Keel Parts: 5 bars -> 1 part (dragon: 2 sheets -> 1)
    keel_mappings = [
        (2349, "Bronze bar", 31999, "Bronze keel parts", 5),
        (2351, "Iron bar", 32002, "Iron keel parts", 5),
        (2353, "Steel bar", 32005, "Steel keel parts", 5),
        (2359, "Mithril bar", 32008, "Mithril keel parts", 5),
        (2361, "Adamantite bar", 32011, "Adamant keel parts", 5),
        (2363, "Runite bar", 32014, "Rune keel parts", 5),
        (31996, "Dragon metal sheet", 32017, "Dragon keel parts", 2),
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
    
    # Large Keel Parts: 5 parts -> 1 large (dragon: 2 -> 1)
    large_keel_mappings = [
        (31999, "Bronze keel parts", 32020, "Large bronze keel parts", 5),
        (32002, "Iron keel parts", 32023, "Large iron keel parts", 5),
        (32005, "Steel keel parts", 32026, "Large steel keel parts", 5),
        (32008, "Mithril keel parts", 32029, "Large mithril keel parts", 5),
        (32011, "Adamant keel parts", 32032, "Large adamant keel parts", 5),
        (32014, "Rune keel parts", 32035, "Large rune keel parts", 5),
        (32017, "Dragon keel parts", 32038, "Large dragon keel parts", 2),
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
    
    # Nails: 1 bar -> 15 nails
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
            ChainStep(nail_id, nail_name, 15, processing_method=processing)
        ]
        chains["Nails"].append(chain)
    
    # Cannonballs: 1 bar -> 4 balls (double: 2 bars -> 8)
    # Dragon cannonballs are drop-only
    cannonball_mappings = [
        (2349, "Bronze bar", 31906, "Bronze cannonball"),
        (2351, "Iron bar", 31908, "Iron cannonball"),
        (2353, "Steel bar", 2, "Steel cannonball"),
        (2359, "Mithril bar", 31910, "Mithril cannonball"),
        (2361, "Adamantite bar", 31912, "Adamant cannonball"),
        (2363, "Runite bar", 31914, "Rune cannonball"),
    ]
    
    for bar_id, bar_name, ball_id, ball_name in cannonball_mappings:
        # Single mould
        chain = ProcessingChain(
            name=f"{ball_name} (Regular)",
            category="Cannonballs"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(ball_id, ball_name, 4)
        ]
        chains["Cannonballs"].append(chain)
        
        # Double mould
        chain_double = ProcessingChain(
            name=f"{ball_name} (Double)",
            category="Cannonballs"
        )
        chain_double.steps = [
            ChainStep(bar_id, bar_name, 2),
            ChainStep(ball_id, ball_name, 8)
        ]
        chains["Cannonballs"].append(chain_double)
    
    # Bar Smelting: ore(s) -> bar at regular furnace or Blast Furnace
    # Blast Furnace halves coal requirement; iron is 100% success (vs 50% at regular furnace)
    # (bar_id, bar_name, primary_ores, regular_coal, bf_coal)
    smelting_recipes = [
        (2349, "Bronze bar", [(436, "Copper ore", 1), (438, "Tin ore", 1)], 0, 0),
        (2351, "Iron bar", [(440, "Iron ore", 1)], 0, 0),
        (2355, "Silver bar", [(442, "Silver ore", 1)], 0, 0),
        (2357, "Gold bar", [(444, "Gold ore", 1)], 0, 0),
        (2353, "Steel bar", [(440, "Iron ore", 1)], 2, 1),
        (2359, "Mithril bar", [(447, "Mithril ore", 1)], 4, 2),
        (2361, "Adamantite bar", [(449, "Adamantite ore", 1)], 6, 3),
        (2363, "Runite bar", [(451, "Runite ore", 1)], 8, 4),
    ]

    for bar_id, bar_name, primary_ores, regular_coal, bf_coal in smelting_recipes:
        # Regular furnace chain
        chain_reg = ProcessingChain(
            name=f"{bar_name} (Furnace)",
            category="Bar Smelting"
        )
        reg_steps = [ChainStep(ore_id, ore_name, qty) for ore_id, ore_name, qty in primary_ores]
        if regular_coal > 0:
            reg_steps.append(ChainStep(453, "Coal", regular_coal))
        reg_steps.append(ChainStep(bar_id, bar_name, 1, processing_method="Smelting"))
        chain_reg.steps = reg_steps
        chains["Bar Smelting"].append(chain_reg)

        # Blast Furnace chain
        chain_bf = ProcessingChain(
            name=f"{bar_name} (Blast Furnace)",
            category="Bar Smelting"
        )
        bf_steps = [ChainStep(ore_id, ore_name, qty) for ore_id, ore_name, qty in primary_ores]
        if bf_coal > 0:
            bf_steps.append(ChainStep(453, "Coal", bf_coal))
        bf_steps.append(ChainStep(bar_id, bar_name, 1, processing_method="Blast Furnace"))
        chain_bf.steps = bf_steps
        chains["Bar Smelting"].append(chain_bf)

    # Fletching: Unstrung Bows (log -> bow (u))
    # 1 log -> 1 unstrung bow, no GP cost (just a knife)
    bow_u_mappings = [
        (1511, "Logs", 50, "Shortbow (u)"),
        (1511, "Logs", 48, "Longbow (u)"),
        (1521, "Oak logs", 54, "Oak shortbow (u)"),
        (1521, "Oak logs", 56, "Oak longbow (u)"),
        (1519, "Willow logs", 60, "Willow shortbow (u)"),
        (1519, "Willow logs", 58, "Willow longbow (u)"),
        (1517, "Maple logs", 64, "Maple shortbow (u)"),
        (1517, "Maple logs", 62, "Maple longbow (u)"),
        (1515, "Yew logs", 68, "Yew shortbow (u)"),
        (1515, "Yew logs", 66, "Yew longbow (u)"),
        (1513, "Magic logs", 72, "Magic shortbow (u)"),
        (1513, "Magic logs", 70, "Magic longbow (u)"),
    ]

    for log_id, log_name, bow_u_id, bow_u_name in bow_u_mappings:
        chain = ProcessingChain(
            name=f"{bow_u_name} fletching",
            category="Unstrung Bows"
        )
        chain.steps = [
            ChainStep(log_id, log_name, 1),
            ChainStep(bow_u_id, bow_u_name, 1, processing_method="Fletching")
        ]
        chains["Unstrung Bows"].append(chain)

    # Fletching: Strung Bows (bow (u) + bow string -> bow)
    strung_bow_mappings = [
        (50, "Shortbow (u)", 841, "Shortbow"),
        (48, "Longbow (u)", 839, "Longbow"),
        (54, "Oak shortbow (u)", 843, "Oak shortbow"),
        (56, "Oak longbow (u)", 845, "Oak longbow"),
        (60, "Willow shortbow (u)", 849, "Willow shortbow"),
        (58, "Willow longbow (u)", 847, "Willow longbow"),
        (64, "Maple shortbow (u)", 853, "Maple shortbow"),
        (62, "Maple longbow (u)", 851, "Maple longbow"),
        (68, "Yew shortbow (u)", 857, "Yew shortbow"),
        (66, "Yew longbow (u)", 855, "Yew longbow"),
        (72, "Magic shortbow (u)", 861, "Magic shortbow"),
        (70, "Magic longbow (u)", 859, "Magic longbow"),
    ]

    for bow_u_id, bow_u_name, bow_id, bow_name in strung_bow_mappings:
        chain = ProcessingChain(
            name=f"{bow_name} stringing",
            category="Strung Bows"
        )
        chain.steps = [
            ChainStep(bow_u_id, bow_u_name, 1),
            ChainStep(1777, "Bow string", 1),
            ChainStep(bow_id, bow_name, 1, processing_method="Fletching")
        ]
        chains["Strung Bows"].append(chain)

    # Fletching: Arrows (headless arrow + arrowtips -> arrows)
    # Ratio is 1:1:1 per arrow; user sets quantity for batch size
    arrow_mappings = [
        (39, "Bronze arrowtips", 882, "Bronze arrow"),
        (40, "Iron arrowtips", 884, "Iron arrow"),
        (41, "Steel arrowtips", 886, "Steel arrow"),
        (42, "Mithril arrowtips", 888, "Mithril arrow"),
        (43, "Adamant arrowtips", 890, "Adamant arrow"),
        (44, "Rune arrowtips", 892, "Rune arrow"),
        (11237, "Dragon arrowtips", 11212, "Dragon arrow"),
        (21350, "Amethyst arrowtips", 21326, "Amethyst arrow"),
    ]

    for tip_id, tip_name, arrow_id, arrow_name in arrow_mappings:
        chain = ProcessingChain(
            name=f"{arrow_name} fletching",
            category="Arrows"
        )
        chain.steps = [
            ChainStep(53, "Headless arrow", 1),
            ChainStep(tip_id, tip_name, 1),
            ChainStep(arrow_id, arrow_name, 1, processing_method="Fletching")
        ]
        chains["Arrows"].append(chain)

    # Fletching: Darts (dart tip + feather -> dart)
    dart_mappings = [
        (819, "Bronze dart tip", 806, "Bronze dart"),
        (820, "Iron dart tip", 807, "Iron dart"),
        (821, "Steel dart tip", 808, "Steel dart"),
        (822, "Mithril dart tip", 809, "Mithril dart"),
        (823, "Adamant dart tip", 810, "Adamant dart"),
        (824, "Rune dart tip", 811, "Rune dart"),
        (11232, "Dragon dart tip", 11230, "Dragon dart"),
        (21352, "Amethyst dart tip", 21332, "Amethyst dart"),
    ]

    for tip_id, tip_name, dart_id, dart_name in dart_mappings:
        chain = ProcessingChain(
            name=f"{dart_name} fletching",
            category="Darts"
        )
        chain.steps = [
            ChainStep(tip_id, tip_name, 1),
            ChainStep(314, "Feather", 1),
            ChainStep(dart_id, dart_name, 1, processing_method="Fletching")
        ]
        chains["Darts"].append(chain)

    # Fletching: Crossbow Stocks (log -> stock)
    # 1 log -> 1 stock, no GP cost (just a knife)
    chains["Crossbow Stocks"] = []
    stock_mappings = [
        (1511, "Logs", 9440, "Wooden stock"),
        (1521, "Oak logs", 9442, "Oak stock"),
        (1519, "Willow logs", 9444, "Willow stock"),
        (6333, "Teak logs", 9446, "Teak stock"),
        (1517, "Maple logs", 9448, "Maple stock"),
        (6332, "Mahogany logs", 9450, "Mahogany stock"),
        (1515, "Yew logs", 9452, "Yew stock"),
        (1513, "Magic logs", 21952, "Magic stock"),
    ]

    for log_id, log_name, stock_id, stock_name in stock_mappings:
        chain = ProcessingChain(
            name=f"{stock_name} fletching",
            category="Crossbow Stocks"
        )
        chain.steps = [
            ChainStep(log_id, log_name, 1),
            ChainStep(stock_id, stock_name, 1, processing_method="Fletching")
        ]
        chains["Crossbow Stocks"].append(chain)

    # Fletching: Crossbow Limbs (bar -> limbs via Smithing, 1 bar -> 1 limb)
    # Dragon limbs are drop-only, not included
    chains["Crossbow Limbs"] = []
    limb_mappings = [
        (2349, "Bronze bar", 9420, "Bronze limbs"),
        (2351, "Iron bar", 9423, "Iron limbs"),
        (2353, "Steel bar", 9425, "Steel limbs"),
        (2359, "Mithril bar", 9427, "Mithril limbs"),
        (2361, "Adamantite bar", 9429, "Adamantite limbs"),
        (2363, "Runite bar", 9431, "Runite limbs"),
    ]

    for bar_id, bar_name, limb_id, limb_name in limb_mappings:
        chain = ProcessingChain(
            name=f"{limb_name} smithing",
            category="Crossbow Limbs"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(limb_id, limb_name, 1, processing_method="Smithing")
        ]
        chains["Crossbow Limbs"].append(chain)

    # Fletching: Unstrung Crossbows (stock + limbs -> crossbow (u))
    chains["Crossbows (u)"] = []
    crossbow_u_mappings = [
        # (stock_id, stock_name, limb_id, limb_name, xbow_u_id, xbow_u_name)
        (9440, "Wooden stock", 9420, "Bronze limbs", 9454, "Bronze crossbow (u)"),
        (9444, "Willow stock", 9423, "Iron limbs", 9457, "Iron crossbow (u)"),
        (9446, "Teak stock", 9425, "Steel limbs", 9459, "Steel crossbow (u)"),
        (9448, "Maple stock", 9427, "Mithril limbs", 9461, "Mithril crossbow (u)"),
        (9450, "Mahogany stock", 9429, "Adamantite limbs", 9463, "Adamant crossbow (u)"),
        (9452, "Yew stock", 9431, "Runite limbs", 9465, "Runite crossbow (u)"),
        (21952, "Magic stock", 21918, "Dragon limbs", 21921, "Dragon crossbow (u)"),
    ]

    for stock_id, stock_name, limb_id, limb_name, xbow_u_id, xbow_u_name in crossbow_u_mappings:
        chain = ProcessingChain(
            name=f"{xbow_u_name} fletching",
            category="Crossbows (u)"
        )
        chain.steps = [
            ChainStep(stock_id, stock_name, 1),
            ChainStep(limb_id, limb_name, 1),
            ChainStep(xbow_u_id, xbow_u_name, 1, processing_method="Fletching")
        ]
        chains["Crossbows (u)"].append(chain)

    # Fletching: Strung Crossbows (crossbow (u) + crossbow string -> crossbow)
    chains["Crossbows"] = []
    crossbow_strung_mappings = [
        (9454, "Bronze crossbow (u)", 9174, "Bronze crossbow"),
        (9457, "Iron crossbow (u)", 9177, "Iron crossbow"),
        (9459, "Steel crossbow (u)", 9179, "Steel crossbow"),
        (9461, "Mithril crossbow (u)", 9181, "Mithril crossbow"),
        (9463, "Adamant crossbow (u)", 9183, "Adamant crossbow"),
        (9465, "Runite crossbow (u)", 9185, "Rune crossbow"),
        (21921, "Dragon crossbow (u)", 21902, "Dragon crossbow"),
    ]

    for xbow_u_id, xbow_u_name, xbow_id, xbow_name in crossbow_strung_mappings:
        chain = ProcessingChain(
            name=f"{xbow_name} stringing",
            category="Crossbows"
        )
        chain.steps = [
            ChainStep(xbow_u_id, xbow_u_name, 1),
            ChainStep(9438, "Crossbow string", 1),
            ChainStep(xbow_id, xbow_name, 1, processing_method="Fletching")
        ]
        chains["Crossbows"].append(chain)

    # Fletching: Bolts (unf) (bar -> unfinished bolts via Smithing, 1 bar -> 10 bolts)
    # Dragon bolts (unf) are not smithed, excluded here
    chains["Bolts (unf)"] = []
    bolt_unf_mappings = [
        (2349, "Bronze bar", 9375, "Bronze bolts (unf)"),
        (2351, "Iron bar", 9377, "Iron bolts (unf)"),
        (2353, "Steel bar", 9378, "Steel bolts (unf)"),
        (2359, "Mithril bar", 9379, "Mithril bolts (unf)"),
        (2361, "Adamantite bar", 9380, "Adamant bolts (unf)"),
        (2363, "Runite bar", 9381, "Runite bolts (unf)"),
    ]

    for bar_id, bar_name, bolt_unf_id, bolt_unf_name in bolt_unf_mappings:
        chain = ProcessingChain(
            name=f"{bolt_unf_name} smithing",
            category="Bolts (unf)"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(bolt_unf_id, bolt_unf_name, 10, processing_method="Smithing")
        ]
        chains["Bolts (unf)"].append(chain)

    # Fletching: Bolts (unf bolts + feathers -> finished bolts, 1:1:1)
    chains["Bolts"] = []
    bolt_mappings = [
        (9375, "Bronze bolts (unf)", 877, "Bronze bolts"),
        (9377, "Iron bolts (unf)", 9140, "Iron bolts"),
        (9378, "Steel bolts (unf)", 9141, "Steel bolts"),
        (9379, "Mithril bolts (unf)", 9142, "Mithril bolts"),
        (9380, "Adamant bolts (unf)", 9143, "Adamant bolts"),
        (9381, "Runite bolts (unf)", 9144, "Runite bolts"),
        (21930, "Dragon bolts (unf)", 21905, "Dragon bolts"),
    ]

    for bolt_unf_id, bolt_unf_name, bolt_id, bolt_name in bolt_mappings:
        chain = ProcessingChain(
            name=f"{bolt_name} fletching",
            category="Bolts"
        )
        chain.steps = [
            ChainStep(bolt_unf_id, bolt_unf_name, 1),
            ChainStep(314, "Feather", 1),
            ChainStep(bolt_id, bolt_name, 1, processing_method="Fletching")
        ]
        chains["Bolts"].append(chain)

    # Fletching: Javelin Heads (bar -> javelin heads via Smithing, 1 bar -> 5 heads)
    # Dragon javelin heads are not smithed, excluded here
    chains["Javelin Heads"] = []
    jav_head_mappings = [
        (2349, "Bronze bar", 19570, "Bronze javelin heads"),
        (2351, "Iron bar", 19572, "Iron javelin heads"),
        (2353, "Steel bar", 19574, "Steel javelin heads"),
        (2359, "Mithril bar", 19576, "Mithril javelin heads"),
        (2361, "Adamantite bar", 19578, "Adamant javelin heads"),
        (2363, "Runite bar", 19580, "Rune javelin heads"),
    ]

    for bar_id, bar_name, head_id, head_name in jav_head_mappings:
        chain = ProcessingChain(
            name=f"{head_name} smithing",
            category="Javelin Heads"
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(head_id, head_name, 5, processing_method="Smithing")
        ]
        chains["Javelin Heads"].append(chain)

    # Fletching: Javelins (javelin heads + javelin shafts -> javelins, 1:1:1)
    chains["Javelins"] = []
    javelin_mappings = [
        (19570, "Bronze javelin heads", 825, "Bronze javelin"),
        (19572, "Iron javelin heads", 826, "Iron javelin"),
        (19574, "Steel javelin heads", 827, "Steel javelin"),
        (19576, "Mithril javelin heads", 828, "Mithril javelin"),
        (19578, "Adamant javelin heads", 829, "Adamant javelin"),
        (19580, "Rune javelin heads", 830, "Rune javelin"),
        (19582, "Dragon javelin heads", 19484, "Dragon javelin"),
    ]

    for head_id, head_name, jav_id, jav_name in javelin_mappings:
        chain = ProcessingChain(
            name=f"{jav_name} fletching",
            category="Javelins"
        )
        chain.steps = [
            ChainStep(head_id, head_name, 1),
            ChainStep(19584, "Javelin shaft", 1),
            ChainStep(jav_id, jav_name, 1, processing_method="Fletching")
        ]
        chains["Javelins"].append(chain)

    # Extended Chains: compose existing recipes into full pipelines
    # (ore/log to final product). Intermediate items use is_self_obtained
    # so they are costed from raw materials, not the GE. Step quantities
    # are pre-scaled so the backward ratio calculation resolves correctly.

    # Only bars with downstream products (exclude silver, gold)
    smeltable = [r for r in smelting_recipes if r[0] not in (2355, 2357)]

    # Metal: Ore -> Bar -> Product
    chains["Nails (from Ore)"] = []
    chains["Keel Parts (from Ore)"] = []
    chains["Cannonballs (from Ore)"] = []

    # (bar_id, product_id, product_name, bars_needed, output_qty, processing)
    ore_downstream = {
        "Nails (from Ore)": [
            (2349, 4819, "Bronze nails", 1, 15, "Smithing"),
            (2351, 4820, "Iron nails", 1, 15, "Smithing"),
            (2353, 1539, "Steel nails", 1, 15, "Smithing"),
            (2359, 4822, "Mithril nails", 1, 15, "Smithing"),
            (2361, 4823, "Adamantite nails", 1, 15, "Smithing"),
            (2363, 4824, "Rune nails", 1, 15, "Smithing"),
        ],
        "Keel Parts (from Ore)": [
            (2349, 31999, "Bronze keel parts", 5, 1, "Smithing"),
            (2351, 32002, "Iron keel parts", 5, 1, "Smithing"),
            (2353, 32005, "Steel keel parts", 5, 1, "Smithing"),
            (2359, 32008, "Mithril keel parts", 5, 1, "Smithing"),
            (2361, 32011, "Adamant keel parts", 5, 1, "Smithing"),
            (2363, 32014, "Rune keel parts", 5, 1, "Smithing"),
        ],
        "Cannonballs (from Ore)": [
            (2349, 31906, "Bronze cannonball", 1, 4, None),
            (2351, 31908, "Iron cannonball", 1, 4, None),
            (2353, 2, "Steel cannonball", 1, 4, None),
            (2359, 31910, "Mithril cannonball", 1, 4, None),
            (2361, 31912, "Adamant cannonball", 1, 4, None),
            (2363, 31914, "Rune cannonball", 1, 4, None),
        ],
    }

    for category_key, products in ore_downstream.items():
        for bar_id, prod_id, prod_name, bars_needed, output_qty, prod_processing in products:
            recipe = next((r for r in smeltable if r[0] == bar_id), None)
            if not recipe:
                continue
            _, bar_name, primary_ores, regular_coal, bf_coal = recipe

            for smelting_label, coal_qty, smelt_method in [
                ("Furnace", regular_coal, "Smelting"),
                ("BF", bf_coal, "Blast Furnace"),
            ]:
                chain = ProcessingChain(
                    name=f"{prod_name} ({smelting_label})",
                    category=category_key,
                )
                steps = []
                for ore_id, ore_name, ore_per_bar in primary_ores:
                    steps.append(ChainStep(ore_id, ore_name, ore_per_bar * bars_needed))
                if coal_qty > 0:
                    steps.append(ChainStep(453, "Coal", coal_qty * bars_needed))
                steps.append(ChainStep(
                    bar_id, bar_name, bars_needed,
                    is_self_obtained=True, processing_method=smelt_method,
                ))
                steps.append(ChainStep(prod_id, prod_name, output_qty, processing_method=prod_processing))
                chain.steps = steps
                chains[category_key].append(chain)

    # Metal: Bar -> Keel -> Large Keel (from GE-bought bars)
    chains["Large Keel Parts (from Bar)"] = []
    # (bar_id, bar_name, keel_id, keel_name, large_id, large_name, bars_per_keel, keels_per_large)
    large_keel_bar_mappings = [
        (2349, "Bronze bar", 31999, "Bronze keel parts", 32020, "Large bronze keel parts", 5, 5),
        (2351, "Iron bar", 32002, "Iron keel parts", 32023, "Large iron keel parts", 5, 5),
        (2353, "Steel bar", 32005, "Steel keel parts", 32026, "Large steel keel parts", 5, 5),
        (2359, "Mithril bar", 32008, "Mithril keel parts", 32029, "Large mithril keel parts", 5, 5),
        (2361, "Adamantite bar", 32011, "Adamant keel parts", 32032, "Large adamant keel parts", 5, 5),
        (2363, "Runite bar", 32014, "Rune keel parts", 32035, "Large rune keel parts", 5, 5),
        (31996, "Dragon metal sheet", 32017, "Dragon keel parts", 32038, "Large dragon keel parts", 2, 2),
    ]

    for bar_id, bar_name, keel_id, keel_name, large_id, large_name, bars_per_keel, keels_per_large in large_keel_bar_mappings:
        total_bars = bars_per_keel * keels_per_large
        chain = ProcessingChain(
            name=large_name,
            category="Large Keel Parts (from Bar)",
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, total_bars),
            ChainStep(keel_id, keel_name, keels_per_large, is_self_obtained=True),
            ChainStep(large_id, large_name, 1),
        ]
        chains["Large Keel Parts (from Bar)"].append(chain)

    # Metal: Ore -> Bar -> Keel -> Large Keel (full pipeline)
    chains["Large Keel Parts (from Ore)"] = []
    for bar_id, bar_name, keel_id, keel_name, large_id, large_name, bars_per_keel, keels_per_large in large_keel_bar_mappings:
        if bar_id == 31996:  # Dragon sheets aren't smelted
            continue
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, _, primary_ores, regular_coal, bf_coal = recipe
        total_bars = bars_per_keel * keels_per_large

        for smelting_label, coal_qty, smelt_method in [
            ("Furnace", regular_coal, "Smelting"),
            ("BF", bf_coal, "Blast Furnace"),
        ]:
            chain = ProcessingChain(
                name=f"{large_name} ({smelting_label})",
                category="Large Keel Parts (from Ore)",
            )
            steps = []
            for ore_id, ore_name, ore_per_bar in primary_ores:
                steps.append(ChainStep(ore_id, ore_name, ore_per_bar * total_bars))
            if coal_qty > 0:
                steps.append(ChainStep(453, "Coal", coal_qty * total_bars))
            steps.append(ChainStep(
                bar_id, bar_name, total_bars,
                is_self_obtained=True, processing_method=smelt_method,
            ))
            steps.append(ChainStep(keel_id, keel_name, keels_per_large, is_self_obtained=True))
            steps.append(ChainStep(large_id, large_name, 1))
            chain.steps = steps
            chains["Large Keel Parts (from Ore)"].append(chain)

    # Wood: Log -> Plank -> Hull Parts
    chains["Hull Parts (from Log)"] = []
    for log_id, log_name, plank_id, plank_name in plank_mappings:
        hull = next((h for h in hull_mappings if h[0] == plank_id), None)
        if not hull:
            continue
        _, _, hull_id, hull_name = hull
        planks_needed = 5  # 5 planks → 1 hull part
        chain = ProcessingChain(
            name=hull_name,
            category="Hull Parts (from Log)",
        )
        chain.steps = [
            ChainStep(log_id, log_name, planks_needed),
            ChainStep(plank_id, plank_name, planks_needed, is_self_obtained=True, processing_method="Sawmill"),
            ChainStep(hull_id, hull_name, 1),
        ]
        chains["Hull Parts (from Log)"].append(chain)

    # Wood: Log -> Plank -> Hull Part -> Large Hull Part
    chains["Large Hull Parts (from Log)"] = []
    for log_id, log_name, plank_id, plank_name in plank_mappings:
        hull = next((h for h in hull_mappings if h[0] == plank_id), None)
        if not hull:
            continue
        _, _, hull_id, hull_name = hull
        large = next((l for l in large_hull_mappings if l[0] == hull_id), None)
        if not large:
            continue
        _, _, large_id, large_name = large
        # 5 planks/hull × 5 hulls/large = 25 planks = 25 logs
        total_planks = 25
        chain = ProcessingChain(
            name=large_name,
            category="Large Hull Parts (from Log)",
        )
        chain.steps = [
            ChainStep(log_id, log_name, total_planks),
            ChainStep(plank_id, plank_name, total_planks, is_self_obtained=True, processing_method="Sawmill"),
            ChainStep(hull_id, hull_name, 5, is_self_obtained=True),
            ChainStep(large_id, large_name, 1),
        ]
        chains["Large Hull Parts (from Log)"].append(chain)

    # Wood: Log -> Plank -> Hull Repair Kit (+ GE nails and paste)
    chains["Repair Kits (from Log)"] = []
    for plank_id, plank_name, nail_id, nail_name, paste_qty, plank_qty, nail_qty, output_qty, kit_id, kit_name in repair_kit_mappings:
        log = next((p for p in plank_mappings if p[2] == plank_id), None)
        if not log:
            continue
        log_id, log_name, _, _ = log
        chain = ProcessingChain(
            name=kit_name,
            category="Repair Kits (from Log)",
        )
        chain.steps = [
            ChainStep(log_id, log_name, plank_qty),
            ChainStep(plank_id, plank_name, plank_qty, is_self_obtained=True, processing_method="Sawmill"),
            ChainStep(nail_id, nail_name, nail_qty),
            ChainStep(1941, "Swamp paste", paste_qty),
            ChainStep(kit_id, kit_name, output_qty),
        ]
        chains["Repair Kits (from Log)"].append(chain)

    # Fletching Extended: Log -> Bow (u) -> Strung Bow (self-obtain the (u))
    chains["Bows (from Log)"] = []
    for bow_u_log_id, bow_u_log_name, bow_u_id, bow_u_name in bow_u_mappings:
        strung = next((s for s in strung_bow_mappings if s[0] == bow_u_id), None)
        if not strung:
            continue
        _, _, bow_id, bow_name = strung
        chain = ProcessingChain(
            name=f"{bow_name} (from log)",
            category="Bows (from Log)",
        )
        chain.steps = [
            ChainStep(bow_u_log_id, bow_u_log_name, 1),
            ChainStep(bow_u_id, bow_u_name, 1, is_self_obtained=True, processing_method="Fletching"),
            ChainStep(1777, "Bow string", 1),
            ChainStep(bow_id, bow_name, 1),
        ]
        chains["Bows (from Log)"].append(chain)

    # Fletching Extended: Log -> Stock -> Crossbow (u) -> Crossbow (self-obtain stock)
    chains["Crossbows (from Log)"] = []
    for stock_log_id, stock_log_name, stock_id, stock_name in stock_mappings:
        xbow_u = next((x for x in crossbow_u_mappings if x[0] == stock_id), None)
        if not xbow_u:
            continue
        _, _, limb_id, limb_name, xbow_u_id, xbow_u_name = xbow_u
        strung_xbow = next((s for s in crossbow_strung_mappings if s[0] == xbow_u_id), None)
        if not strung_xbow:
            continue
        _, _, xbow_id, xbow_name = strung_xbow
        chain = ProcessingChain(
            name=f"{xbow_name} (from log)",
            category="Crossbows (from Log)",
        )
        chain.steps = [
            ChainStep(stock_log_id, stock_log_name, 1),
            ChainStep(stock_id, stock_name, 1, is_self_obtained=True, processing_method="Fletching"),
            ChainStep(limb_id, limb_name, 1),
            ChainStep(xbow_u_id, xbow_u_name, 1, is_self_obtained=True, processing_method="Fletching"),
            ChainStep(9438, "Crossbow string", 1),
            ChainStep(xbow_id, xbow_name, 1),
        ]
        chains["Crossbows (from Log)"].append(chain)

    # Fletching Extended: Ore -> Bar -> Bolts (unf) -> Bolts (full pipeline)
    chains["Bolts (from Ore)"] = []
    # Map bar_id -> (bolt_unf_id, bolt_unf_name, bolt_id, bolt_name)
    bolt_bar_to_product = {}
    for bolt_unf_bar_id, _, bolt_unf_id, bolt_unf_name in bolt_unf_mappings:
        finished = next((b for b in bolt_mappings if b[0] == bolt_unf_id), None)
        if finished:
            _, _, bolt_id, bolt_name = finished
            bolt_bar_to_product[bolt_unf_bar_id] = (bolt_unf_id, bolt_unf_name, bolt_id, bolt_name)

    for bar_id, bolt_info in bolt_bar_to_product.items():
        bolt_unf_id, bolt_unf_name, bolt_id, bolt_name = bolt_info
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, bar_name, primary_ores, regular_coal, bf_coal = recipe

        for smelting_label, coal_qty, smelt_method in [
            ("Furnace", regular_coal, "Smelting"),
            ("BF", bf_coal, "Blast Furnace"),
        ]:
            chain = ProcessingChain(
                name=f"{bolt_name} ({smelting_label})",
                category="Bolts (from Ore)",
            )
            steps = []
            for ore_id, ore_name, ore_per_bar in primary_ores:
                steps.append(ChainStep(ore_id, ore_name, ore_per_bar))
            if coal_qty > 0:
                steps.append(ChainStep(453, "Coal", coal_qty))
            steps.append(ChainStep(
                bar_id, bar_name, 1,
                is_self_obtained=True, processing_method=smelt_method,
            ))
            steps.append(ChainStep(bolt_unf_id, bolt_unf_name, 10, is_self_obtained=True, processing_method="Smithing"))
            steps.append(ChainStep(314, "Feather", 10))
            steps.append(ChainStep(bolt_id, bolt_name, 10))
            chain.steps = steps
            chains["Bolts (from Ore)"].append(chain)

    # Fletching Extended: Ore -> Bar -> Javelin Heads -> Javelins (full pipeline)
    chains["Javelins (from Ore)"] = []
    # Map bar_id -> (head_id, head_name, jav_id, jav_name)
    jav_bar_to_product = {}
    for jav_bar_id, _, jav_head_id, jav_head_name in jav_head_mappings:
        finished_jav = next((j for j in javelin_mappings if j[0] == jav_head_id), None)
        if finished_jav:
            _, _, jav_id, jav_name = finished_jav
            jav_bar_to_product[jav_bar_id] = (jav_head_id, jav_head_name, jav_id, jav_name)

    for bar_id, jav_info in jav_bar_to_product.items():
        jav_head_id, jav_head_name, jav_id, jav_name = jav_info
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, bar_name, primary_ores, regular_coal, bf_coal = recipe

        for smelting_label, coal_qty, smelt_method in [
            ("Furnace", regular_coal, "Smelting"),
            ("BF", bf_coal, "Blast Furnace"),
        ]:
            chain = ProcessingChain(
                name=f"{jav_name} ({smelting_label})",
                category="Javelins (from Ore)",
            )
            steps = []
            for ore_id, ore_name, ore_per_bar in primary_ores:
                steps.append(ChainStep(ore_id, ore_name, ore_per_bar))
            if coal_qty > 0:
                steps.append(ChainStep(453, "Coal", coal_qty))
            steps.append(ChainStep(
                bar_id, bar_name, 1,
                is_self_obtained=True, processing_method=smelt_method,
            ))
            steps.append(ChainStep(jav_head_id, jav_head_name, 5, is_self_obtained=True, processing_method="Smithing"))
            steps.append(ChainStep(19584, "Javelin shaft", 5))
            steps.append(ChainStep(jav_id, jav_name, 5))
            chain.steps = steps
            chains["Javelins (from Ore)"].append(chain)

    # Fletching Extended: Bar -> Arrowtips -> Arrows (bar smithing + fletching)
    # Bar -> 15 arrowtips via Smithing, then tips + headless arrows -> arrows
    chains["Arrows (from Bar)"] = []
    arrow_bar_mappings = [
        (2349, "Bronze bar", 39, "Bronze arrowtips", 882, "Bronze arrow", 15),
        (2351, "Iron bar", 40, "Iron arrowtips", 884, "Iron arrow", 15),
        (2353, "Steel bar", 41, "Steel arrowtips", 886, "Steel arrow", 15),
        (2359, "Mithril bar", 42, "Mithril arrowtips", 888, "Mithril arrow", 15),
        (2361, "Adamantite bar", 43, "Adamant arrowtips", 890, "Adamant arrow", 15),
        (2363, "Runite bar", 44, "Rune arrowtips", 892, "Rune arrow", 15),
    ]

    for bar_id, bar_name, tip_id, tip_name, arrow_id, arrow_name, tips_per_bar in arrow_bar_mappings:
        chain = ProcessingChain(
            name=f"{arrow_name} (from bar)",
            category="Arrows (from Bar)",
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(tip_id, tip_name, tips_per_bar, is_self_obtained=True, processing_method="Smithing"),
            ChainStep(53, "Headless arrow", tips_per_bar),
            ChainStep(arrow_id, arrow_name, tips_per_bar),
        ]
        chains["Arrows (from Bar)"].append(chain)

    # Fletching Extended: Ore -> Bar -> Arrowtips -> Arrows (full pipeline)
    chains["Arrows (from Ore)"] = []
    for bar_id, bar_name, tip_id, tip_name, arrow_id, arrow_name, tips_per_bar in arrow_bar_mappings:
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, _, primary_ores, regular_coal, bf_coal = recipe

        for smelting_label, coal_qty, smelt_method in [
            ("Furnace", regular_coal, "Smelting"),
            ("BF", bf_coal, "Blast Furnace"),
        ]:
            chain = ProcessingChain(
                name=f"{arrow_name} ({smelting_label})",
                category="Arrows (from Ore)",
            )
            steps = []
            for ore_id, ore_name, ore_per_bar in primary_ores:
                steps.append(ChainStep(ore_id, ore_name, ore_per_bar))
            if coal_qty > 0:
                steps.append(ChainStep(453, "Coal", coal_qty))
            steps.append(ChainStep(
                bar_id, bar_name, 1,
                is_self_obtained=True, processing_method=smelt_method,
            ))
            steps.append(ChainStep(tip_id, tip_name, tips_per_bar, is_self_obtained=True, processing_method="Smithing"))
            steps.append(ChainStep(53, "Headless arrow", tips_per_bar))
            steps.append(ChainStep(arrow_id, arrow_name, tips_per_bar))
            chain.steps = steps
            chains["Arrows (from Ore)"].append(chain)

    # Fletching Extended: Bar -> Dart Tips -> Darts (bar smithing + fletching)
    # Bar -> 10 dart tips via Smithing, then tips + feathers -> darts
    chains["Darts (from Bar)"] = []
    dart_bar_mappings = [
        (2349, "Bronze bar", 819, "Bronze dart tip", 806, "Bronze dart", 10),
        (2351, "Iron bar", 820, "Iron dart tip", 807, "Iron dart", 10),
        (2353, "Steel bar", 821, "Steel dart tip", 808, "Steel dart", 10),
        (2359, "Mithril bar", 822, "Mithril dart tip", 809, "Mithril dart", 10),
        (2361, "Adamantite bar", 823, "Adamant dart tip", 810, "Adamant dart", 10),
        (2363, "Runite bar", 824, "Rune dart tip", 811, "Rune dart", 10),
    ]

    for bar_id, bar_name, tip_id, tip_name, dart_id, dart_name, tips_per_bar in dart_bar_mappings:
        chain = ProcessingChain(
            name=f"{dart_name} (from bar)",
            category="Darts (from Bar)",
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(tip_id, tip_name, tips_per_bar, is_self_obtained=True, processing_method="Smithing"),
            ChainStep(314, "Feather", tips_per_bar),
            ChainStep(dart_id, dart_name, tips_per_bar),
        ]
        chains["Darts (from Bar)"].append(chain)

    # Fletching Extended: Ore -> Bar -> Dart Tips -> Darts (full pipeline)
    chains["Darts (from Ore)"] = []
    for bar_id, bar_name, tip_id, tip_name, dart_id, dart_name, tips_per_bar in dart_bar_mappings:
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, _, primary_ores, regular_coal, bf_coal = recipe

        for smelting_label, coal_qty, smelt_method in [
            ("Furnace", regular_coal, "Smelting"),
            ("BF", bf_coal, "Blast Furnace"),
        ]:
            chain = ProcessingChain(
                name=f"{dart_name} ({smelting_label})",
                category="Darts (from Ore)",
            )
            steps = []
            for ore_id, ore_name, ore_per_bar in primary_ores:
                steps.append(ChainStep(ore_id, ore_name, ore_per_bar))
            if coal_qty > 0:
                steps.append(ChainStep(453, "Coal", coal_qty))
            steps.append(ChainStep(
                bar_id, bar_name, 1,
                is_self_obtained=True, processing_method=smelt_method,
            ))
            steps.append(ChainStep(tip_id, tip_name, tips_per_bar, is_self_obtained=True, processing_method="Smithing"))
            steps.append(ChainStep(314, "Feather", tips_per_bar))
            steps.append(ChainStep(dart_id, dart_name, tips_per_bar))
            chain.steps = steps
            chains["Darts (from Ore)"].append(chain)

    # Fletching Extended: Bar -> Bolts (unf) -> Bolts (bar to finished bolts)
    chains["Bolts (from Bar)"] = []
    for bar_id, bolt_info in bolt_bar_to_product.items():
        bolt_unf_id, bolt_unf_name, bolt_id, bolt_name = bolt_info
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, bar_name, _, _, _ = recipe
        chain = ProcessingChain(
            name=f"{bolt_name} (from bar)",
            category="Bolts (from Bar)",
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(bolt_unf_id, bolt_unf_name, 10, is_self_obtained=True, processing_method="Smithing"),
            ChainStep(314, "Feather", 10),
            ChainStep(bolt_id, bolt_name, 10),
        ]
        chains["Bolts (from Bar)"].append(chain)

    # Fletching Extended: Bar -> Javelin Heads -> Javelins (bar to finished javelins)
    chains["Javelins (from Bar)"] = []
    for bar_id, jav_info in jav_bar_to_product.items():
        jav_head_id, jav_head_name, jav_id, jav_name = jav_info
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, bar_name, _, _, _ = recipe
        chain = ProcessingChain(
            name=f"{jav_name} (from bar)",
            category="Javelins (from Bar)",
        )
        chain.steps = [
            ChainStep(bar_id, bar_name, 1),
            ChainStep(jav_head_id, jav_head_name, 5, is_self_obtained=True, processing_method="Smithing"),
            ChainStep(19584, "Javelin shaft", 5),
            ChainStep(jav_id, jav_name, 5),
        ]
        chains["Javelins (from Bar)"].append(chain)

    # Fletching Extended: Ore -> Bar -> Crossbow Limbs (full pipeline)
    chains["Crossbow Limbs (from Ore)"] = []
    for bar_id, bar_name, limb_id, limb_name in limb_mappings:
        recipe = next((r for r in smeltable if r[0] == bar_id), None)
        if not recipe:
            continue
        _, _, primary_ores, regular_coal, bf_coal = recipe

        for smelting_label, coal_qty, smelt_method in [
            ("Furnace", regular_coal, "Smelting"),
            ("BF", bf_coal, "Blast Furnace"),
        ]:
            chain = ProcessingChain(
                name=f"{limb_name} ({smelting_label})",
                category="Crossbow Limbs (from Ore)",
            )
            steps = []
            for ore_id, ore_name, ore_per_bar in primary_ores:
                steps.append(ChainStep(ore_id, ore_name, ore_per_bar))
            if coal_qty > 0:
                steps.append(ChainStep(453, "Coal", coal_qty))
            steps.append(ChainStep(
                bar_id, bar_name, 1,
                is_self_obtained=True, processing_method=smelt_method,
            ))
            steps.append(ChainStep(limb_id, limb_name, 1, processing_method="Smithing"))
            chain.steps = steps
            chains["Crossbow Limbs (from Ore)"].append(chain)

    return chains
