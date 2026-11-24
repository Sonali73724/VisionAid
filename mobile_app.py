"""
VisionAid - Mobile Android & Cross-Platform Client Application
Lightweight mobile client with Lilac & Pink luxury accessibility UI.
Offloads heavy AI inference to VisionAid Cloud/Local Server for maximum mobile performance.
"""

import os
import sys
import time
import threading
import io
import json
import struct
import urllib.request

try:
    import requests
except ImportError:
    requests = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None

try:
    from ultralytics import YOLO as LocalYOLO
except Exception:
    LocalYOLO = None

OBJECT_ALIASES = {
    "cell phone": "mobile phone",
    "dining table": "table",
    "tv": "monitor",
    "couch": "sofa",
    "potted plant": "plant",
}


# Kivy configuration for Mobile Display (Desktop preview only)
from kivy.utils import platform as kivy_platform
if kivy_platform not in ('android', 'ios'):
    from kivy.config import Config
    Config.set('graphics', 'width', '420')
    Config.set('graphics', 'height', '780')
    Config.set('graphics', 'resizable', '1')

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase

# Register Unicode & Devanagari font on Windows for crisp Hindi rendering
for f in [r"C:\Windows\Fonts\mangal.ttf", r"C:\Windows\Fonts\aparaj.ttf"]:
    if os.path.exists(f):
        try:
            fb = r"C:\Windows\Fonts\mangalb.ttf"
            LabelBase.register(name="Roboto", fn_regular=f, fn_bold=fb if os.path.exists(fb) else f)
            break
        except Exception:
            pass

from settings import VisionSettings
from settings_screen import SettingsScreen
from tts_engine import TTSEngine
from sound_effects import sound_manager
from auth_screens import LanguageSelectionScreen, LoginScreen, SignupScreen
from language_manager import language_manager, SUPPORTED_LANGUAGES

# Assets
BASE_DIR = os.path.dirname(__file__)
TEX_BG = os.path.join(BASE_DIR, "assets", "textures", "bg_grad.png")
TEX_CARD = os.path.join(BASE_DIR, "assets", "textures", "card_grad.png")
TEX_CARD_ACTIVE = os.path.join(BASE_DIR, "assets", "textures", "card_active_grad.png")
TEX_HUD = os.path.join(BASE_DIR, "assets", "textures", "hud_grad.png")

ICON_SETTINGS = os.path.join(BASE_DIR, "assets", "icons", "icon_settings.png")
ICON_STATUS = os.path.join(BASE_DIR, "assets", "icons", "icon_status.png")
ICON_CAMERA = os.path.join(BASE_DIR, "assets", "icons", "icon_camera.png")
ICON_EYE = os.path.join(BASE_DIR, "assets", "icons", "icon_eye.png")
ICON_TEXT = os.path.join(BASE_DIR, "assets", "icons", "icon_text.png")
ICON_SHIELD = os.path.join(BASE_DIR, "assets", "icons", "icon_shield.png")
ICON_MIC = os.path.join(BASE_DIR, "assets", "icons", "icon_mic.png")
ICON_STOP = os.path.join(BASE_DIR, "assets", "icons", "icon_stop.png")
ICON_FIND = os.path.join(BASE_DIR, "assets", "icons", "icon_find.png")
ICON_RADAR = os.path.join(BASE_DIR, "assets", "icons", "icon_radar.png")
ICON_FACE = os.path.join(BASE_DIR, "assets", "icons", "icon_face.png")
ICON_GLOBE = os.path.join(BASE_DIR, "assets", "icons", "icon_globe.png")

# Palette - Clean Elegant Theme (matching UI/UX reference)
C_BG = (0.97, 0.96, 0.99, 1.0)              # #F7F5FC Soft Lavender Light BG
C_CARD_BG = (1.0, 1.0, 1.0, 1.0)            # #FFFFFF Pure White
C_CARD_BORDER = (0.91, 0.89, 0.96, 1.0)      # #EAE5F5 Subtle Card Border
C_TEXT_PRIMARY = (0.12, 0.08, 0.22, 1.0)     # #1F1635 Deep Slate Purple
C_TEXT_SECONDARY = (0.45, 0.42, 0.53, 1.0)   # #736B87 Secondary Text
C_TEXT_MUTED = (0.58, 0.55, 0.67, 1.0)       # #948C9E Muted Caption Text
C_PURPLE = (0.43, 0.16, 0.85, 1.0)           # #6D28D9 Brand Deep Violet
C_PURPLE_ACCENT = (0.49, 0.23, 0.93, 1.0)    # #7C3AED Radiant Purple
C_LILAC_BTN_BG = (0.93, 0.90, 0.98, 1.0)     # #EDE7FA Soft Lilac Button BG
C_LILAC_BORDER = (0.85, 0.78, 0.95, 1.0)     # #D9C7F3
C_STANDBY_BG = (0.94, 0.92, 0.98, 1.0)       # #EFEBF9 Viewport Standby BG

# Mode-specific pastel icon backgrounds & tint colors
MODE_ICON_STYLES = {
    "object": {
        "bg": (0.94, 0.92, 0.98, 1.0),       # #F0EBFB Soft Purple
        "color": (0.43, 0.16, 0.85, 1.0)     # #6D28D9
    },
    "find": {
        "bg": (0.90, 0.94, 0.98, 1.0),       # #E6F0FA Soft Blue
        "color": (0.15, 0.45, 0.90, 1.0)     # #2563EB
    },
    "face": {
        "bg": (0.99, 0.92, 0.95, 1.0),       # #FCEBF3 Soft Pink
        "color": (0.86, 0.15, 0.47, 1.0)     # #DB2777
    },
    "text": {
        "bg": (1.0, 0.95, 0.89, 1.0),        # #FEF3E2 Soft Amber
        "color": (0.85, 0.47, 0.05, 1.0)     # #D97706
    },
    "obstacle": {
        "bg": (0.90, 0.97, 0.94, 1.0),       # #E6F8F0 Soft Mint
        "color": (0.02, 0.60, 0.40, 1.0)     # #059669
    },
    "stop": {
        "bg": (1.0, 0.92, 0.92, 1.0),        # #FEECEB Soft Coral
        "color": (0.86, 0.15, 0.15, 1.0)     # #DC2626
    }
}

# Legacy aliases for backward compatibility
C_LILAC = C_PURPLE
C_PINK = (0.86, 0.15, 0.47, 1.0)
C_ROSE = (0.02, 0.60, 0.40, 1.0)
C_MAGENTA = (0.91, 0.47, 0.97, 1)
C_FIND = (0.15, 0.45, 0.90, 1.0)
C_RADAR = (0.42, 0.78, 0.98, 1)
C_FACE = (0.86, 0.15, 0.47, 1.0)
C_CRIMSON = (0.86, 0.15, 0.15, 1.0)
C_TEXT_WHITE = (1.0, 1.0, 1.0, 1.0)
C_BORDER_DEFAULT = C_CARD_BORDER

