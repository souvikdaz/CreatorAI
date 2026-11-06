import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.ctr import CTRCritiqueModule

class TestCTRCritique(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")
        self.module = CTRCritiqueModule(self.config, self.db, self.quota)

    def test_ctr_vs_niche_median_calculation(self):
        """Verifies calculation of CTR difference against niche median."""
        result = self.module.run()
        niche_median = result["niche_median_ctr"]
        self.assertGreater(niche_median, 0)

        critiques = result["critiques"]
        self.assertEqual(len(critiques), 5, "Expected last 5 uploads analyzed")

        for c in critiques:
            expected_diff = round(c["ctr"] - niche_median, 2)
            self.assertEqual(c["ctr_gap"], expected_diff)
            if c["ctr"] >= niche_median:
                self.assertEqual(c["ctr_status"], "ABOVE_NICHE")
            else:
                self.assertEqual(c["ctr_status"], "BELOW_NICHE")

    def test_drop_off_mapping_to_footage(self):
        """Verifies each drop-off has a timestamp and a recognized cause."""
        result = self.module.run()
        for c in result["critiques"]:
            drops = c["drop_off_points"]
            self.assertGreater(len(drops), 0, f"Video {c['video_id']} should have drop-off points")
            for d in drops:
                self.assertIn("timestamp_formatted", d)
                self.assertIn("cause", d)
                self.assertTrue(len(d["cause"].strip()) > 5)

    def test_tool_compliance_in_fixes(self):
        """Verifies fixes only reference Canva Free and Final Cut Pro on Mac Mini M4."""
        result = self.module.run()
        for c in result["critiques"]:
            self.assertIn("Canva", c["canva_thumbnail_fix"])
            self.assertIn("Final Cut Pro", c["final_cut_pro_edit_fix"])
            # Ensure no forbidden editors
            for forbidden in ["Premiere", "Photoshop", "DaVinci"]:
                self.assertNotIn(forbidden, c["canva_thumbnail_fix"])
                self.assertNotIn(forbidden, c["final_cut_pro_edit_fix"])

if __name__ == "__main__":
    unittest.main()
