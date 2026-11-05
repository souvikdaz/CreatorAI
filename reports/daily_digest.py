from datetime import datetime, timezone
from pathlib import Path
from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.ideas import VideoIdeasModule
from modules.timing import TimingModule
from modules.repurpose import RepurposeModule
from modules.sponsors import SponsorshipModule

class DailyDigestGenerator:
    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota

    def generate(self, output_dir: str = "output") -> str:
        ideas_res = VideoIdeasModule(self.config, self.db, self.quota).run()
        timing_res = TimingModule(self.config, self.db, self.quota).run()
        repurpose_res = RepurposeModule(self.config, self.db, self.quota).run()
        sponsors_res = SponsorshipModule(self.config, self.db, self.quota).run()
        quota_summary = self.quota.get_summary()

        now_str = datetime.now(timezone.utc).strftime("%A, %d %B %Y")
        top_idea = ideas_res["ideas"][0]
        top_slot = timing_res["top_3_recommended_slots"][0]
        top_clip = repurpose_res["repurposed_clips"][0]
        top_sponsor_act = sponsors_res["monetization_avenues"][1]  # Affiliate

        md = []
        md.append(f"# 📅 Daily Channel Action Digest — {now_str}")
        md.append(f"**Target Channel:** `{self.config.my_channel_id}` | **Timezone:** `{self.config.timezone}`\n")
        md.append("---")

        md.append("## ⚡ Top 4 Immediate Priorities for Today\n")

        md.append("### 1. 🎬 Production: Script Top Gap Video Idea")
        md.append(f"- **Concept:** **{top_idea['title_concept']}**")
        md.append(f"- **Target Keyword:** `{top_idea['target_keyword']}`")
        md.append(f"- **Hook Line to Record:** *\"{top_idea['hook']}\"*")
        md.append(f"- **Confidence:** `HIGH` | **Source:** Competitor gap analysis ({top_idea['rationale']})\n")

        md.append("### 2. ⏰ Distribution: Best Window to Publish or Schedule")
        md.append(f"- **Optimal Target Slot:** **{top_slot['day']} at {top_slot['time_display']}**")
        md.append(f"- **Benchmark:** {top_slot['median_velocity']:,} views/day median velocity across niche")
        md.append(f"- **Execution:** Upload unlisted 90 minutes prior to let YouTube process 4K and automated captions.\n")

        md.append("### 3. ✂️ Short-Form: Cut & Post 1 Repurposed Short")
        md.append(f"- **Clip Target:** **{top_clip['shorts_title']}**")
        md.append(f"- **Timestamp Range:** `{top_clip['timestamp_range']}`")
        md.append(f"- **On-Screen Text Hook (0-3s):** *\"{top_clip['hook_line']}\"*")
        md.append(f"- **Caption:** {top_clip['caption']}\n")

        md.append("### 4. 💰 Revenue & Partner Action")
        md.append(f"- **Focus:** {top_sponsor_act['avenue']}")
        md.append(f"- **Action:** {top_sponsor_act['next_action']}\n")

        md.append("---")
        md.append("## 📊 Quota & System Health")
        md.append(f"- **Daily API Quota:** {quota_summary['units_used_today']:,} / {quota_summary['daily_limit']:,} units used ({quota_summary['percent_used']}%)")
        md.append(f"- **Remaining Quota:** {quota_summary['units_remaining']:,} units")
        md.append(f"- **Mode:** {'Mock / Offline Dataset' if self.config.use_mock_data or not self.config.youtube_api_key else 'Live YouTube Data API v3'}\n")

        md_text = "\n".join(md)

        # Write to file
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        file_path = out_p / "daily_digest.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        return md_text
