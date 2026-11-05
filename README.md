# 🎬 YouTube Social Media Manager Agent

An intelligent, data-driven YouTube management and strategy agent built in Python. Powered by the **YouTube Data API v3** for public competitive intelligence and the **YouTube Analytics API (OAuth 2.0)** for private channel analytics, with local SQLite caching, strict quota accounting, and out-of-the-box mock testing.

---

## 📁 Project Architecture

```
youtube-manager-agent/
├── config.yaml                    # Channel ID, niche keywords, competitors, timezone, audience
├── .env.example                   # Template for API keys & OAuth credentials (never hardcoded)
├── .gitignore                     # Ignores credentials, SQLite databases, and local cache
├── requirements.txt               # Dependencies (google-api, pyyaml, requests, pytz, pytest)
├── run.py                         # Unified CLI entrypoint
│
├── core/
│   ├── config.py                  # YAML & .env loader with built-in zero-dependency fallbacks
│   ├── quota.py                   # Daily API quota tracker & SQLite unit logger (10k units/day)
│   ├── db.py                      # SQLite database caching layer (channels, videos, reports)
│   ├── ypp_checker.py             # Fetches official YPP documentation & parses current rules
│   ├── mocks.py                   # High-fidelity mock seed data for Motovlogging & Automotive
│   └── youtube_client.py          # Unified live YouTube Data API v3 client & mock fallback
│
├── modules/
│   ├── base.py                    # Base module interface (JSON + Markdown exporters, confidence)
│   ├── ideas.py                   # Module 1: Video Ideas (topic clustering & content gap analysis)
│   ├── metadata.py                # Module 2: Metadata generator & title scorer (<70 chars, 15 tags)
│   ├── timing.py                  # Module 3: Upload timing & velocity windows in local timezone (IST)
│   ├── competitors.py             # Module 4: Competitor insights (cadence, hooks, 3 adapted tactics)
│   ├── repurpose.py               # Module 5: Long-form to Short-form repurposing (15-60s clips)
│   ├── sponsors.py                # Module 6: Sponsorship & commercial monetization avenues
│   └── monetization.py            # Module 7: YPP monetization acceleration & 90-day action plan
│
├── reports/
│   ├── daily_digest.py            # Generates daily high-priority action digest
│   └── weekly_report.py           # Generates comprehensive weekly 7-module audit
│
├── tests/
│   ├── test_metadata_scoring.py   # Unit tests for title length, scoring rules, tag count
│   ├── test_repurpose_timestamps.py # Unit tests for 15-60s clip constraint & timestamp math
│   └── test_quota_and_db.py       # Unit tests for SQLite storage and quota tracking
│
├── data/
│   └── youtube_agent.db           # SQLite database (auto-created on first run)
└── output/                        # Exported JSON artifacts and Markdown reports
```

---

## ⚡ Quick Start (Works Out-of-the-Box with Mocks)

You can run the full suite immediately **without any API keys or network credentials** using the included mock engine:

```bash
cd /Users/sdazz/youtube-manager-agent

# Run all 7 modules + generate daily digest + weekly report
python3 run.py --module all --daily-digest --weekly-report --mock
```

All reports and JSON files will be exported to the `output/` directory.

---

## 🔑 Setup & Live API Configuration

### 1. Configure `config.yaml`
Edit `config.yaml` to set your channel ID, niche keywords, competitors, and timezone:
```yaml
my_channel_id: "UCu2EoFcaIV7rqAXvG9rcUiQ"
niche_keywords:
  - "motovlog"
  - "motorcycle touring"
  - "automotive"
  - "technology"
  - "gadgets"
  - "bike trips"

competitor_channel_ids:
  - "https://www.youtube.com/@SwatiRojha"
  - "https://www.youtube.com/@deepranjansachan"
  - "https://www.youtube.com/@DeepteshLovesTECH"
  - "https://www.youtube.com/@dReamwAlk"
  - "https://www.youtube.com/@throttleyourlife"

timezone: "Asia/Kolkata" # Indian Standard Time (IST)
audience_country: "Global"
```

