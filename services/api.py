"""
OSRS Wiki API client for fetching item mappings and prices.

API Information (from research):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary API: prices.runescape.wiki (RuneLite partnership)
- No API key required
- Custom User-Agent REQUIRED (default user-agents blocked)
- No explicit rate limits (don't poll faster than 5-min refresh)
- BEST PRACTICE: Call /latest once for all items, don't loop individual requests

Historical API: api.weirdgloop.org/exchange/history/osrs
- 90-day and full history endpoints
- Official GE prices (not RuneLite data)

Endpoints:
- /mapping: Item metadata (IDs, names, limits, alch values)
- /latest: Current high/low prices for all ~3,700 items
- /5m: 5-minute average prices with volume
- /1h: 1-hour average prices with volume
- /timeseries: Historical prices (up to 365 data points)

Python Packages (optional):
- osrs-prices (v0.1.0, Nov 2024): Newest, purpose-built for Wiki API
- rswiki-wrapper (v0.0.6): More mature, wraps both APIs
- osrsreboxed (v2.3.33): Item database with 27+ properties
"""

import requests
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# API Base URLs
API_BASE = "https://prices.runescape.wiki/api/v1/osrs"
WEIRDGLOOP_BASE = "https://api.weirdgloop.org/exchange/history/osrs"

# Default User-Agent (REQUIRED - default python-requests is blocked)
DEFAULT_USER_AGENT = "OSRS-Sailing-Tracker/4.6 (Streamlit App - github.com/yourname/repo)"


@dataclass
class PriceData:
    """Structured price data for an item."""
    item_id: int
    high: Optional[int] = None      # Instant buy price
    high_time: Optional[int] = None # Unix timestamp of high price
    low: Optional[int] = None       # Instant sell price  
    low_time: Optional[int] = None  # Unix timestamp of low price
    
    @property
    def margin(self) -> Optional[int]:
        """Calculate buy-sell margin."""
        if self.high is not None and self.low is not None:
            return self.high - self.low
        return None
    
    @property
    def roi(self) -> Optional[float]:
        """Calculate ROI percentage."""
        if self.high and self.low and self.high > 0:
            return ((self.low - self.high) / self.high) * 100
        return None


@dataclass
class ItemMetadata:
    """Item metadata from /mapping endpoint."""
    id: int
    name: str
    examine: str = ""
    members: bool = True
    lowalch: int = 0
    highalch: int = 0
    limit: int = 0      # GE buy limit per 4 hours
    value: int = 0      # Store value


