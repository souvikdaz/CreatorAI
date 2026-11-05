import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.db import Database
from core.quota import QuotaManager

class TestQuotaAndDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:", daily_limit=500)

    def test_quota_tracking(self):
        """Verifies quota subtraction and logging."""
        self.assertEqual(self.quota.get_today_usage(), 0)

        # Spend 100 units on search.list
        cost = self.quota.record_call("search.list")
        self.assertEqual(cost, 100)
        self.assertEqual(self.quota.get_today_usage(), 100)

        # Spend 1 unit on videos.list
        cost2 = self.quota.record_call("videos.list")
        self.assertEqual(cost2, 1)
        self.assertEqual(self.quota.get_today_usage(), 101)

        summary = self.quota.get_summary()
        self.assertEqual(summary["units_remaining"], 399)
        self.assertEqual(summary["percent_used"], 20.2)

    def test_database_upsert_and_retrieval(self):
        """Verifies channel and video upserting into SQLite."""
        ch_data = {
            "channel_id": "UC_test_123456789012345678",
            "title": "Test Channel",
            "subscriber_count": 500,
            "view_count": 10000,
            "is_my_channel": True
        }
        self.db.upsert_channel(ch_data)
        retrieved_ch = self.db.get_channel("UC_test_123456789012345678")
        self.assertIsNotNone(retrieved_ch)
        self.assertEqual(retrieved_ch["title"], "Test Channel")
        self.assertEqual(retrieved_ch["subscriber_count"], 500)

        # Upsert video
        vid_data = {
            "video_id": "vid_abc123",
            "channel_id": "UC_test_123456789012345678",
            "title": "Test Motovlog Video",
            "views": 4000,
            "avg_view_duration_sec": 200.0,
            "is_my_channel": True
        }
        self.db.upsert_video(vid_data)
        my_vids = self.db.get_my_videos()
        self.assertEqual(len(my_vids), 1)
        self.assertEqual(my_vids[0]["title"], "Test Motovlog Video")

if __name__ == "__main__":
    unittest.main()
