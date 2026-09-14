import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "vision_settings.json")

class VisionSettings:
    """Manages user preferences with persistent JSON storage."""

    def __init__(self):
        # Default Speech Settings
        self.volume = 100
        self.rate = 0

        # Obstacle sensitivity (area ratio threshold)
        self.obstacle_threshold = 0.25

        # Voice command activation
        self.voice_enabled = True

        # Language & Localization
        self.language = "en"
        self.language_selected = False

        # User Authentication Session
        self.current_user = None

        # Cloud AI Server Endpoint
        self.server_url = "http://127.0.0.1:8000"

        self.load()

    def load(self):
        """Load settings from local JSON if available."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.volume = int(data.get("volume", self.volume))
                    self.rate = int(data.get("rate", self.rate))
                    self.obstacle_threshold = float(data.get("obstacle_threshold", self.obstacle_threshold))
                    self.voice_enabled = bool(data.get("voice_enabled", self.voice_enabled))
                    self.language = str(data.get("language", self.language))
                    self.language_selected = bool(data.get("language_selected", self.language_selected))
                    self.current_user = data.get("current_user", self.current_user)
                    self.server_url = str(data.get("server_url", self.server_url))
            except Exception as e:
                print("Failed to load settings file, using defaults:", e)

    def save(self):
        """Persist settings to JSON file."""
        try:
            data = {
                "volume": self.volume,
                "rate": self.rate,
                "obstacle_threshold": self.obstacle_threshold,
                "voice_enabled": self.voice_enabled,
                "language": self.language,
                "language_selected": self.language_selected,
                "current_user": self.current_user,
                "server_url": self.server_url,
            }
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Failed to save settings:", e)

    def set_server_url(self, url):
        self.server_url = url.strip().rstrip("/")
        self.save()

    def set_language(self, lang_code):
        self.language = lang_code
        self.language_selected = True
        self.save()

    def set_current_user(self, user_info):
        self.current_user = user_info
        self.save()

    def logout(self):
        self.current_user = None
        self.save()

    def set_volume(self, value):
        self.volume = max(0, min(100, int(value)))
        self.save()

    def set_rate(self, value):
        self.rate = max(-10, min(10, int(value)))
        self.save()

    def set_obstacle_threshold(self, value):
        self.obstacle_threshold = round(max(0.10, min(0.50, float(value))), 2)
        self.save()

    def set_voice_enabled(self, enabled):
        self.voice_enabled = bool(enabled)
        self.save()