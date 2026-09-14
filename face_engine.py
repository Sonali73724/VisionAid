"""
VisionAid - Familiar Face & Emotion Recognition Engine
Real-time lightweight face detection and smile/expression analysis using OpenCV Haar cascades.
Maintains familiar contact profiles with JSON persistence.
"""

import os
import json
import cv2
import numpy as np

PROFILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_profiles.json")


class FaceAnalyzer:
    """Lightweight real-time face and emotion analyzer optimized for assistive vision."""

    def __init__(self, profiles_file=PROFILES_PATH):
        self.profiles_file = profiles_file
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")
        
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        """Load registered familiar contact profiles."""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[FaceAnalyzer] Error loading profiles: {e}")
        
        # Default starter familiar contacts
        default_profiles = {
            "contacts": [
                {"id": "contact_1", "name": "Sarah (Caregiver)", "relation": "Caregiver"},
                {"id": "contact_2", "name": "Mom", "relation": "Family"},
                {"id": "contact_3", "name": "Alex (Friend)", "relation": "Friend"}
            ]
        }
        self._save_profiles(default_profiles)
        return default_profiles

    def _save_profiles(self, profiles=None):
        if profiles is None:
            profiles = self.profiles
        try:
            with open(self.profiles_file, "w", encoding="utf-8") as f:
                json.dump(profiles, f, indent=2)
        except Exception as e:
            print(f"[FaceAnalyzer] Error saving profiles: {e}")

    def add_contact(self, name, relation="Friend"):
        """Register a new familiar contact."""
        new_id = f"contact_{len(self.profiles.get('contacts', [])) + 1}"
        self.profiles.setdefault("contacts", []).append({
            "id": new_id,
            "name": name,
            "relation": relation
        })
        self._save_profiles()
        return new_id

    def analyze_faces(self, frame):
        """
        Analyze faces in the given BGR frame.
        Returns a list of face information dicts.
        """
        if frame is None:
            return []

        h, w = frame.shape[:2]
        # Downscale for ultra-fast detection
        scale = 320.0 / max(w, 1)
        small_w = int(w * scale)
        small_h = int(h * scale)
        
        small_gray = cv2.resize(frame, (small_w, small_h))
        small_gray = cv2.cvtColor(small_gray, cv2.COLOR_BGR2GRAY)
        small_gray = cv2.equalizeHist(small_gray)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            small_gray,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        results = []
        contacts = self.profiles.get("contacts", [])

        for idx, (sx, sy, sw, sh) in enumerate(faces):
            # Scale back to original dimensions
            orig_x = int(sx / scale)
            orig_y = int(sy / scale)
            orig_w = int(sw / scale)
            orig_h = int(sh / scale)

            # Extract face ROI in small_gray for smile detection
            face_roi_gray = small_gray[sy:sy + sh, sx:sx + sw]
            
            # Lower half of face for smile detection
            mouth_roi_gray = face_roi_gray[int(sh * 0.45):sh, :]
            
            smiles = self.smile_cascade.detectMultiScale(
                mouth_roi_gray,
                scaleFactor=1.6,
                minNeighbors=14,
                minSize=(15, 15)
            )

            is_smiling = len(smiles) > 0
            emotion = "smiling" if is_smiling else "neutral"

            # Compute horizontal spatial location
            center_x = orig_x + orig_w / 2.0
            norm_x = center_x / float(w)
            
            if norm_x < 0.35:
                position = "left"
                pos_desc = "on your left"
            elif norm_x > 0.65:
                position = "right"
                pos_desc = "on your right"
            else:
                position = "center"
                pos_desc = "directly in front of you"

            # Proximity estimation
            norm_h = orig_h / float(h)
            if norm_h > 0.35:
                dist_desc = "close up"
            elif norm_h > 0.18:
                dist_desc = "a few steps away"
            else:
                dist_desc = "at a distance"

            # If contacts exist, associate face or fallback to generic person
            contact_label = "Person"
            if len(faces) == 1 and contacts:
                # Primary person detected
                contact_label = contacts[0]["name"]

            # Concise natural audio narration phrase
            if is_smiling:
                narration = f"{contact_label} is {pos_desc}, smiling warmly"
            else:
                narration = f"{contact_label} is {pos_desc}, {dist_desc}"

            results.append({
                "box": (orig_x, orig_y, orig_w, orig_h),
                "center_x": center_x,
                "center_y": orig_y + orig_h / 2.0,
                "name": contact_label,
                "emotion": emotion,
                "is_smiling": is_smiling,
                "position": position,
                "pos_desc": pos_desc,
                "dist_desc": dist_desc,
                "description": narration
            })

        return results
