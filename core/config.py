import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def _load_env_file(env_path: Path):
    """Loads a .env file into os.environ if not already set."""
    if not env_path.exists():
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val
    except Exception as e:
        print(f"[Config] Note: Could not parse .env file: {e}")

def _load_yaml_file(yaml_path: Path) -> dict:
    """Loads YAML file using PyYAML if available, or a fallback parser for basic structures."""
    try:
        import yaml
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass

    # Built-in lightweight YAML parser for key-values, lists, and comments
    data = {}
    current_list_key = None
    if not yaml_path.exists():
        return data

    with open(yaml_path, "r", encoding="utf-8") as f:
        for line in f:
            # Strip comments
            line_clean = line.split("#", 1)[0].rstrip()
            if not line_clean.strip():
                continue

            # List item
            if line_clean.strip().startswith("- "):
                val = line_clean.strip()[2:].strip().strip("'\"")
                if current_list_key:
                    if current_list_key not in data:
                        data[current_list_key] = []
                    data[current_list_key].append(val)
                continue

            # Key-value or list start
            if ":" in line_clean:
                key, val = line_clean.split(":", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if not val:
                    current_list_key = key
                    data[key] = []
                else:
                    current_list_key = None
                    # Try int / float / bool
                    if val.lower() == "true":
                        data[key] = True
                    elif val.lower() == "false":
                        data[key] = False
                    elif val.isdigit():
                        data[key] = int(val)
                    else:
                        data[key] = val

    return data

def extract_channel_identifier(raw_input: str) -> str:
    """Extracts channel ID or handle from YouTube URLs or raw identifiers."""
    if not raw_input:
        return ""
    raw = str(raw_input).strip()
    # Match /channel/(UC[a-zA-Z0-9_-]{22})
    match_uc = re.search(r"channel/(UC[a-zA-Z0-9_-]{22})", raw)
    if match_uc:
        return match_uc.group(1)
    # Match /@handle
    match_handle = re.search(r"@([a-zA-Z0-9_.-]+)", raw)
    if match_handle:
        return f"@{match_handle.group(1)}"
    # If already a UC id
    if raw.startswith("UC") and len(raw) == 24:
        return raw
    # If already a handle
    if raw.startswith("@"):
        return raw
    # Otherwise strip trailing slashes
    return raw.rstrip("/")

class Config:
    def __init__(self, config_path: str = None):
        self.base_dir = BASE_DIR
        env_file = self.base_dir / ".env"
        _load_env_file(env_file)

        cfg_file = Path(config_path) if config_path else (self.base_dir / "config.yaml")
        raw_cfg = _load_yaml_file(cfg_file)

        self.raw = raw_cfg
        self.my_channel_id_raw = raw_cfg.get("my_channel_id", "")
        self.my_channel_id = extract_channel_identifier(self.my_channel_id_raw)
        self.my_channel_handle = str(raw_cfg.get("my_channel_handle", "@SouvikSays")).strip()
        self.my_channel_title = str(raw_cfg.get("my_channel_title", "Souvik Says")).strip()
        self.my_channel_subscribers = int(raw_cfg.get("my_channel_subscribers", 887))

        raw_niche = raw_cfg.get("niche_keywords", [])
        if isinstance(raw_niche, str):
            self.niche_keywords = [k.strip() for k in raw_niche.split(",")]
        else:
            self.niche_keywords = list(raw_niche)

        raw_competitors = raw_cfg.get("competitor_channel_ids", [])
        if isinstance(raw_competitors, str):
            raw_comps = [c.strip() for c in raw_competitors.split(",")]
        else:
            raw_comps = list(raw_competitors)
        self.competitor_channel_ids = [extract_channel_identifier(c) for c in raw_comps if c]

        # Instagram configuration
        raw_ig_handle = str(raw_cfg.get("my_instagram_handle", "@souvik_says")).strip()
        self.my_instagram_handle = raw_ig_handle if raw_ig_handle.startswith("@") else f"@{raw_ig_handle}"
        self.my_instagram_followers = int(raw_cfg.get("my_instagram_followers", 282))
        self.my_instagram_posts_count = int(raw_cfg.get("my_instagram_posts_count", 136))
        self.my_instagram_business_account_id = str(raw_cfg.get("my_instagram_business_account_id", "17841400000000000"))
        raw_ig_comps = raw_cfg.get("competitor_instagram_handles", [])
        if isinstance(raw_ig_comps, str):
            self.competitor_instagram_handles = [h.strip() for h in raw_ig_comps.split(",")]
        else:
            self.competitor_instagram_handles = list(raw_ig_comps)

        self.timezone = raw_cfg.get("timezone", "Asia/Kolkata")
        self.audience_country = raw_cfg.get("audience_country", "Global")
        self.quota_daily_limit = int(raw_cfg.get("quota_daily_limit", 10000))
        self.cache_ttl_hours = int(raw_cfg.get("cache_ttl_hours", 24))

        # Gear configuration
        gear_rel = raw_cfg.get("gear_config_path", "config/gear.yaml")
        self.gear_config_path = str(self.base_dir / gear_rel)
        from core.gear_manager import GearManager
        self.gear_manager = GearManager(self.gear_config_path)

        db_rel = raw_cfg.get("sqlite_db_path", "data/youtube_agent.db")
        self.sqlite_db_path = str(self.base_dir / db_rel)

        # Environment API keys & Streamlit Cloud secrets support
        st_secrets = {}
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                st_secrets = st.secrets
        except Exception:
            pass

        self.youtube_api_key = os.environ.get("YOUTUBE_API_KEY", str(st_secrets.get("YOUTUBE_API_KEY", ""))).strip()
        self.client_secrets_file = os.environ.get("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
        self.oauth_token_file = os.environ.get("YOUTUBE_OAUTH_TOKEN_FILE", "token.json")
        self.instagram_access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", str(st_secrets.get("INSTAGRAM_ACCESS_TOKEN", ""))).strip()
        self.instagram_business_account_id = str(os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", st_secrets.get("INSTAGRAM_BUSINESS_ACCOUNT_ID", self.my_instagram_business_account_id))).strip()
        self.use_mock_data = os.environ.get("USE_MOCK_DATA", "").lower() in ("true", "1", "yes")

    def is_api_configured(self) -> bool:
        """Returns True if YouTube or Instagram API credentials are configured."""
        return bool(self.youtube_api_key and not self.use_mock_data)

    def is_instagram_configured(self) -> bool:
        """Returns True if Instagram access token is present."""
        return bool(self.instagram_access_token and not self.use_mock_data)

    def summary(self) -> dict:
        return {
            "my_channel_id": self.my_channel_id,
            "my_channel_handle": self.my_channel_handle,
            "my_channel_title": self.my_channel_title,
            "my_instagram_handle": self.my_instagram_handle,
            "niche_keywords_count": len(self.niche_keywords),
            "youtube_competitors_count": len(self.competitor_channel_ids),
            "instagram_competitors_count": len(self.competitor_instagram_handles),
            "timezone": self.timezone,
            "audience_country": self.audience_country,
            "youtube_api_key_configured": bool(self.youtube_api_key),
            "instagram_token_configured": bool(self.instagram_access_token),
            "mock_mode": not self.is_api_configured()
        }
