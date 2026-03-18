"""OSRS Wiki API client."""

import requests
from typing import Dict

API_BASE = "https://prices.runescape.wiki/api/v1/osrs"


class OSRSWikiConnection:
    """Client for prices.runescape.wiki API. No API key required."""
    
    def __init__(self, base_url: str = API_BASE, user_agent: str = None):
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': user_agent or 'OSRS-Sailing-Tracker/4.6'
        })
    
    def fetch_mapping(self) -> Dict:
        """Fetch item metadata. Returns {item_id: {name, examine, members, ...}}."""
        response = self._session.get(f"{self.base_url}/mapping")
        response.raise_for_status()
        items = response.json()
        return {item['id']: item for item in items}
    
    def fetch_prices(self) -> Dict:
        """Fetch current prices. Returns {item_id: {high, low, highTime, lowTime}}."""
        response = self._session.get(f"{self.base_url}/latest")
        response.raise_for_status()
        return response.json().get('data', {})
    
    def fetch_5m_prices(self, timestamp: int = None) -> Dict:
        """Fetch 5-minute averages. Optional timestamp for historical data."""
        url = f"{self.base_url}/5m"
        if timestamp:
            url += f"?timestamp={timestamp}"
        response = self._session.get(url)
        response.raise_for_status()
        return response.json().get('data', {})
    
    def fetch_1h_prices(self, timestamp: int = None) -> Dict:
        """Fetch 1-hour averages. Optional timestamp for historical data."""
        url = f"{self.base_url}/1h"
        if timestamp:
            url += f"?timestamp={timestamp}"
        response = self._session.get(url)
        response.raise_for_status()
        return response.json().get('data', {})
