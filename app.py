import os
import sys
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from core.youtube_client import YouTubeClient
from core.instagram_client import InstagramClient
from core.gear_manager import GearManager

from modules.dashboard import DashboardModule
from modules.audit import ContentAuditModule
from modules.ctr import CTRCritiqueModule
from modules.growth import FollowerGrowthModule
from modules.benchmark import NicheBenchmarkModule
from modules.shoot import ShootPlannerModule
from modules.ideas import VideoIdeasModule
from modules.metadata import MetadataModule
from modules.timing import TimingModule
from modules.competitors import CompetitorInsightsModule
from modules.repurpose import RepurposeModule
from modules.sponsors import SponsorshipModule
from modules.monetization import MonetizationAccelerationModule
from reports.daily_digest import DailyDigestGenerator
from reports.weekly_report import WeeklyReportGenerator

# Page Configuration
st.set_page_config(
    page_title="Creator Studio AI Agent | YouTube & Instagram",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Responsive CSS (Dark & Light theme adaptive)
st.markdown("""
<style>
    .kpi-card {
        background-color: var(--secondary-background-color, #1e1e1e);
        border-radius: 12px;
        padding: 18px 20px;
        border-left: 5px solid #FF0000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 0.85rem;
        color: var(--text-color, #a0a0a0);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        margin: 4px 0;
    }
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #81c784;
    }
    .gear-chip {
        display: inline-block;
        background-color: rgba(255, 0, 0, 0.12);
        color: #ff5252;
        border: 1px solid rgba(255, 0, 0, 0.3);
        border-radius: 16px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-score {
        background-color: #2e7d32;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .thumb-card {
        background-color: var(--secondary-background-color, #1e1e1e);
        border-radius: 10px;
        padding: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        height: 100%;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 1. Initialize Core Resources
@st.cache_resource
def get_services():
    config = Config()
    db = Database(config.sqlite_db_path)
    quota = QuotaManager(config.sqlite_db_path, daily_limit=config.quota_daily_limit)
    yt_client = YouTubeClient(config, db, quota)
    ig_client = InstagramClient(config, db, quota)
    gear_mgr = GearManager(config.gear_config_path)
    yt_client.initialize_data(force_refresh=False)

    # Restore recorded snapshots from data/audience_snapshots.json if SQLite is fresh (e.g. Streamlit Cloud)
    snap_json = Path(config.sqlite_db_path).parent / "audience_snapshots.json"
    if snap_json.exists():
        try:
            with open(snap_json, "r") as f_snap:
                saved = json.load(f_snap)
            if saved and len(db.get_audience_snapshots()) < len(saved):
                for s in saved:
                    db.record_audience_snapshot(
                        date_str=s["date"],
                        yt_subs=s["youtube_subscribers"],
                        ig_followers=s["instagram_followers"],
                        yt_views=s.get("youtube_views", 0),
                        ig_posts=s.get("instagram_posts", 0),
                        notes=s.get("notes", "Restored from JSON backup"),
                        source=s.get("source", "json_sync")
                    )
        except Exception:
            pass

    return config, db, quota, yt_client, ig_client, gear_mgr

config, db, quota, yt_client, ig_client, gear_mgr = get_services()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎬 Creator Studio AI")
    st.caption("YouTube (Primary) & Instagram (Mandatory)")

    st.markdown("---")
    st.markdown("#### 📺 Connected Channels")
    st.markdown(f"- **YouTube:** **{config.my_channel_handle}** (`{config.my_channel_id}`)")
    st.markdown(f"- **Instagram:** `{config.my_instagram_handle}`")
    st.caption(f"Timezone: **{config.timezone}** • Audience: **{config.audience_country}**")

    st.markdown("---")
    st.markdown("#### 🎒 Active Gear Manifest (`gear.yaml`)")
    st.markdown(f"""
    <div>
        <span class="gear-chip">🏍️ {gear_mgr.bike}</span>
        <span class="gear-chip">📷 {gear_mgr.action_camera}</span>
        <span class="gear-chip">📱 {gear_mgr.phone}</span>
        <span class="gear-chip">🎙️ Grenaro Wireless</span>
        <span class="gear-chip">🎙️ Generic Wired</span>
        <span class="gear-chip">💻 Mac Mini M4 (FCP)</span>
        <span class="gear-chip">🎨 Canva (Free)</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Rule: 100% of recommendations use only listed gear. Unlisted gear strictly quarantined.")

    st.markdown("---")
    st.markdown("#### ⚙️ Data Mode")
    mode_selection = st.radio(
        "Platform Engine",
        ["Sample / Mock Dataset", "Live APIs (YouTube & Graph API)"],
        index=0 if (config.use_mock_data or not config.youtube_api_key) else 1
    )
    config.use_mock_data = (mode_selection == "Sample / Mock Dataset")

    st.markdown("---")
    st.markdown("#### 📊 Quota Tracker")
    q_info = quota.get_summary()
    st.progress(q_info["percent_used"] / 100.0)
    st.caption(f"{q_info['units_used_today']:,} / {q_info['daily_limit']:,} units ({q_info['percent_used']}%)")
    st.caption(f"Remaining units: **{q_info['units_remaining']:,}**")

    st.markdown("---")
    if st.button("🔄 Sync & Refresh Cache", use_container_width=True):
        yt_client.initialize_data(force_refresh=True)
        st.success("Refreshed cache!")
        st.rerun()

# --- MAIN NAVIGATION TABS ---
tabs = st.tabs([
    "📊 Executive Dashboard",
    "📱 Instagram Audit",
    "📉 CTR & Watch-Time Critique",
    "📈 Follower Growth Plan",
    "🔭 Niche Competitor Benchmark",
    "🎬 Gear-Aware Shoot Planner",
    "💡 YouTube Ideas & Gaps",
    "🏷️ Metadata & Title Scorer",
    "💼 Monetization & YPP"
])

# ==========================================
# TAB 1: VISUAL-FIRST EXECUTIVE DASHBOARD
# ==========================================
with tabs[0]:
    dash_mod = DashboardModule(config, db, quota)
    d_data = dash_mod.run()
    k = d_data["kpis"]

    # Top Row: 4 KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Audience</div>
            <div class="kpi-value">{k['total_audience_followers']:,}</div>
            <div class="kpi-subtitle">IG: {k['instagram_followers']:,} • YT: {k['youtube_subscribers']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #4caf50;">
            <div class="kpi-title">Follower Delta (30d)</div>
            <div class="kpi-value">+{k['follower_delta_30d']}</div>
            <div class="kpi-subtitle">Combined Net New Community</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #2196f3;">
            <div class="kpi-title">Average Reel Plays</div>
            <div class="kpi-value">{k['average_reel_plays']:,}</div>
            <div class="kpi-subtitle">High Organic Explore Reach</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #ff9800;">
            <div class="kpi-title">Average YouTube CTR</div>
            <div class="kpi-value">{k['average_ctr_pct']}%</div>
            <div class="kpi-subtitle">Niche Median: {d_data['niche_median_ctr']}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Chart Row 1: Follower Growth Line & Reels Plays vs Saves Scatter
    c_row1_1, c_row1_2 = st.columns([1.2, 1.0])

    with c_row1_1:
        st.markdown("##### 📈 Follower Growth Trajectory (Last 90 Days)")
        df_growth = pd.DataFrame(d_data["growth_timeline"])
        fig_growth = px.line(
            df_growth,
            x="date",
            y=["total_followers", "instagram_followers", "youtube_subs"],
            labels={"value": "Followers / Subscribers", "date": "Date", "variable": "Audience Stream"},
            color_discrete_map={
                "total_followers": "#FF0000",
                "instagram_followers": "#E1306C",
                "youtube_subs": "#00E5FF"
            },
            template="plotly_dark"
        )
        fig_growth.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320, legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig_growth, use_container_width=True)

    with c_row1_2:
        st.markdown("##### 🎯 Reels Plays vs Saves (Colored by Format)")
        df_scatter = pd.DataFrame(d_data["scatter_data"])
        fig_scatter = px.scatter(
            df_scatter,
            x="plays",
            y="saves",
            size="reach",
            color="format",
            hover_name="post_id",
            hover_data=["caption_snippet"],
            color_discrete_map={"REEL": "#E1306C", "CAROUSEL": "#FFD700", "SINGLE_IMAGE": "#00E5FF"},
            template="plotly_dark"
        )
        fig_scatter.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=320, legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Historical Snapshot Ledger & Weekly Run Trigger
    with st.expander("📸 Recorded Audience Snapshots & Weekly History Ledger", expanded=False):
        st.markdown("**Weekly Snapshot Ledger (Stored in SQLite `data/youtube_agent.db` & backup `data/audience_snapshots.json`)**")
        snaps_list = d_data.get("audience_snapshots", [])
        if snaps_list:
            df_snaps = pd.DataFrame(snaps_list)[["date", "youtube_subscribers", "instagram_followers", "total_audience", "source"]]
            df_snaps.columns = ["Date", "YouTube Subs", "Instagram Followers", "Total Audience", "Source"]
            st.dataframe(df_snaps, use_container_width=True, hide_index=True)
        else:
            st.info("No snapshots recorded yet. Click below to take your first snapshot.")

        col_sn1, col_sn2 = st.columns([1, 2])
        with col_sn1:
            if st.button("📸 Record Snapshot for Today", key="btn_take_snapshot", use_container_width=True):
                yt_cnt = yt_client.get_live_subscriber_count()
                ig_cnt = ig_client.get_live_follower_count()
                ig_info = ig_client.fetch_public_profile_stats(config.my_instagram_handle)
                t_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                my_ch = db.get_my_channel()
                db.record_audience_snapshot(
                    date_str=t_str,
                    yt_subs=yt_cnt,
                    ig_followers=ig_cnt,
                    yt_views=my_ch.get("view_count", 0) if my_ch else 0,
                    ig_posts=ig_info.get("posts", 136),
                    notes="Recorded via Streamlit UI",
                    source="ui_manual"
                )
                all_s = db.get_audience_snapshots()
                j_path = Path(config.sqlite_db_path).parent / "audience_snapshots.json"
                with open(j_path, "w") as f_snap:
                    json.dump(all_s, f_snap, indent=2)
                st.success(f"Snapshot recorded for {t_str}! YouTube: {yt_cnt:,} | Instagram: {ig_cnt:,}")
                st.rerun()
        with col_sn2:
            st.caption("🤖 **Automated Weekly Run:** Run `python run.py --snapshot` via crontab or GitHub Actions. The app will automatically read the latest numbers from the database.")

    # Chart Row 2: Best Posting Hours Heatmap & CTR Bar Chart
    c_row2_1, c_row2_2 = st.columns([1.2, 1.0])

    with c_row2_1:
        st.markdown("##### ⏰ Best Posting Hours Heatmap (Day of Week × Hour in IST)")
        df_heat = pd.DataFrame(d_data["heatmap_matrix"])
        heat_pivot = df_heat.pivot(index="day", columns="hour", values="intensity")
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heat_pivot = heat_pivot.reindex(days_order)
        fig_heat = px.imshow(
            heat_pivot,
            labels=dict(x="Hour of Day (IST)", y="Day of Week", color="Engagement Index"),
            color_continuous_scale="Reds",
            template="plotly_dark"
        )
        fig_heat.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300)
        st.plotly_chart(fig_heat, use_container_width=True)

    with c_row2_2:
        st.markdown("##### 📊 YouTube CTR vs Niche Median (10.4%)")
        df_ctr = pd.DataFrame(d_data["ctr_bar_data"])
        df_ctr["Color"] = df_ctr["difference"].apply(lambda x: "#4caf50" if x >= 0 else "#f44336")
        fig_ctr = go.Figure()
        fig_ctr.add_trace(go.Bar(
            x=df_ctr["title"],
            y=df_ctr["channel_ctr"],
            marker_color=df_ctr["Color"],
            name="Channel CTR (%)"
        ))
        fig_ctr.add_hline(y=d_data["niche_median_ctr"], line_dash="dash", line_color="#ffeb3b", annotation_text="Niche Median (10.4%)")
        fig_ctr.update_layout(
            template="plotly_dark",
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            yaxis_title="CTR (%)",
            xaxis_tickangle=-25
        )
        st.plotly_chart(fig_ctr, use_container_width=True)

    # Chart Row 3: YouTube Retention Curves with Drop-off Points
    st.markdown("##### 📉 YouTube Retention Curves & Drop-Off Markers (Last 5 Uploads)")
    ret_cols = st.columns(len(d_data["retention_chart_data"]))
    for idx, r_item in enumerate(d_data["retention_chart_data"]):
        with ret_cols[idx]:
            df_curv = pd.DataFrame(r_item["curve"])
            fig_curv = px.area(
                df_curv,
                x="second",
                y="retention_pct",
                title=f"{r_item['video_id']}: {r_item['title'][:20]}...",
                template="plotly_dark"
            )
            fig_curv.update_traces(line_color="#00e5ff", fillcolor="rgba(0, 229, 255, 0.2)")
            # Add drop off points as vertical markers
            for d in r_item["drop_offs"]:
                fig_curv.add_vline(x=d["timestamp_sec"], line_width=1.5, line_dash="dot", line_color="#ff5252")
            fig_curv.update_layout(
                margin=dict(l=10, r=10, t=35, b=10),
                height=220,
                xaxis_title="Sec",
                yaxis_title="Ret %",
                yaxis=dict(range=[0, 105])
            )
            st.plotly_chart(fig_curv, use_container_width=True)

    st.markdown("---")

    # Thumbnail Gallery: Last 5 YouTube & Last 6 Instagram
    st.markdown("### 🖼️ Thumbnail & Creative Gallery (With Diagnostic Scores & Fixes)")
    st.caption("Displays image assets using official platform image URLs. No local downloading or re-distribution of third-party media.")

    t_tab_yt, t_tab_ig = st.tabs(["YouTube Uploads (Last 5)", "Instagram Posts (Recent)"])

    with t_tab_yt:
        yt_cols = st.columns(len(d_data["youtube_gallery"]))
        for i, thumb in enumerate(d_data["youtube_gallery"]):
            with yt_cols[i]:
                st.markdown(f"""
                <div class="thumb-card">
                    <img src="{thumb['thumbnail_url']}" style="width:100%; border-radius:6px; aspect-ratio:16/9; object-fit:cover;"/>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                        <span style="font-weight:600; font-size:0.85rem;">{thumb['title']}</span>
                        <span class="badge-score">{thumb['critique_score']}/100</span>
                    </div>
                    <p style="font-size:0.75rem; color:#b0bec5; margin-top:6px;"><strong>Canva Free Fix:</strong> {thumb['top_fix']}</p>
                </div>
                """, unsafe_allow_html=True)

    with t_tab_ig:
        ig_cols = st.columns(len(d_data["instagram_gallery"]))
        for j, ig_post in enumerate(d_data["instagram_gallery"]):
            with ig_cols[j]:
                st.markdown(f"""
                <div class="thumb-card">
                    <img src="{ig_post['thumbnail_url']}" style="width:100%; border-radius:6px; aspect-ratio:4/5; object-fit:cover;"/>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                        <span style="font-weight:600; font-size:0.85rem;">{ig_post['format']}</span>
                        <span class="badge-score">{ig_post['critique_score']}/100</span>
                    </div>
                    <p style="font-size:0.75rem; color:#b0bec5; margin-top:6px;"><strong>Fix:</strong> {ig_post['top_fix']}</p>
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 2: INSTAGRAM CONTENT AUDIT
# ==========================================
with tabs[1]:
    audit_mod = ContentAuditModule(config, db, quota)
    audit_res = audit_mod.run()
    st.subheader("📱 Instagram Content Quality Audit (Last 5 Posts)")
    st.caption(f"Data Source: {audit_res['data_source']} • Confidence: {audit_res['confidence']}")

    for p in audit_res["audited_posts"]:
        with st.expander(f"Post `{p['post_id']}` ({p['format']}) — Quality Score: {p['scores']['overall_score']}/100", expanded=True):
            col_sc, col_fix = st.columns([1, 2])
            with col_sc:
                st.write(f"- **Plays:** {p['plays']:,}")
                st.write(f"- **Reach:** {p['reach']:,}")
                st.write(f"- **Saves:** {p['saves']:,}")
                st.write(f"- **Shares:** {p['shares']:,}")
                st.write(f"- **Follows Gained:** **+{p['follows_gained']}**")
                st.markdown(f"""
                <div style="margin-top:8px;">
                    <span class="badge-score">Hook: {p['scores']['hook_3s']}/10</span>
                    <span class="badge-score">Pacing: {p['scores']['pacing']}/10</span>
                    <span class="badge-score">CTA: {p['scores']['cta']}/10</span>
                </div>
                """, unsafe_allow_html=True)
            with col_fix:
                st.markdown("**3 Specific Actionable Fixes:**")
                for fix in p["specific_fixes"]:
                    st.markdown(f"- {fix}")
                st.markdown(f"**Hook Rewrite:** *\"{p['rewritten_hook']}\"*")
                st.code(p["rewritten_caption"], language="text")

# ==========================================
# TAB 3: CTR & RETENTION CRITIQUE
# ==========================================
with tabs[2]:
    ctr_mod = CTRCritiqueModule(config, db, quota)
    ctr_res = ctr_mod.run()
    st.subheader("📉 YouTube CTR & Retention Curve Critique")
    st.caption(f"Niche Median CTR: **{ctr_res['niche_median_ctr']}%** • Confidence: {ctr_res['confidence']}")

    for c in ctr_res["critiques"]:
        with st.expander(f"{c['video_id']}: {c['title']} (CTR: {c['ctr']}%)", expanded=True):
            c1, c2 = st.columns([1.2, 1.8])
            with c1:
                st.metric("CTR vs Niche Median", f"{c['ctr']}%", f"{c['ctr_gap']:+.1f}% vs 10.4%")
                st.metric("Avg Percentage Viewed", f"{c['avg_percentage_viewed']}%")
                st.markdown("**Mapped Footage Drop-Offs:**")
                for d in c["drop_off_points"]:
                    st.markdown(f"- ⏱️ `{d['timestamp_formatted']}` (-{d['drop_pct']}%): {d['cause']}")
            with c2:
                st.markdown(f"**Optimized Title Fix:** `{c['title_fix']}`")
                st.info(f"🎨 **Canva Free Thumbnail Fix:** {c['canva_thumbnail_fix']}")
                st.success(f"✂️ **Final Cut Pro Edit Fix (Mac Mini M4):** {c['final_cut_pro_edit_fix']}")

# ==========================================
# TAB 4: FOLLOWER GROWTH PLAN
# ==========================================
with tabs[3]:
    growth_mod = FollowerGrowthModule(config, db, quota)
    growth_res = growth_mod.run()
    st.subheader("📈 Instagram Follower Growth Plan & 30-Day Cadence")

    st.markdown("#### 🏆 Top 3 Formats That Gained Followers")
    for tf in growth_res["top_3_performing_formats"]:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #81c784;">
            <h4>#{tf['rank']}: {tf['sub_format']}</h4>
            <p><strong>Metric Delta:</strong> <code>{tf['delta_metric']}</code></p>
            <p style="color:#b0bec5;"><small>{tf['reasoning']}</small></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🗓️ 30-Day Posting Plan (Cadence: 3 Reels + 1 Carousel / Week)")
    for week in growth_res["thirty_day_plan"]:
        with st.expander(f"{week['week']} — ({week['cadence']})", expanded=True):
            for post in week["schedule"]:
                st.markdown(f"- **{post['day']}:** `{post['format']}` → *{post['theme']}*")

# ==========================================
# TAB 5: NICHE COMPETITOR BENCHMARK
# ==========================================
with tabs[4]:
    bench_mod = NicheBenchmarkModule(config, db, quota)
    bench_res = bench_mod.run()
    st.subheader(f"🔭 Competitor Benchmark ({bench_res['accounts_tracked_count']} Accounts Tracked)")

    b1, b2, b3 = st.columns(3)
    b1.metric("Average Competitor Reach", f"{bench_res['average_competitor_followers']:,}")
    b2.metric("Niche Avg Engagement", f"{bench_res['average_engagement_rate_pct']}%")
    b3.metric("Optimal Hashtags", bench_res["hashtag_benchmarks"]["optimal_range"])

    st.markdown("#### 🚀 4 Adaptable Tactics (Do NOT Copy Content)")
    for idx, rec in enumerate(bench_res["adaptable_recommendations"], 1):
        st.markdown(f"""
        <div class="kpi-card">
            <h4>#{idx}: {rec['recommendation']}</h4>
            <p><strong>Why It Works:</strong> {rec['why_it_works']}</p>
            <p style="color:#a5d6a7;"><strong>How to Adapt on Himalayan 450:</strong> {rec['how_to_adapt']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 6: GEAR-AWARE SHOOT PLANNER
# ==========================================
with tabs[5]:
    shoot_mod = ShootPlannerModule(config, db, quota)
    shoot_res = shoot_mod.run()
    st.subheader("🎬 Gear-Aware Shoot Planner (100% Compliant with `config/gear.yaml`)")
    st.warning(shoot_res["phone_notice"])

    for shoot in shoot_res["planned_shoots"]:
        with st.expander(f"#{shoot['id']}: {shoot['title']} ({shoot['format']})", expanded=True):
            s1, s2 = st.columns([1, 2])
            with s1:
                st.write(f"- **Bike:** `{shoot['gear_assigned']['motorcycle']}`")
                st.write(f"- **Primary Cam:** `{shoot['gear_assigned']['primary_camera']}`")
                st.write(f"- **Microphone:** `{shoot['gear_assigned']['microphone']}`")
                st.write(f"- **Editor:** `{shoot['gear_assigned']['editing_station']}`")
                st.write(f"- **Design:** `{shoot['gear_assigned']['graphics_tool']}`")
                if shoot["is_moving_shot"]:
                    st.error("🎙️ Moving shot rule: Grenaro wireless mic required.")
            with s2:
                st.markdown("**Setup Steps:**")
                for step in shoot["step_by_step_setup"]:
                    st.markdown(f"- {step}")
                st.info(f"🎨 **Canva Free Plan:** {shoot['canva_free_graphic_plan']}")

    st.markdown("---")
    st.markdown("### 📦 Needs gear (optional)")
    st.caption("These ideas require unlisted hardware and are kept strictly out of the main production plan.")
    for og in shoot_res["needs_gear_optional"]:
        st.markdown(f"- **{og['concept']}** (Missing: `{og['required_missing_gear']}`) → *{og['current_workaround']}*")

# ==========================================
# TAB 7: YOUTUBE VIDEO IDEAS & GAPS
# ==========================================
with tabs[6]:
    ideas_mod = VideoIdeasModule(config, db, quota)
    ideas_res = ideas_mod.run()
    st.subheader("💡 YouTube Topic Cluster Gaps & 10 Ideas")
    for idea in ideas_res["ideas"]:
        with st.container():
            st.markdown(f"""
            <div class="kpi-card">
                <h4>#{idea['id']}. {idea['title_concept']}</h4>
                <p>Keyword: <code>{idea['target_keyword']}</code> • Urgency: <strong>{idea['gap_urgency']}</strong></p>
                <p><strong>Hook:</strong> <em>"{idea['hook']}"</em></p>
                <p><small style="color:#b0bec5;">Rationale: {idea['rationale']}</small></p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 8: METADATA & TITLE SCORER
# ==========================================
with tabs[7]:
    meta_mod = MetadataModule(config, db, quota)
    meta_res = meta_mod.run()
    st.subheader("🏷️ YouTube Metadata Generator & Title Scorer")
    st.markdown("#### 5 Scored Title Options (<70 characters)")
    for t in meta_res["title_options"]:
        st.markdown(f"- **{t['title']}** (Score: `{t['score']}/100`, Grade: `{t['grade']}`, Length: {t['char_count']} chars)")
    st.markdown("#### First 150 Characters Description Preview:")
    st.info(f"\"{meta_res['description']['first_150_chars']}\"")
    st.markdown("#### 15 Targeted Tags:")
    st.code(", ".join(meta_res["tags_15"]))

# ==========================================
# TAB 9: MONETIZATION & YPP ROADMAP
# ==========================================
with tabs[8]:
    mon_mod = MonetizationAccelerationModule(config, db, quota)
    mon_res = mon_mod.run()
    st.subheader("💼 YouTube Partner Program (YPP) Monetization Acceleration")
    curr = mon_res["current_status"]
    t1 = mon_res["tier_1_fan_funding_gap"]
    t2 = mon_res["tier_2_ad_revenue_gap"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Subscribers", f"{curr['subscribers']:,} / 1,000", f"{t2['subscribers_needed']} to Tier 2 (500 Met)")
    m2.metric("Watch Hours (365d)", f"{curr['public_watch_hours_365d']:,} / 3,000 hrs", f"{t1['watch_hours_needed']:,} hrs to Tier 1")
    m3.metric("Shorts View Hours (90d)", f"{curr['shorts_watch_hours_90d']:,} hrs", "Studio Verified")
    m4.metric("Uploads (90d)", f"{curr['public_uploads_90d']} / 3", "MET (Eligible)")

    st.markdown("#### 🗓️ 90-Day Step-by-Step Action Plan")
    for phase in mon_res["ninety_day_plan"]:
        st.markdown(f"""
        <div class="kpi-card">
            <h4>{phase['phase']}</h4>
            <p><strong>Target:</strong> {phase['target']} • <strong>Cadence:</strong> <code>{phase['cadence']}</code></p>
            <p><strong>Focus:</strong> {phase['content_focus']}</p>
            <p style="color:#81c784;"><strong>Outcome:</strong> {phase['milestone']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("🎬 Dual-Platform Social Media Manager Agent • Powered by YouTube Data API v3, YouTube Analytics API & Instagram Graph API")