if kivy_platform not in ('android', 'ios'):
    Window.size = (420, 780)
Window.clearcolor = C_BG

settings = VisionSettings()
language_manager.set_language(settings.language)
tts = TTSEngine(language=settings.language)


def speak(text, interrupt=False):
    tts.speak(text, interrupt=interrupt)



class ThreadedCamera:
    """Thread-safe non-blocking camera capture supporting both PC (OpenCV) and Android (Kivy CoreCamera)."""
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.width = width
        self.height = height
        self.stopped = False
        self.grabbed = False
        self.frame = None
        self.lock = threading.Lock()
        self.cap = None
        self.core_cam = None

        # 1. Try OpenCV (Desktop / PC)
        if cv2 is not None:
            try:
                self.cap = cv2.VideoCapture(self.src)
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    self.grabbed, self.frame = self.cap.read()
                    self.thread = threading.Thread(target=self._capture_loop, daemon=True)
                    self.thread.start()
                    return
            except Exception as e:
                print("OpenCV camera init exception:", e)

        # 2. Fallback to Kivy CoreCamera (Native Android / mobile)
        try:
            from kivy.core.camera import Camera as CoreCamera
            try:
                self.core_cam = CoreCamera(index=self.src, resolution=(width, height), stopped=True)
            except Exception:
                self.core_cam = CoreCamera(index=self.src, stopped=True)
            self.core_cam.bind(on_texture=self._on_core_texture)
            self.core_cam.start()
            self.grabbed = True
        except Exception as e:
            print("Kivy CoreCamera init exception:", e)

    def _on_core_texture(self, camera):
        tex = camera.texture
        if tex:
            with self.lock:
                self.frame = tex
                self.grabbed = True

    def _capture_loop(self):
        while not self.stopped:
            if not self.cap or not self.cap.isOpened():
                break
            grabbed, frame = self.cap.read()
            if grabbed and frame is not None:
                with self.lock:
                    self.grabbed = grabbed
                    self.frame = frame
            time.sleep(0.015)

    def read(self):
        with self.lock:
            if self.frame is not None:
                if hasattr(self.frame, "copy"):
                    return self.grabbed, self.frame.copy()
                return self.grabbed, self.frame
            return False, None

    def is_opened(self):
        if self.cap is not None and self.cap.isOpened():
            return True
        if self.core_cam is not None:
            return True
        return False

    def release(self):
        self.stopped = True
        if hasattr(self, "thread") and self.thread.is_alive():
            self.thread.join(timeout=0.4)
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.core_cam is not None:
            try:
                self.core_cam.stop()
            except Exception:
                pass
            self.core_cam = None


