import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.gear_manager import GearManager
from modules.shoot import ShootPlannerModule
from modules.ideas import VideoIdeasModule
from core.config import Config
from core.db import Database
from core.quota import QuotaManager

class TestBikeFilter(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")
        self.gear_mgr = GearManager()

    def test_bike_manifest_strictly_himalayan_450(self):
        """Verifies gear.yaml bike is strictly Himalayan 450."""
        self.assertEqual(self.gear_mgr.bike, "Himalayan 450")

    def test_unauthorized_bike_detection(self):
        """Verifies that suggestions containing other motorcycle brands or models fail validation."""
        forbidden_bike_texts = [
            "Take your KTM 390 Adventure for this offroad tour",
            "Compare this with a BMW GS on the highway",
            "Ride the Royal Enfield Classic 350 to Spiti",
            "Take the Triumph Scrambler 400X across the river",
            "Cruising on an Interceptor 650"
        ]
        for text in forbidden_bike_texts:
            is_valid, violations = self.gear_mgr.validate_suggestion(text)
            self.assertFalse(is_valid, f"Expected validation failure for unauthorized bike: '{text}'")
            self.assertTrue(any("unauthorized bike" in v.lower() or "ktm" in v.lower() or "bmw" in v.lower() for v in violations))

    def test_shoot_planner_bike_filter_compliance(self):
        """Verifies that all shoot plans in ShootPlannerModule use strictly Himalayan 450."""
        shoot_mod = ShootPlannerModule(self.config, self.db, self.quota)
        result = shoot_mod.run()

        for shoot in result["planned_shoots"]:
            bike_used = shoot["gear_assigned"]["motorcycle"]
            self.assertEqual(bike_used, "Himalayan 450", f"Shoot {shoot['id']} must use Himalayan 450 only")

    def test_video_ideas_bike_filter_compliance(self):
        """Verifies that all 10 video ideas in VideoIdeasModule do not suggest any bike other than Himalayan 450."""
        ideas_mod = VideoIdeasModule(self.config, self.db, self.quota)
        result = ideas_mod.run()

        for idea in result["ideas"]:
            full_text = f"{idea['title_concept']} {idea['hook']} {idea['rationale']}"
            is_valid, violations = self.gear_mgr.validate_suggestion(full_text)
            self.assertTrue(is_valid, f"Idea {idea['id']} contained forbidden bike or gear: {violations}")

if __name__ == "__main__":
    unittest.main()
