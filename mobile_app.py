"""
VisionAid - Mobile Android & Cross-Platform Client Application
Lightweight mobile client with Lilac & Pink luxury accessibility UI.
Offloads heavy AI inference to VisionAid Cloud/Local Server for maximum mobile performance.
"""

import os
import sys
import time
import threading
import requests
import cv2

# Kivy configuration for Mobile Display
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
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView

from settings import VisionSettings
from settings_screen import SettingsScreen
from tts_engine import TTSEngine
from sound_effects import sound_manager
from auth_screens import LanguageSelectionScreen, LoginScreen, SignupScreen

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

# Palette
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

tts = TTSEngine()
settings = VisionSettings()


def speak(text, interrupt=False):
    tts.speak(text, interrupt=interrupt)


class ThreadedCamera:
    """Thread-safe non-blocking camera capture for mobile preview."""
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
                return self.grabbed, self.frame.copy()
            return False, None

    def is_opened(self):
        return self.cap is not None and self.cap.isOpened()

    def release(self):
        self.stopped = True
        if hasattr(self, "thread") and self.thread.is_alive():
            self.thread.join(timeout=0.4)
        if self.cap is not None:
            self.cap.release()
            self.cap = None


class GradientActionCard(ButtonBehavior, BoxLayout):
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

        with self.canvas.before:
            self.canvas_tint = Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)], source=TEX_CARD)
            self.canvas_border = Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)), width=1.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # Icon
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

        # Info
        info_box = BoxLayout(orientation="vertical", spacing=dp(2))
        self.title_lbl = Label(text=title, font_size=15, bold=True, color=C_TEXT_WHITE, halign="left", valign="bottom", size_hint=(1, 0.55))
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))
        self.desc_lbl = Label(text=subtitle, font_size=12, color=C_TEXT_MUTED, halign="left", valign="top", size_hint=(1, 0.45))
        self.desc_lbl.bind(size=self.desc_lbl.setter("text_size"))
        info_box.add_widget(self.title_lbl)
        info_box.add_widget(self.desc_lbl)
        self.add_widget(info_box)

        # Status Tag
        self.status_tag = Label(text="START", font_size=11, bold=True, color=C_TEXT_MUTED, size_hint=(None, 1), width=dp(52), halign="right", valign="middle")
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


class StatusPill(BoxLayout):
    def __init__(self, icon_path=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, 1)
        self.width = dp(96)
        self.padding = [dp(6), dp(6), dp(8), dp(6)]
        self.spacing = dp(4)

        with self.canvas.before:
            Color(0.20, 0.12, 0.32, 0.90)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.status_icon = Image(source=icon_path or ICON_STATUS, size_hint=(None, 1), width=dp(16), fit_mode="contain", color=C_LILAC)
        self.text_lbl = Label(text="STANDBY", font_size=10.5, bold=True, color=C_LILAC, halign="center", valign="middle")
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
        self.text_lbl.text = val.replace("●", "").replace("•", "").strip()

    @property
    def color(self):
        return self.text_lbl.color

    @color.setter
    def color(self, val):
        self.text_lbl.color = val
        self.status_icon.color = val


class SettingsPillButton(ButtonBehavior, BoxLayout):
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
            Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.3)

        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self.gear_icon = Image(source=icon_path, size_hint=(None, 1), width=dp(22), fit_mode="contain")
        self.text_lbl = Label(text="SETTINGS", font_size=11, bold=True, color=C_TEXT_WHITE, halign="center", valign="middle")
        self.add_widget(self.gear_icon)
        self.add_widget(self.text_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))


