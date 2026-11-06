# 🎬 Dual-Platform Social Media Manager Agent (YouTube & Instagram)

An intelligent, data-driven social media management and production agent built in Python. **YouTube** serves as the primary engine for deep search data, long-form ideas, and watch-time analytics, while **Instagram** operates as a secondary, mandatory high-velocity distribution channel for Reels, carousels, and community growth.

---

## 🎒 Gear & Hardware Governance (`config/gear.yaml`)

The agent is strictly governed by `config/gear.yaml` as the **only authorized source** for hardware and software recommendations. The agent will **never** suggest unlisted cameras (no Insta360, GoPro, etc.), unlisted bikes, or unlisted software:

```yaml
bike: Himalayan 450
action_camera: DJI Osmo Action 3
phone: Motorola Edge 40 Neo
microphones:
  - Generic wired microphone
  - Grenaro wireless microphone
computer: Apple Mac Mini M4
video_editing_fx: Final Cut Pro
image_editing: Canva (Free tier)
other: []
```

### Specific Device Roles & Constraints
1. **Himalayan 450:** Ride and travel content only. No other bikes are ever suggested.
2. **DJI Osmo Action 3:** Primary motovlog footage, rides, and outdoor B-roll.
3. **Motorola Edge 40 Neo:** Quick-capture vertical Reels. *Specs (resolution, frame rate, stabilization) are not assumed—user must confirm them in `gear.yaml`.*
4. **Microphones:** Generic wired mic for stationary/fixed setups; **Grenaro wireless microphone** flagged and required for all moving shots.
5. **Apple Mac Mini M4 with Final Cut Pro:** All video editing, audio mixing, color, and export.
6. **Canva (Free tier):** Covers, carousels, and thumbnails. *Never assumes Pro features (Brand Kit, Magic Resize, 1-click background remover).*
7. **"Needs gear (optional)":** Any creative idea requiring missing gear (drones, 360 cams) is strictly quarantined from the main production plan.

---

## 📁 Project Architecture

```
youtube-manager-agent/
├── config/
│   └── gear.yaml                  # Single source of truth for all hardware & software
├── config.yaml                    # Dual-platform identities, competitors, timezone, quota
├── .env.example                   # Template for YouTube & Instagram Graph API secrets
├── .gitignore                     # Ignores secrets, SQLite databases, and output cache
├── requirements.txt               # Dependencies
├── run.py                         # Dual-platform CLI entrypoint
├── run_app.sh                     # Streamlit Web App launch script
├── app.py                         # Visual-First Streamlit Dashboard
│
├── core/
│   ├── config.py                  # YAML & .env loader with built-in zero-dependency fallbacks
│   ├── gear_manager.py            # Strict gear governance, brand validator & phone notice
│   ├── quota.py                   # Daily API quota accounting & SQLite logging (10k units/day)
│   ├── db.py                      # Shared SQLite database (YouTube + Instagram tables)
│   ├── mocks.py                   # Mock dataset (Himalayan 450, Osmo Action 3, Instagram reels)
│   ├── youtube_client.py          # YouTube Data API v3 live client with mock fallback
│   ├── instagram_client.py        # Instagram Graph API client with mock fallback
│   └── ypp_checker.py             # Fetches official Google YPP support page & parses requirements
│
├── modules/
│   ├── base.py                    # Base module interface (JSON + Markdown exporters, confidence)
│   ├── audit.py                   # Instagram Module 1: Content Quality Audit (last 5 posts)
│   ├── ctr.py                     # Instagram/YT Module 2: CTR & Retention Drop-Off Critique
│   ├── growth.py                  # Instagram Module 3: Follower Growth Plan & 30-Day Cadence
│   ├── benchmark.py               # Instagram Module 4: Niche Benchmark (10-20 competitor accounts)
│   ├── shoot.py                   # Cross-Platform Module 5: Gear-Aware Shoot Planner
│   ├── dashboard.py               # Visual-First Dashboard Data Aggregator & Gallery
│   ├── ideas.py                   # YouTube Module 1: Video Ideas & Content Gap Analysis
│   ├── metadata.py                # YouTube Module 2: Metadata generator & Title Scorer (<70 chars)
│   ├── timing.py                  # YouTube Module 3: Upload Timing & Velocity Windows in IST
│   ├── competitors.py             # YouTube Module 4: Competitor Intelligence & Pattern Synthesis
│   ├── repurpose.py               # YouTube Module 5: Long-Form to Short-Form Repurposing
│   ├── sponsors.py                # YouTube Module 6: Sponsorship & Commercial Monetization
│   └── monetization.py            # YouTube Module 7: YPP Monetization Acceleration & 90-Day Plan
│
├── reports/
│   ├── daily_digest.py            # Generates daily dual-platform action digest
│   └── weekly_report.py           # Generates comprehensive dual-platform weekly report
│
├── tests/
│   ├── test_follower_delta.py     # Unit test: Instagram follower delta calculations
│   ├── test_ctr_critique.py       # Unit test: CTR vs niche median & drop-off mapping
│   ├── test_gear_filter.py        # Unit test: Gear filter (0 unlisted items permitted)
│   ├── test_bike_filter.py        # Unit test: Bike filter (Himalayan 450 strictly enforced)
│   ├── test_metadata_scoring.py   # Unit test: Title length <70, clickbait penalty, 15 tags
│   ├── test_quota_and_db.py       # Unit test: SQLite storage and quota tracking
│   └── test_repurpose_timestamps.py # Unit test: 15-60s clip duration constraints
│
├── data/
│   └── youtube_agent.db           # SQLite database
└── output/                        # Exported JSON artifacts and Markdown reports
```

