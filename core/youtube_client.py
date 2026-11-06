import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from core.config import Config
from core.quota import QuotaManager
from core.db import Database
from core.mocks import get_mock_database_seed

class YouTubeClient:
    def __init__(self, config: Config, db: Database, quota: QuotaManager):
        self.config = config
        self.db = db
        self.quota = quota
        self.api_key = config.youtube_api_key
        self.use_mock = config.use_mock_data or not bool(self.api_key)

    def initialize_data(self, force_refresh: bool = False):
        """Initializes database with mock data or fetches live data."""
        if self.use_mock:
            self._seed_mock_data(force=force_refresh)
        else:
            self._sync_live_data(force=force_refresh)

    def _fetch_public_subscriber_count(self, handle: str) -> int:
        """Attempts to parse public subscriber count from YouTube channel page if API key is absent."""
        try:
            import re
            clean_handle = handle if handle.startswith("@") else f"@{handle}"
            url = f"https://www.youtube.com/{clean_handle}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
            with urllib.request.urlopen(req, timeout=5) as res:
                html = res.read().decode("utf-8", errors="ignore")
                matches = re.findall(r"(\d+[\.\d]*[KkMm]?)\s+subscribers", html)
                if matches:
                    raw_val = matches[0].strip()
                    if "K" in raw_val.upper():
                        return int(float(raw_val.upper().replace("K", "")) * 1000)
                    elif "M" in raw_val.upper():
                        return int(float(raw_val.upper().replace("M", "")) * 1000000)
                    else:
                        return int(raw_val.replace(",", ""))
        except Exception:
            pass
        return None

    def _seed_mock_data(self, force: bool = False):
        subs = self._fetch_public_subscriber_count(self.config.my_channel_handle) or getattr(self.config, "my_channel_subscribers", 887)
        existing_my = self.db.get_my_channel()
        if existing_my and not force:
            if (existing_my.get("channel_id") == self.config.my_channel_id and
                existing_my.get("custom_url") == self.config.my_channel_handle and
                existing_my.get("subscriber_count") == subs):
                return

        print("[YouTubeClient] Initializing sample/mock dataset for channel, Instagram & competitors...")
        seed = get_mock_database_seed(self.config.my_channel_id, self.config.my_channel_handle, self.config.my_channel_title, subs)
        for ch in seed.get("channels", []):
            self.db.upsert_channel(ch)
        for vid in seed.get("videos", []):
            self.db.upsert_video(vid)
        for ig_post in seed.get("instagram_posts", []):
            self.db.upsert_instagram_post(ig_post)
        for ig_creator in seed.get("instagram_creators", []):
            self.db.upsert_instagram_creator(ig_creator)
        for curve in seed.get("youtube_retention_curves", []):
            self.db.upsert_retention_curve(curve)
        print(f"[YouTubeClient] Successfully loaded {len(seed.get('channels', []))} channels, {len(seed.get('videos', []))} videos, {len(seed.get('instagram_posts', []))} IG posts, and {len(seed.get('youtube_retention_curves', []))} retention curves into SQLite cache.")

    def _sync_live_data(self, force: bool = False):
        """Syncs my channel and competitors using YouTube Data API v3."""
        print("[YouTubeClient] Connecting to YouTube Data API v3...")
        # 1. Fetch My Channel
        my_id = self.config.my_channel_id
        if my_id:
            self._fetch_and_cache_channel(my_id, is_my_channel=True)
            self._fetch_channel_recent_videos(my_id, is_my_channel=True, days=90)

        # 2. Fetch Competitors
        for comp_id in self.config.competitor_channel_ids:
            if not self.quota.can_spend("channels.list"):
                print("[YouTubeClient] Quota limit reached; stopping live fetch.")
                break
            self._fetch_and_cache_channel(comp_id, is_my_channel=False)
            self._fetch_channel_recent_videos(comp_id, is_my_channel=False, days=90)

        # 3. Pull trending niche videos
        self._fetch_trending_niche_videos()

    def _api_get(self, endpoint: str, params: dict) -> dict:
        """Helper to call YouTube Data API v3 with quota tracking."""
        if not self.quota.can_spend(endpoint):
            raise RuntimeError(f"Cannot call {endpoint}: daily quota limit reached.")

        params["key"] = self.api_key
        url = f"https://www.googleapis.com/youtube/v3/{endpoint}?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "YouTubeManagerAgent/1.0"})

        with urllib.request.urlopen(req, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))
            self.quota.record_call(endpoint, details=f"Params: {list(params.keys())}")
            return data

    def _fetch_and_cache_channel(self, identifier: str, is_my_channel: bool = False):
        params = {"part": "snippet,statistics"}
        if identifier.startswith("@"):
            params["forHandle"] = identifier
        else:
            params["id"] = identifier

        try:
            res = self._api_get("channels.list", params)
            items = res.get("items", [])
            if not items:
                print(f"[YouTubeClient] Warning: Channel not found for {identifier}")
                return

            item = items[0]
            ch_data = {
                "channel_id": item["id"],
                "title": item["snippet"]["title"],
                "custom_url": item["snippet"].get("customUrl", identifier),
                "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
                "view_count": int(item["statistics"].get("viewCount", 0)),
                "video_count": int(item["statistics"].get("videoCount", 0)),
                "is_my_channel": is_my_channel
            }
            self.db.upsert_channel(ch_data)
        except Exception as e:
            print(f"[YouTubeClient] Error fetching channel {identifier}: {e}")

    def _fetch_channel_recent_videos(self, channel_id: str, is_my_channel: bool = False, days: int = 90):
        # 1. Get uploads playlist id
        try:
            ch_res = self._api_get("channels.list", {"part": "contentDetails", "id": channel_id})
            items = ch_res.get("items", [])
            if not items:
                return
            uploads_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

            # 2. List playlist items
            p_res = self._api_get("playlistItems.list", {
                "part": "snippet",
                "playlistId": uploads_id,
                "maxResults": 25
            })

            video_ids = []
            for item in p_res.get("items", []):
                pub_time = item["snippet"]["publishedAt"]
                pub_dt = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                if (datetime.now(timezone.utc) - pub_dt).days <= days:
                    video_ids.append(item["snippet"]["resourceId"]["videoId"])

            if not video_ids:
                return

            # 3. Get video statistics and details
            v_res = self._api_get("videos.list", {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(video_ids)
            })

            for v in v_res.get("items", []):
                stats = v.get("statistics", {})
                snip = v.get("snippet", {})
                dur_raw = v.get("contentDetails", {}).get("duration", "PT0S")

                # Parse ISO duration (approx)
                dur_sec = self._parse_iso_duration(dur_raw)

                vid_dict = {
                    "video_id": v["id"],
                    "channel_id": channel_id,
                    "title": snip.get("title", ""),
                    "description": snip.get("description", ""),
                    "tags": snip.get("tags", []),
                    "published_at": snip.get("publishedAt", ""),
                    "duration_sec": dur_sec,
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "is_my_channel": is_my_channel
                }
                self.db.upsert_video(vid_dict)

        except Exception as e:
            print(f"[YouTubeClient] Error fetching uploads for {channel_id}: {e}")

    def _fetch_trending_niche_videos(self):
        """Pulls trending videos for configured niche keywords."""
        published_after = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()
        for kw in self.config.niche_keywords[:3]:  # Limit calls to preserve quota
            if not self.quota.can_spend("search.list"):
                break
            try:
                res = self._api_get("search.list", {
                    "part": "snippet",
                    "q": kw,
                    "type": "video",
                    "order": "viewCount",
                    "publishedAfter": published_after,
                    "maxResults": 10
                })
                # Cache results in db
                now_str = datetime.now(timezone.utc).isoformat()
                with self.db._get_connection() as conn:
                    for item in res.get("items", []):
                        vid_id = item["id"].get("videoId")
                        if vid_id:
                            conn.execute("""
                                INSERT INTO trending_searches (keyword, video_id, title, channel_title, published_at, cached_at)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (kw, vid_id, item["snippet"]["title"], item["snippet"]["channelTitle"], item["snippet"]["publishedAt"], now_str))
                    conn.commit()
            except Exception as e:
                print(f"[YouTubeClient] Search error for '{kw}': {e}")

    @staticmethod
    def _parse_iso_duration(iso_str: str) -> int:
        """Parses ISO 8601 duration string (e.g. PT14M32S) to seconds."""
        import re
        m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_str)
        if not m:
            return 0
        h = int(m.group(1) or 0)
        minutes = int(m.group(2) or 0)
        s = int(m.group(3) or 0)
        return (h * 3600) + (minutes * 60) + s
