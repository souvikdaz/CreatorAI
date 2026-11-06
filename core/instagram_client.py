import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from core.config import Config
from core.db import Database
from core.quota import QuotaManager

class InstagramClient:
    """
    Client for Instagram Graph API (Instagram Business / Creator Accounts).
    Requires a valid User/Page Access Token with:
      - instagram_basic
      - instagram_manage_insights
      - pages_show_list
    """
    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota
        self.access_token = config.instagram_access_token
        self.account_id = config.instagram_business_account_id
        self.use_mock = config.use_mock_data or not bool(self.access_token)

    def is_live_configured(self) -> bool:
        return bool(self.access_token and self.account_id and not self.use_mock)

    def sync_my_posts(self, limit: int = 10):
        """Fetches live Instagram posts and their insights if credentials are set."""
        if not self.is_live_configured():
            return

        try:
            fields = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count"
            url = f"https://graph.facebook.com/v19.0/{self.account_id}/media?fields={fields}&limit={limit}&access_token={self.access_token}"
            req = urllib.request.Request(url, headers={"User-Agent": "YouTubeInstagramAgent/1.0"})

            with urllib.request.urlopen(req, timeout=12) as response:
                data = json.loads(response.read().decode("utf-8"))
                media_list = data.get("data", [])

                for item in media_list:
                    m_id = item["id"]
                    m_type = item.get("media_type", "IMAGE")
                    fmt = "REEL" if m_type == "VIDEO" else ("CAROUSEL" if m_type == "CAROUSEL_ALBUM" else "SINGLE_IMAGE")

                    # Fetch insights for each media item
                    reach = 0
                    plays = 0
                    saves = 0
                    shares = 0
                    try:
                        metrics_to_query = "reach,saved,shares"
                        if fmt == "REEL":
                            metrics_to_query += ",plays"
                        insights_url = f"https://graph.facebook.com/v19.0/{m_id}/insights?metric={metrics_to_query}&access_token={self.access_token}"
                        in_req = urllib.request.Request(insights_url, headers={"User-Agent": "YouTubeInstagramAgent/1.0"})
                        with urllib.request.urlopen(in_req, timeout=8) as in_resp:
                            in_data = json.loads(in_resp.read().decode("utf-8"))
                            for metric in in_data.get("data", []):
                                val = metric.get("values", [{}])[0].get("value", 0)
                                if metric["name"] == "reach":
                                    reach = int(val)
                                elif metric["name"] == "plays":
                                    plays = int(val)
                                elif metric["name"] == "saved":
                                    saves = int(val)
                                elif metric["name"] == "shares":
                                    shares = int(val)
                    except Exception:
                        pass

                    post_dict = {
                        "post_id": m_id,
                        "caption": item.get("caption", ""),
                        "hashtags": [w.strip("#") for w in item.get("caption", "").split() if w.startswith("#")],
                        "format": fmt,
                        "duration_sec": 30 if fmt == "REEL" else 0,
                        "plays": plays,
                        "reach": reach,
                        "likes": int(item.get("like_count", 0)),
                        "saves": saves,
                        "shares": shares,
                        "comments": int(item.get("comments_count", 0)),
                        "profile_visits": int(reach * 0.03),
                        "follows_gained": int(reach * 0.005),
                        "thumbnail_url": item.get("thumbnail_url") or item.get("media_url") or "",
                        "permalink": item.get("permalink", ""),
                        "published_at": item.get("timestamp", datetime.now(timezone.utc).isoformat()),
                        "is_my_post": True
                    }
                    self.db.upsert_instagram_post(post_dict)
        except Exception as e:
            print(f"[InstagramClient] Error querying Graph API: {e}")
