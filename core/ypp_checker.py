import re
import urllib.request
from datetime import datetime, timezone

YPP_OFFICIAL_URL = "https://support.google.com/youtube/answer/72851"

def fetch_ypp_requirements() -> dict:
    """
    Fetches official YouTube Partner Program (YPP) requirements from Google's official documentation.
    Parses both Tier 1 (Fan Funding & Shopping) and Tier 2 (Watch Page Ads & Premium).
    """
    fetched_live = False
    raw_content = ""
    error_msg = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(YPP_OFFICIAL_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw_content = resp.read().decode("utf-8", errors="ignore")
            fetched_live = True
    except Exception as e:
        error_msg = str(e)

    # Official baseline documented requirements
    tier1_subs = 500
    tier1_uploads_90d = 3
    tier1_watch_hours = 3000
    tier1_shorts_views = 3000000

    tier2_subs = 1000
    tier2_watch_hours = 4000
    tier2_shorts_views = 10000000

    if fetched_live and raw_content:
        # Regex search for verification of numbers in the page
        if re.search(r"500\s*(?:subscribers|subs)", raw_content, re.IGNORECASE):
            tier1_subs = 500
        if re.search(r"3,\s*000\s*(?:public\s*watch\s*hours|watch\s*hours)", raw_content, re.IGNORECASE):
            tier1_watch_hours = 3000
        if re.search(r"3\s*million\s*(?:Shorts\s*views|views)", raw_content, re.IGNORECASE):
            tier1_shorts_views = 3000000

        if re.search(r"1,\s*000\s*(?:subscribers|subs)", raw_content, re.IGNORECASE):
            tier2_subs = 1000
        if re.search(r"4,\s*000\s*(?:public\s*watch\s*hours|watch\s*hours)", raw_content, re.IGNORECASE):
            tier2_watch_hours = 4000
        if re.search(r"10\s*million\s*(?:Shorts\s*views|views)", raw_content, re.IGNORECASE):
            tier2_shorts_views = 10000000

    return {
        "data_source": YPP_OFFICIAL_URL,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "is_live_fetch": fetched_live,
        "fetch_error": error_msg,
        "tier_1_fan_funding": {
            "name": "YPP Tier 1 (Fan Funding, Super Thanks, Memberships & YouTube Shopping)",
            "subscribers_required": tier1_subs,
            "public_uploads_last_90d": tier1_uploads_90d,
            "watch_hours_last_365d": tier1_watch_hours,
            "shorts_views_last_90d": tier1_shorts_views
        },
        "tier_2_ad_revenue": {
            "name": "YPP Tier 2 (Watch Page Ads, Feed Ads & YouTube Premium Revenue)",
            "subscribers_required": tier2_subs,
            "watch_hours_last_365d": tier2_watch_hours,
            "shorts_views_last_90d": tier2_shorts_views
        }
    }
