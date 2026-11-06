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

class TestGearFilter(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")
        self.gear_mgr = GearManager()

    def test_gear_manifest_items(self):
        """Verifies gear.yaml only contains the specified items."""
        self.assertEqual(self.gear_mgr.bike, "Himalayan 450")
        self.assertEqual(self.gear_mgr.action_camera, "DJI Osmo Action 3")
        self.assertEqual(self.gear_mgr.phone, "Motorola Edge 40 Neo")
        self.assertIn("Generic wired microphone", self.gear_mgr.microphones)
        self.assertIn("Grenaro wireless microphone", self.gear_mgr.microphones)
        self.assertEqual(self.gear_mgr.computer, "Apple Mac Mini M4")
        self.assertEqual(self.gear_mgr.video_editing, "Final Cut Pro")
        self.assertEqual(self.gear_mgr.image_editing, "Canva (Free tier)")

    def test_forbidden_gear_rejection(self):
        """Verifies that suggestions containing unauthorized cameras, editors, or mics fail validation."""
        forbidden_samples = [
            "Shoot this with your Insta360 X4 on the handlebar",
            "Mount your GoPro Hero 12 on the helmet",
            "Use Adobe Premiere Pro on your PC to color grade",
            "Edit this in DaVinci Resolve",
            "Use your DJI Mic 2 wireless kit",
            "Fly a DJI Mini drone over the pass"
        ]
        for sample in forbidden_samples:
            is_valid, violations = self.gear_mgr.validate_suggestion(sample)
            self.assertFalse(is_valid, f"Expected validation failure for: '{sample}'")
            self.assertGreater(len(violations), 0)

    def test_authorized_gear_acceptance(self):
        """Verifies that authorized gear passes validation."""
        authorized_sample = (
            "Mount DJI Osmo Action 3 to helmet chin mount. Record moving audio using Grenaro wireless microphone. "
            "Use Motorola Edge 40 Neo for vertical B-roll. Ingest into Apple Mac Mini M4, edit in Final Cut Pro, "
            "and create thumbnail in Canva (Free tier)."
        )
        is_valid, violations = self.gear_mgr.validate_suggestion(authorized_sample)
        self.assertTrue(is_valid, f"Unexpected validation violations: {violations}")

    def test_shoot_planner_main_plan_gear_compliance(self):
        """Verifies that all shoots in the main plan use ONLY authorized gear."""
        shoot_mod = ShootPlannerModule(self.config, self.db, self.quota)
        result = shoot_mod.run()

        for shoot in result["planned_shoots"]:
            gear_used = shoot["gear_assigned"]
            # Check camera is authorized from gear.yaml
            self.assertIn(gear_used["primary_camera"], ["DJI Osmo Action 3", "Motorola Edge 40 Neo"])
            # Check mic assignment matches moving rule
            if shoot["is_moving_shot"]:
                self.assertIn("Grenaro wireless", gear_used["microphone"])
            else:
                self.assertIn("Generic wired", gear_used["microphone"])
            # Check editor
            self.assertIn("Final Cut Pro", gear_used["editing_station"])
            self.assertIn("Canva (Free tier)", gear_used["graphics_tool"])

    def test_optional_missing_gear_isolation(self):
        """Verifies that ideas needing missing gear are kept out of main plan under 'Needs gear (optional)'."""
        shoot_mod = ShootPlannerModule(self.config, self.db, self.quota)
        result = shoot_mod.run()

        self.assertIn("needs_gear_optional", result)
        optional_items = result["needs_gear_optional"]
        self.assertGreater(len(optional_items), 0)

        for item in optional_items:
            self.assertIn("required_missing_gear", item)
            self.assertIn("why_kept_out_of_main_plan", item)
            self.assertIn("current_workaround", item)

    def test_phone_spec_confirmation_removes_notice(self):
        """Verifies that defining phone settings removes the unconfirmed warning notice."""
        gm = GearManager()
        # Test unconfirmed behavior when settings are cleared
        gm.gear["phone_settings"] = {}
        if "capture profile" in gm.gear:
            del gm.gear["capture profile"]
        if "capture_profile" in gm.gear:
            del gm.gear["capture_profile"]
        self.assertFalse(gm.is_phone_spec_confirmed())
        self.assertIn("Note on Phone Settings", gm.get_phone_spec_notice())

        # When specs are provided
        gm.gear["phone_settings"] = {
            "resolution": "4K",
            "frame_rate": "30fps",
            "stabilization": "EIS On"
        }
        self.assertTrue(gm.is_phone_spec_confirmed())
        self.assertEqual(gm.get_phone_spec_notice(), "")
        self.assertEqual(gm.phone_settings["resolution"], "4K")

if __name__ == "__main__":
    unittest.main()
