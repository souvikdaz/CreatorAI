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
from modules.audit import ContentAuditModule
from modules.ctr import CTRCritiqueModule
from modules.growth import FollowerGrowthModule
from modules.benchmark import NicheBenchmarkModule
from modules.shoot import ShootPlannerModule

class WeeklyReportGenerator:
    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota

    def generate(self, output_dir: str = "output", platform: str = "both") -> str:
        now_str = datetime.now(timezone.utc).strftime("%d %B %Y")
        md = []
        md.append(f"# 📈 Complete Weekly Dual-Platform Strategy Report")
        md.append(f"**Primary YouTube Channel:** `{self.config.my_channel_id}` | **Instagram:** `{self.config.my_instagram_handle}`")
        md.append(f"**Audit Date:** `{now_str}` | **Timezone:** `{self.config.timezone}` | **Platform Scope:** `{platform.upper()}`\n")
        md.append("---")

        md.append("## 🧭 Executive Summary & Weekly Scorecard\n")
        md.append("| Platform | Module | Key Strategic Insight | Immediate Action | Confidence |")
        md.append("| :--- | :--- | :--- | :--- | :--- |")

        include_yt = platform in ("youtube", "both")
        include_ig = platform in ("instagram", "both")

        # Run Instagram modules if requested
        if include_ig:
            m_audit = ContentAuditModule(self.config, self.db, self.quota)
            m_ctr = CTRCritiqueModule(self.config, self.db, self.quota)
            m_growth = FollowerGrowthModule(self.config, self.db, self.quota)
            m_bench = NicheBenchmarkModule(self.config, self.db, self.quota)
            m_shoot = ShootPlannerModule(self.config, self.db, self.quota)

            r_audit = m_audit.run()
            r_ctr = m_ctr.run()
            r_growth = m_growth.run()
            r_bench = m_bench.run()
            r_shoot = m_shoot.run()

            top_fix = r_audit['audited_posts'][0]['specific_fixes'][0].split(':')[0]
            md.append(f"| Instagram | **Audit** | Top Post: `{r_audit['audited_posts'][0]['post_id']}` ({r_audit['audited_posts'][0]['scores']['overall_score']}/100) | {top_fix} | `{r_audit['confidence']}` |")
            md.append(f"| Instagram/YT | **CTR Critique** | Niche Median CTR: `{r_ctr['niche_median_ctr']}%` | Title & Canva Free thumbnail fixes | `{r_ctr['confidence']}` |")
            md.append(f"| Instagram | **Growth Plan** | Top Format: `{r_growth['top_3_performing_formats'][0]['parent_format']}` ({r_growth['top_3_performing_formats'][0]['sub_format'][:30]}...) | Cadence: 3 Reels + 1 Carousel / wk | `{r_growth['confidence']}` |")
            md.append(f"| Instagram | **Benchmark** | Tracked `{r_bench['accounts_tracked_count']}` niche creators | 4 adaptable hook & tag patterns | `{r_bench['confidence']}` |")
            md.append(f"| Dual-Platform | **Shoot Planner** | 100% compliant with `gear.yaml` | Grenaro wireless mic for moving shots | `{r_shoot['confidence']}` |")

        # Run YouTube modules if requested
        if include_yt:
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

            md.append(f"| YouTube | **Ideas** | Top gap in `{r1['cluster_gap_analysis'][0]['cluster']}` | Script: *\"{r1['ideas'][0]['title_concept']}\"* | `{r1['confidence']}` |")
            md.append(f"| YouTube | **Metadata** | Top Title: *\"{r2['title_options'][0]['title']}\"* | Score: `{r2['title_options'][0]['score']}/100` | `{r2['confidence']}` |")
            md.append(f"| YouTube | **Timing** | Peak Window: `{r3['top_3_recommended_slots'][0]['day']} at {r3['top_3_recommended_slots'][0]['time_display']}` | Schedule 90 mins prior | `{r3['confidence']}` |")
            md.append(f"| YouTube | **Monetization** | YPP Tier 1 Gap: {r7['tier_1_fan_funding_gap']['subscribers_needed']} subs, {r7['tier_1_fan_funding_gap']['watch_hours_needed']:,} watch hrs | Execute Month 1 Cadence | `{r7['confidence']}` |")

        md.append("\n---\n")

        # Append detailed markdown sections
        if include_ig:
            md.append("## 📱 PART I: INSTAGRAM INTELLIGENCE & PRODUCTION MODULES\n")
            md.append(m_audit.to_markdown(r_audit))
            md.append("\n---\n")
            md.append(m_ctr.to_markdown(r_ctr))
            md.append("\n---\n")
            md.append(m_growth.to_markdown(r_growth))
            md.append("\n---\n")
            md.append(m_bench.to_markdown(r_bench))
            md.append("\n---\n")
            md.append(m_shoot.to_markdown(r_shoot))
            md.append("\n---\n")

        if include_yt:
            md.append("## 🎬 PART II: YOUTUBE MACRO DATA & MONETIZATION MODULES\n")
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