class OSRSWikiConnection:
    """
    Connection to the OSRS Wiki Prices API.
    
    Best Practices (from research):
    1. Always use a descriptive User-Agent
    2. Call /latest once to get all prices (don't loop per-item)
    3. Don't poll faster than 5-minute data refresh interval
    4. Cache /mapping data (changes infrequently)
    
    Usage:
        conn = OSRSWikiConnection()
        mapping = conn.fetch_mapping()  # Get all item metadata
        prices = conn.fetch_prices()    # Get current prices
    """
    
    def __init__(self, base_url: str = API_BASE, user_agent: str = None):
        """
        Initialize the API connection.
        
        Args:
            base_url: API base URL (default: prices.runescape.wiki)
            user_agent: Custom User-Agent string (REQUIRED by API)
        """
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': user_agent or DEFAULT_USER_AGENT,
            'Accept': 'application/json'
        })
        self._mapping_cache: Optional[Dict] = None
        self._mapping_cache_time: Optional[datetime] = None
    
    def fetch_mapping(self, use_cache: bool = True) -> Dict[int, ItemMetadata]:
        """
        Fetch item mapping (ID -> metadata).
        
        Args:
            use_cache: Use cached mapping if available (default True)
        
        Returns:
            Dict mapping item_id to ItemMetadata:
            {
                item_id: ItemMetadata(id, name, examine, members, ...)
            }
        """
        # Return cached data if fresh (< 5 minutes old)
        if use_cache and self._mapping_cache and self._mapping_cache_time:
            age = (datetime.now() - self._mapping_cache_time).total_seconds()
            if age < 300:  # 5 minutes
                return self._mapping_cache
        
        response = self._session.get(f"{self.base_url}/mapping")
        response.raise_for_status()
        items = response.json()
        
        # Convert to structured data
        result = {}
        for item in items:
            result[item['id']] = ItemMetadata(
                id=item['id'],
                name=item.get('name', ''),
                examine=item.get('examine', ''),
                members=item.get('members', True),
                lowalch=item.get('lowalch', 0),
                highalch=item.get('highalch', 0),
                limit=item.get('limit', 0),
                value=item.get('value', 0)
            )
        
        self._mapping_cache = result
        self._mapping_cache_time = datetime.now()
        
        return result
    
    def fetch_mapping_raw(self) -> Dict:
        """
        Fetch raw item mapping as dict (for backward compatibility).
        
        Returns:
            Dict mapping item_id to raw item data dict
        """
        response = self._session.get(f"{self.base_url}/mapping")
        response.raise_for_status()
        items = response.json()
        return {item['id']: item for item in items}
    
    def fetch_prices(self) -> Dict[str, Dict]:
        """
        Fetch latest prices for all items.
        
        BEST PRACTICE: Call this once and cache, don't loop per-item.
        
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
    
    def fetch_prices_structured(self) -> Dict[int, PriceData]:
        """
        Fetch latest prices as structured PriceData objects.
        
        Returns:
            Dict mapping item_id (int) to PriceData objects
        """
        raw_prices = self.fetch_prices()
        result = {}
        
        for item_id_str, data in raw_prices.items():
            item_id = int(item_id_str)
            result[item_id] = PriceData(
                item_id=item_id,
                high=data.get('high'),
                high_time=data.get('highTime'),
                low=data.get('low'),
                low_time=data.get('lowTime')
            )
        
        return result
    
    def fetch_item_price(self, item_id: int) -> Optional[PriceData]:
        """
        Fetch price for a single item.
        
        NOTE: For multiple items, use fetch_prices() instead.
        This method is provided for convenience but is less efficient.
        
        Args:
            item_id: The item ID to look up
            
        Returns:
            PriceData object or None if not found
        """
        response = self._session.get(f"{self.base_url}/latest", params={'id': item_id})
        response.raise_for_status()
        data = response.json().get('data', {}).get(str(item_id))
        
        if not data:
            return None
        
        return PriceData(
            item_id=item_id,
            high=data.get('high'),
            high_time=data.get('highTime'),
            low=data.get('low'),
            low_time=data.get('lowTime')
        )
    
    def fetch_5m_prices(self, timestamp: int = None) -> Dict:
        """
        Fetch 5-minute average prices.
        
        Args:
            timestamp: Optional Unix timestamp to fetch historical data
            
        Returns:
            Dict with price averages and volume data
        """
        url = f"{self.base_url}/5m"
        params = {}
        if timestamp:
            params['timestamp'] = timestamp
        
        response = self._session.get(url, params=params if params else None)
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
        params = {}
        if timestamp:
            params['timestamp'] = timestamp
        
        response = self._session.get(url, params=params if params else None)
        response.raise_for_status()
        return response.json().get('data', {})
    
    def fetch_timeseries(self, item_id: int, timestep: str = "1h") -> List[Dict]:
        """
        Fetch historical price timeseries for an item.
        
        Args:
            item_id: The item ID
            timestep: Time interval - "5m", "1h", or "6h"
            
        Returns:
            List of price data points (up to 365 points)
        """
        response = self._session.get(
            f"{self.base_url}/timeseries",
            params={'id': item_id, 'timestep': timestep}
        )
        response.raise_for_status()
        return response.json().get('data', [])


class WeirdGloopConnection:
    """
    Connection to the Weird Gloop historical prices API.
    
    Provides official GE prices (not RuneLite data) with:
    - 90-day history
    - Full historical data
    
    Useful for long-term price analysis and trends.
    """
    
    def __init__(self, base_url: str = WEIRDGLOOP_BASE, user_agent: str = None):
        """Initialize the Weird Gloop API connection."""
        self.base_url = base_url
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': user_agent or DEFAULT_USER_AGENT,
            'Accept': 'application/json'
        })
    
    def fetch_history(self, item_name: str, days: int = 90) -> Dict:
        """
        Fetch price history for an item.
        
        Args:
            item_name: Name of the item (e.g., "Steel bar")
            days: Number of days of history (max 90 for standard endpoint)
            
        Returns:
            Dict with historical price data
        """
        # URL encode the item name
        encoded_name = requests.utils.quote(item_name)
        
        response = self._session.get(f"{self.base_url}/latest?name={encoded_name}")
        response.raise_for_status()
        return response.json()
    
    def fetch_full_history(self, item_id: int) -> Dict:
        """
        Fetch complete price history for an item.
        
        Args:
            item_id: The item ID
            
        Returns:
            Dict with full historical price data
        """
        response = self._session.get(f"{self.base_url}/all?id={item_id}")
        response.raise_for_status()
        return response.json()


# Optional: Try to use osrs-prices package if available
try:
    from osrs_prices import OSRSPrices
    
    class OSRSPricesWrapper:
        """Wrapper for osrs-prices package (if installed)."""
        
        def __init__(self, user_agent: str = None):
            self._client = OSRSPrices(user_agent=user_agent or DEFAULT_USER_AGENT)
        
        def fetch_prices(self) -> Dict:
            """Fetch all prices using osrs-prices package."""
            return self._client.get_latest()
        
        def fetch_mapping(self) -> Dict:
            """Fetch mapping using osrs-prices package."""
            return self._client.get_mapping()
    
    OSRS_PRICES_AVAILABLE = True
    logger.info("osrs-prices package available - can use OSRSPricesWrapper")

except ImportError:
    OSRS_PRICES_AVAILABLE = False
    OSRSPricesWrapper = None
    logger.debug("osrs-prices package not installed - using raw API requests")


def get_api_connection(use_package: bool = False, user_agent: str = None):
    """
    Factory function to get an API connection.
    
    Args:
        use_package: Try to use osrs-prices package if available
        user_agent: Custom User-Agent string
        
    Returns:
        OSRSWikiConnection or OSRSPricesWrapper
    """
    if use_package and OSRS_PRICES_AVAILABLE:
        return OSRSPricesWrapper(user_agent)
    return OSRSWikiConnection(user_agent=user_agent)
