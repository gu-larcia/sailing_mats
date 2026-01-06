"""
Core data classes for processing chain calculations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..services.lookup import ItemIDLookup


@dataclass
class ChainStep:
    """A single step in a processing chain."""
    item_id: Optional[int]
    item_name: str
    quantity: float = 1
    is_self_obtained: bool = False
    processing_method: Optional[str] = None
    custom_cost: Optional[float] = None


@dataclass
class ProcessingChain:
    """
    A complete processing chain from raw materials to finished product.
    
    Example: Bronze bar -> Bronze keel parts
    
    Ratios verified per research:
    - Hull/Keel parts: 5:1 standard, 2:1 dragon
    - Nails: 15 per bar
    - Cannonballs: 4 per bar (8 with double mould)
    """
    name: str
    category: str
    steps: List[ChainStep] = field(default_factory=list)
    special_ratio: Optional[Dict] = field(default_factory=dict)
    
    def get_output_item_name(self) -> str:
        """Get the name of the output item (last step)."""
        if self.steps:
            return self.steps[-1].item_name
        # Fallback to cleaning the chain name
        clean = self.name.replace(" processing", "").replace(" smithing", "")
        clean = clean.replace(" (Regular)", "").replace(" (Double)", "")
        return clean
    
    def calculate(self, prices: Dict, config: Dict, id_lookup: 'ItemIDLookup') -> Dict:
        """
        Calculate the profitability of this processing chain.
        
        Args:
            prices: Dict of item_id -> price data from the Wiki API
            config: User configuration (quantity, self_collected, plank_method, etc.)
            id_lookup: ItemIDLookup instance for resolving item names to IDs
            
        Returns:
            Dict with calculation results including costs, profit, ROI
        """
        try:
            from ..data import (
                SAWMILL_COSTS, PLANK_MAKE_COSTS, RUNE_IDS,
                GE_TAX_RATE, GE_TAX_CAP, GE_TAX_THRESHOLD
            )
        except ImportError:
            from data import (
                SAWMILL_COSTS, PLANK_MAKE_COSTS, RUNE_IDS,
                GE_TAX_RATE, GE_TAX_CAP, GE_TAX_THRESHOLD
            )
        
        results = {
            "chain_name": self.name,
            "category": self.category,
            "steps": [],
            "raw_material_cost": 0,
            "processing_costs": 0,
            "total_input_cost": 0,
            "output_value": 0,
            "ge_tax": 0,
            "net_profit": 0,
            "roi": 0,
            "profit_per_item": 0,
            "missing_prices": [],
            "output_item_name": self.get_output_item_name()
        }
        
        if not self.steps:
            results["error"] = "No steps in chain"
            return results
        
        final_quantity = config.get("quantity", 1)
        
        # Handle special dragon ratio (2:1 instead of 5:1) - VERIFIED
        if self.special_ratio and "dragon" in self.name.lower():
            ratio = self.special_ratio.get("conversion_ratio", 5)
        else:
            ratio = 5
        
        # Calculate needed quantities for each step (working backwards)
        num_steps = len(self.steps)
        needed = [0.0] * num_steps
        needed[-1] = final_quantity

        for idx in range(num_steps - 2, -1, -1):
            prev = self.steps[idx]
            nxt = self.steps[idx + 1]
            if getattr(nxt, 'quantity', 0) == 0:
                needed[idx] = needed[idx + 1] * getattr(prev, 'quantity', 1)
            else:
                needed[idx] = needed[idx + 1] * (getattr(prev, 'quantity', 1) / getattr(nxt, 'quantity', 1))

        # Calculate costs for each step
        for i, step in enumerate(self.steps):
            resolved_id = id_lookup.get_or_find_id(step.item_id, step.item_name)

            if not resolved_id:
                results["missing_prices"].append(step.item_name)
                continue

            price_data = prices.get(str(resolved_id), {})

            if not price_data:
                results["missing_prices"].append(step.item_name)

            step_qty = needed[i]
            is_output = (i == len(self.steps) - 1)
            is_input = (i == 0)

            if is_output:
                # Output uses low price (what we sell at)
                unit_price = price_data.get("low", 0) if price_data else 0
                total_value = unit_price * step_qty
                results["output_value"] = total_value
            else:
                # Inputs use high price (what we buy at)
                is_free = step.is_self_obtained or config.get("self_collected", False)
                unit_price = price_data.get("high", 0) if price_data and not is_free else 0
                total_value = unit_price * step_qty
                results["raw_material_cost"] += total_value

            # Calculate processing costs
            processing_cost = 0
            process_notes = ""

            if step.processing_method:
                processing_cost, process_notes = self._calculate_processing_cost(
                    step, step_qty, prices, config, id_lookup,
                    SAWMILL_COSTS, PLANK_MAKE_COSTS, RUNE_IDS
                )
                results["processing_costs"] += processing_cost

            results["steps"].append({
                "name": step.item_name,
                "quantity": step_qty,
                "unit_price": unit_price,
                "total_value": total_value,
                "is_self_obtained": step.is_self_obtained or config.get("self_collected", False),
                "processing_cost": processing_cost,
                "processing_notes": process_notes,
                "step_type": "Output" if is_output else ("Input" if is_input else "Intermediate")
            })
        
        # Final calculations
        results["total_input_cost"] = results["raw_material_cost"] + results["processing_costs"]
        
        # GE Tax (2%, capped at 5M, only on sales >= 50gp)
        if results["output_value"] >= GE_TAX_THRESHOLD:
            results["ge_tax"] = min(results["output_value"] * GE_TAX_RATE, GE_TAX_CAP)
        
        results["net_profit"] = results["output_value"] - results["total_input_cost"] - results["ge_tax"]
        results["profit_per_item"] = results["net_profit"] / final_quantity if final_quantity > 0 else 0
        
        # ROI calculation
        if results["total_input_cost"] > 0:
            results["roi"] = (results["net_profit"] / results["total_input_cost"]) * 100
        elif results["raw_material_cost"] == 0:
            results["roi"] = float('inf')
        
        return results
    
    def _calculate_processing_cost(
        self, 
        step: ChainStep, 
        quantity: float, 
        prices: Dict, 
        config: Dict, 
        id_lookup: 'ItemIDLookup',
        sawmill_costs: Dict,
        plank_make_costs: Dict,
        rune_ids: Dict
    ) -> Tuple[float, str]:
        """Calculate the processing cost for a step."""
        
        if step.custom_cost is not None:
            return step.custom_cost * quantity, f"Custom: {step.custom_cost} gp each"
        
        if step.processing_method == "Sawmill":
            if step.item_name in sawmill_costs:
                cost = sawmill_costs[step.item_name] * quantity
                return cost, f"Sawmill: {sawmill_costs[step.item_name]} gp each"
        
        elif step.processing_method == "Plank Make":
            if step.item_name in plank_make_costs:
                base_cost = plank_make_costs[step.item_name] * quantity
                
                # Calculate rune costs (2 Astral + 1 Nature + 15 Earth)
                astral_price = prices.get(str(rune_ids["Astral rune"]), {}).get("high", 0)
                nature_price = prices.get(str(rune_ids["Nature rune"]), {}).get("high", 0)
                
                rune_cost = (astral_price * 2 + nature_price) * quantity
                
                if not config.get("use_earth_staff", False):
                    earth_price = prices.get(str(rune_ids["Earth rune"]), {}).get("high", 0)
                    rune_cost += earth_price * 15 * quantity
                    notes = f"Plank Make: {plank_make_costs[step.item_name]} + runes"
                else:
                    notes = f"Plank Make (Earth staff): {plank_make_costs[step.item_name]} + runes"
                
                return base_cost + rune_cost, notes
        
        elif step.processing_method == "Smithing":
            return 0, "Smithing (no cost)"
        
        elif step.processing_method == "Dragon Forge":
            return 0, "Dragon Forge (no cost, 92 Smithing req)"
        
        return 0, ""
