"""
VisionAid - Authentication & Profile Manager
Handles user registration, credential hashing with salt, and persistent user sessions in users.json.
"""

import os
import json
import hashlib
import uuid

def _get_users_file_path():
    try:
        from kivy.app import App
        app = App.get_running_app()
        if app and getattr(app, "user_data_dir", None):
            return os.path.join(app.user_data_dir, "users.json")
    except Exception:
        pass
    if "ANDROID_ARGUMENT" in os.environ or "ANDROID_ROOT" in os.environ:
        home = os.path.expanduser("~")
        if os.path.exists(home):
            return os.path.join(home, "users.json")
    return os.path.join(os.path.dirname(__file__), "users.json")

BUNDLE_USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if salt is None:
        salt = uuid.uuid4().hex[:16]
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt


class AuthManager:
    """Manages user accounts, credential verification, and user sessions."""

    def __init__(self, storage_path=None):
        self.storage_path = storage_path
        self.users = self._load_users()

    def _get_target_path(self):
        if self.storage_path:
            return self.storage_path
        return _get_users_file_path()

    def _load_users(self):
        target = self._get_target_path()
        file_to_load = None
        if os.path.exists(target):
            file_to_load = target
        elif os.path.exists(BUNDLE_USERS_FILE):
            file_to_load = BUNDLE_USERS_FILE

        if file_to_load and os.path.exists(file_to_load):
            try:
                with open(file_to_load, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[AuthManager] Error loading users: {e}")
        
        # Starter default demonstration user
        default_hash, default_salt = _hash_password("vision123")
        starter = {
            "users": [
                {
                    "id": "usr_demo",
                    "name": "Demo User",
                    "email": "user@visionaid.ai",
                    "password_hash": default_hash,
                    "salt": default_salt
                }
            ]
        }
        self._save_users(starter)
        return starter

    def _save_users(self, data=None):
        if data is None:
            data = self.users
        target = self._get_target_path()
        try:
            target_dir = os.path.dirname(target)
            if target_dir:
                os.makedirs(target_dir, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[AuthManager] Error saving users: {e}")

    def register_user(self, name: str, email: str, password: str) -> tuple[bool, dict | None, str]:
        name = name.strip()
        email = email.strip().lower()

        if not name:
            return False, None, "Please enter your full name."
        if not email or "@" not in email or "." not in email:
            return False, None, "Please enter a valid email address."
        if len(password) < 4:
            return False, None, "Password must be at least 4 characters."

        # Check existing user
        for u in self.users.get("users", []):
            if u["email"] == email:
                return False, None, "An account with this email already exists."

        pwd_hash, salt = _hash_password(password)
        new_user = {
            "id": f"usr_{uuid.uuid4().hex[:8]}",
            "name": name,
            "email": email,
            "password_hash": pwd_hash,
            "salt": salt,
            "is_guest": False
        }

        self.users.setdefault("users", []).append(new_user)
        self._save_users()
        
        # Return user info without hash
        user_info = {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "is_guest": False
        }
        return True, user_info, "Account created successfully!"

    def authenticate_user(self, email_or_name: str, password: str) -> tuple[bool, dict | None, str]:
        ident = email_or_name.strip().lower()
        if not ident or not password:
            return False, None, "Please enter your email and password."

        for u in self.users.get("users", []):
            if u["email"].lower() == ident or u["name"].lower() == ident:
                salt = u["salt"]
                expected_hash, _ = _hash_password(password, salt)
                if expected_hash == u["password_hash"]:
                    user_info = {
                        "id": u["id"],
                        "name": u["name"],
                        "email": u["email"],
                        "is_guest": False
                    }
                    return True, user_info, f"Welcome back, {u['name']}!"
                else:
                    return False, None, "Incorrect password. Please try again."

        return False, None, "No account found with this email or username."

    def guest_login(self) -> dict:
        """Provide instant guest session for accessibility."""
        return {
            "id": "usr_guest",
            "name": "Guest Explorer",
            "email": "guest@visionaid.ai",
            "is_guest": True
        }


# Global singleton instance
auth_manager = AuthManager()
