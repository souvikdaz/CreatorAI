import os
import sys
import json
import streamlit as st
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from core.youtube_client import YouTubeClient
from modules.ideas import VideoIdeasModule
from modules.metadata import MetadataModule
from modules.timing import TimingModule
from modules.competitors import CompetitorInsightsModule
from modules.repurpose import RepurposeModule
from modules.sponsors import SponsorshipModule
from modules.monetization import MonetizationAccelerationModule
from reports.daily_digest import DailyDigestGenerator
from reports.weekly_report import WeeklyReportGenerator

# Page setup
st.set_page_config(
    page_title="YouTube Creator AI Agent",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (YouTube Creator Aesthetic)
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 16px;
        border-left: 4px solid #ff0000;
        margin-bottom: 12px;
    }
    .badge-high {
        background-color: #1b5e20;
        color: #a5d6a7;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: #f57f17;
        color: #fff9c4;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-red {
        background-color: #b71c1c;
        color: #ffcdd2;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .clip-box {
        background-color: #181818;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# 1. Initialize Core Singletons
@st.cache_resource
def get_core_services():
    config = Config()
    db = Database(config.sqlite_db_path)
    quota = QuotaManager(config.sqlite_db_path, daily_limit=config.quota_daily_limit)
    client = YouTubeClient(config, db, quota)
    client.initialize_data(force_refresh=False)
    return config, db, quota, client

config, db, quota, client = get_core_services()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎬 YouTube Studio Agent")
    st.caption("AI Social Media Manager & Growth Copilot")

    my_ch = db.get_my_channel() or {
        "title": "MotoTech Explorer",
        "custom_url": "@MotoTechExplorer",
        "subscriber_count": 420,
        "view_count": 82400,
        "video_count": 18
    }

    st.markdown("---")
    st.subheader(f"📺 {my_ch['title']}")
    st.caption(f"Handle: `{my_ch.get('custom_url', '@MotoTechExplorer')}`")
    st.caption(f"Channel ID: `{config.my_channel_id}`")

    c1, c2 = st.columns(2)
    c1.metric("Subscribers", f"{my_ch['subscriber_count']:,}")
    c2.metric("Total Views", f"{my_ch['view_count']:,}")

    st.markdown("---")
    st.subheader("⚙️ Mode & Settings")
    mode_selection = st.radio(
        "Data Engine Mode",
        ["Sample / Mock Dataset", "Live YouTube Data API v3"],
        index=0 if (config.use_mock_data or not config.youtube_api_key) else 1,
        help="Use mock mode to test with zero quota usage, or connect your API key in .env"
    )
    config.use_mock_data = (mode_selection == "Sample / Mock Dataset")

    st.caption(f"Timezone: **{config.timezone}**")
    st.caption(f"Audience: **{config.audience_country}**")

    st.markdown("---")
    st.subheader("📊 API Quota Monitor")
    quota_info = quota.get_summary()
    st.progress(quota_info["percent_used"] / 100.0)
    st.caption(f"{quota_info['units_used_today']:,} / {quota_info['daily_limit']:,} units used ({quota_info['percent_used']}%)")
    st.caption(f"Remaining units: **{quota_info['units_remaining']:,}**")

    st.markdown("---")
    if st.button("🔄 Sync & Refresh Data", use_container_width=True):
        client.initialize_data(force_refresh=True)
        st.success("Refreshed SQLite cache successfully!")
        st.rerun()

# --- HEADER STATUS BAR ---
head_col1, head_col2, head_col3 = st.columns([3, 2, 2])
with head_col1:
    st.title("YouTube Manager Agent")
    st.caption(f"Niche: {', '.join(config.niche_keywords[:4])} • Timezone: {config.timezone}")
with head_col2:
    st.metric("Monitored Competitors", f"{len(config.competitor_channel_ids)} Channels")
with head_col3:
    st.metric("YPP Tier 1 Gap", f"{max(0, 500 - my_ch['subscriber_count'])} Subs Remaining")

st.markdown("---")

# --- MAIN TABS ---
tab_digest, tab_ideas, tab_metadata, tab_timing, tab_competitors, tab_repurpose, tab_monetization = st.tabs([
    "📅 Daily Digest",
    "💡 Video Ideas & Gaps",
    "🏷️ Metadata & Title Scorer",
    "⏰ Upload Timing (IST)",
    "🔍 Competitor Intelligence",
    "✂️ Shorts Repurposing",
    "💼 Monetization & YPP"
])

# ==========================================
# TAB 1: DAILY DIGEST
# ==========================================
with tab_digest:
    st.subheader("📅 Today's High-Priority Action Digest")
    digest_gen = DailyDigestGenerator(config, db, quota)
    
    ideas_m = VideoIdeasModule(config, db, quota).run()
    timing_m = TimingModule(config, db, quota).run()
    repurpose_m = RepurposeModule(config, db, quota).run()
    sponsors_m = SponsorshipModule(config, db, quota).run()

    top_idea = ideas_m["ideas"][0]
    top_slot = timing_m["top_3_recommended_slots"][0]
    top_clip = repurpose_m["repurposed_clips"][0]
    top_sponsor = sponsors_m["monetization_avenues"][1]

    d1, d2 = st.columns(2)

    with d1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>🎬 1. Production Priority: Script Top Gap Idea</h4>
            <h5 style="color: #64b5f6; margin-top: 4px;">{top_idea['title_concept']}</h5>
            <p><strong>Target Keyword:</strong> <code>{top_idea['target_keyword']}</code></p>
            <p><strong>Hook Line:</strong> <em>"{top_idea['hook']}"</em></p>
            <p><small style="color: #9e9e9e;">Rationale: {top_idea['rationale']}</small></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <h4>✂️ 3. Short-Form Priority: Cut & Post 1 Short</h4>
            <h5 style="color: #81c784; margin-top: 4px;">{top_clip['shorts_title']}</h5>
            <p><strong>Timestamps:</strong> <code>{top_clip['timestamp_range']}</code> (Duration: {top_clip['duration_sec']}s)</p>
            <p><strong>Visual Hook (0-3s):</strong> <em>"{top_clip['hook_line']}"</em></p>
            <p><small style="color: #9e9e9e;">{top_clip['caption']}</small></p>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>⏰ 2. Distribution: Peak Upload Window</h4>
            <h5 style="color: #ffb74d; margin-top: 4px;">{top_slot['day']} at {top_slot['time_display']}</h5>
            <p><strong>Niche Velocity Benchmark:</strong> {top_slot['median_velocity']:,} views/day</p>
            <p><strong>Execution Rule:</strong> Upload unlisted 90 minutes before to allow 4K rendering & closed captions.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <h4>💰 4. Commercial Priority: Monetization Action</h4>
            <h5 style="color: #ba68c8; margin-top: 4px;">{top_sponsor['avenue']}</h5>
            <p><strong>Action Item:</strong> {top_sponsor['next_action']}</p>
            <p><small style="color: #9e9e9e;">{top_sponsor['realistic_financial_model']}</small></p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📄 View & Copy Raw Daily Digest Markdown", expanded=False):
        raw_digest_text = digest_gen.generate()
        st.text_area("Markdown Output", raw_digest_text, height=220)

# ==========================================
# TAB 2: VIDEO IDEAS & CONTENT GAPS
# ==========================================
with tab_ideas:
    st.subheader("💡 Topic Cluster Gap Analysis & 10 Data-Backed Video Ideas")
    ideas_mod = VideoIdeasModule(config, db, quota)
    ideas_data = ideas_mod.run()

    st.markdown(f"**Data Source:** `{ideas_data['data_source']}` • **Confidence Level:** `{ideas_data['confidence']}`")

    st.markdown("#### 📊 Topic Cluster Competitor Demand vs Channel Coverage")
    gap_rows = []
    for c in ideas_data.get("cluster_gap_analysis", []):
        gap_rows.append({
            "Topic Cluster": c["cluster"],
            "Competitor Uploads": c["competitor_video_count"],
            "Comp Avg Velocity (views/day)": f"{c['avg_view_velocity']:,}",
            "My Coverage": f"{c['my_coverage_count']} videos",
            "Gap Priority Score": c["gap_score"]
        })
    st.dataframe(gap_rows, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🎯 10 Structured Video Ideas")
    for idea in ideas_data.get("ideas", []):
        urgency_class = "badge-high" if idea["gap_urgency"] == "HIGH" else "badge-medium"
        with st.container():
            st.markdown(f"""
            <div class="metric-card">
                <h4>#{idea['id']}. {idea['title_concept']}</h4>
                <p>
                    <span class="{urgency_class}">Urgency: {idea['gap_urgency']}</span> • 
                    Cluster: <strong>{idea['cluster']}</strong> • 
                    Format: <em>{idea['suggested_format']}</em>
                </p>
                <p><strong>Target Keyword:</strong> <code>{idea['target_keyword']}</code></p>
                <p><strong>Hook Opener (First 5s):</strong> <em>"{idea['hook']}"</em></p>
                <p style="color: #b0bec5;"><small><strong>Data-Backed Rationale:</strong> {idea['rationale']}</small></p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: METADATA & TITLE SCORER
# ==========================================
with tab_metadata:
    st.subheader("🏷️ Interactive Metadata Generator & Title Scorer")
    st.markdown("Test any upcoming video script or topic. Enforces `<70` characters, front-loaded keywords, and strict clickbait penalties.")

    col_input, col_results = st.columns([1.2, 1.8])

    with col_input:
        st.markdown("#### ✍️ Input Topic or Draft Script")
        user_topic = st.text_area(
            "Topic / Script Summary",
            value="Solo motorcycle touring packing list, luggage choices, action camera mounts, and fuel management on Himalayan 450",
            height=130
        )
        custom_kw = st.text_input("Primary Target Keyword", value="motorcycle touring packing list")
        generate_btn = st.button("🚀 Score & Optimize Metadata", use_container_width=True, type="primary")

    meta_mod = MetadataModule(config, db, quota)
    meta_data = meta_mod.run(draft_topic_or_script=user_topic)

    with col_results:
        st.markdown("#### 🏆 5 Algorithmic Title Options (Ranked by Score)")
        for i, t in enumerate(meta_data["title_options"], 1):
            badge = "badge-high" if t["score"] >= 80 else ("badge-medium" if t["score"] >= 70 else "badge-red")
            st.markdown(f"""
            <div style="background-color: #1a1a1a; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #ff0000;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="font-size: 1.05rem;">#{i}. {t['title']}</strong>
                    <span class="{badge}">{t['score']}/100 ({t['grade']})</span>
                </div>
                <small style="color: #9e9e9e;">Length: {t['char_count']} chars (Limit: 70) • Signals: {', '.join(t['breakdown'][:2])}</small>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📝 Description Preview (First 150 Characters Front-Loaded)")
        st.info(f"\"{meta_data['description']['first_150_chars']}\"")
        with st.expander("Show Complete Description Template", expanded=False):
            st.text_area("Full Description Text", meta_data["description"]["full_text"], height=180)

        st.markdown("#### 🏷️ 15 Targeted Tags (Tiered: Broad, Specific, Long-Tail)")
        st.code(", ".join(meta_data["tags_15"]), language="text")

# ==========================================
# TAB 4: UPLOAD TIMING (IST)
# ==========================================
with tab_timing:
    st.subheader("⏰ Upload Timing Windows & Audience Velocity (IST)")
    timing_mod = TimingModule(config, db, quota)
    timing_data = timing_mod.run()

    st.markdown(f"**Target Timezone:** `{timing_data['timezone']}` • **Audience:** `{timing_data['audience_country']}`")

    st.markdown("#### 🏆 Top 3 Recommended Slots")
    tcols = st.columns(3)
    for idx, slot in enumerate(timing_data["top_3_recommended_slots"]):
        with tcols[idx]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Rank #{idx+1}</h3>
                <h4>{slot['day']}</h4>
                <h5 style="color: #ff9800;">{slot['time_display']}</h5>
                <p>Niche Velocity: <strong>{slot['median_velocity']:,} views/day</strong></p>
                <small style="color: #9e9e9e;">Based on {slot['sample_count']} competitor uploads</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🚩 Channel vs Niche Contradiction Analysis")
    if timing_data["contradiction_flag"]:
        st.warning(f"⚠️ {timing_data['contradiction_notes']}")
    else:
        st.success(f"✅ {timing_data['contradiction_notes']}")

    st.markdown("#### 📌 Practical Distribution Rules")
    for rule in timing_data["actionable_rules"]:
        st.markdown(f"- {rule}")

# ==========================================
# TAB 5: COMPETITOR INTELLIGENCE
# ==========================================
with tab_competitors:
    st.subheader("🔍 Competitor Intelligence & Pattern Synthesis (Top 5)")
    comp_mod = CompetitorInsightsModule(config, db, quota)
    comp_data = comp_mod.run()

    st.markdown(f"**Data Source:** `{comp_data['data_source']}` • **Confidence Level:** `{comp_data['confidence']}`")

    for c in comp_data.get("top_5_competitors", []):
        with st.expander(f"🏍️ {c['title']} ({c.get('custom_url', '')}) — {c['avg_view_velocity']:,} views/day velocity", expanded=True):
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Subscribers", f"{c['subscriber_count']:,}")
            col_m2.metric("90d Velocity", f"{c['avg_view_velocity']:,} v/d")
            col_m3.metric("Upload Cadence", f"{c['days_between_uploads']} days")
            col_m4.metric("Avg Video Length", c["avg_length_formatted"])

            st.markdown(f"- **Thumbnail Style (Describe, don't copy):** {c['thumbnail_style']}")
            st.markdown(f"- **Title Patterns:** {c['title_patterns']}")
            st.markdown(f"- **First 30 Seconds Hook Structure:** {c['hook_structure_30s']}")
            st.markdown(f"- **Core Formats:** {c['recurring_formats']}")

    st.markdown("---")
    st.markdown("### 🚀 3 Data-Backed Tactics to Adapt (Not Copy)")
    for i, t in enumerate(comp_data.get("tactics_to_adapt", []), 1):
        st.markdown(f"""
        <div class="metric-card">
            <h4>#{i}: {t['tactic']}</h4>
            <p><strong>Why It Works:</strong> {t['why_it_works']}</p>
            <p style="color: #81c784;"><strong>How to Adapt on Your Channel:</strong> {t['how_to_adapt']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 6: SHORTS REPURPOSING
# ==========================================
with tab_repurpose:
    st.subheader("✂️ Long-Form to Short-Form Repurposing Engine (15-60s)")
    repurpose_mod = RepurposeModule(config, db, quota)
    repurpose_data = repurpose_mod.run()

    st.caption(f"Source Long-Form: **{repurpose_data['source_video_title']}**")

    for clip in repurpose_data.get("repurposed_clips", []):
        st.markdown(f"""
        <div class="clip-box">
            <div style="display: flex; justify-content: space-between; align-items:center;">
                <h4 style="margin:0;">Clip #{clip['id']}: {clip['shorts_title']}</h4>
                <span class="badge-high">⏱️ {clip['duration_sec']} Seconds ({clip['timestamp_range']})</span>
            </div>
            <p style="margin-top: 6px;">Theme: <strong>{clip['theme']}</strong></p>
            <p><strong>Visual On-Screen Hook (First 3s):</strong> <em style="color: #ffcc80;">"{clip['hook_line']}"</em></p>
            <p><strong>Caption & Hashtags:</strong><br/><code>{clip['caption']}</code></p>
            <p style="color: #90caf9;"><small><strong>Vertical Crop Blueprint (9:16):</strong> {clip['vertical_crop_notes']}</small></p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 7: MONETIZATION & YPP
# ==========================================
with tab_monetization:
    st.subheader("💼 Commercial Monetization & YPP Acceleration Roadmap")
    sponsors_mod = SponsorshipModule(config, db, quota)
    sponsors_data = sponsors_mod.run()

    ypp_mod = MonetizationAccelerationModule(config, db, quota)
    ypp_data = ypp_mod.run()

    # YPP Progress Bar
    curr = ypp_data["current_status"]
    t1_gap = ypp_data["tier_1_fan_funding_gap"]
    t2_gap = ypp_data["tier_2_ad_revenue_gap"]

    st.markdown("#### 🎯 Official YouTube Partner Program (YPP) Status")
    st.caption(f"Official Source: `{ypp_data['data_source']}` ({ypp_data['official_ypp_source_status']})")

    yp1, yp2, yp3 = st.columns(3)
    yp1.metric("Subscribers", f"{curr['subscribers']:,} / 500", f"{t1_gap['subscribers_needed']} to Tier 1")
    yp2.metric("Watch Hours (365d)", f"{curr['estimated_watch_hours_365d']:,} / 3,000 hrs", f"{t1_gap['watch_hours_needed']:,} hrs to Tier 1")
    yp3.metric("Uploads (90d)", f"{curr['public_uploads_90d']} / 3", "MET (Eligible)")

    st.markdown("---")
    st.markdown("#### ⚡ Fastest Growth Levers for Your Channel")
    levers = ypp_data["fastest_levers"]
    st.markdown(f"- **Top Sub-Conversion Content:** {levers['highest_converting_format']}")
    st.markdown(f"- **Top Watch-Time Producer:** {levers['highest_watchtime_format']}")
    st.markdown(f"- **Optimal Cadence:** `{levers['optimal_cadence']}`")
    st.markdown(f"- **Projected Tier 1 Unlock:** ~`{levers['projected_t1_unlock_days']} days` under recommended cadence")

    st.markdown("---")
    st.markdown("#### 🛣️ 5 Realistic Commercial Revenue Avenues (Current Channel Size)")
    for av in sponsors_data.get("monetization_avenues", []):
        with st.expander(f"{av['avenue']} — ({av['current_viability']})", expanded=False):
            st.markdown(f"- **Target Brands / Partners:** {', '.join(av.get('target_brands', av.get('target_programs', av.get('target_products', []))))}")
            st.markdown(f"- **Audience Fit:** {av['audience_fit']}")
            st.markdown(f"- **Financial Outlook:** {av['realistic_financial_model']}")
            st.markdown(f"- **Immediate Next Action:** {av['next_action']}")

    st.markdown("---")
    st.markdown("#### 🗓️ 90-Day Execution Plan")
    for phase in ypp_data.get("ninety_day_plan", []):
        st.markdown(f"""
        <div class="metric-card">
            <h4>{phase['phase']}</h4>
            <p><strong>Milestone Target:</strong> {phase['target']}</p>
            <p><strong>Cadence:</strong> <code>{phase['cadence']}</code></p>
            <p><strong>Content Focus:</strong> {phase['content_focus']}</p>
            <p style="color: #a5d6a7;"><strong>Target Outcome:</strong> {phase['milestone']}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🎬 YouTube Creator AI Agent • Powered by YouTube Data API v3 & YouTube Analytics API (OAuth 2.0) • Developed for @MotoTechExplorer")
