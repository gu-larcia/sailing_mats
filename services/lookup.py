"""
Item ID lookup service for resolving item names to IDs.

Provides multiple lookup strategies:
1. Pre-defined item ID mappings (ALL_ITEMS)
2. API mapping data (for dynamic lookups)
3. Fuzzy name matching (as fallback)
"""

from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

try:
    from ..data import ALL_ITEMS, SAILING_ITEMS
except ImportError:
    from data import ALL_ITEMS, SAILING_ITEMS


class ItemIDLookup:
    """
    Lookup service for finding item IDs by name.
    
    Uses a combination of:
    1. Pre-defined item ID mappings (ALL_ITEMS)
    2. API mapping data (for dynamic lookups)
    3. Fuzzy name matching (as fallback)
    
    Usage:
        lookup = ItemIDLookup(api_mapping)
        item_id = lookup.find_id_by_name("Bronze bar")
        name = lookup.get_item_name(2349)
    """
    
    def __init__(self, item_mapping: Dict):
        """
        Initialize the lookup service.
        
        Args:
            item_mapping: Dict from API /mapping endpoint (id -> item data)
        """
        self.item_mapping = item_mapping
        self.name_to_id_cache: Dict[str, int] = {}
        self._build_cache()
    
    def _build_cache(self):
        """Build name -> ID cache from API mapping."""
        for item_id, item_data in self.item_mapping.items():
            if isinstance(item_data, dict) and 'name' in item_data:
                self.name_to_id_cache[item_data['name'].lower()] = item_id
            elif hasattr(item_data, 'name'):  # ItemMetadata object
                self.name_to_id_cache[item_data.name.lower()] = item_id
    
    def find_id_by_name(self, item_name: str) -> Optional[int]:
        """
        Find an item ID by its name.
        
        Args:
            item_name: The item name to search for
            
        Returns:
            Item ID if found, None otherwise
        """
        search_name = item_name.lower()
        
        # Exact match first
        if search_name in self.name_to_id_cache:
            return self.name_to_id_cache[search_name]
        
        # Check pre-defined items
        for item_id, name in ALL_ITEMS.items():
            if name.lower() == search_name:
                return item_id
        
        # Fuzzy match (substring)
        for name, item_id in self.name_to_id_cache.items():
            if search_name in name or name in search_name:
                return item_id
        
        return None
    
    def find_ids_by_pattern(self, pattern: str) -> List[int]:
        """
        Find all item IDs matching a pattern.
        
        Args:
            pattern: Substring to search for in item names
            
        Returns:
            List of matching item IDs
        """
        pattern_lower = pattern.lower()
        matches = []
        
        for name, item_id in self.name_to_id_cache.items():
            if pattern_lower in name:
                matches.append(item_id)
        
        return matches
    
    def get_or_find_id(self, item_id: Optional[int], item_name: str) -> Optional[int]:
        """
        Get an item ID, looking it up by name if not provided.
        
        Args:
            item_id: Known item ID (may be None)
            item_name: Item name to search for if ID is None
            
        Returns:
            Item ID if found, None otherwise
        """
        if item_id:
            return item_id
        
        found_id = self.find_id_by_name(item_name)
        if found_id:
            # Cache in ALL_ITEMS for future use
            if found_id not in ALL_ITEMS:
                ALL_ITEMS[found_id] = item_name
                logger.debug(f"Added {item_name} (ID: {found_id}) to ALL_ITEMS cache")
        return found_id
    
    def get_item_name(self, item_id: int) -> Optional[str]:
        """
        Get an item name by its ID.
        
        Args:
            item_id: The item ID to look up
            
        Returns:
            Item name if found, None otherwise
        """
        # Check pre-defined items first
        if item_id in ALL_ITEMS:
            return ALL_ITEMS[item_id]
        
        # Check API mapping
        item_data = self.item_mapping.get(item_id)
        if item_data:
            if isinstance(item_data, dict):
                return item_data.get('name')
            elif hasattr(item_data, 'name'):
                return item_data.name
        
        return None
    
    def is_sailing_item(self, item_id: int) -> bool:
        """
        Check if an item is a Sailing-related item.
        
        Args:
            item_id: The item ID to check
            
        Returns:
            True if the item is Sailing-related
        """
        return item_id in SAILING_ITEMS
    
    def get_all_sailing_items(self) -> Dict[int, str]:
        """
        Get all known Sailing items.
        
        Returns:
            Dict mapping item_id to item_name for Sailing items
        """
        return SAILING_ITEMS.copy()
    
    def refresh_from_api(self, new_mapping: Dict):
        """
        Refresh the lookup cache with new API data.
        
        Args:
            new_mapping: Fresh mapping data from /mapping endpoint
        """
        self.item_mapping = new_mapping
        self.name_to_id_cache.clear()
        self._build_cache()
        logger.info(f"Refreshed item lookup cache with {len(self.name_to_id_cache)} items")
