from datetime import datetime, timezone
from pathlib import Path
from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from modules.ideas import VideoIdeasModule
from modules.metadata import MetadataModule
from modules.timing import TimingModule
from modules.competitors import CompetitorInsightsModule
from modules.repurpose import RepurposeModule
from modules.sponsors import SponsorshipModule
from modules.monetization import MonetizationAccelerationModule

class WeeklyReportGenerator:
    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota

    def generate(self, output_dir: str = "output") -> str:
        # Run all 7 modules
        m1 = VideoIdeasModule(self.config, self.db, self.quota)
        m2 = MetadataModule(self.config, self.db, self.quota)
        m3 = TimingModule(self.config, self.db, self.quota)
        m4 = CompetitorInsightsModule(self.config, self.db, self.quota)
        m5 = RepurposeModule(self.config, self.db, self.quota)
        m6 = SponsorshipModule(self.config, self.db, self.quota)
        m7 = MonetizationAccelerationModule(self.config, self.db, self.quota)

        r1 = m1.run()
        r2 = m2.run()
        r3 = m3.run()
        r4 = m4.run()
        r5 = m5.run()
        r6 = m6.run()
        r7 = m7.run()

        now_str = datetime.now(timezone.utc).strftime("%d %B %Y")

        md = []
        md.append(f"# 📈 Complete Weekly YouTube Channel Strategy Report")
        md.append(f"**Channel ID:** `{self.config.my_channel_id}` | **Audit Date:** `{now_str}`")
        md.append(f"**Timezone:** `{self.config.timezone}` | **Primary Audience:** `{self.config.audience_country}`\n")
        md.append("---")

        # Executive Summary & Scorecard
        md.append("## 🧭 Executive Summary & Weekly Scorecard\n")
        md.append("| Module | Primary Insight / Objective | Key Action | Confidence |")
        md.append("| :--- | :--- | :--- | :--- |")
        md.append(f"| **1. Ideas** | Top gap in `{r1['cluster_gap_analysis'][0]['cluster']}` | Script: *\"{r1['ideas'][0]['title_concept']}\"* | `{r1['confidence']}` |")
        md.append(f"| **2. Metadata** | Top Title: *\"{r2['title_options'][0]['title']}\"* | Score: `{r2['title_options'][0]['score']}/100` | `{r2['confidence']}` |")
        md.append(f"| **3. Timing** | Peak Window: `{r3['top_3_recommended_slots'][0]['day']} at {r3['top_3_recommended_slots'][0]['time_display']}` | Schedule 90 mins prior | `{r3['confidence']}` |")
        md.append(f"| **4. Competitors** | Top Velocity: `{r4['top_5_competitors'][0]['title']}` ({r4['top_5_competitors'][0]['avg_view_velocity']:,} v/d) | Adapt Side-by-Side Audio Hook | `{r4['confidence']}` |")
        md.append(f"| **5. Repurposing** | 5 High-Retention Short-Form Clips Identified | Cut 45s Camera Cold-Weather clip | `{r5['confidence']}` |")
        md.append(f"| **6. Sponsors** | Immediate focus: Affiliate links & Brand Seeding | Add Amazon gear kit links | `{r6['confidence']}` |")
        md.append(f"| **7. Monetization** | YPP Tier 1 Gap: {r7['tier_1_fan_funding_gap']['subscribers_needed']} subs, {r7['tier_1_fan_funding_gap']['watch_hours_needed']:,} watch hrs | Execute Month 1 Cadence (1 Long + 2 Shorts/wk) | `{r7['confidence']}` |\n")
        md.append("---")

        # Full module sections
        md.append(m1.to_markdown(r1))
        md.append("\n---\n")
        md.append(m2.to_markdown(r2))
        md.append("\n---\n")
        md.append(m3.to_markdown(r3))
        md.append("\n---\n")
        md.append(m4.to_markdown(r4))
        md.append("\n---\n")
        md.append(m5.to_markdown(r5))
        md.append("\n---\n")
        md.append(m6.to_markdown(r6))
        md.append("\n---\n")
        md.append(m7.to_markdown(r7))

        full_report_text = "\n".join(md)

        # Write to file
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        file_path = out_p / "weekly_report.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_report_text)

        return full_report_text
