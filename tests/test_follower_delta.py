import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.growth import FollowerGrowthModule

class TestFollowerDelta(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")
        self.module = FollowerGrowthModule(self.config, self.db, self.quota)

    def test_follower_delta_aggregation(self):
        """Verifies calculation of follower deltas per format."""
        result = self.module.run()
        rankings = result["format_rankings"]

        self.assertGreater(len(rankings), 0)
        # Verify that all formats have non-negative follows gained
        total_follows = sum(f["total_follows_gained"] for f in rankings)
        self.assertGreater(total_follows, 0)

        # REEL format should be #1 driver of net followers
        top_format = rankings[0]
        self.assertEqual(top_format["format"], "REEL")
        self.assertGreater(top_format["avg_follows_per_post"], 0)

    def test_top_3_performing_sub_formats(self):
        """Verifies exactly 3 data-backed sub-formats are returned."""
        result = self.module.run()
        top_3 = result["top_3_performing_formats"]
        self.assertEqual(len(top_3), 3)

        for item in top_3:
            self.assertIn("rank", item)
            self.assertIn("sub_format", item)
            self.assertIn("delta_metric", item)
            self.assertIn("reasoning", item)
            self.assertTrue(len(item["reasoning"].strip()) > 10)

    def test_projections_labeled_as_estimates(self):
        """Ensures follower projections are explicitly presented as ranges and labeled as estimates."""
        result = self.module.run()
        gp = result["growth_projections"]
        self.assertIn("disclaimer", gp)
        self.assertIn("Estimates based strictly", gp["disclaimer"])
        self.assertIn("range", gp["projected_30d_follower_delta_range"].lower())

if __name__ == "__main__":
    unittest.main()
