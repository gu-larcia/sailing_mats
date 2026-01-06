"""Item ID lookup service."""

from typing import Dict, Optional

try:
    from ..data import ALL_ITEMS
except ImportError:
    from data import ALL_ITEMS


class ItemIDLookup:
    """Resolves item names to IDs using predefined mappings and API data."""
    
    def __init__(self, item_mapping: Dict):
        """
        Args:
            item_mapping: Dict from /mapping endpoint (id -> item data)
        """
        self.item_mapping = item_mapping
        self.name_to_id_cache = {}
        
        for item_id, item_data in item_mapping.items():
            if isinstance(item_data, dict) and 'name' in item_data:
                self.name_to_id_cache[item_data['name'].lower()] = item_id
    
    def find_id_by_name(self, item_name: str) -> Optional[int]:
        """Find item ID by name. Tries exact match, then substring."""
        search_name = item_name.lower()
        
        if search_name in self.name_to_id_cache:
            return self.name_to_id_cache[search_name]
        
        for name, item_id in self.name_to_id_cache.items():
            if search_name in name or name in search_name:
                return item_id
        
        return None
    
    def get_or_find_id(self, item_id: Optional[int], item_name: str) -> Optional[int]:
        """Return item_id if provided, otherwise look up by name."""
        if item_id:
            return item_id
        
        found_id = self.find_id_by_name(item_name)
        if found_id:
            ALL_ITEMS[found_id] = item_name
        return found_id
    
    def get_item_name(self, item_id: int) -> Optional[str]:
        """Get item name by ID. Checks ALL_ITEMS first, then API mapping."""
        if item_id in ALL_ITEMS:
            return ALL_ITEMS[item_id]
        
        item_data = self.item_mapping.get(item_id)
        if item_data and isinstance(item_data, dict):
            return item_data.get('name')
        
        return None
