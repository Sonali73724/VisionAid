import os
import sys
import time
import threading
import cv2
import easyocr
import speech_recognition as sr
from ultralytics import YOLO

import torch
# Limit PyTorch threads to prevent CPU thread starvation of Kivy UI and camera loops
torch.set_num_threads(2)

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Kivy configuration & imports
from kivy.config import Config
Config.set('graphics', 'width', '420')
Config.set('graphics', 'height', '780')
Config.set('graphics', 'resizable', '1')

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
# pyrefly: ignore [missing-import]
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView

from settings import VisionSettings
from settings_screen import SettingsScreen
from tts_engine import TTSEngine
from sound_effects import sound_manager
from face_engine import FaceAnalyzer
from auth_screens import LanguageSelectionScreen, LoginScreen, SignupScreen

# Paths to Lilac & Pink textures and sharp vector icons
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

# Lilac & Pink Theme Colors
C_LILAC = (0.75, 0.52, 0.98, 1)          # #C084FC Soft Radiant Lilac
C_PINK = (0.96, 0.45, 0.71, 1)           # #F472B6 Blossom Pink
C_ROSE = (0.98, 0.44, 0.52, 1)           # #FB7185 Coral Rose
C_MAGENTA = (0.91, 0.47, 0.97, 1)        # #E879F9 Orchid Fuchsia
C_FIND = (0.98, 0.65, 0.42, 1)           # #FA9E6B Radiant Amber Bloom
C_RADAR = (0.42, 0.78, 0.98, 1)          # #6BC7FA Sky Lilac Blue
C_FACE = (0.86, 0.58, 0.98, 1)           # #DB94FA Celestial Violet
C_CRIMSON = (0.96, 0.25, 0.37, 1)        # #F43F5E Soft Crimson
C_TEXT_WHITE = (0.99, 0.96, 1.0, 1)      # #FDF4FF Warm Lilac-White
C_TEXT_MUTED = (0.76, 0.70, 0.86, 1)      # #C4B5FD Soft Lavender
C_BORDER_DEFAULT = (0.40, 0.24, 0.56, 0.8)

Window.size = (420, 780)
Window.clearcolor = (0.07, 0.04, 0.11, 1)

# Initialize AI Services
print("Initializing VisionAid AI engines...")
model = YOLO("yolo11n.pt")
print("YOLO ready")

reader = easyocr.Reader(["en"], gpu=False)
print("EasyOCR ready")

tts = TTSEngine()
settings = VisionSettings()
recognizer = sr.Recognizer()
try:
    microphone = sr.Microphone()
except Exception as e:
    microphone = None
    print("Microphone not available:", e)


def speak(text, interrupt=False):
    """Global async speech helper."""
    tts.speak(text, interrupt=interrupt)


# =====================================================================
# THREADED HIGH-FPS CAMERA STREAM
# =====================================================================

class ThreadedCamera:
    """Thread-safe, non-blocking camera reader that continuously captures frames in a background thread."""

    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.stopped = False
        self.grabbed = False
        self.frame = None
        self.lock = threading.Lock()

        if self.cap.isOpened():
            self.grabbed, self.frame = self.cap.read()
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()

    def is_opened(self):
        return self.cap is not None and self.cap.isOpened() and not self.stopped

    def _capture_loop(self):
        while not self.stopped:
            if self.cap is None or not self.cap.isOpened():
                break
            grabbed, frame = self.cap.read()
            if not grabbed or frame is None:
                time.sleep(0.01)
                continue
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame
            time.sleep(0.005)

    def read(self):
        with self.lock:
            if self.frame is None:
                return False, None
            return self.grabbed, self.frame

    def release(self):
        self.stopped = True
        if hasattr(self, "thread") and self.thread.is_alive():
            self.thread.join(timeout=0.4)
        if self.cap is not None:
            self.cap.release()
            self.cap = None


# =====================================================================
# CUSTOM WIDGETS: GRADIENT ACTION CARD WITH VECTOR ICON
# =====================================================================

class GradientActionCard(ButtonBehavior, BoxLayout):
    """An elegant card with smooth Lilac/Pink gradient textures and custom icons."""

    def __init__(self, icon_path, title, subtitle, accent_color, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(70)
        self.padding = [dp(12), dp(10), dp(14), dp(10)]
        self.spacing = dp(12)

        self.icon_path = icon_path
        self.accent_color = accent_color
        self.is_active = False

        # Card Canvas: Velvet Amethyst gradient with glowing lilac border
        with self.canvas.before:
            self.canvas_tint = Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)], source=TEX_CARD)
            self.canvas_border = Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)), width=1.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # 1. Left Icon Container
        icon_wrapper = BoxLayout(size_hint=(None, None), size=(dp(46), dp(46)), padding=dp(4))
        with icon_wrapper.canvas.before:
            Color(0.26, 0.14, 0.38, 0.9)
            self.icon_bg = RoundedRectangle(pos=icon_wrapper.pos, size=icon_wrapper.size, radius=[dp(12)])
            self.icon_border_color = Color(accent_color[0], accent_color[1], accent_color[2], 0.8)
            self.icon_border = Line(rounded_rectangle=(icon_wrapper.x, icon_wrapper.y, icon_wrapper.width, icon_wrapper.height, dp(12)), width=1.2)

        icon_wrapper.bind(pos=lambda *_: (setattr(self.icon_bg, "pos", icon_wrapper.pos),
                                          setattr(self.icon_border, "rounded_rectangle", (icon_wrapper.x, icon_wrapper.y, icon_wrapper.width, icon_wrapper.height, dp(12)))),
                          size=lambda *_: (setattr(self.icon_bg, "size", icon_wrapper.size),
                                           setattr(self.icon_border, "rounded_rectangle", (icon_wrapper.x, icon_wrapper.y, icon_wrapper.width, icon_wrapper.height, dp(12)))))

        self.icon_img = Image(source=self.icon_path, fit_mode="contain")
        icon_wrapper.add_widget(self.icon_img)
        self.add_widget(icon_wrapper)

        # 2. Middle Text Info
        info_box = BoxLayout(orientation="vertical", spacing=dp(2))
        self.title_lbl = Label(
            text=title,
            font_size=15,
            bold=True,
            color=C_TEXT_WHITE,
            halign="left",
            valign="bottom",
            size_hint=(1, 0.55)
        )
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))

        self.desc_lbl = Label(
            text=subtitle,
            font_size=12,
            color=C_TEXT_MUTED,
            halign="left",
            valign="top",
            size_hint=(1, 0.45)
        )
        self.desc_lbl.bind(size=self.desc_lbl.setter("text_size"))

        info_box.add_widget(self.title_lbl)
        info_box.add_widget(self.desc_lbl)
        self.add_widget(info_box)

        # 3. Right Status Pill
        self.status_tag = Label(
            text="START",
            font_size=11,
            bold=True,
            color=C_TEXT_MUTED,
            size_hint=(None, 1),
            width=dp(52),
            halign="right",
            valign="middle"
        )
        self.status_tag.bind(size=self.status_tag.setter("text_size"))
        self.add_widget(self.status_tag)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(16))

    def set_active(self, active):
        self.is_active = active
        if active:
            self.bg_rect.source = TEX_CARD_ACTIVE
            self.canvas_border.rgba = self.accent_color
            self.border_line.width = 1.8
            self.status_tag.text = "ACTIVE"
            self.status_tag.color = self.accent_color
        else:
            self.bg_rect.source = TEX_CARD
            self.canvas_border.rgba = C_BORDER_DEFAULT
            self.border_line.width = 1.2
            self.status_tag.text = "START"
            self.status_tag.color = C_TEXT_MUTED

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.is_active:
                self.canvas_tint.rgba = (0.88, 0.88, 0.88, 1)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if not self.is_active:
            self.canvas_tint.rgba = (1, 1, 1, 1)
        return super().on_touch_up(touch)