### 2. Configure Environment Secrets (`.env`)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your credentials:
```ini
YOUTUBE_API_KEY=AIzaSy...your_actual_key_here
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
YOUTUBE_OAUTH_TOKEN_FILE=token.json
USE_MOCK_DATA=false
```

---

## 🔐 Google Cloud Console & OAuth 2.0 Steps

### Step A: Enable APIs & Create API Key (Public Data)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `YouTube-Manager-Agent`).
3. Navigate to **APIs & Services > Library**.
4. Search for and **Enable** both:
   - **YouTube Data API v3**
   - **YouTube Analytics API**
5. Go to **APIs & Services > Credentials** > **Create Credentials** > **API Key**.
6. Copy the API key and paste it as `YOUTUBE_API_KEY` in your `.env`.

### Step B: Configure OAuth 2.0 (Private Channel Analytics)
1. In **APIs & Services > OAuth consent screen**:
   - Choose **External** user type.
   - Enter your App name and developer email.
   - In Scopes, add:
     - `https://www.googleapis.com/auth/yt-analytics.readonly`
     - `https://www.googleapis.com/auth/youtube.readonly`
   - Add your Google account email under **Test Users**.
2. In **APIs & Services > Credentials** > **Create Credentials** > **OAuth client ID**:
   - Application type: **Desktop app**.
   - Name: `YouTube Agent Desktop Client`.
3. Click **Download JSON** and save the file as `client_secrets.json` in the project root directory.

---

## 📊 YouTube Data API Quota Accounting

The YouTube Data API v3 provides a default free tier quota of **10,000 units per calendar day** (resetting at midnight Pacific Time / 1:30 PM IST).

The agent's built-in `core/quota.py` monitors and enforces this budget:
| API Endpoint | Unit Cost | Agent Usage & Optimization |
| :--- | :--- | :--- |
| `search.list` | **100 units** | Restricted to top niche keywords with 24h caching. |
| `videos.list` | **1 unit** | Batch-fetches up to 50 videos in a single 1-unit request. |
| `channels.list` | **1 unit** | Fetches channel profile & upload playlists. |
| `playlistItems.list`| **1 unit** | Pulls recent upload IDs without expensive searches. |
| `analytics.reports` | **0 units** | Uses requests-per-minute quota (separate from Data units). |

The agent warns when daily usage exceeds 80% and halts queries before hitting 100%.

---

## 💻 CLI Commands

### Run All Modules & Reports
```bash
python3 run.py --module all --daily-digest --weekly-report
```

### Run an Individual Module
```bash
# Module 1: Video Ideas & Content Gap Analysis
python3 run.py --module ideas

# Module 2: Metadata Optimization for Upcoming Script
python3 run.py --module metadata --script "Complete Ladakh Bike Trip Packing Guide"

# Module 3: Upload Timing Windows (IST)
python3 run.py --module timing

# Module 4: Competitor Intelligence & Tactics
python3 run.py --module competitors

# Module 5: Long-Form to Short-Form Repurposing
python3 run.py --module repurpose

# Module 6: Sponsorship & Revenue Opportunities
python3 run.py --module sponsors

# Module 7: YouTube Partner Program (YPP) Monetization Acceleration
python3 run.py --module monetization
```

### Generate Daily Action Digest Only
```bash
python3 run.py --daily-digest
```

---

## 🧪 Running Unit Tests

Unit tests verify title scoring algorithms, character truncation limits, tag counts, timestamp calculations, and SQLite quota tracking:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📜 Ethical Constraints & Data Integrity
1. **Never fabricate metrics**: Missing analytics trigger explicit data gaps rather than synthetic placeholders.
2. **Never copy competitor assets**: Recommendations adapt high-performing structural patterns (e.g. hook pacing, question framing), never titles or scripts.
3. **No misleading engagement claims**: Subscriber projections rely strictly on your channel's verified conversion rate per 1,000 views.
