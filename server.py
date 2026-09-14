"""
VisionAid - Cloud AI Backend Server (FastAPI)
Hosts YOLO11, EasyOCR, and FaceAnalyzer for lightweight mobile Android clients.
"""

import os
import sys
import time
import io
import cv2
import numpy as np
import torch
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ultralytics import YOLO
import easyocr

# Cap PyTorch threads for server stability
torch.set_num_threads(2)

from auth_manager import auth_manager
from face_engine import FaceAnalyzer
from language_manager import language_manager

app = FastAPI(title="VisionAid AI Server", version="1.0.0")

# Enable CORS for mobile apps and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Starting VisionAid AI Server...")
print("Loading YOLO11...")
model = YOLO("yolo11n.pt")
print("Loading EasyOCR...")
ocr_reader = easyocr.Reader(["en"], gpu=False)
print("Loading FaceAnalyzer...")
face_analyzer = FaceAnalyzer()
print("✅ All AI models initialized successfully!")


class AuthRequest(BaseModel):
    email_or_name: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "VisionAid AI Cloud Server",
        "models": ["yolo11n", "easyocr", "haar_face", "haar_smile"]
    }


@app.post("/api/auth/login")
def login(req: AuthRequest):
    ok, user, msg = auth_manager.authenticate_user(req.email_or_name, req.password)
    if not ok:
        raise HTTPException(status_code=401, detail=msg)
    return {"status": "success", "user": user, "message": msg}


@app.post("/api/auth/register")
def register(req: RegisterRequest):
    ok, user, msg = auth_manager.register_user(req.name, req.email, req.password)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "user": user, "message": msg}


