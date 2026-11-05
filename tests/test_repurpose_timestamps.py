import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.repurpose import RepurposeModule

class TestRepurposeTimestamps(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")
        self.module = RepurposeModule(self.config, self.db, self.quota)

    def test_timestamp_formatting(self):
        """Verifies MM:SS formatting."""
        self.assertEqual(RepurposeModule.format_timestamp(0), "00:00")
        self.assertEqual(RepurposeModule.format_timestamp(45), "00:45")
        self.assertEqual(RepurposeModule.format_timestamp(135), "02:15")
        self.assertEqual(RepurposeModule.format_timestamp(660), "11:00")

    def test_clip_durations_between_15_and_60_seconds(self):
        """All repurposed short-form clips must strictly be between 15 and 60 seconds."""
        result = self.module.run()
        clips = result["repurposed_clips"]

        self.assertEqual(len(clips), 5, "Expected exactly 5 repurposed clips")

        for clip in clips:
            start = clip["start_sec"]
            end = clip["end_sec"]
            duration = clip["duration_sec"]

            # Mathematical validity
            self.assertGreater(end, start, f"Clip {clip['id']}: end ({end}) must be greater than start ({start})")
            self.assertEqual(duration, end - start, f"Clip {clip['id']}: duration calculation mismatch")

            # Hard constraint: 15 to 60 seconds
            self.assertGreaterEqual(duration, 15, f"Clip {clip['id']} duration {duration}s is shorter than 15 seconds")
            self.assertLessEqual(duration, 60, f"Clip {clip['id']} duration {duration}s is longer than 60 seconds")

            # Hook and crop notes checks
            self.assertTrue(bool(clip["hook_line"].strip()))
            self.assertTrue(bool(clip["vertical_crop_notes"].strip()))
            self.assertLessEqual(len(clip["shorts_title"]), 60)

if __name__ == "__main__":
    unittest.main()
