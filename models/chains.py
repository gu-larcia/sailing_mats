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

    # ================================================================
    # Extended Chains
    #
    # Compose existing recipes into full pipelines (ore/log → final
    # product).  Intermediate items are is_self_obtained so they are
    # costed from raw materials, not the GE.  Step quantities are
    # pre-scaled so the backward ratio calculation resolves correctly.
    # ================================================================

    # Only bars with downstream products (exclude silver, gold)
    smeltable = [r for r in smelting_recipes if r[0] not in (2355, 2357)]

    # --- Metal: Ore → Bar → Product --------------------------------
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

    # --- Metal: Bar → Keel → Large Keel (from GE-bought bars) ------
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

    # --- Metal: Ore → Bar → Keel → Large Keel (full pipeline) ------
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

    # --- Wood: Log → Plank → Hull Parts ----------------------------
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

    # --- Wood: Log → Plank → Hull Part → Large Hull Part ------------
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

    # --- Wood: Log → Plank → Hull Repair Kit (+ GE nails & paste) --
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

    return chains
