"""Bank location data. Times in seconds."""

from dataclasses import dataclass


@dataclass
class BankLocation:
    """Bank location with travel overhead."""
    name: str
    bank_time: float
    travel_time: float
    has_anvil: bool
    has_furnace: bool
    has_shipwright: bool
    has_sawmill: bool
    requirements: str
    stamina_dependent: bool
    
    @property
    def total_overhead(self) -> float:
        return self.bank_time + self.travel_time


BANK_LOCATIONS = {
    "Deepfin Point": BankLocation(
        name="Deepfin Point",
        bank_time=3.0,
        travel_time=4.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=False,
        requirements="67 Sailing",
        stamina_dependent=False
    ),
    
    "Prifddinas": BankLocation(
        name="Prifddinas",
        bank_time=4.0,
        travel_time=4.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=True,
        requirements="Song of the Elves",
        stamina_dependent=False
    ),
    
    "Edgeville Furnace": BankLocation(
        name="Edgeville Furnace",
        bank_time=4.0,
        travel_time=6.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="None",
        stamina_dependent=False
    ),
    
    "Varrock West Anvil": BankLocation(
        name="Varrock West Anvil",
        bank_time=4.0,
        travel_time=8.0,
        has_anvil=True,
        has_furnace=False,
        has_shipwright=False,
        has_sawmill=False,
        requirements="None",
        stamina_dependent=False
    ),
    
    "Port Phasmatys": BankLocation(
        name="Port Phasmatys",
        bank_time=5.0,
        travel_time=10.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="Priest in Peril",
        stamina_dependent=False
    ),
    
    "Neitiznot": BankLocation(
        name="Neitiznot",
        bank_time=4.0,
        travel_time=8.0,
        has_anvil=True,
        has_furnace=False,
        has_shipwright=False,
        has_sawmill=False,
        requirements="The Fremennik Isles (partial)",
        stamina_dependent=False
    ),
    
    "Al Kharid Furnace": BankLocation(
        name="Al Kharid Furnace",
        bank_time=5.0,
        travel_time=12.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="None (10gp gate or Prince Ali Rescue)",
        stamina_dependent=False
    ),
    
    "Shilo Village": BankLocation(
        name="Shilo Village",
        bank_time=5.0,
        travel_time=10.0,
        has_anvil=False,
        has_furnace=True,
        has_shipwright=False,
        has_sawmill=False,
        requirements="Shilo Village quest",
        stamina_dependent=False
    ),
    
    "WC Guild Sawmill": BankLocation(
        name="WC Guild Sawmill",
        bank_time=4.0,
        travel_time=8.0,
        has_anvil=False,
        has_furnace=False,
        has_shipwright=False,
        has_sawmill=True,
        requirements="60 Woodcutting",
        stamina_dependent=False
    ),
    
    "Fast (Optimal)": BankLocation(
        name="Fast (Optimal)",
        bank_time=4.0,
        travel_time=4.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=True,
        requirements="Best available setup",
        stamina_dependent=False
    ),
    
    "Medium (Typical)": BankLocation(
        name="Medium (Typical)",
        bank_time=5.0,
        travel_time=10.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=True,
        requirements="Typical efficient banking",
        stamina_dependent=False
    ),
    
    "Slow (Suboptimal)": BankLocation(
        name="Slow (Suboptimal)",
        bank_time=6.0,
        travel_time=19.0,
        has_anvil=True,
        has_furnace=True,
        has_shipwright=True,
        has_sawmill=True,
        requirements="Suboptimal setup",
        stamina_dependent=True
    ),
}
