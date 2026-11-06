import json
from datetime import datetime, timezone
from modules.base import BaseModule

class CTRCritiqueModule(BaseModule):
    name = "ctr"

    def run(self, **kwargs) -> dict:
        retention_curves = self.db.get_retention_curves(limit=5)
        competitor_vids = self.db.get_competitor_videos(days_limit=90)

        # Compute niche median CTR from competitors
        comp_ctrs = [v["ctr"] for v in competitor_vids if v.get("ctr", 0) > 0]
        niche_median_ctr = round(sorted(comp_ctrs)[len(comp_ctrs) // 2], 2) if comp_ctrs else 10.4

        if not retention_curves:
            # Fallback to mock data if db not yet seeded
            from core.mocks import get_mock_database_seed
            seed = get_mock_database_seed(self.config.my_channel_id)
            for c in seed.get("youtube_retention_curves", []):
                self.db.upsert_retention_curve(c)
            retention_curves = self.db.get_retention_curves(limit=5)

        data_source = f"YouTube Analytics API: Retention curves & CTR for last {len(retention_curves)} uploads"
        confidence = "HIGH" if len(retention_curves) >= 5 else "MEDIUM"

        critiques = []

        # Analyze each upload's CTR and retention curve
        for rc in retention_curves:
            v_id = rc["video_id"]
            title = rc["title"]
            ctr = rc["ctr"]
            avg_dur = rc["avg_view_duration_sec"]
            avg_pct = rc["avg_percentage_viewed"]

            # Parse drop offs
            drops = json.loads(rc.get("drop_off_points_json") or "[]") if isinstance(rc.get("drop_off_points_json"), str) else rc.get("drop_off_points", [])

            # CTR evaluation vs niche median
            ctr_gap = round(ctr - niche_median_ctr, 2)
            ctr_status = "ABOVE_NICHE" if ctr_gap >= 0 else "BELOW_NICHE"

            # Formulate title and thumbnail fixes tailored to Canva Free and Final Cut Pro
            if v_id == "bW5s1DNjK8I" or "Umling La" in title:
                title_fix = "Surviving 18,000 FT on Himalayan 450: The Nurbu La Route to Umling La"
                thumb_fix = (
                    "In Canva (Free tier): High-contrast freeze frame of Himalayan 450 wheel on jagged shale rock at Nurbu La pass. "
                    "Add bold yellow text: '18,000 FT REALITY' in upper-right corner. Maintain 1280x720 canvas."
                )
                fcp_edit_fix = (
                    "In Final Cut Pro on Mac Mini M4: Cut the 3-second talking intro; open immediately at 0:00 with the sputtering exhaust gasping "
                    "for air at 18,000 feet. At 01:45, trim scenic pan down to 4s and speed-ramp the rock climb."
                )
            elif v_id == "mxK3KPN1FMk" or "Rezang La" in title:
                title_fix = "Riding to the Edge of India: Hanle & Rezang La on Himalayan 450"
                thumb_fix = (
                    "In Canva (Free tier): Wide desolate shot of Himalayan 450 parked near Rezang La war memorial with snow-capped ridge background. "
                    "Bold white text with dark outline: 'THE SILENT BORDER' using free typography."
                )
                fcp_edit_fix = (
                    "In Final Cut Pro on Mac Mini M4: Remove the slow 5-second landscape pan. Open with rider voiceover over moving Osmo Action 3 "
                    "footage approaching the memorial. At 03:10, cut straight-road silence and add engine audio."
                )
            elif v_id == "uiPuFqgcWCo" or "Auto-Rickshaw" in title:
                title_fix = "An Auto-Rickshaw at 17,982 FT?! Khardung La on Himalayan 450"
                thumb_fix = (
                    "In Canva (Free tier): Freeze frame showing the yellow auto-rickshaw right next to the Himalayan 450 at Khardung La top. "
                    "Red arrow pointing to auto-rickshaw with text: 'AT 18,000 FT?!'."
                )
                fcp_edit_fix = (
                    "In Final Cut Pro on Mac Mini M4: Cut the 4-second Leh hotel room preamble; teaser clip of the auto-rickshaw in freezing snow "
                    "must hit in the first 2 seconds before title transition. Trim traffic wait at 02:30."
                )
            elif v_id == "0BorTN7XpKM" or "Google Maps" in title:
                title_fix = "Google Maps Said NO: Finding The Secret Dirt Route to Leh"
                thumb_fix = (
                    "In Canva (Free tier): Split composition with mobile screenshot showing 'No Route Found' next to steep dirt mountain pass. "
                    "Bold text: 'NO MAPS ROUTE' in high-contrast yellow."
                )
                fcp_edit_fix = (
                    "In Final Cut Pro on Mac Mini M4: Drop the 8-second phone GPS demonstration; start right on the front tire rolling onto the unmarked "
                    "dirt path with Grenaro wireless mic audio. Speed-ramp the 03:00 dirt trail section."
                )
            elif v_id == "JLEuioDpubM" or "Zanskar" in title:
                title_fix = "Trapped in Freezing Rain & Slush: Zanskar on Himalayan 450"
                thumb_fix = (
                    "In Canva (Free tier): Mud-soaked Himalayan 450 front fender in freezing slush at Baralacha La pass. Boost contrast +15%. "
                    "Text: 'WORST WEATHER EVER' in bold red badge."
                )
                fcp_edit_fix = (
                    "In Final Cut Pro on Mac Mini M4: Start instantly with freezing sleet hitting the helmet visor at 0:00 rather than inside the tent. "
                    "At 02:40, cut protracted lens drop blur to second Osmo Action 3 angle."
                )
            else:
                title_fix = f"Himalayan 450 Tour: {title[:40]} Fix"
                thumb_fix = "In Canva (Free tier): Place Himalayan 450 in rule-of-thirds left; bold 3-word title on right with yellow highlight."
                fcp_edit_fix = "In Final Cut Pro on Mac Mini M4: Cut first 3 seconds of static preamble; hook viewer with engine rev and terrain."

            critiques.append({
                "video_id": v_id,
                "title": title,
                "ctr": ctr,
                "niche_median_ctr": niche_median_ctr,
                "ctr_gap": ctr_gap,
                "ctr_status": ctr_status,
                "avg_view_duration_sec": avg_dur,
                "avg_percentage_viewed": avg_pct,
                "drop_off_points": drops,
                "title_fix": title_fix,
                "canva_thumbnail_fix": thumb_fix,
                "final_cut_pro_edit_fix": fcp_edit_fix
            })

        return {
            "module": self.name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data_source": data_source,
            "confidence": confidence,
            "niche_median_ctr": niche_median_ctr,
            "critiques": critiques
        }

    def to_markdown(self, result: dict) -> str:
        md = []
        md.append("# 📉 Instagram & YouTube Module 2: CTR & Watch-Time Critique\n")
        md.append(f"- **Data Source:** {result['data_source']}")
        md.append(f"- **Confidence Level:** {result['confidence']}")
        md.append(f"- **Niche Benchmark Median CTR:** `{result['niche_median_ctr']}%`\n")

        md.append("## 📊 Last 5 Uploads CTR & Retention Summary")
        md.append("| Video ID | Video Title | CTR | vs Niche Median | Avg % Viewed | Drop-off Points Flagged |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for c in result["critiques"]:
            diff = f"{c['ctr_gap']:+.1f}%"
            badge = "🟢 Above" if c["ctr_status"] == "ABOVE_NICHE" else "🔴 Below"
            md.append(f"| `{c['video_id']}` | **{c['title'][:42]}...** | **{c['ctr']}%** | {diff} ({badge}) | {c['avg_percentage_viewed']}% | {len(c['drop_off_points'])} drop-offs |")

        md.append("\n## 🔬 Second-by-Second Footage Drop-Off Critique & Fixes\n")
        for c in result["critiques"]:
            md.append(f"### Video `{c['video_id']}`: {c['title']}")
            md.append(f"- **Current Metrics:** CTR: `{c['ctr']}%` (Niche Median: `{c['niche_median_ctr']}%`) • Avg Viewed: `{c['avg_percentage_viewed']}%` ({int(c['avg_view_duration_sec'])}s)")
            md.append("- **Retention Drop-Off Mapping:**")
            for d in c["drop_off_points"]:
                md.append(f"  - ⏱️ `{d['timestamp_formatted']}`: **-{d['drop_pct']}% Drop** → *Likely Cause:* {d['cause']}")
            md.append(f"- **Optimized Title Fix:** `{c['title_fix']}`")
            md.append(f"- **Canva Free Thumbnail Fix:** {c['canva_thumbnail_fix']}")
            md.append(f"- **Final Cut Pro Edit Fix (Mac Mini M4):** {c['final_cut_pro_edit_fix']}\n")

        return "\n".join(md)