@app.post("/api/analyze")
async def analyze_frame(
    file: UploadFile = File(...),
    mode: str = Form("object"),
    find_target: str = Form("cup"),
    language: str = Form("en"),
):
    """
    Core vision endpoint: processes mobile camera frame and returns
    bounding boxes, spatial cues, and audio instructions.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        raise HTTPException(status_code=400, detail="Invalid image frame")

    h, w = frame.shape[:2]
    frame_area = float(w * h)

    response = {
        "mode": mode,
        "hud_text": "",
        "speech_text": None,
        "play_sound": None,
        "detections": [],
        "faces": [],
        "read_text": "",
        "target_locked": False,
    }

    # 1. OBJECT, OBSTACLE, RADAR, FIND MODES (YOLO)
    if mode in ("object", "obstacle", "radar", "find"):
        results = model(frame, imgsz=320, conf=0.45, verbose=False)
        detections = []

        for box in results[0].boxes:
            conf = float(box.conf[0])
            if conf < 0.45:
                continue
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
            obj_name = model.names[int(box.cls[0])]
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            box_area = float((x2 - x1) * (y2 - y1))
            area_ratio = box_area / frame_area

            # Spatial horizontal location
            if cx < w * 0.35:
                position = "left"
            elif cx > w * 0.65:
                position = "right"
            else:
                position = "center"

            if area_ratio >= 0.18:
                proximity = "close"
            elif area_ratio >= 0.04:
                proximity = "nearby"
            else:
                proximity = "distant"

            detections.append({
                "name": obj_name,
                "conf": conf,
                "bbox": [x1, y1, x2, y2],
                "area_ratio": area_ratio,
                "position": position,
                "proximity": proximity,
                "cx": cx,
                "cy": cy
            })

        detections.sort(key=lambda d: d["area_ratio"], reverse=True)
        response["detections"] = detections

        # Mode Specific Logic
        if mode == "object":
            if detections:
                top = detections[:3]
                items = [f"{d['name'].capitalize()} ({d['position']})" for d in top]
                response["hud_text"] = " • ".join(items)
                phrases = [f"a {d['name']} on your {d['position']}" if d['position'] != 'center' else f"a {d['name']} in front" for d in top]
                response["speech_text"] = "I see " + ", and ".join(phrases) + "."
            else:
                response["hud_text"] = "Scanning for objects..."

        elif mode == "obstacle":
            if detections:
                crit = max(detections, key=lambda d: d["area_ratio"] + (0.25 if d["position"] == "center" else 0.0))
                pos_desc = "directly in front" if crit["position"] == "center" else f"on your {crit['position']}"
                if crit["area_ratio"] >= 0.18 or (crit["position"] == "center" and crit["area_ratio"] >= 0.10):
                    response["hud_text"] = f"Warning! {crit['name']} very close {pos_desc}"
                    response["speech_text"] = f"Warning! {crit['name']} is close {pos_desc}."
                else:
                    response["hud_text"] = f"Caution: {crit['name']} nearby {pos_desc}"
                    response["speech_text"] = f"{crit['name'].capitalize()} {pos_desc}."
            else:
                response["hud_text"] = "Path appears clear"

        elif mode == "radar":
            if detections:
                crit = max(detections, key=lambda d: d["area_ratio"] + (0.25 if d["position"] == "center" else 0.0))
                pos = crit["position"]
                response["hud_text"] = f"Radar Tone: {crit['name'].capitalize()} [{pos.upper()}]"
                response["play_sound"] = f"radar_{pos}"  # e.g. radar_left, radar_center, radar_right
            else:
                response["hud_text"] = "Path clear • No obstacles"

        elif mode == "find":
            target = find_target.lower().strip()
            synonyms = {
                "phone": ["cell phone", "phone"],
                "mobile": ["cell phone", "phone"],
                "bottle": ["bottle", "wine glass", "cup"],
                "cup": ["cup", "bottle", "bowl", "mug"],
                "keys": ["key", "remote", "scissors"],
                "computer": ["laptop", "keyboard"],
                "laptop": ["laptop"],
            }
            cands = synonyms.get(target, [target])
            matching = [d for d in detections if any(c in d["name"].lower() for c in cands)]

            if matching:
                best = matching[0]
                offset = best["cx"] - (w / 2.0)
                is_locked = abs(offset) < (w * 0.12)
                response["target_locked"] = is_locked

                if is_locked:
                    response["hud_text"] = f"TARGET LOCKED! {best['name'].capitalize()} is centered"
                    response["play_sound"] = "beacon_lock"
                    response["speech_text"] = f"Target locked! {best['name']} is directly in front of you."
                else:
                    dir_cue = "left" if offset < 0 else "right"
                    response["hud_text"] = f"Found {best['name'].capitalize()} • Pan {dir_cue.upper()}"
                    response["play_sound"] = "beacon_ping"
                    response["speech_text"] = f"{best['name']} is on your {dir_cue}. Move camera {dir_cue}."
            else:
                response["hud_text"] = f"Searching for {find_target}... Pan camera slowly"

    # 2. FACE & EMOTION COMPANION
    elif mode == "face":
        faces = face_analyzer.analyze_faces(frame)
        response["faces"] = faces
        if faces:
            primary = faces[0]
            summaries = [f"{f['name']}: {f['emotion']} ({f['position']})" for f in faces[:2]]
            response["hud_text"] = " • ".join(summaries)
            response["speech_text"] = primary["description"]
        else:
            response["hud_text"] = "Scanning for companions & faces..."

    # 3. TEXT OCR
    elif mode == "text":
        scale = 384.0 / max(w, 1)
        small = cv2.resize(frame, (384, int(h * scale)))
        ocr_res = ocr_reader.readtext(small)
        text_lines = [r[1].strip() for r in ocr_res if r[2] >= 0.40 and len(r[1].strip()) > 1]
        full_text = " ".join(text_lines)
        response["read_text"] = full_text
        if full_text:
            response["hud_text"] = f"Read: {full_text[:50]}..."
            response["speech_text"] = "I can read: " + full_text
        else:
            response["hud_text"] = "Scanning for text..."

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Running VisionAid Server on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
