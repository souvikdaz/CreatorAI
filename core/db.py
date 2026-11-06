import sqlite3
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        if db_path == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:")
            self._mem_conn.row_factory = sqlite3.Row
        else:
            self._mem_conn = None
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        if self._mem_conn:
            return self._mem_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            # Channels table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    custom_url TEXT,
                    subscriber_count INTEGER DEFAULT 0,
                    view_count INTEGER DEFAULT 0,
                    video_count INTEGER DEFAULT 0,
                    is_my_channel INTEGER DEFAULT 0,
                    updated_at TEXT NOT NULL
                )
            """)

            # Videos table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    video_id TEXT PRIMARY KEY,
                    channel_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    tags_json TEXT,
                    published_at TEXT NOT NULL,
                    duration_sec INTEGER DEFAULT 0,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    ctr REAL DEFAULT 0.0,
                    avg_view_duration_sec REAL DEFAULT 0.0,
                    retention_pct REAL DEFAULT 0.0,
                    traffic_sources_json TEXT,
                    sub_change INTEGER DEFAULT 0,
                    view_velocity REAL DEFAULT 0.0,
                    is_my_channel INTEGER DEFAULT 0,
                    transcript_json TEXT,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(channel_id) REFERENCES channels(channel_id)
                )
            """)

            # Trending searches table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trending_searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    video_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    channel_title TEXT,
                    published_at TEXT NOT NULL,
                    view_count INTEGER DEFAULT 0,
                    cached_at TEXT NOT NULL
                )
            """)

            # Reports cache table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reports_cache (
                    module_name TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    json_content TEXT NOT NULL,
                    markdown_content TEXT NOT NULL
                )
            """)

            # Instagram posts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS instagram_posts (
                    post_id TEXT PRIMARY KEY,
                    caption TEXT,
                    hashtags_json TEXT,
                    format TEXT NOT NULL,
                    duration_sec INTEGER DEFAULT 0,
                    plays INTEGER DEFAULT 0,
                    reach INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    saves INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    profile_visits INTEGER DEFAULT 0,
                    follows_gained INTEGER DEFAULT 0,
                    thumbnail_url TEXT,
                    permalink TEXT,
                    published_at TEXT NOT NULL,
                    is_my_post INTEGER DEFAULT 1,
                    updated_at TEXT NOT NULL
                )
            """)

            # Instagram competitor creators table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS instagram_creators (
                    handle TEXT PRIMARY KEY,
                    name TEXT,
                    followers_count INTEGER DEFAULT 0,
                    posts_count INTEGER DEFAULT 0,
                    avg_reach INTEGER DEFAULT 0,
                    avg_engagement_rate REAL DEFAULT 0.0,
                    top_formats_json TEXT,
                    sample_posts_json TEXT,
                    updated_at TEXT NOT NULL
                )
            """)

            # YouTube retention curves table for CTR / watch-time critique
            conn.execute("""
                CREATE TABLE IF NOT EXISTS youtube_retention_curves (
                    video_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    ctr REAL DEFAULT 0.0,
                    avg_view_duration_sec REAL DEFAULT 0.0,
                    avg_percentage_viewed REAL DEFAULT 0.0,
                    retention_curve_json TEXT,
                    drop_off_points_json TEXT,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def upsert_channel(self, channel: dict):
        now_str = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO channels (
                    channel_id, title, custom_url, subscriber_count,
                    view_count, video_count, is_my_channel, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(channel_id) DO UPDATE SET
                    title=excluded.title,
                    custom_url=excluded.custom_url,
                    subscriber_count=excluded.subscriber_count,
                    view_count=excluded.view_count,
                    video_count=excluded.video_count,
                    is_my_channel=excluded.is_my_channel,
                    updated_at=excluded.updated_at
            """, (
                channel["channel_id"],
                channel.get("title", ""),
                channel.get("custom_url", ""),
                int(channel.get("subscriber_count", 0)),
                int(channel.get("view_count", 0)),
                int(channel.get("video_count", 0)),
                1 if channel.get("is_my_channel") else 0,
                now_str
            ))
            conn.commit()

    def upsert_video(self, video: dict):
        now_str = datetime.now(timezone.utc).isoformat()
        tags_json = json.dumps(video.get("tags", [])) if isinstance(video.get("tags"), list) else (video.get("tags_json") or "[]")
        traffic_json = json.dumps(video.get("traffic_sources", {})) if isinstance(video.get("traffic_sources"), dict) else (video.get("traffic_sources_json") or "{}")
        transcript_json = json.dumps(video.get("transcript", [])) if isinstance(video.get("transcript"), list) else (video.get("transcript_json") or "[]")

        # Compute view velocity if not supplied: views / days since upload
        views = int(video.get("views", 0))
        pub_at = video.get("published_at", now_str)
        try:
            pub_dt = datetime.fromisoformat(pub_at.replace("Z", "+00:00"))
            days_since = max(0.1, (datetime.now(timezone.utc) - pub_dt).total_seconds() / 86400.0)
            velocity = round(views / days_since, 2)
        except Exception:
            velocity = float(video.get("view_velocity", 0.0))

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO videos (
                    video_id, channel_id, title, description, tags_json,
                    published_at, duration_sec, views, likes, comments,
                    ctr, avg_view_duration_sec, retention_pct, traffic_sources_json,
                    sub_change, view_velocity, is_my_channel, transcript_json, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    channel_id=excluded.channel_id,
                    title=excluded.title,
                    description=excluded.description,
                    tags_json=excluded.tags_json,
                    published_at=excluded.published_at,
                    duration_sec=excluded.duration_sec,
                    views=excluded.views,
                    likes=excluded.likes,
                    comments=excluded.comments,
                    ctr=excluded.ctr,
                    avg_view_duration_sec=excluded.avg_view_duration_sec,
                    retention_pct=excluded.retention_pct,
                    traffic_sources_json=excluded.traffic_sources_json,
                    sub_change=excluded.sub_change,
                    view_velocity=excluded.view_velocity,
                    is_my_channel=excluded.is_my_channel,
                    transcript_json=excluded.transcript_json,
                    updated_at=excluded.updated_at
            """, (
                video["video_id"],
                video["channel_id"],
                video.get("title", ""),
                video.get("description", ""),
                tags_json,
                pub_at,
                int(video.get("duration_sec", 0)),
                views,
                int(video.get("likes", 0)),
                int(video.get("comments", 0)),
                float(video.get("ctr", 0.0)),
                float(video.get("avg_view_duration_sec", 0.0)),
                float(video.get("retention_pct", 0.0)),
                traffic_json,
                int(video.get("sub_change", 0)),
                velocity,
                1 if video.get("is_my_channel") else 0,
                transcript_json,
                now_str
            ))
            conn.commit()

    def get_channel(self, channel_id: str) -> dict:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM channels WHERE channel_id = ?", (channel_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_my_channel(self) -> dict:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM channels WHERE is_my_channel = 1 LIMIT 1")
            row = cur.fetchone()
            return dict(row) if row else None

    def get_my_videos(self, limit: int = 100) -> list:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM videos
                WHERE is_my_channel = 1
                ORDER BY published_at DESC
                LIMIT ?
            """, (limit,))
            return [dict(r) for r in cur.fetchall()]

    def get_competitor_videos(self, days_limit: int = 90) -> list:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days_limit)).isoformat()
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT v.*, c.title AS channel_title
                FROM videos v
                JOIN channels c ON v.channel_id = c.channel_id
                WHERE v.is_my_channel = 0 AND v.published_at >= ?
                ORDER BY v.view_velocity DESC
            """, (cutoff,))
            return [dict(r) for r in cur.fetchall()]

    def get_all_videos(self) -> list:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT v.*, c.title AS channel_title
                FROM videos v
                LEFT JOIN channels c ON v.channel_id = c.channel_id
                ORDER BY v.published_at DESC
            """)
            return [dict(r) for r in cur.fetchall()]

    def get_competitor_channels(self) -> list:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM channels WHERE is_my_channel = 0")
            return [dict(r) for r in cur.fetchall()]

    def save_report(self, module_name: str, json_data: dict, markdown_content: str):
        now_str = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO reports_cache (module_name, timestamp, json_content, markdown_content)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(module_name) DO UPDATE SET
                    timestamp=excluded.timestamp,
                    json_content=excluded.json_content,
                    markdown_content=excluded.markdown_content
            """, (module_name, now_str, json.dumps(json_data, indent=2), markdown_content))
            conn.commit()

    def get_cached_report(self, module_name: str) -> dict:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM reports_cache WHERE module_name = ?", (module_name,))
            row = cur.fetchone()
            if row:
                return {
                    "module_name": row["module_name"],
                    "timestamp": row["timestamp"],
                    "json_data": json.loads(row["json_content"]),
                    "markdown": row["markdown_content"]
                }
            return None

    # --- Instagram Methods ---
    def upsert_instagram_post(self, post: dict):
        now_str = datetime.now(timezone.utc).isoformat()
        hashtags_json = json.dumps(post.get("hashtags", [])) if isinstance(post.get("hashtags"), list) else (post.get("hashtags_json") or "[]")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO instagram_posts (
                    post_id, caption, hashtags_json, format, duration_sec,
                    plays, reach, likes, saves, shares, comments,
                    profile_visits, follows_gained, thumbnail_url, permalink,
                    published_at, is_my_post, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(post_id) DO UPDATE SET
                    caption=excluded.caption,
                    hashtags_json=excluded.hashtags_json,
                    format=excluded.format,
                    duration_sec=excluded.duration_sec,
                    plays=excluded.plays,
                    reach=excluded.reach,
                    likes=excluded.likes,
                    saves=excluded.saves,
                    shares=excluded.shares,
                    comments=excluded.comments,
                    profile_visits=excluded.profile_visits,
                    follows_gained=excluded.follows_gained,
                    thumbnail_url=excluded.thumbnail_url,
                    permalink=excluded.permalink,
                    published_at=excluded.published_at,
                    is_my_post=excluded.is_my_post,
                    updated_at=excluded.updated_at
            """, (
                post["post_id"],
                post.get("caption", ""),
                hashtags_json,
                post.get("format", "REEL"),
                int(post.get("duration_sec", 0)),
                int(post.get("plays", 0)),
                int(post.get("reach", 0)),
                int(post.get("likes", 0)),
                int(post.get("saves", 0)),
                int(post.get("shares", 0)),
                int(post.get("comments", 0)),
                int(post.get("profile_visits", 0)),
                int(post.get("follows_gained", 0)),
                post.get("thumbnail_url", ""),
                post.get("permalink", ""),
                post.get("published_at", now_str),
                1 if post.get("is_my_post", True) else 0,
                now_str
            ))
            conn.commit()

    def get_my_instagram_posts(self, limit: int = 10) -> list:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM instagram_posts
                WHERE is_my_post = 1
                ORDER BY published_at DESC
                LIMIT ?
            """, (limit,))
            return [dict(r) for r in cur.fetchall()]

    def upsert_instagram_creator(self, creator: dict):
        now_str = datetime.now(timezone.utc).isoformat()
        top_f_json = json.dumps(creator.get("top_formats", [])) if isinstance(creator.get("top_formats"), list) else (creator.get("top_formats_json") or "[]")
        sample_p_json = json.dumps(creator.get("sample_posts", [])) if isinstance(creator.get("sample_posts"), list) else (creator.get("sample_posts_json") or "[]")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO instagram_creators (
                    handle, name, followers_count, posts_count, avg_reach,
                    avg_engagement_rate, top_formats_json, sample_posts_json, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(handle) DO UPDATE SET
                    name=excluded.name,
                    followers_count=excluded.followers_count,
                    posts_count=excluded.posts_count,
                    avg_reach=excluded.avg_reach,
                    avg_engagement_rate=excluded.avg_engagement_rate,
                    top_formats_json=excluded.top_formats_json,
                    sample_posts_json=excluded.sample_posts_json,
                    updated_at=excluded.updated_at
            """, (
                creator["handle"],
                creator.get("name", creator["handle"]),
                int(creator.get("followers_count", 0)),
                int(creator.get("posts_count", 0)),
                int(creator.get("avg_reach", 0)),
                float(creator.get("avg_engagement_rate", 0.0)),
                top_f_json,
                sample_p_json,
                now_str
            ))
            conn.commit()

    def get_competitor_instagram_creators(self) -> list:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM instagram_creators ORDER BY followers_count DESC")
            return [dict(r) for r in cur.fetchall()]

    # --- YouTube Retention & CTR Methods ---
    def upsert_retention_curve(self, curve: dict):
        now_str = datetime.now(timezone.utc).isoformat()
        curve_json = json.dumps(curve.get("retention_curve", [])) if isinstance(curve.get("retention_curve"), list) else (curve.get("retention_curve_json") or "[]")
        drops_json = json.dumps(curve.get("drop_off_points", [])) if isinstance(curve.get("drop_off_points"), list) else (curve.get("drop_off_points_json") or "[]")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO youtube_retention_curves (
                    video_id, title, ctr, avg_view_duration_sec,
                    avg_percentage_viewed, retention_curve_json, drop_off_points_json, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(video_id) DO UPDATE SET
                    title=excluded.title,
                    ctr=excluded.ctr,
                    avg_view_duration_sec=excluded.avg_view_duration_sec,
                    avg_percentage_viewed=excluded.avg_percentage_viewed,
                    retention_curve_json=excluded.retention_curve_json,
                    drop_off_points_json=excluded.drop_off_points_json,
                    updated_at=excluded.updated_at
            """, (
                curve["video_id"],
                curve.get("title", ""),
                float(curve.get("ctr", 0.0)),
                float(curve.get("avg_view_duration_sec", 0.0)),
                float(curve.get("avg_percentage_viewed", 0.0)),
                curve_json,
                drops_json,
                now_str
            ))
            conn.commit()

    def get_retention_curves(self, limit: int = 5) -> list:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM youtube_retention_curves ORDER BY updated_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cur.fetchall()]