---

## ⚡ Quick Start (Instant Mock Run)

The agent runs out-of-the-box with **zero API keys** using high-fidelity mock data for both YouTube and Instagram:

```bash
cd /Users/sdazz/youtube-manager-agent

# Run all modules for both platforms and generate weekly audit report
python3 run.py --platform both --module all --report weekly --mock
```

---

## 🌐 Visual-First Streamlit Web Dashboard

Launch the interactive web dashboard:
```bash
cd /Users/sdazz/youtube-manager-agent
./run_app.sh
```
Or with direct streamlit binary:
```bash
/Users/sdazz/nifty-swing-assistant/venv/bin/streamlit run app.py --server.port 8502
```
Open in your browser: **`http://localhost:8502`**

### Visual Dashboard Features
- **4 Top KPI Cards:** Total Audience, Follower Delta 30d, Average Reel Plays, Average YouTube CTR.
- **Interactive Plotly Visualizations:**
  1. Follower Growth Line (30/90 days).
  2. Reels Plays vs. Saves Scatter Plot (colored by format).
  3. Best Posting Hours Heatmap (Day × Hour in IST).
  4. YouTube Retention Curves for last 5 uploads with vertical drop-off markers.
  5. CTR Bar Chart for last 5 uploads vs Niche Median (10.4%).
- **Thumbnail Gallery:** Last 5 YouTube thumbnails & Last 6 Instagram posts with critique scores and Canva Free / Final Cut Pro fixes.
- **Mobile-Responsive:** Dark and Light theme adaptive layout.

---

## 💻 CLI Usage Guide

```bash
# Run specific Instagram modules
python3 run.py --module audit --mock
python3 run.py --module ctr --mock
python3 run.py --module growth --mock
python3 run.py --module benchmark --mock
python3 run.py --module shoot --mock
python3 run.py --module dashboard --mock

# Filter by platform
python3 run.py --platform instagram --report weekly --mock
python3 run.py --platform youtube --daily-digest --mock
python3 run.py --platform both --module all --mock

# Metadata optimization with custom script
python3 run.py --module metadata --script "Monsoon Riding Hacks on Himalayan 450" --mock
```

---

## 🔑 Live API Setup (Instagram Graph API & YouTube)

### Step 1: Instagram Graph API Setup
1. Convert your Instagram account to a **Professional Creator or Business Account**.
2. Link your Instagram account to a **Facebook Page**.
3. Go to [Meta for Developers](https://developers.facebook.com/) and create an App (Type: **Business**).
4. In App Dashboard, add **Instagram Graph API**.
5. Generate an Access Token with these 3 mandatory permissions:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `pages_show_list`
6. Exchange short-lived token for a **60-day Long-Lived Token** via:
   ```text
   GET https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}
   ```
7. Find your `instagram_business_account_id` via:
   ```text
   GET https://graph.facebook.com/v19.0/me/accounts?access_token={token}
   GET https://graph.facebook.com/v19.0/{page-id}?fields=instagram_business_account&access_token={token}
   ```
8. Save credentials in `.env`:
   ```ini
   INSTAGRAM_ACCESS_TOKEN=your_token_here
   INSTAGRAM_BUSINESS_ACCOUNT_ID=17841400000000000
   ```

### Step 2: Rate Limits & Quotas
- **YouTube Data API v3:** 10,000 units/day. Monitored strictly in SQLite `quota_logs`.
- **Instagram Graph API:** 200 API calls per hour per user account. The agent caches insights in SQLite for 24 hours to stay well within limits.

---

## 🧪 Unit Testing

Run the complete 23-test unit suite:
```bash
cd /Users/sdazz/youtube-manager-agent
python3 -m unittest discover -s tests -p "test_*.py"
```
```
.......................
----------------------------------------------------------------------
Ran 23 tests in 0.016s

OK
```
Tests explicitly verify:
- **Follower delta** calculation per post and format.
- **CTR vs. niche median** calculation and drop-off mapping.
- **Gear filter:** strictly rejects any unauthorized cameras, drones, or editors.
- **Bike filter:** strictly enforces Himalayan 450 for ride content.
- **Metadata scoring:** enforces title length `<70` chars, keyword front-loading, and clickbait penalties.
- **Repurposing timestamps:** guarantees clips are between 15 and 60 seconds.
