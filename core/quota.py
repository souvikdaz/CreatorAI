import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# YouTube Data API v3 unit costs
ENDPOINT_COSTS = {
    "search.list": 100,
    "videos.list": 1,
    "channels.list": 1,
    "playlistItems.list": 1,
    "playlists.list": 1,
    "captions.list": 50,
    "commentThreads.list": 1,
    "analytics.reports.query": 0,  # Analytics uses requests-per-minute quota, 0 data units
}

class QuotaManager:
    def __init__(self, db_path: str, daily_limit: int = 10000):
        self.db_path = db_path
        self.daily_limit = daily_limit
        if db_path == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:")
        else:
            self._mem_conn = None
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        if self._mem_conn:
            return self._mem_conn
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quota_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    endpoint TEXT NOT NULL,
                    units_spent INTEGER NOT NULL,
                    daily_cumulative INTEGER NOT NULL,
                    details TEXT
                )
            """)
            conn.commit()

    def get_today_usage(self) -> int:
        today_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT SUM(units_spent) FROM quota_logs
                WHERE timestamp LIKE ?
            """, (f"{today_prefix}%",))
            row = cur.fetchone()
            return int(row[0]) if row and row[0] is not None else 0

    def can_spend(self, endpoint: str, count: int = 1) -> bool:
        cost = ENDPOINT_COSTS.get(endpoint, 1) * count
        used = self.get_today_usage()
        return (used + cost) <= self.daily_limit

    def record_call(self, endpoint: str, count: int = 1, details: str = "") -> int:
        cost = ENDPOINT_COSTS.get(endpoint, 1) * count
        now_str = datetime.now(timezone.utc).isoformat()
        current_used = self.get_today_usage()
        new_total = current_used + cost

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO quota_logs (timestamp, endpoint, units_spent, daily_cumulative, details)
                VALUES (?, ?, ?, ?, ?)
            """, (now_str, endpoint, cost, new_total, details))
            conn.commit()

        if new_total >= (self.daily_limit * 0.8):
            pct = (new_total / self.daily_limit) * 100
            print(f"[Quota Warning] Daily quota usage at {pct:.1f}% ({new_total}/{self.daily_limit} units)")

        return cost

    def get_summary(self) -> dict:
        used = self.get_today_usage()
        remaining = max(0, self.daily_limit - used)
        pct = (used / self.daily_limit) * 100 if self.daily_limit > 0 else 0

        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT endpoint, SUM(units_spent), COUNT(*)
                FROM quota_logs
                WHERE timestamp LIKE ?
                GROUP BY endpoint
            """, (f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}%",))
            breakdown = [{"endpoint": r[0], "units": r[1], "calls": r[2]} for r in cur.fetchall()]

        return {
            "daily_limit": self.daily_limit,
            "units_used_today": used,
            "units_remaining": remaining,
            "percent_used": round(pct, 2),
            "breakdown": breakdown
        }