def encode_frame_to_bytes(frame_to_send, target_w=480):
    """
    Converts either a numpy ndarray (desktop OpenCV) or a Kivy Texture (Android CoreCamera)
    into standard compressed image bytes (JPEG preferred, BMP fallback).
    Requires ZERO external C/pip packages on Android.
    """
    if frame_to_send is None:
        return None, None

    # CASE 1: Numpy ndarray (Desktop OpenCV)
    if hasattr(frame_to_send, "shape"):
        h, w = frame_to_send.shape[:2]
        target_h = max(1, int(h * (target_w / max(1, w))))
        if cv2 is not None:
            small = cv2.resize(frame_to_send, (target_w, target_h))
            ret, jpeg = cv2.imencode('.jpg', small, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if ret:
                return jpeg.tobytes(), "image/jpeg"
        if PILImage is not None:
            try:
                pil_img = PILImage.fromarray(frame_to_send)
                buf = io.BytesIO()
                pil_img.resize((target_w, target_h)).save(buf, format="JPEG", quality=75)
                return buf.getvalue(), "image/jpeg"
            except Exception:
                pass

    # CASE 2: Kivy Texture (Mobile Android CoreCamera)
    if hasattr(frame_to_send, "pixels"):
        tex = frame_to_send
        tw, th = tex.width, tex.height
        target_h = max(1, int(target_w * th / max(1, tw))) if tw > 0 else 240

        # Method 2A: Pillow (Ultra-fast compiled C JPEG encoding - ~2ms)
        if PILImage is not None:
            try:
                pil_img = PILImage.frombytes('RGBA', tex.size, tex.pixels)
                buf = io.BytesIO()
                pil_img.convert('RGB').resize((target_w, target_h)).save(buf, format="JPEG", quality=60)
                return buf.getvalue(), "image/jpeg"
            except Exception:
                pass

        # Method 2B: Android Native Java Bitmap Compression (Hardware JPEG encoder on device)
        if kivy_platform == 'android':
            try:
                from jnius import autoclass
                Bitmap = autoclass('android.graphics.Bitmap')
                BitmapConfig = autoclass('android.graphics.Bitmap$Config')
                CompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')
                ByteArrayOutputStream = autoclass('java.io.ByteArrayOutputStream')
                ByteBuffer = autoclass('java.nio.ByteBuffer')

                raw_bytes = tex.pixels
                if raw_bytes:
                    bb = ByteBuffer.wrap(raw_bytes)
                    bmp = Bitmap.createBitmap(tw, th, BitmapConfig.ARGB_8888)
                    bmp.copyPixelsFromBuffer(bb)
                    scaled = Bitmap.createScaledBitmap(bmp, target_w, target_h, True)
                    stream = ByteArrayOutputStream()
                    scaled.compress(CompressFormat.JPEG, 60, stream)
                    jpeg_bytes = bytes(stream.toByteArray())
                    stream.close()
                    bmp.recycle()
                    scaled.recycle()
                    return jpeg_bytes, "image/jpeg"
            except Exception as e:
                pass

        # Method 2C: Fast Direct Downsampled BMP Fallback (Zero loops, instantaneous)
        try:
            raw = tex.pixels
            if raw and tw > 0 and th > 0:
                step_x = max(1, tw // target_w)
                step_y = max(1, th // target_h)
                actual_w = tw // step_x
                actual_h = th // step_y
                mv = memoryview(raw)
                row_stride = tw * 4
                rows = []
                for y in range(0, actual_h * step_y, step_y):
                    row_data = mv[y * row_stride : (y + 1) * row_stride]
                    sampled_bgr = bytearray()
                    for x in range(0, actual_w * step_x * 4, step_x * 4):
                        sampled_bgr.extend([row_data[x+2], row_data[x+1], row_data[x]])
                    pad = (4 - len(sampled_bgr) % 4) % 4
                    if pad:
                        sampled_bgr.extend(b'\x00' * pad)
                    rows.append(sampled_bgr)
                out_rows = b''.join(rows)
                file_size = 54 + len(out_rows)
                header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, 54)
                info = struct.pack('<IiiHHIIIIII', 40, actual_w, -actual_h, 1, 24, 0, len(out_rows), 2835, 2835, 0, 0)
                return header + info + out_rows, "image/bmp"
        except Exception:
            pass

    return None, None


class BoundingBoxOverlay(Widget):
    """Draws visual detection boxes and object labels on top of the camera viewport for both Android and Desktop."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.detections = []
        self.size_hint = (1, 1)
        self.is_mirrored = (cv2 is not None)
        self.label_pool = []
        for _ in range(8):
            lbl = Label(
                text="",
                font_size=10,
                bold=True,
                color=(1, 1, 1, 1),
                size_hint=(None, None),
                height=dp(18),
                opacity=0
            )
            with lbl.canvas.before:
                lbl._bg_color = Color(0.12, 0.06, 0.20, 0.85)
                lbl._bg_rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[dp(4)])
                lbl._border_color = Color(0.75, 0.52, 0.98, 0.9)
                lbl._border_line = Line(rounded_rectangle=(lbl.x, lbl.y, lbl.width, lbl.height, dp(4)), width=1.0)
            lbl.bind(
                pos=lambda inst, val: (
                    setattr(inst._bg_rect, "pos", val),
                    setattr(inst._border_line, "rounded_rectangle", (val[0], val[1], inst.width, inst.height, dp(4)))
                ),
                size=lambda inst, val: (
                    setattr(inst._bg_rect, "size", val),
                    setattr(inst._border_line, "rounded_rectangle", (inst.x, inst.y, val[0], val[1], dp(4)))
                )
            )
            self.add_widget(lbl)
            self.label_pool.append(lbl)

        self.bind(pos=lambda *_: self.draw_boxes(), size=lambda *_: self.draw_boxes())

    def update_boxes(self, detections, is_mirrored=None):
        if is_mirrored is not None:
            self.is_mirrored = is_mirrored
        self.detections = detections or []
        self.draw_boxes()

    def clear_boxes(self):
        self.detections = []
        self.canvas.clear()
        for lbl in self.label_pool:
            lbl.opacity = 0

    def draw_boxes(self):
        self.canvas.clear()
        if not self.detections or self.width <= 0 or self.height <= 0:
            for lbl in self.label_pool:
                lbl.opacity = 0
            return

        with self.canvas:
            for i, d in enumerate(self.detections[:8]):
                norm = d.get("norm_bbox")
                if norm and len(norm) == 4:
                    norm_x1, norm_y1, norm_x2, norm_y2 = norm
                else:
                    fw = float(d.get("frame_w", 320.0)) or 320.0
                    fh = float(d.get("frame_h", 240.0)) or 240.0
                    bbox = d.get("bbox", [0, 0, 0, 0])
                    norm_x1 = bbox[0] / fw
                    norm_y1 = bbox[1] / fh
                    norm_x2 = bbox[2] / fw
                    norm_y2 = bbox[3] / fh

                norm_x1 = max(0.0, min(1.0, norm_x1))
                norm_x2 = max(0.0, min(1.0, norm_x2))
                norm_y1 = max(0.0, min(1.0, norm_y1))
                norm_y2 = max(0.0, min(1.0, norm_y2))

                # If preview is mirrored (desktop webcam or selfie camera)
                if self.is_mirrored:
                    disp_x1 = 1.0 - norm_x2
                    disp_x2 = 1.0 - norm_x1
                else:
                    disp_x1 = norm_x1
                    disp_x2 = norm_x2

                w = max(dp(16), (disp_x2 - disp_x1) * self.width)
                h = max(dp(16), (norm_y2 - norm_y1) * self.height)
                x = self.x + disp_x1 * self.width
                y = self.y + (1.0 - norm_y2) * self.height

                pos = d.get("position", "center")
                if pos == "center":
                    box_color = (0.96, 0.45, 0.71, 0.95)  # Blossom Pink
                else:
                    box_color = (0.75, 0.52, 0.98, 0.95)  # Radiant Lilac

                Color(*box_color)
                Line(rounded_rectangle=(x, y, w, h, dp(6)), width=2.0)

                # Render badge label
                if i < len(self.label_pool):
                    lbl = self.label_pool[i]
                    name = d.get("name", "object")
                    conf_pct = d.get("confidence_pct", int(d.get("conf", 0.0) * 100))
                    lbl.text = f" {name.upper()} {conf_pct}% "
                    lbl._border_color.rgba = box_color
                    lbl.texture_update()
                    lbl_w = max(dp(44), lbl.texture_size[0] + dp(8))
                    lbl_h = dp(18)
                    lbl.size = (lbl_w, lbl_h)
                    lbl.pos = (x, min(self.y + self.height - lbl_h - dp(2), max(self.y + dp(2), y + h - dp(2))))
                    lbl.opacity = 1

            for j in range(len(self.detections), len(self.label_pool)):
                self.label_pool[j].opacity = 0


class GradientActionCard(ButtonBehavior, BoxLayout):
    def __init__(self, icon_path, title, subtitle, accent_color, mode_key="object", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(70)
        self.padding = [dp(12), dp(10), dp(12), dp(10)]
        self.spacing = dp(12)

        self.icon_path = icon_path
        self.accent_color = accent_color
        self.mode_key = mode_key
        self.is_active = False

        with self.canvas.before:
            Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            self.canvas_border = Color(*C_CARD_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)), width=1.1)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        style = MODE_ICON_STYLES.get(mode_key, {
            "bg": (0.94, 0.92, 0.98, 1.0),
            "color": C_PURPLE
        })

        # Pastel Icon Wrapper
        icon_wrapper = BoxLayout(size_hint=(None, None), size=(dp(48), dp(48)), padding=dp(8), pos_hint={"center_y": 0.5})
        with icon_wrapper.canvas.before:
            self.icon_bg_color = Color(*style["bg"])
            self.icon_bg = RoundedRectangle(pos=icon_wrapper.pos, size=icon_wrapper.size, radius=[dp(12)])

        icon_wrapper.bind(pos=lambda *_: setattr(self.icon_bg, "pos", icon_wrapper.pos),
                          size=lambda *_: setattr(self.icon_bg, "size", icon_wrapper.size))

        self.icon_img = Image(source=self.icon_path, fit_mode="contain", color=style["color"])
        icon_wrapper.add_widget(self.icon_img)
        self.add_widget(icon_wrapper)

        # Info
        info_box = BoxLayout(orientation="vertical", spacing=dp(2), pos_hint={"center_y": 0.5})
        self.title_lbl = Label(text=title, font_size=14.5, bold=True, color=C_TEXT_PRIMARY, halign="left", valign="middle", size_hint=(1, 0.55))
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))
        self.desc_lbl = Label(text=subtitle, font_size=11.5, color=C_TEXT_SECONDARY, halign="left", valign="top", size_hint=(1, 0.45))
        self.desc_lbl.bind(size=self.desc_lbl.setter("text_size"))
        info_box.add_widget(self.title_lbl)
        info_box.add_widget(self.desc_lbl)
        self.add_widget(info_box)

        # Start Button Pill
        self.btn_pill = BoxLayout(size_hint=(None, None), size=(dp(76), dp(32)), pos_hint={"center_y": 0.5})
        with self.btn_pill.canvas.before:
            self.btn_bg_color = Color(*C_PURPLE)
            self.btn_bg = RoundedRectangle(pos=self.btn_pill.pos, size=self.btn_pill.size, radius=[dp(16)])

        self.btn_pill.bind(pos=lambda *_: setattr(self.btn_bg, "pos", self.btn_pill.pos),
                           size=lambda *_: setattr(self.btn_bg, "size", self.btn_pill.size))

        self.status_tag = Label(text="[b]Start ▶[/b]", markup=True, font_size=11.5, color=(1.0, 1.0, 1.0, 1.0), halign="center", valign="middle")
        self.btn_pill.add_widget(self.status_tag)
        self.add_widget(self.btn_pill)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(16))

    def set_active(self, active):
        self.is_active = active
        if active:
            self.canvas_border.rgba = C_PURPLE
            self.border_line.width = 1.6
            self.btn_bg_color.rgba = C_PURPLE_ACCENT
            self.status_tag.text = "[b]Active ●[/b]"
        else:
            self.canvas_border.rgba = C_CARD_BORDER
            self.border_line.width = 1.1
            self.btn_bg_color.rgba = C_PURPLE
            self.status_tag.text = "[b]Start ▶[/b]"


class StatusPill(BoxLayout):
    def __init__(self, icon_path=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.size = (dp(86), dp(36))
        self.pos_hint = {"center_y": 0.5}
        self.padding = [dp(6), dp(4), dp(8), dp(4)]
        self.spacing = dp(4)

        with self.canvas.before:
            Color(*C_LILAC_BTN_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(*C_LILAC_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.0)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.status_icon = Image(source=icon_path or ICON_STATUS, size_hint=(None, 1), width=dp(16), fit_mode="contain", color=C_PURPLE)
        self.text_lbl = Label(text="Standby", font_size=11, bold=True, color=C_PURPLE, halign="center", valign="middle")
        self.add_widget(self.status_icon)
        self.add_widget(self.text_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))

    @property
    def text(self):
        return self.text_lbl.text

    @text.setter
    def text(self, val):
        clean = val.replace("●", "").replace("•", "").strip()
        self.text_lbl.text = clean.capitalize() if clean.isupper() else clean

    @property
    def color(self):
        return self.text_lbl.color

    @color.setter
    def color(self, val):
        self.text_lbl.color = val
        self.status_icon.color = val


class LanguagePillButton(ButtonBehavior, BoxLayout):
    def __init__(self, icon_path=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.size = (dp(62), dp(36))
        self.pos_hint = {"center_y": 0.5}
        self.padding = [dp(6), dp(4), dp(6), dp(4)]
        self.spacing = dp(4)

        with self.canvas.before:
            Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(*C_CARD_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.1)

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self.globe_icon = Image(source=icon_path or ICON_GLOBE, size_hint=(None, 1), width=dp(16), fit_mode="contain", color=C_PURPLE)
        self.text_lbl = Label(text="EN", font_size=11, bold=True, color=C_TEXT_PRIMARY, halign="center", valign="middle")
        self.add_widget(self.globe_icon)
        self.add_widget(self.text_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))

    @property
    def text(self):
        return self.text_lbl.text

    @text.setter
    def text(self, val):
        self.text_lbl.text = val

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.7
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class SettingsPillButton(ButtonBehavior, BoxLayout):
    def __init__(self, icon_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.size = (dp(92), dp(36))
        self.pos_hint = {"center_y": 0.5}
        self.padding = [dp(6), dp(4), dp(8), dp(4)]
        self.spacing = dp(4)

        with self.canvas.before:
            Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(*C_CARD_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.1)

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self.gear_icon = Image(source=icon_path, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.text_lbl = Label(text="Settings", font_size=11, bold=True, color=C_TEXT_PRIMARY, halign="center", valign="middle")
        self.add_widget(self.gear_icon)
        self.add_widget(self.text_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.7
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class FlipCameraButton(ButtonBehavior, BoxLayout):
    """Floating white pill button on camera viewport matching the design reference."""
    def __init__(self, on_press_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.size = (dp(78), dp(32))
        self.padding = [dp(8), dp(4), dp(8), dp(4)]
        self.spacing = dp(5)
        self.pos_hint = {"right": 0.97, "top": 0.96}
        self.on_press_callback = on_press_callback

        with self.canvas.before:
            Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            Color(0.88, 0.84, 0.95, 1.0)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)), width=1.1)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        cam_icon = Image(source=ICON_CAMERA, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.lbl = Label(text="Flip", font_size=12, bold=True, color=C_TEXT_PRIMARY, halign="center", valign="middle")
        self.add_widget(cam_icon)
        self.add_widget(self.lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(16))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.7
            if self.on_press_callback:
                self.on_press_callback()
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class MainScreen(Screen):
    """Mobile dashboard streaming frames to VisionAid AI Server."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.camera_index = 0
        self.mode = None
        self.find_target = "cup"
        self.target_locked = False

        # Streaming thread state
        self.network_running = False
        self.network_thread = None
        self.latest_frame = None
        self.frame_lock = threading.Lock()
        self.server_detections = []
        self.server_faces = []

        # Local inference fallback & speech interval control
        self.local_model = None
        self.local_model_failed = False
        self.speech_interval = 3.5
        self.last_speech_time = 0
        self.last_spoken_text = ""
        self.last_spoken_key = ""

        self._build_ui()
        self.update_language()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", padding=[dp(16), dp(12), dp(16), dp(12)], spacing=dp(10))
        with root.canvas.before:
            Color(*C_BG)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *_: setattr(self.bg_rect, "pos", root.pos),
                  size=lambda *_: setattr(self.bg_rect, "size", root.size))

        # Top Bar
        header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(46), spacing=dp(6))
        brand = BoxLayout(orientation="vertical", size_hint=(1, 1), spacing=dp(1))
        app_title = Label(text="[b]VisionAid[/b]", markup=True, font_size=21, color=C_TEXT_PRIMARY, halign="left", valign="bottom", size_hint=(1, 0.58))
        app_title.bind(size=app_title.setter("text_size"))
        self.app_sub = Label(text=language_manager.get_string("app_subtitle"), font_size=11, color=C_TEXT_SECONDARY, halign="left", valign="top", size_hint=(1, 0.42))
        self.app_sub.bind(size=self.app_sub.setter("text_size"))
        brand.add_widget(app_title)
        brand.add_widget(self.app_sub)

        self.status_pill = StatusPill(icon_path=ICON_STATUS)
        self.lang_pill = LanguagePillButton(icon_path=ICON_GLOBE)
        self.lang_pill.bind(on_press=self.cycle_language)

        settings_btn = SettingsPillButton(icon_path=ICON_SETTINGS)
        settings_btn.bind(on_press=self.open_settings)

        header.add_widget(brand)
        header.add_widget(self.status_pill)
        header.add_widget(self.lang_pill)
        header.add_widget(settings_btn)
        root.add_widget(header)

        # Viewport
        vp_wrapper = RelativeLayout(size_hint=(1, 0.38))
        with vp_wrapper.canvas.before:
            Color(*C_STANDBY_BG)
            self.vp_bg = RoundedRectangle(pos=(0, 0), size=vp_wrapper.size, radius=[dp(18)])
            Color(0.88, 0.84, 0.95, 1.0)
            self.vp_border = Line(rounded_rectangle=(0, 0, vp_wrapper.width, vp_wrapper.height, dp(18)), width=1.1)
        vp_wrapper.bind(size=lambda _, s: (setattr(self.vp_bg, "size", s), setattr(self.vp_border, "rounded_rectangle", (0, 0, s[0], s[1], dp(18)))))

        self.camera_image = Image(fit_mode="contain", size_hint=(1, 1), pos_hint={"x": 0, "y": 0}, opacity=0)

        # Standby Placeholder
        self.placeholder = BoxLayout(orientation="vertical", spacing=dp(6), padding=[dp(14), dp(16), dp(14), dp(16)], size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        cam_icon = Image(source=ICON_CAMERA, size_hint=(1, 0.42), fit_mode="contain", color=C_PURPLE_ACCENT)
        self.ready_t = Label(text="Vision Camera Standby", font_size=17, bold=True, color=C_TEXT_PRIMARY, size_hint=(1, None), height=dp(26), halign="center")

        pill_box = BoxLayout(size_hint=(None, None), size=(dp(210), dp(28)), pos_hint={"center_x": 0.5}, padding=[dp(8), dp(2), dp(8), dp(2)])
        with pill_box.canvas.before:
            Color(*C_CARD_BG)
            self.standby_pill_bg = RoundedRectangle(pos=pill_box.pos, size=pill_box.size, radius=[dp(14)])
            Color(0.88, 0.84, 0.95, 1.0)
            self.standby_pill_border = Line(rounded_rectangle=(pill_box.x, pill_box.y, pill_box.width, pill_box.height, dp(14)), width=1.0)
        pill_box.bind(pos=lambda *_: (setattr(self.standby_pill_bg, "pos", pill_box.pos), setattr(self.standby_pill_border, "rounded_rectangle", (pill_box.x, pill_box.y, pill_box.width, pill_box.height, dp(14)))),
                      size=lambda *_: (setattr(self.standby_pill_bg, "size", pill_box.size), setattr(self.standby_pill_border, "rounded_rectangle", (pill_box.x, pill_box.y, pill_box.width, pill_box.height, dp(14)))))

        self.ready_s = Label(text="[color=10B981]●[/color]  System ready to assist you.", markup=True, font_size=11.5, color=C_TEXT_PRIMARY, halign="center", valign="middle")
        pill_box.add_widget(self.ready_s)

        self.placeholder.add_widget(cam_icon)
        self.placeholder.add_widget(self.ready_t)
        self.placeholder.add_widget(pill_box)

        # Floating HUD Banner
        self.hud_banner = Label(text=language_manager.get_string("banner_standby"), font_size=13, bold=True, color=C_PURPLE, size_hint=(0.92, None), height=dp(36), pos_hint={"center_x": 0.5, "y": 0.04}, halign="center", valign="middle")
        self.hud_banner.bind(size=self.hud_banner.setter("text_size"))
        with self.hud_banner.canvas.before:
            Color(1, 1, 1, 0.92)
            self.hud_bg = RoundedRectangle(pos=self.hud_banner.pos, size=self.hud_banner.size, radius=[dp(12)])
            Color(0.88, 0.84, 0.95, 1.0)
            self.hud_border = Line(rounded_rectangle=(self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)), width=1.1)
        self.hud_banner.bind(pos=lambda *_: (setattr(self.hud_bg, "pos", self.hud_banner.pos), setattr(self.hud_border, "rounded_rectangle", (self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)))),
                             size=lambda *_: (setattr(self.hud_bg, "size", self.hud_banner.size), setattr(self.hud_border, "rounded_rectangle", (self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)))))

        self.bbox_overlay = BoundingBoxOverlay()
        self.btn_flip = FlipCameraButton(on_press_callback=self.switch_camera)
        vp_wrapper.add_widget(self.placeholder)
        vp_wrapper.add_widget(self.camera_image)
        vp_wrapper.add_widget(self.bbox_overlay)
        vp_wrapper.add_widget(self.btn_flip)
        vp_wrapper.add_widget(self.hud_banner)
        root.add_widget(vp_wrapper)

        # Action Cards ScrollView
        scroll = ScrollView(size_hint=(1, 0.62), do_scroll_x=False, bar_width=dp(3))
        card_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, dp(4), 0, dp(12)])
        card_list.bind(minimum_height=card_list.setter("height"))

        self.card_object = GradientActionCard(ICON_EYE, "Object Guidance", "Identifies items, people & vehicles", C_PURPLE, mode_key="object")
        self.card_object.bind(on_press=lambda _: self.start_mode("object"))
        card_list.add_widget(self.card_object)

        self.card_find = GradientActionCard(ICON_FIND, "Find My Object", "Target locator with audio feedback", (0.15, 0.45, 0.90, 1.0), mode_key="find")
        self.card_find.bind(on_press=lambda _: self.start_mode("find"))
        card_list.add_widget(self.card_find)

        self.card_face = GradientActionCard(ICON_FACE, "Face Companion", "Identify familiar contacts & expressions", (0.86, 0.15, 0.47, 1.0), mode_key="face")
        self.card_face.bind(on_press=lambda _: self.start_mode("face"))
        card_list.add_widget(self.card_face)

        self.card_text = GradientActionCard(ICON_TEXT, "Read Text", "Recognize documents, signage & books", (0.85, 0.47, 0.05, 1.0), mode_key="text")
        self.card_text.bind(on_press=lambda _: self.start_mode("text"))
        card_list.add_widget(self.card_text)

        self.card_obstacle = GradientActionCard(ICON_SHIELD, "Obstacle Guidance", "Real-time proximity warnings & alerts", (0.02, 0.60, 0.40, 1.0), mode_key="obstacle")
        self.card_obstacle.bind(on_press=lambda _: self.start_mode("obstacle"))
        card_list.add_widget(self.card_obstacle)

        self.card_stop = GradientActionCard(ICON_STOP, "Stop Camera", "Turn off video feed & pause vision", (0.86, 0.15, 0.15, 1.0), mode_key="stop")
        self.card_stop.bind(on_press=self.stop_camera)
        card_list.add_widget(self.card_stop)

        # Footer Tagline
        footer_wrap = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(34), spacing=dp(8), padding=[dp(12), dp(4), dp(12), dp(4)])
        left_div = Widget(size_hint=(1, None), height=dp(1), pos_hint={"center_y": 0.5})
        with left_div.canvas:
            Color(*C_LILAC_BORDER)
            left_line = Line(points=[0, 0, 10, 0], width=1.0)
        left_div.bind(pos=lambda *_: setattr(left_line, "points", [left_div.x, left_div.center_y, left_div.right, left_div.center_y]),
                      size=lambda *_: setattr(left_line, "points", [left_div.x, left_div.center_y, left_div.right, left_div.center_y]))

        footer_lbl = Label(
            text="[b]♡[/b]  VisionAid — See. Understand. Live Better.",
            markup=True,
            font_size=11,
            color=C_PURPLE,
            size_hint=(None, 1),
            width=dp(250),
            halign="center",
            valign="middle"
        )

        right_div = Widget(size_hint=(1, None), height=dp(1), pos_hint={"center_y": 0.5})
        with right_div.canvas:
            Color(*C_LILAC_BORDER)
            right_line = Line(points=[0, 0, 10, 0], width=1.0)
        right_div.bind(pos=lambda *_: setattr(right_line, "points", [right_div.x, right_div.center_y, right_div.right, right_div.center_y]),
                       size=lambda *_: setattr(right_line, "points", [right_div.x, right_div.center_y, right_div.right, right_div.center_y]))

        footer_wrap.add_widget(left_div)
        footer_wrap.add_widget(footer_lbl)
        footer_wrap.add_widget(right_div)
        card_list.add_widget(footer_wrap)

        scroll.add_widget(card_list)
        root.add_widget(scroll)
        self.add_widget(root)

    def on_enter(self):
        self.update_language()

    def cycle_language(self, *args):
        langs = [l["code"] for l in SUPPORTED_LANGUAGES]
        cur = settings.language or "en"
        next_idx = (langs.index(cur) + 1) % len(langs) if cur in langs else 0
        new_lang = langs[next_idx]
        settings.set_language(new_lang)
        language_manager.set_language(new_lang)
        tts.set_language(new_lang)
        self.update_language()
        info = language_manager.get_language_info(new_lang)
        speak(info["confirmation"], interrupt=True)

    def update_language(self):
        lang = settings.language or "en"
        language_manager.set_language(lang)
        tts.set_language(lang)

        lang_info = language_manager.get_language_info(lang)
        if hasattr(self, "lang_pill"):
            self.lang_pill.text = lang_info["badge"]

        if hasattr(self, "app_sub"):
            self.app_sub.text = language_manager.get_string("app_subtitle", lang)

        if hasattr(self, "ready_t"):
            self.ready_t.text = language_manager.get_string("cam_standby_title", lang)
        if hasattr(self, "ready_s"):
            self.ready_s.text = language_manager.get_string("cam_standby_sub", lang)

        if self.mode is None:
            if hasattr(self, "status_pill"):
                self.status_pill.text = language_manager.get_string("status_standby", lang)
            if hasattr(self, "hud_banner"):
                self.hud_banner.text = language_manager.get_string("banner_standby", lang)

        if hasattr(self, "card_find"):
            self.card_find.title_lbl.text = language_manager.get_string("card_find_title", lang)
            self.card_find.desc_lbl.text = language_manager.get_string("card_find_sub", lang)
        if hasattr(self, "card_object"):
            self.card_object.title_lbl.text = language_manager.get_string("card_object_title", lang)
            self.card_object.desc_lbl.text = language_manager.get_string("card_object_sub", lang)
        if hasattr(self, "card_face"):
            self.card_face.title_lbl.text = language_manager.get_string("card_face_title", lang)
            self.card_face.desc_lbl.text = language_manager.get_string("card_face_sub", lang)
        if hasattr(self, "card_text"):
            self.card_text.title_lbl.text = language_manager.get_string("card_text_title", lang)
            self.card_text.desc_lbl.text = language_manager.get_string("card_text_sub", lang)
        if hasattr(self, "card_obstacle"):
            self.card_obstacle.title_lbl.text = language_manager.get_string("card_obstacle_title", lang)
            self.card_obstacle.desc_lbl.text = language_manager.get_string("card_obstacle_sub", lang)
        if hasattr(self, "card_stop"):
            self.card_stop.title_lbl.text = language_manager.get_string("card_stop_title", lang)
            self.card_stop.desc_lbl.text = language_manager.get_string("card_stop_sub", lang)

    def open_settings(self, *args):
        if self.manager:
            self.manager.transition.direction = "left"
            self.manager.current = "settings"

    def open_camera(self):
        if kivy_platform == 'android':
            try:
                from android.permissions import check_permission, request_permissions, Permission
                if not check_permission(Permission.CAMERA):
                    print("Camera permission not granted, requesting...")
                    request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO])
                    self.hud_banner.text = "Please allow Camera permission"
                    return False
            except Exception as e:
                print("Permission check error:", e)

        if self.camera is not None and self.camera.is_opened():
            return True
        self.camera = ThreadedCamera(self.camera_index, 640, 480)
        if not self.camera.is_opened():
            err_msg = language_manager.get_string("camera_error")
            self.hud_banner.text = err_msg
            speak(err_msg, interrupt=True)
            self.camera = None
            return False
        self.placeholder.opacity = 0
        self.camera_image.opacity = 1
        self._start_network_worker()
        return True

    def switch_camera(self, *args):
        """Toggle between back camera (0) and front selfie camera (1)."""
        self.camera_index = 1 if self.camera_index == 0 else 0
        cam_name = "Front Camera" if self.camera_index == 1 else "Back Camera"
        if self.camera is not None and self.camera.is_opened():
            self.camera.release()
            self.camera = ThreadedCamera(self.camera_index, 640, 480)
            self.hud_banner.text = f"Switched to {cam_name}"
            speak(f"{cam_name} active", interrupt=True)
        else:
            self.hud_banner.text = f"Selected {cam_name}"
            speak(f"{cam_name} selected", interrupt=True)

    def stop_camera(self, *args):
        Clock.unschedule(self.update_camera)
        self._stop_network_worker()
        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.mode = None
        self.camera_image.texture = None
        self.camera_image.opacity = 0
        self.placeholder.opacity = 1
        self.last_spoken_text = ""
        self.last_spoken_key = ""
        self.last_speech_time = 0
        if hasattr(self, "bbox_overlay"):
            self.bbox_overlay.clear_boxes()
        self.status_pill.text = language_manager.get_string("status_standby")
        self.status_pill.color = C_LILAC
        self.hud_banner.text = language_manager.get_string("banner_standby")

        self.card_object.set_active(False)
        self.card_find.set_active(False)
        self.card_face.set_active(False)
        self.card_text.set_active(False)
        self.card_obstacle.set_active(False)
        speak(language_manager.get_string("camera_stopped"), interrupt=True)

    def start_mode(self, mode):
        if not self.open_camera():
            return
        self.mode = mode
        self.card_object.set_active(mode == "object")
        self.card_find.set_active(mode == "find")
        self.card_face.set_active(mode == "face")
        self.card_text.set_active(mode == "text")
        self.card_obstacle.set_active(mode == "obstacle")

        lang = settings.language
        card_key = f"card_{mode}_title"
        mode_title = language_manager.get_string(card_key, lang)
        self.status_pill.text = mode_title.upper()
        self.status_pill.color = C_PINK if mode == "text" else (C_FIND if mode == "find" else C_LILAC)
        self.hud_banner.text = f"{mode_title}..."
        mode_speak = language_manager.get_string(f"mode_{mode}", lang)
        speak(mode_speak, interrupt=True)

        Clock.unschedule(self.update_camera)
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

    def update_camera(self, dt):
        if self.camera is None:
            return
        ret, frame = self.camera.read()
        if not ret or frame is None:
            return

        with self.frame_lock:
            self.latest_frame = frame

        # Case A: Kivy Texture (Mobile Android CoreCamera)
        if hasattr(frame, 'pixels') or not hasattr(frame, 'shape'):
            self.camera_image.texture = frame
            if hasattr(frame, 'size'):
                self.camera_image.texture_size = list(frame.size)
            self.camera_image.canvas.ask_update()
            return

        # Case B: Numpy ndarray (Desktop OpenCV)
        if cv2 is not None and hasattr(frame, 'shape'):
            display_frame = cv2.flip(frame, 1)
            fh, fw = display_frame.shape[:2]
            rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            if self.camera_image.texture is None or self.camera_image.texture.size != (fw, fh):
                self.camera_image.texture = Texture.create(size=(fw, fh), colorfmt="rgb")
            self.camera_image.texture.blit_buffer(rgb.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
            self.camera_image.texture.flip_vertical()
            self.camera_image.canvas.ask_update()

    def _start_network_worker(self):
        if self.network_running:
            return
        self.network_running = True
        self.network_thread = threading.Thread(target=self._network_loop, daemon=True)
        self.network_thread.start()

    def _stop_network_worker(self):
        self.network_running = False
        if self.network_thread and self.network_thread.is_alive():
            self.network_thread.join(timeout=0.3)
            self.network_thread = None
        self.server_detections = []
        self.server_faces = []
        if hasattr(self, "bbox_overlay"):
            self.bbox_overlay.clear_boxes()

    def _network_loop(self):
        """Streams lightweight compressed JPEG frames to the AI Server."""
        offline_ticks = 0
        while self.network_running:
            if self.mode is None:
                time.sleep(0.08)
                continue

            frame_to_send = None
            with self.frame_lock:
                if self.latest_frame is not None:
                    if hasattr(self.latest_frame, "copy"):
                        frame_to_send = self.latest_frame.copy()
                    else:
                        frame_to_send = self.latest_frame

            if frame_to_send is None:
                time.sleep(0.04)
                continue

            try:
                image_bytes, mime_type = encode_frame_to_bytes(frame_to_send, target_w=480)
                if not image_bytes:
                    time.sleep(0.04)
                    continue

                url = f"{settings.server_url}/api/analyze"
                data = {
                    "mode": self.mode,
                    "find_target": self.find_target,
                    "language": settings.language
                }

                payload = None
                ext = "jpg" if mime_type == "image/jpeg" else "bmp"

                # Pure Python urllib multipart (zero pip wheel dependencies)
                try:
                    boundary = '----VisionAid' + hex(int(time.time() * 1000))[2:]
                    body = bytearray()
                    for k, v in data.items():
                        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode('utf-8'))
                    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="frame.{ext}"\r\nContent-Type: {mime_type}\r\n\r\n'.encode('utf-8'))
                    body.extend(image_bytes)
                    body.extend(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

                    req = urllib.request.Request(
                        url,
                        data=bytes(body),
                        headers={'Content-Type': f'multipart/form-data; boundary={boundary}', 'User-Agent': 'VisionAid-Mobile'}
                    )
                    import ssl
                    _ssl_ctx = None
                    try:
                        _ssl_ctx = ssl._create_unverified_context()
                    except Exception:
                        pass
                    with urllib.request.urlopen(req, timeout=2.8, context=_ssl_ctx) as resp:
                        if resp.status == 200:
                            payload = json.loads(resp.read().decode('utf-8'))
                except Exception:
                    # Fallback to requests if present
                    if requests is not None:
                        try:
                            files = {"file": (f"frame.{ext}", image_bytes, mime_type)}
                            r = requests.post(url, files=files, data=data, timeout=1.4)
                            if r.status_code == 200:
                                payload = r.json()
                        except Exception:
                            pass

                if payload is not None:
                    offline_ticks = 0
                    Clock.schedule_once(lambda dt, res=payload: self._on_server_response(res))
                    time.sleep(0.12)  # ~8 FPS smooth streaming
                else:
                    offline_ticks += 1
                    # Seamless local YOLO fallback when server is unreachable or offline
                    if LocalYOLO is not None and not self.local_model_failed and hasattr(frame_to_send, "shape") and self.mode in ("object", "obstacle", "find"):
                        if self.local_model is None:
                            try:
                                yolo_path = os.path.join(BASE_DIR, "yolo11n.pt")
                                if os.path.exists(yolo_path):
                                    self.local_model = LocalYOLO(yolo_path)
                                else:
                                    self.local_model = LocalYOLO("yolo11n.pt")
                            except Exception as le:
                                print("Local YOLO fallback error:", le)
                                self.local_model_failed = True

                        if self.local_model is not None:
                            try:
                                local_res = self.local_model(frame_to_send, imgsz=320, conf=0.30, iou=0.45, verbose=False)
                                fh, fw = frame_to_send.shape[:2]
                                f_area = float(fw * fh)
                                dets = []
                                for box in local_res[0].boxes:
                                    conf = float(box.conf[0])
                                    if conf < 0.30:
                                        continue
                                    x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                                    raw_name = self.local_model.names[int(box.cls[0])]
                                    obj_name = OBJECT_ALIASES.get(raw_name, raw_name)
                                    cx = (x1 + x2) / 2.0
                                    cy = (y1 + y2) / 2.0
                                    box_area = float(max(0, x2 - x1) * max(0, y2 - y1))
                                    area_ratio = box_area / max(1.0, f_area)
                                    pos = "left" if cx < fw * 0.35 else ("right" if cx > fw * 0.65 else "center")
                                    prox = "close" if area_ratio >= 0.18 else ("nearby" if area_ratio >= 0.04 else "distant")
                                    norm_bbox = [
                                        round(max(0.0, min(1.0, x1 / float(fw))), 4),
                                        round(max(0.0, min(1.0, y1 / float(fh))), 4),
                                        round(max(0.0, min(1.0, x2 / float(fw))), 4),
                                        round(max(0.0, min(1.0, y2 / float(fh))), 4),
                                    ]
                                    dets.append({
                                        "name": obj_name,
                                        "raw_name": raw_name,
                                        "conf": round(conf, 2),
                                        "confidence_pct": int(round(conf * 100)),
                                        "bbox": [x1, y1, x2, y2],
                                        "norm_bbox": norm_bbox,
                                        "area_ratio": area_ratio,
                                        "position": pos,
                                        "proximity": prox,
                                        "cx": cx,
                                        "cy": cy,
                                        "frame_w": fw,
                                        "frame_h": fh,
                                    })
                                dets.sort(key=lambda d: d["area_ratio"], reverse=True)
                                lang = settings.language or "en"
                                if dets:
                                    top = dets[:3]
                                    items = [f"{language_manager.translate_label(d['name'], lang)} ({d['confidence_pct']}%)" for d in top]
                                    hud = " • ".join(items)
                                    speech = language_manager.format_object_announcement(dets, lang)
                                else:
                                    hud = language_manager.get_string("no_objects_detected", lang)
                                    speech = None

                                fallback_payload = {
                                    "mode": self.mode,
                                    "hud_text": hud,
                                    "speech_text": speech,
                                    "detections": dets,
                                    "target_locked": False,
                                }
                                Clock.schedule_once(lambda dt, res=fallback_payload: self._on_server_response(res))
                                time.sleep(0.08)
                                continue
                            except Exception as infer_err:
                                print("Local inference exception:", infer_err)

                    if offline_ticks % 8 == 1:
                        Clock.schedule_once(lambda dt: setattr(self.hud_banner, "text", "Server offline. Set IP in Settings ⚙️"))
                    time.sleep(0.50)  # Back off smoothly when server is unreachable to avoid UI hang
            except Exception:
                time.sleep(0.50)

    def _on_server_response(self, res):
        if self.mode != res.get("mode"):
            return

        dets = res.get("detections", [])
        if dets:
            if res.get("hud_text"):
                self.hud_banner.text = res["hud_text"]
        else:
            if self.mode == "object":
                self.hud_banner.text = language_manager.get_string("no_objects_detected", settings.language)
            elif res.get("hud_text"):
                self.hud_banner.text = res["hud_text"]

        if res.get("play_sound"):
            snd = res["play_sound"]
            if snd.startswith("radar_"):
                pos = snd.replace("radar_", "")
                sound_manager.play_spatial_radar(pos)
            elif snd == "beacon_lock":
                sound_manager.play_beacon(is_locked=True)
            elif snd == "beacon_ping":
                sound_manager.play_beacon(is_locked=False)

        speech_text = res.get("speech_text")
        if speech_text:
            now = time.time()
            min_cd = 2.5  # Prevent audio chatter and queue buildup
            if self.mode == "object":
                obj_key = "_".join([f"{d.get('name')}_{d.get('position')}" for d in dets[:3]])
                if now - self.last_speech_time >= min_cd:
                    if (obj_key != self.last_spoken_key) or (now - self.last_speech_time >= 5.0):
                        speak(speech_text, interrupt=True)
                        self.last_spoken_text = speech_text
                        self.last_spoken_key = obj_key
                        self.last_speech_time = now
            elif self.mode == "obstacle":
                if now - self.last_speech_time >= 2.2:
                    if (speech_text != self.last_spoken_text) or (now - self.last_speech_time >= 4.0):
                        speak(speech_text, interrupt=True)
                        self.last_spoken_text = speech_text
                        self.last_speech_time = now
            elif self.mode == "find":
                is_locked = res.get("target_locked", False)
                lock_key = f"{is_locked}_{res.get('hud_text', '')}"
                if now - self.last_speech_time >= 2.5:
                    if (lock_key != self.last_spoken_key) or (now - self.last_speech_time >= 4.5):
                        speak(speech_text, interrupt=True)
                        self.last_spoken_text = speech_text
                        self.last_spoken_key = lock_key
                        self.last_speech_time = now
            elif self.mode == "face":
                faces = res.get("faces", [])
                face_key = "_".join([f"{f.get('name')}_{f.get('emotion')}" for f in faces[:2]])
                if now - self.last_speech_time >= 3.0:
                    if (face_key != self.last_spoken_key) or (now - self.last_speech_time >= 5.0):
                        speak(speech_text, interrupt=True)
                        self.last_spoken_text = speech_text
                        self.last_spoken_key = face_key
                        self.last_speech_time = now
            elif self.mode == "text":
                read_t = res.get("read_text", "").strip()
                if read_t and (now - self.last_speech_time >= 3.5):
                    if read_t != self.last_spoken_text:
                        speak(speech_text, interrupt=True)
                        self.last_spoken_text = read_t
                        self.last_speech_time = now

        self.server_detections = dets
        self.server_faces = res.get("faces", [])
        self.target_locked = res.get("target_locked", False)
        if hasattr(self, "bbox_overlay"):
            if dets:
                self.bbox_overlay.update_boxes(dets, is_mirrored=(self.camera_index == 1 or cv2 is not None))
            else:
                self.bbox_overlay.clear_boxes()


class VisionAidMobileApp(App):
    """VisionAid Mobile Application Root."""
    def build(self):
        self.title = "VisionAid Mobile"

        sm = ScreenManager(transition=SlideTransition(duration=0.25))

        self.language_screen = LanguageSelectionScreen(settings=settings, tts=tts, name="language_select")
        self.login_screen = LoginScreen(settings=settings, tts=tts, name="login")
        self.signup_screen = SignupScreen(settings=settings, tts=tts, name="signup")
        self.main_screen = MainScreen(name="main")
        self.settings_screen = SettingsScreen(settings=settings, tts=tts, name="settings")

        sm.add_widget(self.language_screen)
        sm.add_widget(self.login_screen)
        sm.add_widget(self.signup_screen)
        sm.add_widget(self.main_screen)
        sm.add_widget(self.settings_screen)

        if settings.current_user:
            sm.current = "main"
        elif not settings.language_selected:
            sm.current = "language_select"
        else:
            sm.current = "login"

        return sm

    def on_start(self):
        Clock.schedule_once(self._request_permissions_delayed, 0.6)
        from kivy.utils import platform as kivy_platform
        if kivy_platform not in ('android', 'ios'):
            threading.Thread(target=self._ensure_local_server, daemon=True).start()

    def _ensure_local_server(self):
        url = getattr(settings, "server_url", "http://127.0.0.1:8000")
        if "127.0.0.1" in url or "localhost" in url:
            try:
                urllib.request.urlopen(f"{url}/api/health", timeout=1.2)
            except Exception:
                import subprocess
                server_py = os.path.join(os.path.dirname(__file__), "server.py")
                if os.path.exists(server_py):
                    print("[VisionAid] Local AI Server is offline. Starting server.py automatically...")
                    subprocess.Popen([sys.executable, server_py], cwd=os.path.dirname(__file__))

    def _request_permissions_delayed(self, dt):
        from kivy.utils import platform as kivy_platform
        if kivy_platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO])
                print("Android camera/mic permissions requested safely")
            except Exception as e:
                print("Android permissions request error:", e)

    def on_stop(self):
        if hasattr(self, "main_screen") and self.main_screen is not None:
            try:
                self.main_screen.stop_camera()
            except Exception:
                pass


if __name__ == "__main__":
    VisionAidMobileApp().run()
