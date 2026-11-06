import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.dashboard import DashboardModule

class TestAudienceSnapshots(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")

    def test_record_and_retrieve_snapshots(self):
        """Verifies recording snapshots and chronological retrieval."""
        self.db.record_audience_snapshot("2026-10-01", 800, 240, source="test")
        self.db.record_audience_snapshot("2026-10-08", 820, 250, source="test")
        self.db.record_audience_snapshot("2026-10-15", 845, 260, source="test")

        snapshots = self.db.get_audience_snapshots()
        self.assertEqual(len(snapshots), 3)
        self.assertEqual(snapshots[0]["date"], "2026-10-01")
        self.assertEqual(snapshots[0]["total_audience"], 1040)
        self.assertEqual(snapshots[2]["date"], "2026-10-15")
        self.assertEqual(snapshots[2]["total_audience"], 1105)

    def test_conflict_resolution_same_date(self):
        """Verifies that recording on the same calendar date updates instead of duplicating."""
        self.db.record_audience_snapshot("2026-11-06", 880, 280, source="run1")
        self.db.record_audience_snapshot("2026-11-06", 887, 282, source="run2")

        snapshots = self.db.get_audience_snapshots()
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[0]["youtube_subscribers"], 887)
        self.assertEqual(snapshots[0]["instagram_followers"], 282)
        self.assertEqual(snapshots[0]["total_audience"], 1169)
        self.assertEqual(snapshots[0]["source"], "run2")

    def test_seeding_snapshots(self):
        """Verifies seeding baseline milestones into an empty table."""
        history = [
            {"date": "2026-08-14", "youtube_subs": 740, "instagram_followers": 230},
            {"date": "2026-09-01", "youtube_subs": 775, "instagram_followers": 242}
        ]
        inserted = self.db.seed_audience_snapshots_if_empty(history)
        self.assertEqual(inserted, 2)
        snapshots = self.db.get_audience_snapshots()
        self.assertEqual(len(snapshots), 2)

        # Calling again should not re-insert because table has >= 2 records
        inserted2 = self.db.seed_audience_snapshots_if_empty(history)
        self.assertEqual(inserted2, 0)

    def test_dashboard_uses_snapshots(self):
        """Verifies that DashboardModule leverages audience snapshots for timeline and delta."""
        self.db.record_audience_snapshot("2026-10-01", 800, 240, source="test")
        self.db.record_audience_snapshot("2026-11-06", 887, 282, source="test")

        dash = DashboardModule(self.config, self.db, self.quota)
        res = dash.run()

        self.assertIn("audience_snapshots", res)
        self.assertEqual(len(res["audience_snapshots"]), 2)
        timeline = res["growth_timeline"]
        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0]["date"], "2026-10-01")
        self.assertEqual(timeline[1]["date"], "2026-11-06")
        self.assertEqual(timeline[1]["total_followers"], 1169)

if __name__ == "__main__":
    unittest.main()