class StatusPill(BoxLayout):
    """An elegant status badge displaying a glowing status indicator icon and state text."""

    def __init__(self, icon_path=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, 1)
        self.width = dp(96)
        self.padding = [dp(6), dp(6), dp(8), dp(6)]
        self.spacing = dp(4)

        with self.canvas.before:
            self.canvas_bg = Color(0.20, 0.12, 0.32, 0.90)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            self.canvas_border = Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.status_icon = Image(
            source=icon_path or ICON_STATUS,
            size_hint=(None, 1),
            width=dp(16),
            fit_mode="contain",
            color=C_LILAC
        )
        self.text_lbl = Label(
            text="STANDBY",
            font_size=10.5,
            bold=True,
            color=C_LILAC,
            halign="center",
            valign="middle"
        )

        self.add_widget(self.status_icon)
        self.add_widget(self.text_lbl)
        self._text = "● STANDBY"

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val
        clean = val.replace("●", "").replace("•", "").strip()
        self.text_lbl.text = clean

    @property
    def color(self):
        return self.text_lbl.color

    @color.setter
    def color(self, val):
        self.text_lbl.color = val
        self.status_icon.color = val

    @property
    def text_size(self):
        return self.text_lbl.text_size

    @text_size.setter
    def text_size(self, val):
        self.text_lbl.text_size = val

    def setter(self, name):
        if name == "text_size":
            return lambda _, val: setattr(self.text_lbl, "text_size", val)
        return super().setter(name)