class MainScreen(Screen):
    """Mobile dashboard streaming frames to VisionAid AI Server."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
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

        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", padding=[dp(16), dp(14), dp(16), dp(16)], spacing=dp(10))
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size, source=TEX_BG)
        root.bind(pos=lambda *_: setattr(self.bg_rect, "pos", root.pos),
                  size=lambda *_: setattr(self.bg_rect, "size", root.size))

        # Top Bar
        header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(8))
        brand = BoxLayout(orientation="vertical", size_hint=(1, 1), spacing=dp(1))
        app_title = Label(text="[b][color=C084FC]VISION[/color][color=F472B6]AID[/color][/b]", markup=True, font_size=23, halign="left", valign="bottom", size_hint=(1, 0.6))
        app_title.bind(size=app_title.setter("text_size"))
        app_sub = Label(text="Mobile Cloud Companion", font_size=11, color=C_TEXT_MUTED, halign="left", valign="top", size_hint=(1, 0.4))
        app_sub.bind(size=app_sub.setter("text_size"))
        brand.add_widget(app_title)
        brand.add_widget(app_sub)

        self.status_pill = StatusPill(icon_path=ICON_STATUS)
        settings_btn = SettingsPillButton(icon_path=ICON_SETTINGS)
        settings_btn.bind(on_press=self.open_settings)

        header.add_widget(brand)
        header.add_widget(self.status_pill)
        header.add_widget(settings_btn)
        root.add_widget(header)

        # Viewport
        vp_wrapper = RelativeLayout(size_hint=(1, 0.40))
        with vp_wrapper.canvas.before:
            Color(0.12, 0.07, 0.18, 1)
            self.vp_bg = RoundedRectangle(pos=(0, 0), size=vp_wrapper.size, radius=[dp(18)])
            Color(0.55, 0.32, 0.75, 0.9)
            self.vp_border = Line(rounded_rectangle=(0, 0, vp_wrapper.width, vp_wrapper.height, dp(18)), width=1.5)
        vp_wrapper.bind(size=lambda _, s: (setattr(self.vp_bg, "size", s), setattr(self.vp_border, "rounded_rectangle", (0, 0, s[0], s[1], dp(18)))))

        self.camera_image = Image(fit_mode="contain", size_hint=(1, 1), pos_hint={"x": 0, "y": 0}, opacity=0)

        # Standby Placeholder
        self.placeholder = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(14), size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        cam_icon = Image(source=ICON_CAMERA, size_hint=(1, 0.42), fit_mode="contain")
        ready_t = Label(text="Vision Camera Standby", font_size=16, bold=True, color=C_TEXT_WHITE, size_hint=(1, 0.32), halign="center")
        ready_s = Label(text="Select an AI mode below to begin assistance", font_size=12, color=C_TEXT_MUTED, size_hint=(1, 0.26), halign="center")
        self.placeholder.add_widget(cam_icon)
        self.placeholder.add_widget(ready_t)
        self.placeholder.add_widget(ready_s)

        # Floating HUD Banner
        self.hud_banner = Label(text="System ready. Select a mode below.", font_size=13, bold=True, color=C_TEXT_WHITE, size_hint=(0.92, None), height=dp(38), pos_hint={"center_x": 0.5, "y": 0.04}, halign="center", valign="middle")
        self.hud_banner.bind(size=self.hud_banner.setter("text_size"))
        with self.hud_banner.canvas.before:
            Color(1, 1, 1, 1)
            self.hud_bg = RoundedRectangle(pos=self.hud_banner.pos, size=self.hud_banner.size, radius=[dp(12)], source=TEX_HUD)
            Color(0.65, 0.40, 0.85, 0.8)
            self.hud_border = Line(rounded_rectangle=(self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)), width=1.2)
        self.hud_banner.bind(pos=lambda *_: (setattr(self.hud_bg, "pos", self.hud_banner.pos), setattr(self.hud_border, "rounded_rectangle", (self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)))),
                             size=lambda *_: (setattr(self.hud_bg, "size", self.hud_banner.size), setattr(self.hud_border, "rounded_rectangle", (self.hud_banner.x, self.hud_banner.y, self.hud_banner.width, self.hud_banner.height, dp(12)))))

        vp_wrapper.add_widget(self.placeholder)
        vp_wrapper.add_widget(self.camera_image)
        vp_wrapper.add_widget(self.hud_banner)
        root.add_widget(vp_wrapper)

        # Action Cards ScrollView
        scroll = ScrollView(size_hint=(1, 0.60), do_scroll_x=False, bar_width=dp(3))
        card_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, dp(4), 0, dp(8)])
        card_list.bind(minimum_height=card_list.setter("height"))

        self.card_object = GradientActionCard(ICON_EYE, "Object Detection", "Identify everyday objects & surroundings", C_LILAC)
        self.card_object.bind(on_press=lambda _: self.start_mode("object"))
        card_list.add_widget(self.card_object)

        self.card_find = GradientActionCard(ICON_FIND, "Find My Object", "Auditory radar beacon guides you directly to items", C_FIND)
        self.card_find.bind(on_press=lambda _: self.start_mode("find"))
        card_list.add_widget(self.card_find)

        self.card_radar = GradientActionCard(ICON_RADAR, "Spatial Audio Radar", "Directional stereo pulses alert without speech", C_RADAR)
        self.card_radar.bind(on_press=lambda _: self.start_mode("radar"))
        card_list.add_widget(self.card_radar)

        self.card_face = GradientActionCard(ICON_FACE, "Face & Emotion Companion", "Identify familiar contacts & smiling expressions", C_FACE)
        self.card_face.bind(on_press=lambda _: self.start_mode("face"))
        card_list.add_widget(self.card_face)

        self.card_text = GradientActionCard(ICON_TEXT, "Read Text", "Recognize documents, signage, packaging & books", C_PINK)
        self.card_text.bind(on_press=lambda _: self.start_mode("text"))
        card_list.add_widget(self.card_text)

        self.card_obstacle = GradientActionCard(ICON_SHIELD, "Obstacle Guidance", "Real-time proximity warnings & distance alerts", C_ROSE)
        self.card_obstacle.bind(on_press=lambda _: self.start_mode("obstacle"))
        card_list.add_widget(self.card_obstacle)

        self.card_stop = GradientActionCard(ICON_STOP, "Stop Camera", "Turn off video feed & pause vision analysis", C_CRIMSON)
        self.card_stop.bind(on_press=self.stop_camera)
        card_list.add_widget(self.card_stop)

        scroll.add_widget(card_list)
        root.add_widget(scroll)
        self.add_widget(root)

    def open_settings(self, *args):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "settings"

    def open_camera(self):
        if self.camera is not None and self.camera.is_opened():
            return True
        self.camera = ThreadedCamera(0, 640, 480)
        if not self.camera.is_opened():
            self.hud_banner.text = "Camera access error"
            speak("Could not access camera", interrupt=True)
            self.camera = None
            return False
        self.placeholder.opacity = 0
        self.camera_image.opacity = 1
        self._start_network_worker()
        return True

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
        self.status_pill.text = "STANDBY"
        self.status_pill.color = C_LILAC
        self.hud_banner.text = "Camera stopped. Ready to assist."

        self.card_object.set_active(False)
        self.card_find.set_active(False)
        self.card_radar.set_active(False)
        self.card_face.set_active(False)
        self.card_text.set_active(False)
        self.card_obstacle.set_active(False)
        speak("Camera stopped", interrupt=True)

    def start_mode(self, mode):
        if not self.open_camera():
            return
        self.mode = mode
        self.card_object.set_active(mode == "object")
        self.card_find.set_active(mode == "find")
        self.card_radar.set_active(mode == "radar")
        self.card_face.set_active(mode == "face")
        self.card_text.set_active(mode == "text")
        self.card_obstacle.set_active(mode == "obstacle")

        self.status_pill.text = mode.upper()
        self.status_pill.color = C_PINK if mode == "text" else (C_FIND if mode == "find" else C_LILAC)
        self.hud_banner.text = f"Connecting to AI server for {mode} mode..."
        speak(f"{mode} mode activated", interrupt=True)

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

        display_frame = cv2.flip(frame, 1)
        fh, fw = display_frame.shape[:2]

        # Draw overlays from latest server response
        for d in self.server_detections:
            x1, y1, x2, y2 = d["bbox"]
            disp_x1 = max(0, min(fw, fw - x2))
            disp_x2 = max(0, min(fw, fw - x1))
            color = (244, 114, 182) if d.get("position") == "center" else (192, 132, 252)
            cv2.rectangle(display_frame, (disp_x1, y1), (disp_x2, y2), color, 2)
            lbl = f"{d['name']} [{d.get('position', 'C')[0].upper()}]"
            cv2.putText(display_frame, lbl, (disp_x1 + 4, max(18, y1 - 4)), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

        # Blit frame to texture
        rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        if self.camera_image.texture is None or self.camera_image.texture.size != (fw, fh):
            self.camera_image.texture = Texture.create(size=(fw, fh), colorfmt="rgb")
        self.camera_image.texture.blit_buffer(rgb.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
        self.camera_image.texture.flip_vertical()

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

    def _network_loop(self):
        """Streams lightweight compressed JPEG frames to the AI Server."""
        while self.network_running:
            if self.mode is None:
                time.sleep(0.05)
                continue

            frame_to_send = None
            with self.frame_lock:
                if self.latest_frame is not None:
                    frame_to_send = self.latest_frame.copy()

            if frame_to_send is None:
                time.sleep(0.02)
                continue

            try:
                # Downscale to 320px & compress to ~12KB JPEG
                h, w = frame_to_send.shape[:2]
                scale = 320.0 / max(w, 1)
                small = cv2.resize(frame_to_send, (320, int(h * scale)))
                ret, jpeg = cv2.imencode('.jpg', small, [cv2.IMWRITE_JPEG_QUALITY, 65])
                if not ret:
                    continue

                url = f"{settings.server_url}/api/analyze"
                files = {"file": ("frame.jpg", jpeg.tobytes(), "image/jpeg")}
                data = {
                    "mode": self.mode,
                    "find_target": self.find_target,
                    "language": settings.language
                }

                r = requests.post(url, files=files, data=data, timeout=1.2)
                if r.status_code == 200:
                    payload = r.json()
                    Clock.schedule_once(lambda dt, res=payload: self._on_server_response(res))
            except Exception as e:
                # Handle connection timeout gracefully
                Clock.schedule_once(lambda dt: setattr(self.hud_banner, "text", "Connecting to AI Server..."))

            time.sleep(0.08)  # ~12 requests per second

    def _on_server_response(self, res):
        if self.mode != res.get("mode"):
            return

        if res.get("hud_text"):
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

        if res.get("speech_text"):
            speak(res["speech_text"])

        self.server_detections = res.get("detections", [])
        self.server_faces = res.get("faces", [])
        self.target_locked = res.get("target_locked", False)


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

    def on_stop(self):
        if hasattr(self, "main_screen") and self.main_screen is not None:
            self.main_screen.stop_camera()


if __name__ == "__main__":
    VisionAidMobileApp().run()
