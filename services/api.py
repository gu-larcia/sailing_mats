"""
OSRS Wiki API client for fetching item mappings and prices.

Uses the prices.runescape.wiki API:
- No API key required
- Custom User-Agent is required
- No explicit rate limits (but don't poll faster than 5-minute refresh)

Endpoints:
- /mapping: Item metadata (IDs, names, limits)
- /latest: Current high/low prices for all items
"""

import requests
from typing import Dict

# API Base URL
API_BASE = "https://prices.runescape.wiki/api/v1/osrs"


class OSRSWikiConnection:
    """
    Connection to the OSRS Wiki Prices API.
    
    Usage:
        conn = OSRSWikiConnection()
        mapping = conn.fetch_mapping()  # Get all item metadata
        prices = conn.fetch_prices()     # Get current prices
    """
    
    def __init__(self, base_url: str = API_BASE, user_agent: str = None):
        """
        Initialize the API connection.
        
        Args:
            base_url: API base URL (default: prices.runescape.wiki)
            user_agent: Custom User-Agent string (required by API)
        """
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': user_agent or 'OSRS-Sailing-Tracker/4.5 (Streamlit App)'
        })
    
    def fetch_mapping(self) -> Dict:
        """
        Fetch item mapping (ID -> metadata).
        
        Returns:
            Dict mapping item_id to item data:
            {
                item_id: {
                    'id': int,
                    'name': str,
                    'examine': str,
                    'members': bool,
                    'lowalch': int,
                    'highalch': int,
                    'limit': int,
                    'value': int
                }
            }
        """
        response = self._session.get(f"{self.base_url}/mapping")
        response.raise_for_status()
        items = response.json()
        return {item['id']: item for item in items}
    
    def fetch_prices(self) -> Dict:
        """
        Fetch latest prices for all items.
        
        Returns:
            Dict mapping item_id (as string) to price data:
            {
                "item_id": {
                    'high': int,      # Instant buy price
                    'highTime': int,  # Unix timestamp
                    'low': int,       # Instant sell price
                    'lowTime': int    # Unix timestamp
                }
            }
        """
        response = self._session.get(f"{self.base_url}/latest")
        response.raise_for_status()
        return response.json().get('data', {})
    
    def fetch_5m_prices(self, timestamp: int = None) -> Dict:
        """
        Fetch 5-minute average prices.
        
        Args:
            timestamp: Optional Unix timestamp to fetch historical data
            
        Returns:
            Dict with price averages and volume data
        """
        url = f"{self.base_url}/5m"
        if timestamp:
            url += f"?timestamp={timestamp}"
        response = self._session.get(url)
        response.raise_for_status()
        return response.json().get('data', {})
    
    def fetch_1h_prices(self, timestamp: int = None) -> Dict:
        """
        Fetch 1-hour average prices.
        
        Args:
            timestamp: Optional Unix timestamp to fetch historical data
            
        Returns:
            Dict with price averages and volume data
        """
        url = f"{self.base_url}/1h"
        if timestamp:
            url += f"?timestamp={timestamp}"
        response = self._session.get(url)
        response.raise_for_status()
        return response.json().get('data', {})
