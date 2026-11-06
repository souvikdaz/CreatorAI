from datetime import datetime, timezone
from pathlib import Path
from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.ideas import VideoIdeasModule
from modules.timing import TimingModule
from modules.repurpose import RepurposeModule
from modules.sponsors import SponsorshipModule
from modules.audit import ContentAuditModule
from modules.growth import FollowerGrowthModule
from modules.shoot import ShootPlannerModule

class DailyDigestGenerator:
    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota

    def generate(self, output_dir: str = "output", platform: str = "both") -> str:
        now_str = datetime.now(timezone.utc).strftime("%A, %d %B %Y")
        quota_summary = self.quota.get_summary()

        md = []
        md.append(f"# 📅 Daily Dual-Platform Action Digest — {now_str}")
        md.append(f"**YouTube:** `{self.config.my_channel_handle}` (`{self.config.my_channel_id}`) | **Instagram:** `{self.config.my_instagram_handle}`")
        md.append(f"**Timezone:** `{self.config.timezone}` | **Platform Scope:** `{platform.upper()}`\n")
        md.append("---")

        md.append("## ⚡ High-Priority Daily Execution Checklist\n")

        # 1. Instagram Immediate Action
        if platform in ("instagram", "both"):
            growth_m = FollowerGrowthModule(self.config, self.db, self.quota).run()
            shoot_m = ShootPlannerModule(self.config, self.db, self.quota).run()
            audit_m = ContentAuditModule(self.config, self.db, self.quota).run()

            top_shoot = shoot_m["planned_shoots"][0]
            top_slot = growth_m["recommended_posting_slots"][0]
            top_fix = audit_m["audited_posts"][0]["specific_fixes"][0]

            md.append("### 1. 📱 Instagram Reel / Post of the Day")
            md.append(f"- **Scheduled Upload:** **{top_slot['day']} at {top_slot['time_ist']}** ({top_slot['intent']})")
            md.append(f"- **Planned Concept:** **{top_shoot['title']}**")
            md.append(f"- **Gear Assigned:** {top_shoot['gear_assigned']['motorcycle']} • {top_shoot['gear_assigned']['primary_camera']} • {top_shoot['gear_assigned']['microphone']}")
            if top_shoot["is_moving_shot"]:
                md.append(f"- 🎙️ **Microphone Rule:** {top_shoot['moving_subject_flag']}")
            md.append(f"- **Audit Fix to Apply:** {top_fix}\n")

        # 2. YouTube Immediate Action
        if platform in ("youtube", "both"):
            ideas_res = VideoIdeasModule(self.config, self.db, self.quota).run()
            timing_res = TimingModule(self.config, self.db, self.quota).run()
            repurpose_res = RepurposeModule(self.config, self.db, self.quota).run()
            sponsors_res = SponsorshipModule(self.config, self.db, self.quota).run()

            top_idea = ideas_res["ideas"][0]
            top_yt_slot = timing_res["top_3_recommended_slots"][0]
            top_clip = repurpose_res["repurposed_clips"][0]
            top_sponsor = sponsors_res["monetization_avenues"][1]

            md.append("### 2. 🎬 YouTube Long-Form Scripting")
            md.append(f"- **Script Priority:** **{top_idea['title_concept']}**")
            md.append(f"- **Target Keyword:** `{top_idea['target_keyword']}`")
            md.append(f"- **Opening Hook:** *\"{top_idea['hook']}\"*")
            md.append(f"- **Upcoming Slot:** {top_yt_slot['day']} at {top_yt_slot['time_display']}\n")

            md.append("### 3. ✂️ YouTube Shorts Repurposing Task")
            md.append(f"- **Clip:** **{top_clip['shorts_title']}** (`{top_clip['timestamp_range']}`)")
            md.append(f"- **On-Screen Text Hook (0-3s):** *\"{top_clip['hook_line']}\"*")
            md.append(f"- **Crop Blueprint:** {top_clip['vertical_crop_notes']}\n")

            md.append("### 4. 💰 Revenue & Affiliate Outreach")
            md.append(f"- **Focus:** {top_sponsor['avenue']}")
            md.append(f"- **Action:** {top_sponsor['next_action']}\n")

        md.append("---")
        md.append("## 📊 Quota & System Health")
        md.append(f"- **Daily API Quota:** {quota_summary['units_used_today']:,} / {quota_summary['daily_limit']:,} units used ({quota_summary['percent_used']}%)")
        md.append(f"- **Remaining Quota:** {quota_summary['units_remaining']:,} units")
        md.append(f"- **Mode:** {'Mock / Offline Dataset' if self.config.use_mock_data or not self.config.youtube_api_key else 'Live Graph / Data API'}\n")

        md_text = "\n".join(md)

        # Write to file
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        file_path = out_p / "daily_digest.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        return md_text
