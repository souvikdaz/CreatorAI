import unittest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.metadata import MetadataModule

class TestMetadataScoring(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.use_mock_data = True
        self.db = Database(":memory:")
        self.quota = QuotaManager(":memory:")
        self.module = MetadataModule(self.config, self.db, self.quota)
        self.top_titles = [
            "Don't Buy Himalayan 450 Before Watching This: Long Term Truth",
            "Insta360 X4 vs GoPro Hero 12 for Motovlogging: Tested at 100km/h",
            "Solo Winter Ride to Spiti Valley in -15°C Extreme Challenge"
        ]

    def test_title_under_70_characters_rule(self):
        """Verifies that titles under 70 characters score higher and titles >70 are flagged."""
        short_title = "Motorcycle Touring Packing List: 7 Items I Regret Carrying"  # 57 chars
        long_title = "This Is A Very Long Title That Exceeds The Mobile Screen Truncation Limit Of Seventy Characters So Viewers Cannot See The End"  # 126 chars

        score_short = self.module.score_title(short_title, self.top_titles, "motorcycle touring")
        score_long = self.module.score_title(long_title, self.top_titles, "motorcycle touring")

        self.assertLessEqual(len(short_title), 70)
        self.assertGreater(len(long_title), 70)
        self.assertGreater(score_short["score"], score_long["score"])
        self.assertTrue(any("Over 70 characters" in note for note in score_long["breakdown"]))

    def test_front_loaded_keyword_bonus(self):
        """Titles with the primary keyword in the first 25 chars should score higher."""
        front_loaded = "Motorcycle Touring Gear: 5 Mistakes That Ruined My Trip"
        back_loaded = "5 Common Mistakes That Ruined My Trip While Motorcycle Touring"

        score_front = self.module.score_title(front_loaded, self.top_titles, "motorcycle touring")
        score_back = self.module.score_title(back_loaded, self.top_titles, "motorcycle touring")

        self.assertGreater(score_front["score"], score_back["score"])
        self.assertTrue(any("strongly front-loaded" in note for note in score_front["breakdown"]))

    def test_clickbait_spam_penalty(self):
        """Deceitful or spammy clickbait words must incur a penalty."""
        clean_title = "Himalayan 450 Touring Setup: The Real Luggage & Tool Kit"
        spam_title = "You Won't Believe What Happened On Himalayan 450 OMG INSANE!!!"

        score_clean = self.module.score_title(clean_title, self.top_titles, "himalayan 450")
        score_spam = self.module.score_title(spam_title, self.top_titles, "himalayan 450")

        self.assertGreater(score_clean["score"], score_spam["score"])
        self.assertTrue(any("clickbait penalty" in note for note in score_spam["breakdown"]))

    def test_module_run_output_structure(self):
        """Module run() should return 5 scored title options, description, and 15 tags."""
        result = self.module.run()
        self.assertIn("title_options", result)
        self.assertEqual(len(result["title_options"]), 5)

        # All 5 generated titles must be strictly <= 70 chars
        for t in result["title_options"]:
            self.assertLessEqual(t["char_count"], 70, f"Title '{t['title']}' exceeded 70 characters")

        # Description check
        self.assertIn("first_150_chars", result["description"])
        self.assertLessEqual(result["description"]["first_150_char_length"], 160)

        # 15 tags check
        self.assertIn("tags_15", result)
        self.assertEqual(len(result["tags_15"]), 15)

if __name__ == "__main__":
    unittest.main()
