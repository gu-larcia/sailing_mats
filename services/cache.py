"""
In-memory SQLite cache for OSRS item data and prices.

Uses SQLite :memory: database cached within Streamlit's session/cache layer
for fast queryable access to item mappings and market prices without
requiring a persistent local database.
"""

import sqlite3
from typing import Dict, List, Optional, Tuple


class OSRSDataCache:
    """In-memory SQLite cache for item data and prices."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._create_tables()

    def _create_tables(self):
        """Create cache tables."""
        cur = self.conn.cursor()

        cur.executescript("""
            CREATE TABLE IF NOT EXISTS items (
                item_id   INTEGER PRIMARY KEY,
                name      TEXT NOT NULL,
                examine   TEXT,
                members   INTEGER DEFAULT 0,
                highalch  INTEGER DEFAULT 0,
                lowalch   INTEGER DEFAULT 0,
                buy_limit INTEGER DEFAULT 0,
                icon_url  TEXT
            );

            CREATE TABLE IF NOT EXISTS prices (
                item_id   INTEGER PRIMARY KEY,
                high      INTEGER DEFAULT 0,
                low       INTEGER DEFAULT 0,
                high_time INTEGER DEFAULT 0,
                low_time  INTEGER DEFAULT 0,
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            );

            CREATE TABLE IF NOT EXISTS tracked_items (
                item_id    INTEGER NOT NULL,
                name       TEXT NOT NULL,
                item_group TEXT NOT NULL,
                sort_order INTEGER DEFAULT 0,
                PRIMARY KEY (item_id, item_group),
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            );

            CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);
            CREATE INDEX IF NOT EXISTS idx_tracked_group ON tracked_items(item_group);
            CREATE INDEX IF NOT EXISTS idx_prices_high ON prices(high);
            CREATE INDEX IF NOT EXISTS idx_prices_low ON prices(low);
        """)

        self.conn.commit()

    # ------------------------------------------------------------------
    # Bulk loading
    # ------------------------------------------------------------------

    def load_item_mapping(self, mapping: Dict):
        """Load item mapping from Wiki API into items table."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM items")

        rows = []
        for item_id, item_data in mapping.items():
            if isinstance(item_data, dict):
                rows.append((
                    int(item_id),
                    item_data.get("name", ""),
                    item_data.get("examine", ""),
                    1 if item_data.get("members", False) else 0,
                    item_data.get("highalch", 0) or 0,
                    item_data.get("lowalch", 0) or 0,
                    item_data.get("limit", 0) or 0,
                    item_data.get("icon", ""),
                ))

        cur.executemany(
            "INSERT OR REPLACE INTO items (item_id, name, examine, members, highalch, lowalch, buy_limit, icon_url) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
        self.conn.commit()

    def load_prices(self, prices: Dict):
        """Load latest prices into prices table."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM prices")

        rows = []
        for item_id_str, price_data in prices.items():
            if isinstance(price_data, dict):
                rows.append((
                    int(item_id_str),
                    price_data.get("high", 0) or 0,
                    price_data.get("low", 0) or 0,
                    price_data.get("highTime", 0) or 0,
                    price_data.get("lowTime", 0) or 0,
                ))

        cur.executemany(
            "INSERT OR REPLACE INTO prices (item_id, high, low, high_time, low_time) "
            "VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        self.conn.commit()

    def load_tracked_items(self, tracked: Dict[int, str], group: str, clear_group: bool = True):
        """
        Load a set of tracked items into a named group.

        Args:
            tracked: {item_id: item_name} mapping
            group: Group name (e.g. 'sailing', 'all_logs', 'keel_parts')
            clear_group: If True, remove existing items in this group first
        """
        cur = self.conn.cursor()
        if clear_group:
            cur.execute("DELETE FROM tracked_items WHERE item_group = ?", (group,))

        rows = [(int(item_id), name, group, idx) for idx, (item_id, name) in enumerate(tracked.items())]
        cur.executemany(
            "INSERT OR REPLACE INTO tracked_items (item_id, name, item_group, sort_order) "
            "VALUES (?, ?, ?, ?)",
            rows,
        )
        self.conn.commit()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search_items(
        self,
        query: str = "",
        members_only: Optional[bool] = None,
        has_price: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        """
        Search items by name with optional filters.

        Returns list of dicts with item info + prices.
        """
        sql = """
            SELECT i.item_id, i.name, i.examine, i.members,
                   i.highalch, i.lowalch, i.buy_limit,
                   COALESCE(p.high, 0) AS buy_price,
                   COALESCE(p.low, 0) AS sell_price,
                   COALESCE(p.high, 0) - COALESCE(p.low, 0) AS margin
            FROM items i
            LEFT JOIN prices p ON i.item_id = p.item_id
            WHERE 1=1
        """
        params = []

        if query:
            sql += " AND i.name LIKE ?"
            params.append(f"%{query}%")

        if members_only is not None:
            sql += " AND i.members = ?"
            params.append(1 if members_only else 0)

        if has_price:
            sql += " AND p.item_id IS NOT NULL AND (p.high > 0 OR p.low > 0)"

        sql += " ORDER BY i.name LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cur = self.conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def search_items_count(self, query: str = "", members_only: Optional[bool] = None, has_price: bool = False) -> int:
        """Count matching items for a search."""
        sql = """
            SELECT COUNT(*) FROM items i
            LEFT JOIN prices p ON i.item_id = p.item_id
            WHERE 1=1
        """
        params = []
        if query:
            sql += " AND i.name LIKE ?"
            params.append(f"%{query}%")
        if members_only is not None:
            sql += " AND i.members = ?"
            params.append(1 if members_only else 0)
        if has_price:
            sql += " AND p.item_id IS NOT NULL AND (p.high > 0 OR p.low > 0)"

        return self.conn.execute(sql, params).fetchone()[0]

    def get_tracked_items(self, group: str) -> List[Dict]:
        """Get tracked items in a group with their prices."""
        sql = """
            SELECT t.item_id, t.name, t.item_group, t.sort_order,
                   COALESCE(p.high, 0) AS buy_price,
                   COALESCE(p.low, 0) AS sell_price,
                   COALESCE(p.high, 0) - COALESCE(p.low, 0) AS margin
            FROM tracked_items t
            LEFT JOIN prices p ON t.item_id = p.item_id
            ORDER BY t.sort_order
        """
        params = []
        if group != "all":
            sql = sql.replace("ORDER BY", "WHERE t.item_group = ? ORDER BY")
            params.append(group)

        cur = self.conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def get_tracked_groups(self) -> List[str]:
        """Get list of all tracked item groups."""
        cur = self.conn.execute("SELECT DISTINCT item_group FROM tracked_items ORDER BY item_group")
        return [row[0] for row in cur.fetchall()]

    def get_price(self, item_id: int) -> Dict:
        """Get price for a single item."""
        cur = self.conn.execute(
            "SELECT high, low, high_time, low_time FROM prices WHERE item_id = ?",
            (item_id,),
        )
        row = cur.fetchone()
        if row:
            return {"high": row[0], "low": row[1], "highTime": row[2], "lowTime": row[3]}
        return {}

    def get_prices_dict(self) -> Dict:
        """Get all prices as a dict keyed by string item_id (API-compatible format)."""
        cur = self.conn.execute("SELECT item_id, high, low, high_time, low_time FROM prices")
        result = {}
        for row in cur.fetchall():
            result[str(row[0])] = {
                "high": row[1],
                "low": row[2],
                "highTime": row[3],
                "lowTime": row[4],
            }
        return result

    def get_item_count(self) -> int:
        """Total items loaded."""
        return self.conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]

    def get_price_count(self) -> int:
        """Total prices loaded."""
        return self.conn.execute("SELECT COUNT(*) FROM prices WHERE high > 0 OR low > 0").fetchone()[0]

    def get_tracked_count(self) -> int:
        """Total tracked items."""
        return self.conn.execute("SELECT COUNT(*) FROM tracked_items").fetchone()[0]

    def get_top_margins(self, limit: int = 20) -> List[Dict]:
        """Get items with highest buy/sell margins."""
        sql = """
            SELECT i.item_id, i.name, i.members, i.buy_limit,
                   p.high AS buy_price, p.low AS sell_price,
                   (p.high - p.low) AS margin,
                   CASE WHEN p.high > 0
                        THEN ROUND((CAST(p.low - p.high AS REAL) / p.high) * 100, 2)
                        ELSE 0 END AS roi_pct
            FROM items i
            JOIN prices p ON i.item_id = p.item_id
            WHERE p.high > 0 AND p.low > 0 AND p.low < p.high
            ORDER BY margin DESC
            LIMIT ?
        """
        cur = self.conn.execute(sql, (limit,))
        return [dict(row) for row in cur.fetchall()]

    def get_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "total_items": self.get_item_count(),
            "prices_loaded": self.get_price_count(),
            "tracked_items": self.get_tracked_count(),
            "tracked_groups": len(self.get_tracked_groups()),
        }