class SettingsPillButton(ButtonBehavior, BoxLayout):
    """An elegant pill button displaying a glowing gear icon and SETTINGS text."""

    def __init__(self, icon_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, 1)
        self.width = dp(112)
        self.padding = [dp(8), dp(6), dp(10), dp(6)]
        self.spacing = dp(6)

        with self.canvas.before:
            self.canvas_bg = Color(0.24, 0.14, 0.38, 0.95)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            self.canvas_border = Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.3)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.gear_icon = Image(
            source=icon_path,
            size_hint=(None, 1),
            width=dp(22),
            fit_mode="contain"
        )
        self.text_lbl = Label(
            text="SETTINGS",
            font_size=11,
            bold=True,
            color=C_TEXT_WHITE,
            halign="center",
            valign="middle"
        )

        self.add_widget(self.gear_icon)
        self.add_widget(self.text_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.canvas_bg.rgba = (0.38, 0.20, 0.58, 1)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.canvas_bg.rgba = (0.24, 0.14, 0.38, 0.95)
        return super().on_touch_up(touch)


# =====================================================================
# MAIN APPLICATION SCREEN
# =====================================================================

class MainScreen(Screen):
    """The central VisionAid assistive dashboard with Lilac & Pink luxury styling."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.mode = None
        self.frame_count = 0

        # Threaded AI Inference Engine
        self.inference_thread = None
        self.inference_running = False
        self.latest_detections = []
        self.detections_lock = threading.Lock()
        self.latest_frame_for_inference = None
        self.frame_available_event = threading.Event()

        # Speech cooldowns
        self.last_spoken_objects = ""
        self.last_speech_time = 0
        self.speech_interval = 4

        # Async OCR state
        self.last_ocr_time = 0
        self.ocr_interval = 2.5
        self.last_read_text = ""
        self.ocr_busy = False
        self.ocr_session_id = 0

        # Obstacle state
        self.last_obstacle_message = ""
        self.last_obstacle_time = 0
        self.obstacle_interval = 3

        # Option 1: Find My Object (Auditory Radar Beacon)
        self.find_target = "cup"
        self.target_locked = False
        self.last_target_spoken_time = 0
        self.last_target_spoken_msg = ""
        self.last_beacon_time = 0

        # Option 3: Spatial Audio Radar
        self.last_radar_time = 0

        # Option 6: Familiar Face & Emotion Recognition
        self.face_analyzer = FaceAnalyzer()
        self.face_lock = threading.Lock()
        self.latest_face_results = []
        self.last_face_speech_time = 0
        self.last_spoken_face = ""

        # Voice state
        self.listening = False

        self._build_ui()

    def _build_ui(self):
        root_box = BoxLayout(orientation="vertical", padding=[dp(16), dp(14), dp(16), dp(16)], spacing=dp(10))

        # Background canvas: Deep Midnight Orchid gradient texture
        with root_box.canvas.before:
            Color(1, 1, 1, 1)
            self.root_bg = RoundedRectangle(pos=root_box.pos, size=root_box.size, source=TEX_BG)

        root_box.bind(pos=lambda _, v: setattr(self.root_bg, "pos", v),
                      size=lambda _, v: setattr(self.root_bg, "size", v))

        # -------------------------------------------------------------
        # 1. TOP HEADER BAR
        # -------------------------------------------------------------
        header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(8))

        # Brand Title
        brand_box = BoxLayout(orientation="vertical", size_hint=(1, 1), spacing=dp(1))
        app_title = Label(
            text="[b][color=C084FC]VISION[/color][color=F472B6]AID[/color][/b]",
            markup=True,
            font_size=23,
            halign="left",
            valign="bottom",
            size_hint=(1, 0.6)
        )
        app_title.bind(size=app_title.setter("text_size"))

        app_subtitle = Label(
            text="AI Accessibility Companion",
            font_size=11,
            color=C_TEXT_MUTED,
            halign="left",
            valign="top",
            size_hint=(1, 0.4)
        )
        app_subtitle.bind(size=app_subtitle.setter("text_size"))

        brand_box.add_widget(app_title)
        brand_box.add_widget(app_subtitle)

        # Status Pill with Glowing Status Indicator Icon & Text
        self.status_pill = StatusPill(icon_path=ICON_STATUS)

        # Settings Button with Custom Gear Icon & Text (100% visible & properly laid out)
        settings_btn = SettingsPillButton(icon_path=ICON_SETTINGS)
        settings_btn.bind(on_press=self.open_settings)

        header.add_widget(brand_box)
        header.add_widget(self.status_pill)
        header.add_widget(settings_btn)
        root_box.add_widget(header)

        # -------------------------------------------------------------
        # 2. CAMERA VIEWPORT & HUD CONTAINER
        # -------------------------------------------------------------
        viewport_wrapper = RelativeLayout(size_hint=(1, 0.40))

        with viewport_wrapper.canvas.before:
            Color(0.12, 0.07, 0.18, 1)
            self.vp_bg = RoundedRectangle(pos=(0, 0), size=viewport_wrapper.size, radius=[dp(18)])
            Color(0.55, 0.32, 0.75, 0.9)
            self.vp_border = Line(rounded_rectangle=(0, 0, viewport_wrapper.width, viewport_wrapper.height, dp(18)), width=1.5)

        viewport_wrapper.bind(size=self._update_viewport_canvas)

        # Live Camera Texture Image
        self.camera_image = Image(
            fit_mode="contain",
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            opacity=0
        )

        # Empty State Placeholder Card (Lilac & Pink Camera Icon)
        self.placeholder = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            padding=dp(14),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        cam_icon_img = Image(
            source=ICON_CAMERA,
            size_hint=(1, 0.42),
            fit_mode="contain"
        )
        ready_title = Label(
            text="Vision Camera Standby",
            font_size=16,
            bold=True,
            color=C_TEXT_WHITE,
            size_hint=(1, 0.32),
            halign="center"
        )
        ready_sub = Label(
            text="Select an AI mode below to activate vision assistance",
            font_size=12,
            color=C_TEXT_MUTED,
            size_hint=(1, 0.26),
            halign="center"
        )
        self.placeholder.add_widget(cam_icon_img)
        self.placeholder.add_widget(ready_title)
        self.placeholder.add_widget(ready_sub)

        # Mode Chip (Floating top-left badge)
        self.mode_chip = Label(
            text="IDLE",
            font_size=11,
            bold=True,
            color=C_PINK,
            size_hint=(None, None),
            size=(dp(135), dp(26)),
            pos_hint={"x": 0.04, "top": 0.94},
            opacity=0
        )
        with self.mode_chip.canvas.before:
            Color(0.16, 0.09, 0.24, 0.90)
            self.mode_chip_bg = RoundedRectangle(pos=self.mode_chip.pos, size=self.mode_chip.size, radius=[dp(8)])
            Color(*C_BORDER_DEFAULT)
            self.mode_chip_border = Line(rounded_rectangle=(self.mode_chip.x, self.mode_chip.y, self.mode_chip.width, self.mode_chip.height, dp(8)), width=1.1)

        self.mode_chip.bind(pos=lambda *_: (setattr(self.mode_chip_bg, "pos", self.mode_chip.pos),
                                            setattr(self.mode_chip_border, "rounded_rectangle", (self.mode_chip.x, self.mode_chip.y, self.mode_chip.width, self.mode_chip.height, dp(8)))),
                            size=lambda *_: (setattr(self.mode_chip_bg, "size", self.mode_chip.size),
                                             setattr(self.mode_chip_border, "rounded_rectangle", (self.mode_chip.x, self.mode_chip.y, self.mode_chip.width, self.mode_chip.height, dp(8)))))

        # Floating HUD Banner (Frosted Lilac gradient bar at bottom of viewport)
        self.hud_banner = Label(
            text="System ready to assist you.",
            font_size=13,
            bold=True,
            color=C_TEXT_WHITE,
            size_hint=(0.92, None),
            height=dp(38),
            pos_hint={"center_x": 0.5, "y": 0.04},
            halign="center",
            valign="middle"
        )
        self.hud_banner.bind(size=self.hud_banner.setter("text_size"))
        with self.hud_banner.canvas.before:
            Color(1, 1, 1, 1)
            self.hud_bg = RoundedRectangle(pos=self.hud_banner.pos, size=self.hud_banner.size, radius=[dp(12)], source=TEX_HUD)
            Color(0.65, 0.40, 0.85, 0.8)
            self.hud_border = Line(rounded_rectangle=(self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)), width=1.2)

        self.hud_banner.bind(pos=lambda *_: (setattr(self.hud_bg, "pos", self.hud_banner.pos),
                                            setattr(self.hud_border, "rounded_rectangle", (self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)))),
                             size=lambda *_: (setattr(self.hud_bg, "size", self.hud_banner.size),
                                             setattr(self.hud_border, "rounded_rectangle", (self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)))))

        viewport_wrapper.add_widget(self.placeholder)
        viewport_wrapper.add_widget(self.camera_image)
        viewport_wrapper.add_widget(self.mode_chip)
        viewport_wrapper.add_widget(self.hud_banner)

        root_box.add_widget(viewport_wrapper)

        # -------------------------------------------------------------
        # 3. INTERACTIVE AI ACTION CARDS (Scrollable)
        # -------------------------------------------------------------
        scroll = ScrollView(size_hint=(1, 0.60), do_scroll_x=False, bar_width=dp(3))
        card_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, dp(4), 0, dp(8)])
        card_list.bind(minimum_height=card_list.setter("height"))

        # Card 1: Object Detection (Radiant Lilac)
        self.card_object = GradientActionCard(
            icon_path=ICON_EYE,
            title="Object Detection",
            subtitle="Identify everyday objects, items & surroundings",
            accent_color=C_LILAC
        )
        self.card_object.bind(on_press=lambda _: self.start_mode("object"))
        card_list.add_widget(self.card_object)

        # Card 2: Find My Object (Radiant Amber Bloom - Option 1)
        self.card_find = GradientActionCard(
            icon_path=ICON_FIND,
            title="Find My Object",
            subtitle="Auditory radar beacon guides you directly to items",
            accent_color=C_FIND
        )
        self.card_find.bind(on_press=lambda _: self.start_mode("find"))
        card_list.add_widget(self.card_find)

        # Card 3: Spatial Audio Radar (Sky Lilac Blue - Option 3)
        self.card_radar = GradientActionCard(
            icon_path=ICON_RADAR,
            title="Spatial Audio Radar",
            subtitle="Directional stereo pulses alert to obstacles without speech",
            accent_color=C_RADAR
        )
        self.card_radar.bind(on_press=lambda _: self.start_mode("radar"))
        card_list.add_widget(self.card_radar)

        # Card 4: Face & Emotion Companion (Celestial Violet - Option 6)
        self.card_face = GradientActionCard(
            icon_path=ICON_FACE,
            title="Face & Emotion Companion",
            subtitle="Identify familiar contacts, smiling expressions & positions",
            accent_color=C_FACE
        )
        self.card_face.bind(on_press=lambda _: self.start_mode("face"))
        card_list.add_widget(self.card_face)

        # Card 5: Read Text (Blossom Pink)
        self.card_text = GradientActionCard(
            icon_path=ICON_TEXT,
            title="Read Text",
            subtitle="Recognize documents, signage, packaging & books",
            accent_color=C_PINK
        )
        self.card_text.bind(on_press=lambda _: self.start_mode("text"))
        card_list.add_widget(self.card_text)

        # Card 6: Obstacle Alert (Coral Rose)
        self.card_obstacle = GradientActionCard(
            icon_path=ICON_SHIELD,
            title="Obstacle Guidance",
            subtitle="Real-time proximity warnings & distance alerts",
            accent_color=C_ROSE
        )
        self.card_obstacle.bind(on_press=lambda _: self.start_mode("obstacle"))
        card_list.add_widget(self.card_obstacle)

        # Card 7: Voice Assistant (Orchid Fuchsia)
        self.card_voice = GradientActionCard(
            icon_path=ICON_MIC,
            title="Voice Assistant",
            subtitle="Hands-free control ('find cup', 'radar', 'face', 'read')",
            accent_color=C_MAGENTA
        )
        self.card_voice.bind(on_press=self.start_voice_command)
        card_list.add_widget(self.card_voice)

        # Card 8: Stop Camera (Soft Crimson)
        self.card_stop = GradientActionCard(
            icon_path=ICON_STOP,
            title="Stop Camera",
            subtitle="Turn off video feed & pause vision analysis",
            accent_color=C_CRIMSON
        )
        self.card_stop.bind(on_press=self.stop_camera)
        card_list.add_widget(self.card_stop)

        scroll.add_widget(card_list)
        root_box.add_widget(scroll)

        self.add_widget(root_box)

    def _update_viewport_canvas(self, instance, value):
        self.vp_bg.size = instance.size
        self.vp_border.rounded_rectangle = (0, 0, instance.width, instance.height, dp(18))

    # =================================================================
    # NAVIGATION
    # =================================================================

    def open_settings(self, instance):
        if self.manager:
            self.manager.transition.direction = "left"
            self.manager.current = "settings"

    # =================================================================
    # CAMERA & INFERENCE CONTROLS
    # =================================================================

    def open_camera(self):
        if self.camera is not None and self.camera.is_opened():
            return True

        print("Opening threaded camera stream...")
        self.camera = ThreadedCamera(0, 640, 480)

        if not self.camera.is_opened():
            print("❌ Camera could not be opened")
            self.hud_banner.text = "Error: Could not access camera."
            self.status_pill.text = "● CAM ERROR"
            self.status_pill.color = C_CRIMSON
            speak("Could not access camera device", interrupt=True)
            self.camera = None
            return False

        print("✅ Threaded camera opened successfully")
        self.placeholder.opacity = 0
        self.camera_image.opacity = 1
        self._start_inference_worker()
        return True

    def stop_camera(self, instance=None):
        print("Stopping camera...")
        Clock.unschedule(self.update_camera)
        self._stop_inference_worker()

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.mode = None
        self.camera_image.texture = None
        self.camera_image.opacity = 0
        self.placeholder.opacity = 1
        self.mode_chip.opacity = 0

        self.status_pill.text = "● STANDBY"
        self.status_pill.color = C_LILAC
        self.hud_banner.text = "Camera stopped. Ready to assist."

        # Reset card highlights
        self.card_object.set_active(False)
        self.card_find.set_active(False)
        self.card_radar.set_active(False)
        self.card_face.set_active(False)
        self.card_text.set_active(False)
        self.card_obstacle.set_active(False)
        self.card_voice.set_active(False)

        tts.stop()
        speak("Camera stopped", interrupt=True)

    def _start_inference_worker(self):
        if self.inference_running:
            return
        self.inference_running = True
        self.frame_available_event.clear()
        self.inference_thread = threading.Thread(target=self._inference_loop, daemon=True)
        self.inference_thread.start()

    def _stop_inference_worker(self):
        self.inference_running = False
        self.frame_available_event.set()
        if self.inference_thread and self.inference_thread.is_alive():
            self.inference_thread.join(timeout=0.3)
            self.inference_thread = None
        with self.detections_lock:
            self.latest_detections = []
            self.latest_frame_for_inference = None
        with self.face_lock:
            self.latest_face_results = []

    def _inference_loop(self):
        """Background AI worker executing YOLO and Face inference without blocking UI thread."""
        while self.inference_running:
            self.frame_available_event.wait(timeout=0.08)
            self.frame_available_event.clear()
            if not self.inference_running:
                break

            mode_to_process = self.mode
            if mode_to_process not in ("object", "obstacle", "find", "radar", "face"):
                time.sleep(0.02)
                continue

            frame_to_process = None
            with self.detections_lock:
                if self.latest_frame_for_inference is not None:
                    frame_to_process = self.latest_frame_for_inference
                    self.latest_frame_for_inference = None

            if frame_to_process is None:
                time.sleep(0.01)
                continue

            h, w = frame_to_process.shape[:2]
            frame_area = float(w * h)

            try:
                if mode_to_process in ("object", "obstacle", "find", "radar"):
                    # Fast CPU inference at 320px (~30ms) with conf=0.45 to eliminate false positives
                    results = model(frame_to_process, imgsz=320, conf=0.45, verbose=False)

                    # Discard results if user switched modes during calculation
                    if self.mode != mode_to_process:
                        continue

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

                        # Display mirror coordinate conversion (flip horizontal)
                        display_cx = w - cx
                        if display_cx < w * 0.35:
                            position = "left"
                        elif display_cx > w * 0.65:
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
                            "bbox": (w - x2, y1, w - x1, y2),
                            "area_ratio": area_ratio,
                            "position": position,
                            "proximity": proximity,
                            "cx": display_cx,
                            "cy": cy
                        })

                    detections.sort(key=lambda d: d["area_ratio"], reverse=True)

                    if self.mode == mode_to_process:
                        with self.detections_lock:
                            self.latest_detections = detections

                        Clock.schedule_once(lambda dt, m=mode_to_process, dets=detections, fw=w, fh=h: self._handle_detection_announcements(m, dets, fw, fh))

                elif mode_to_process == "face":
                    face_results = self.face_analyzer.analyze_faces(frame_to_process)
                    if self.mode == "face":
                        with self.face_lock:
                            self.latest_face_results = face_results
                        Clock.schedule_once(lambda dt, faces=face_results: self._handle_face_announcements(faces))

            except Exception as e:
                print("Inference error:", e)

            # Throttle inference to leave ample CPU headroom for smooth video
            time.sleep(0.06)

    # =================================================================
    # MODE SWITCHING
    # =================================================================

    def start_mode(self, mode):
        # 1. Immediately silence previous speech & cancel in-flight tasks
        tts.stop()
        self.ocr_session_id += 1
        self.ocr_busy = False
        with self.detections_lock:
            self.latest_detections = []
            self.latest_frame_for_inference = None
        with self.face_lock:
            self.latest_face_results = []

        self.last_spoken_objects = ""
        self.last_obstacle_message = ""
        self.last_read_text = ""
        self.last_speech_time = 0
        self.last_obstacle_time = 0
        self.last_ocr_time = 0
        self.last_target_spoken_time = 0
        self.last_target_spoken_msg = ""
        self.last_radar_time = 0
        self.last_face_speech_time = 0
        self.last_spoken_face = ""
        self.target_locked = False

        if not self.open_camera():
            return

        self.mode = mode
        self.frame_count = 0

        # Update card highlights
        self.card_object.set_active(mode == "object")
        self.card_find.set_active(mode == "find")
        self.card_radar.set_active(mode == "radar")
        self.card_face.set_active(mode == "face")
        self.card_text.set_active(mode == "text")
        self.card_obstacle.set_active(mode == "obstacle")
        self.card_voice.set_active(False)

        self.mode_chip.opacity = 1

        if mode == "object":
            self.status_pill.text = "● OBJECTS"
            self.status_pill.color = C_LILAC
            self.mode_chip.text = "OBJECT DETECTION"
            self.mode_chip.color = C_LILAC
            self.hud_banner.text = "Scanning surroundings for objects..."
            speak("Object detection started", interrupt=True)

        elif mode == "find":
            self.status_pill.text = "● RADAR BEACON"
            self.status_pill.color = C_FIND
            self.mode_chip.text = f"FIND: {self.find_target.upper()}"
            self.mode_chip.color = C_FIND
            self.hud_banner.text = f"Auditory beacon active. Pan camera to find {self.find_target}..."
            speak(f"Find my object started. Searching for {self.find_target}. Pan camera slowly.", interrupt=True)

        elif mode == "radar":
            self.status_pill.text = "● SPATIAL RADAR"
            self.status_pill.color = C_RADAR
            self.mode_chip.text = "SPATIAL AUDIO RADAR"
            self.mode_chip.color = C_RADAR
            self.hud_banner.text = "Spatial radar active. Stereo tones indicate obstacles..."
            speak("Spatial audio radar activated. Listen for left and right acoustic cues.", interrupt=True)

        elif mode == "face":
            self.status_pill.text = "● FACE & EMOTION"
            self.status_pill.color = C_FACE
            self.mode_chip.text = "FACE & EMOTION COMPANION"
            self.mode_chip.color = C_FACE
            self.hud_banner.text = "Scanning for companions, familiar faces and expressions..."
            speak("Face and emotion companion started. Point camera towards people.", interrupt=True)

        elif mode == "text":
            self.status_pill.text = "● TEXT OCR"
            self.status_pill.color = C_PINK
            self.mode_chip.text = "READ TEXT"
            self.mode_chip.color = C_PINK
            self.hud_banner.text = "Point camera at any printed text..."
            speak("Text reader started", interrupt=True)

        elif mode == "obstacle":
            self.status_pill.text = "● OBSTACLES"
            self.status_pill.color = C_ROSE
            self.mode_chip.text = "OBSTACLE GUIDANCE"
            self.mode_chip.color = C_ROSE
            self.hud_banner.text = "Monitoring path for obstacles..."
            speak("Obstacle guidance started", interrupt=True)

        Clock.unschedule(self.update_camera)
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

    # =================================================================
    # MAIN CAMERA LOOP (30 FPS)
    # =================================================================

    def update_camera(self, dt):
        if self.camera is None:
            return

        ret, frame = self.camera.read()
        if not ret or frame is None:
            return

        self.frame_count += 1

        # Mirror frame once for preview
        display_frame = cv2.flip(frame, 1)
        fh, fw = display_frame.shape[:2]

        # -------------------------------------------------------------
        # OBJECT, OBSTACLE, RADAR & FIND DETECTION (Non-blocking background feed)
        # -------------------------------------------------------------
        if self.mode in ("object", "obstacle", "radar", "find"):
            # Queue frame for background inference
            with self.detections_lock:
                if self.latest_frame_for_inference is None:
                    self.latest_frame_for_inference = frame
                    self.frame_available_event.set()
                current_dets = list(self.latest_detections)

            if self.mode in ("object", "obstacle", "radar"):
                for d in current_dets:
                    x1, y1, x2, y2 = d["bbox"]
                    x1 = max(0, min(fw, x1))
                    y1 = max(0, min(fh, y1))
                    x2 = max(0, min(fw, x2))
                    y2 = max(0, min(fh, y2))

                    if self.mode == "radar":
                        color = (250, 199, 107)  # Sky Lilac / Cyan in BGR
                        pos_indicator = "C" if d["position"] == "center" else ("L" if d["position"] == "left" else "R")
                        lbl = f"{d['name']} [RADAR: {pos_indicator}]"
                    else:
                        color = (244, 114, 182) if d["position"] == "center" else (192, 132, 252) # BGR
                        pos_indicator = "C" if d["position"] == "center" else ("L" if d["position"] == "left" else "R")
                        lbl = f"{d['name']} [{pos_indicator}]"

                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                    (tw, th), _ = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)
                    bg_y1 = max(0, y1 - th - 8)
                    cv2.rectangle(display_frame, (x1, bg_y1), (min(fw, x1 + tw + 8), max(0, y1)), color, -1)
                    cv2.putText(display_frame, lbl, (x1 + 4, max(th + 2, y1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

            elif self.mode == "find":
                target = self.find_target.lower().strip()
                synonyms = {
                    "phone": ["cell phone", "phone", "telephone"],
                    "mobile": ["cell phone", "phone"],
                    "bottle": ["bottle", "wine glass", "cup"],
                    "cup": ["cup", "bottle", "bowl", "mug"],
                    "glasses": ["glasses", "sunglasses"],
                    "specs": ["glasses"],
                    "keys": ["key", "remote", "scissors"],
                    "computer": ["laptop", "tv", "keyboard", "mouse"],
                    "laptop": ["laptop"],
                    "person": ["person"],
                    "chair": ["chair", "couch", "bench"]
                }
                candidates = synonyms.get(target, [target])
                matching = [d for d in current_dets if any(cand in d["name"].lower() for cand in candidates)]

                if matching:
                    best = matching[0]
                    x1, y1, x2, y2 = best["bbox"]
                    x1 = max(0, min(fw, x1))
                    y1 = max(0, min(fh, y1))
                    x2 = max(0, min(fw, x2))
                    y2 = max(0, min(fh, y2))

                    # Radiant Amber or Emerald Locked Color
                    color = (100, 220, 120) if self.target_locked else (66, 165, 250)
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 3 if self.target_locked else 2)

                    # Center crosshair target reticle
                    t_cx = int((x1 + x2) / 2)
                    t_cy = int((y1 + y2) / 2)
                    cv2.drawMarker(display_frame, (t_cx, t_cy), color, cv2.MARKER_CROSS, 24, 2)

                    if self.target_locked:
                        lbl = f"LOCKED: {best['name'].upper()}"
                    else:
                        cue = "<-- PAN LEFT" if (best["cx"] < fw * 0.45) else ("PAN RIGHT -->" if best["cx"] > fw * 0.55 else "CENTERING...")
                        lbl = f"{best['name'].upper()} [{cue}]"

                    (tw, th), _ = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.50, 1)
                    bg_y1 = max(0, y1 - th - 8)
                    cv2.rectangle(display_frame, (x1, bg_y1), (min(fw, x1 + tw + 8), max(0, y1)), color, -1)
                    cv2.putText(display_frame, lbl, (x1 + 4, max(th + 2, y1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 1, cv2.LINE_AA)

        # -------------------------------------------------------------
        # FACE & EMOTION COMPANION
        # -------------------------------------------------------------
        elif self.mode == "face":
            # Queue frame for face analysis
            with self.detections_lock:
                if self.latest_frame_for_inference is None:
                    self.latest_frame_for_inference = frame
                    self.frame_available_event.set()

            with self.face_lock:
                faces = list(self.latest_face_results)

            for face in faces:
                x, y, w, h = face["box"]
                # Display frame is flipped horizontally
                disp_x = max(0, min(fw, fw - (x + w)))
                color = (250, 148, 219) if not face["is_smiling"] else (182, 114, 244) # Celestial Violet / Warm Rose
                cv2.rectangle(display_frame, (disp_x, y), (disp_x + w, y + h), color, 2)
                
                lbl = f"{face['name']} [{face['emotion'].upper()}]"
                (tw, th), _ = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)
                bg_y1 = max(0, y - th - 8)
                cv2.rectangle(display_frame, (disp_x, bg_y1), (min(fw, disp_x + tw + 8), max(0, y)), color, -1)
                cv2.putText(display_frame, lbl, (disp_x + 4, max(th + 2, y - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

        # -------------------------------------------------------------
        # TEXT READER (Async OCR with session tracking)
        # -------------------------------------------------------------
        elif self.mode == "text":
            now = time.time()
            if not self.ocr_busy and (now - self.last_ocr_time >= self.ocr_interval):
                self.last_ocr_time = now
                self.ocr_busy = True
                frame_copy = frame.copy()
                session = self.ocr_session_id
                threading.Thread(target=self._run_async_ocr, args=(frame_copy, session), daemon=True).start()

        # -------------------------------------------------------------
        # BLIT FRAME TO TEXTURE (Fluid 30+ FPS)
        # -------------------------------------------------------------
        rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)

        if self.camera_image.texture is None or self.camera_image.texture.size != (fw, fh):
            self.camera_image.texture = Texture.create(size=(fw, fh), colorfmt="rgb")

        self.camera_image.texture.blit_buffer(rgb_frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        self.camera_image.texture.flip_vertical()

    # =================================================================
    # ASYNC OCR WORKER (Optimized 384px resolution)
    # =================================================================

    def _run_async_ocr(self, frame, session_id):
        try:
            h, w = frame.shape[:2]
            scale = 384.0 / max(w, 1)
            target_size = (384, int(h * scale))
            small_frame = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)

            ocr_results = reader.readtext(small_frame)
            if session_id != self.ocr_session_id or self.mode != "text":
                self.ocr_busy = False
                return

            detected = [r[1].strip() for r in ocr_results if r[2] >= 0.40 and len(r[1].strip()) > 1]
            Clock.schedule_once(lambda dt: self._on_ocr_complete(detected, session_id))
        except Exception as e:
            print("OCR Error:", e)
            self.ocr_busy = False

    def _on_ocr_complete(self, detected_text, session_id):
        self.ocr_busy = False
        if session_id != self.ocr_session_id or self.mode != "text":
            return

        if detected_text:
            full_text = " ".join(detected_text)
            self.hud_banner.text = f"Read: {full_text[:50]}..."
            if full_text != self.last_read_text:
                speak("I can read: " + full_text)
                self.last_read_text = full_text
        else:
            self.hud_banner.text = "Scanning for text..."

    # =================================================================
    # RICH SPATIAL & PROXIMITY ANNOUNCEMENTS
    # =================================================================

    def _handle_detection_announcements(self, mode, detections, fw=640, fh=480):
        if self.mode != mode:
            return

        now = time.time()
        if mode == "object":
            if not detections:
                self.hud_banner.text = "Scanning surroundings for objects..."
                return

            hud_items = []
            for d in detections[:3]:
                pos_str = "in front" if d["position"] == "center" else d["position"]
                hud_items.append(f"{d['name'].capitalize()} ({pos_str}, {d['proximity']})")
            self.hud_banner.text = " • ".join(hud_items)

            unique_top = []
            seen = set()
            for d in detections:
                if d["name"] not in seen:
                    seen.add(d["name"])
                    unique_top.append(d)
                if len(unique_top) >= 3:
                    break

            speech_key = "_".join([f"{d['name']}_{d['position']}_{d['proximity']}" for d in unique_top])
            if speech_key != self.last_spoken_objects and (now - self.last_speech_time >= self.speech_interval):
                sentence = self._create_spatial_sentence(unique_top)
                speak(sentence)
                self.last_spoken_objects = speech_key
                self.last_speech_time = now

        elif mode == "obstacle":
            if not detections:
                self.hud_banner.text = "Path appears clear"
                return

            def obstacle_priority(d):
                score = d["area_ratio"]
                if d["position"] == "center":
                    score += 0.25
                return score

            critical = max(detections, key=obstacle_priority)
            obj_name = critical["name"]
            pos = critical["position"]
            ratio = critical["area_ratio"]
            pos_desc = "directly in front of you" if pos == "center" else f"on your {pos}"

            is_warning = ratio >= settings.obstacle_threshold or (pos == "center" and ratio >= 0.12)
            if is_warning:
                message = f"Warning! {obj_name} is very close {pos_desc}."
            elif ratio >= 0.05:
                message = f"Caution, {obj_name} nearby {pos_desc}."
            else:
                message = f"{obj_name.capitalize()} {pos_desc}."

            self.hud_banner.text = message
            if message != self.last_obstacle_message and (now - self.last_obstacle_time >= self.obstacle_interval):
                speak(message, interrupt=is_warning)
                self.last_obstacle_message = message
                self.last_obstacle_time = now

        elif mode == "radar":
            if not detections:
                self.hud_banner.text = "Path appears clear • No obstacles detected"
                return

            def obstacle_priority(d):
                score = d["area_ratio"]
                if d["position"] == "center":
                    score += 0.25
                return score

            critical = max(detections, key=obstacle_priority)
            pos = critical["position"]
            obj_name = critical["name"]
            prox = critical["proximity"]

            # Directional stereo radar pulse
            sound_manager.play_spatial_radar(pos)
            self.hud_banner.text = f"Radar Tone: {obj_name.capitalize()} on {pos.upper()} ({prox})"

        elif mode == "find":
            target = self.find_target.lower().strip()
            synonyms = {
                "phone": ["cell phone", "phone", "telephone"],
                "mobile": ["cell phone", "phone"],
                "bottle": ["bottle", "wine glass", "cup"],
                "cup": ["cup", "bottle", "bowl", "mug"],
                "glasses": ["glasses", "sunglasses"],
                "specs": ["glasses"],
                "keys": ["key", "remote", "scissors"],
                "computer": ["laptop", "tv", "keyboard", "mouse"],
                "laptop": ["laptop"],
                "person": ["person"],
                "chair": ["chair", "couch", "bench"]
            }
            candidates = synonyms.get(target, [target])

            matching = [d for d in detections if any(cand in d["name"].lower() for cand in candidates)]
            if not matching:
                self.target_locked = False
                self.hud_banner.text = f"Searching for {self.find_target}... Pan camera slowly"
                if now - self.last_target_spoken_time >= 5.0:
                    speak(f"Searching for {self.find_target}. Pan camera slowly.")
                    self.last_target_spoken_time = now
                return

            best = matching[0]
            cx = best["cx"]
            frame_center = fw / 2.0
            offset = cx - frame_center
            abs_offset = abs(offset)
            is_locked = abs_offset < (fw * 0.12)
            self.target_locked = is_locked

            # Play auditory beacon audio
            sound_manager.play_beacon(is_locked=is_locked)

            if is_locked:
                self.hud_banner.text = f"TARGET LOCKED! {best['name'].capitalize()} is directly in front of you."
                if now - self.last_target_spoken_time >= 3.0 or self.last_target_spoken_msg != "locked":
                    speak(f"Target locked! {best['name']} is directly in front of you.", interrupt=True)
                    self.last_target_spoken_time = now
                    self.last_target_spoken_msg = "locked"
            else:
                dir_cue = "left" if offset < 0 else "right"
                self.hud_banner.text = f"Target Detected: {best['name'].capitalize()} • Move camera {dir_cue.upper()}"
                if now - self.last_target_spoken_time >= 3.2 or self.last_target_spoken_msg != dir_cue:
                    speak(f"{best['name']} is on your {dir_cue}. Move camera {dir_cue}.")
                    self.last_target_spoken_time = now
                    self.last_target_spoken_msg = dir_cue

    def _handle_face_announcements(self, faces):
        if self.mode != "face":
            return
        now = time.time()
        if not faces:
            self.hud_banner.text = "No faces in view • Looking for companions..."
            return

        summaries = [f"{f['name']}: {f['emotion']} ({f['position']})" for f in faces[:2]]
        self.hud_banner.text = " • ".join(summaries)

        primary = faces[0]
        speech_key = f"{primary['name']}_{primary['emotion']}_{primary['position']}"
        if speech_key != self.last_spoken_face and (now - self.last_face_speech_time >= 3.5):
            speak(primary["description"])
            self.last_spoken_face = speech_key
            self.last_face_speech_time = now

    def _create_spatial_sentence(self, detections):
        if not detections:
            return "I do not see any objects nearby."

        phrases = []
        for d in detections:
            name = d["name"]
            pos = d["position"]
            prox = d["proximity"]

            if pos == "center":
                if prox == "close":
                    phrases.append(f"a {name} close in front of you")
                elif prox == "nearby":
                    phrases.append(f"a {name} directly ahead")
                else:
                    phrases.append(f"a {name} ahead in the distance")
            else:
                if prox == "close":
                    phrases.append(f"a {name} close on your {pos}")
                elif prox == "nearby":
                    phrases.append(f"a {name} nearby on your {pos}")
                else:
                    phrases.append(f"a {name} on your {pos}")

        if len(phrases) == 1:
            return f"I see {phrases[0]}."
        elif len(phrases) == 2:
            return f"I see {phrases[0]}, and {phrases[1]}."
        else:
            return f"I see {phrases[0]}, {phrases[1]}, and {phrases[2]}."

    # =================================================================
    # VOICE RECOGNITION
    # =================================================================

    def start_voice_command(self, instance=None):
        if not settings.voice_enabled:
            self.hud_banner.text = "Voice commands are disabled in Settings."
            speak("Voice commands are disabled in settings", interrupt=True)
            return

        if self.listening:
            return

        if microphone is None:
            self.hud_banner.text = "Microphone is unavailable."
            speak("Microphone is unavailable", interrupt=True)
            return

        self.listening = True
        self.card_voice.set_active(True)
        self.status_pill.text = "● LISTENING"
        self.status_pill.color = C_MAGENTA
        self.hud_banner.text = "Listening for command... ('find cup', 'radar', 'face')"
        speak("Listening", interrupt=True)

        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            text = recognizer.recognize_google(audio).lower().strip()
            print("Voice Command recognized:", text)
            Clock.schedule_once(lambda dt: self._process_voice_command(text))

        except sr.WaitTimeoutError:
            Clock.schedule_once(lambda dt: self._voice_feedback("No speech detected."))
        except sr.UnknownValueError:
            Clock.schedule_once(lambda dt: self._voice_feedback("Sorry, command not understood."))
        except Exception as e:
            Clock.schedule_once(lambda dt: self._voice_feedback(f"Voice error: {str(e)[:30]}"))

    def _process_voice_command(self, text):
        self.listening = False
        self.card_voice.set_active(False)

        if any(w in text for w in ["find", "locate", "where is", "search for"]):
            # Extract target object name
            target = "cup"
            for trigger in ["find", "locate", "where is my", "where is", "search for"]:
                if trigger in text:
                    parts = text.split(trigger, 1)
                    cand = parts[1].replace("my", "").replace("the", "").replace("a", "").strip()
                    if cand:
                        target = cand.split()[0]
                    break
            self.find_target = target
            self.start_mode("find")
        elif any(w in text for w in ["radar", "spatial audio", "sonar", "audio radar"]):
            self.start_mode("radar")
        elif any(w in text for w in ["face", "faces", "emotion", "who is here", "who is that", "companion"]):
            self.start_mode("face")
        elif any(w in text for w in ["what can you see", "detect objects", "object", "objects", "see"]):
            self.start_mode("object")
        elif any(w in text for w in ["read text", "read this", "read", "text", "ocr"]):
            self.start_mode("text")
        elif any(w in text for w in ["obstacle", "obstacles", "walk", "navigation", "danger"]):
            self.start_mode("obstacle")
        elif any(w in text for w in ["stop", "close camera", "exit", "pause"]):
            self.stop_camera()
        else:
            self.hud_banner.text = f"Unrecognized: '{text}'"
            speak("Sorry, command not recognized")

    def _voice_feedback(self, msg):
        self.listening = False
        self.card_voice.set_active(False)
        self.hud_banner.text = msg
        speak(msg)


# =====================================================================
# MASTER APPLICATION
# =====================================================================

class VisionAidApp(App):
    """VisionAid Master Application with ScreenManager and Lilac/Pink gradient styling."""

    def build(self):
        self.title = "VisionAid AI"

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

        # Onboarding & Authentication Routing
        if settings.current_user:
            sm.current = "main"
        elif not settings.language_selected:
            sm.current = "language_select"
        else:
            sm.current = "login"

        return sm

    def on_stop(self):
        if hasattr(self, "main_screen") and self.main_screen is not None:
            self.main_screen.stop_camera()


if __name__ == "__main__":
    VisionAidApp().run()