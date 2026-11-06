import os
import re
from pathlib import Path
from core.config import _load_yaml_file

BASE_DIR = Path(__file__).resolve().parent.parent

# List of unauthorized gear brands and products to strictly guard against
FORBIDDEN_GEAR_PATTERNS = [
    r"\binsta\s*360\b",
    r"\bgopro\b",
    r"\bdji\s*action\s*[245]\b",  # only Osmo Action 3 is allowed
    r"\bhero\s*\d+\b",
    r"\bktm\b",
    r"\bbmw\s*gs\b",
    r"\binterceptor\b",
    r"\bclassic\s*350\b",
    r"\bdominar\b",
    r"\bdrone\b",
    r"\bdji\s*mavic\b",
    r"\bdji\s*mini\b",
    r"\brode\b",
    r"\bdji\s*mic\b",
    r"\bhollyland\b",
    r"\bboy\w*\s*mic\b",
    r"\bpremiere\s*pro\b",
    r"\bdavinci\s*resolve\b",
    r"\bcapcut\b",
    r"\bphotoshop\b",
    r"\billustrator\b",
    r"\bcanva\s*pro\b",
    r"\biphone\b",
    r"\bsamsung\s*s\d+\b",
    r"\bpixel\b"
]

class GearManager:
    """
    Single source of truth for gear and tools.
    Enforces strict compliance with config/gear.yaml.
    """
    def __init__(self, gear_file_path: str = None):
        if not gear_file_path:
            gear_file_path = str(BASE_DIR / "config" / "gear.yaml")
        self.gear_file_path = Path(gear_file_path)
        self.gear = self._load_gear()

    def _load_gear(self) -> dict:
        if self.gear_file_path.exists():
            return _load_yaml_file(self.gear_file_path)
        # Fallback default adhering to specification
        return {
            "bike": "Himalayan 450",
            "action_camera": "DJI Osmo Action 3",
            "phone": "Motorola Edge 40 Neo",
            "microphones": [
                "Generic wired microphone",
                "Grenaro wireless microphone"
            ],
            "computer": "Apple Mac Mini M4",
            "video_editing_fx": "Final Cut Pro",
            "image_editing": "Canva (Free tier)",
            "other": []
        }

    @property
    def bike(self) -> str:
        return self.gear.get("bike", "Himalayan 450")

    @property
    def action_camera(self) -> str:
        return self.gear.get("action_camera", "DJI Osmo Action 3")

    @property
    def phone(self) -> str:
        p = self.gear.get("phone", "Motorola Edge 40 Neo")
        if isinstance(p, dict):
            return p.get("model", "Motorola Edge 40 Neo")
        return str(p)

    @property
    def phone_settings(self) -> dict:
        """Returns confirmed phone camera settings if specified in gear.yaml."""
        if "phone_settings" in self.gear and isinstance(self.gear["phone_settings"], dict):
            return self.gear["phone_settings"]
        if "phone_specs" in self.gear and isinstance(self.gear["phone_specs"], dict):
            return self.gear["phone_specs"]
        p = self.gear.get("phone")
        if isinstance(p, dict):
            return {k: v for k, v in p.items() if k != "model"}
        return {}

    def is_phone_spec_confirmed(self) -> bool:
        """Checks if phone capture settings (resolution, frame rate, stabilization) are confirmed."""
        ps = self.phone_settings
        if not ps:
            return False
        return any(k in ps for k in ["resolution", "frame_rate", "fps", "framerate", "stabilization", "capture_profile", "profile"])

    @property
    def microphones(self) -> list:
        return self.gear.get("microphones", ["Generic wired microphone", "Grenaro wireless microphone"])

    @property
    def computer(self) -> str:
        return self.gear.get("computer", "Apple Mac Mini M4")

    @property
    def video_editing(self) -> str:
        return self.gear.get("video_editing_fx", "Final Cut Pro")

    @property
    def image_editing(self) -> str:
        return self.gear.get("image_editing", "Canva (Free tier)")

    def validate_suggestion(self, text: str) -> tuple:
        """
        Validates text against forbidden gear brands and items.
        Returns (is_valid: bool, violations: list).
        """
        violations = []
        text_lower = text.lower()
        for pattern in FORBIDDEN_GEAR_PATTERNS:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                violations.append(match.group(0))

        # Check bike rule: no motorcycle brand or model other than Himalayan 450 is allowed
        unauthorized_bikes = ["ktm", "duke", "adventure 390", "triumph", "scrambler", "bmw", "bullet", "classic 350", "hunter", "interceptor", "dominar"]
        for ub in unauthorized_bikes:
            if re.search(r"\b" + re.escape(ub) + r"\b", text_lower):
                violations.append(f"unauthorized bike '{ub}' (only Himalayan 450 allowed)")

        is_valid = len(violations) == 0
        return is_valid, violations

    def get_mic_for_setup(self, is_moving_shot: bool = False) -> str:
        """Selects microphone strictly according to moving vs fixed setup rule."""
        if is_moving_shot:
            return "Grenaro wireless microphone"
        return "Generic wired microphone"

    def get_phone_spec_notice(self) -> str:
        """Mandatory notice if unconfirmed. If confirmed in gear.yaml, returns empty string."""
        if self.is_phone_spec_confirmed():
            return ""
        return (
            "⚠️ Note on Phone Settings: Motorola Edge 40 Neo camera specs (resolution, frame rate, "
            "stabilization profile) are not assumed. Please confirm your exact preferred capture profile "
            "in config/gear.yaml before locking in 4K/60fps or Horizon Lock workflows."
        )

    def get_canva_free_limitation_note(self, needs_transparent_cutout: bool = False) -> str:
        """Notes Canva Free limitations (e.g. Magic Resize, Brand Kit, background remover)."""
        notes = ["Designed in Canva (Free tier). Brand Kit and Magic Resize are not available on the free tier."]
        if needs_transparent_cutout:
            notes.append(
                "Canva Free lacks one-click background remover. Suggest using free manual cutout utilities or "
                "placing subject directly onto high-contrast solid/gradient backgrounds."
            )
        return " ".join(notes)

    def get_gear_manifest(self) -> dict:
        return {
            "authorized_bike": self.bike,
            "authorized_action_camera": self.action_camera,
            "authorized_phone": self.phone,
            "authorized_microphones": self.microphones,
            "authorized_workstation": self.computer,
            "authorized_video_editor": self.video_editing,
            "authorized_image_editor": self.image_editing,
            "other_items": self.gear.get("other", [])
        }
