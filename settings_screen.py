import os
import threading
import urllib.request
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp

BASE_DIR = os.path.dirname(__file__)
ICON_BACK = os.path.join(BASE_DIR, "assets", "icons", "icon_back.png")
ICON_GLOBE = os.path.join(BASE_DIR, "assets", "icons", "icon_globe.png")
ICON_MIC = os.path.join(BASE_DIR, "assets", "icons", "icon_mic.png")
ICON_SHIELD = os.path.join(BASE_DIR, "assets", "icons", "icon_shield.png")
ICON_USER = os.path.join(BASE_DIR, "assets", "icons", "icon_user.png")
ICON_RADAR = os.path.join(BASE_DIR, "assets", "icons", "icon_radar.png")

from language_manager import language_manager, SUPPORTED_LANGUAGES

# Elegant Clean Theme Colors (matching UI/UX reference)
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
C_DANGER_BORDER = (0.98, 0.72, 0.72, 1.0)    # #FCA5A5 Soft Red Border
C_DANGER_TEXT = (0.93, 0.25, 0.25, 1.0)      # #EF4444 Danger Red Text

# Legacy aliases for compatibility
C_LILAC = C_PURPLE_ACCENT
C_PINK = C_PURPLE
C_ROSE = (0.96, 0.45, 0.71, 1)
C_TEXT_WHITE = (1.0, 1.0, 1.0, 1.0)
C_BORDER = C_CARD_BORDER


class BackButton(ButtonBehavior, BoxLayout):
    """Clean minimal back button matching the design reference."""
    def __init__(self, icon_path=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.size = (dp(92), dp(38))
        self.pos_hint = {"center_y": 0.5}
        self.spacing = dp(6)
        self.padding = [dp(4), dp(4), dp(4), dp(4)]

        self.text_lbl = Label(
            text="[b]←  Back[/b]",
            markup=True,
            font_size=15,
            color=C_PURPLE,
            halign="left",
            valign="middle"
        )
        self.text_lbl.bind(size=self.text_lbl.setter("text_size"))
        self.add_widget(self.text_lbl)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.65
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class LilacCard(BoxLayout):
    """Pure white card with rounded corners and subtle border."""
    def __init__(self, radius=16, **kwargs):
        super().__init__(**kwargs)
        self.card_radius = [dp(radius)]

        with self.canvas.before:
            Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.card_radius)
            Color(*C_CARD_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(radius)), width=1.1)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.card_radius[0])


class GradientButton(ButtonBehavior, BoxLayout):
    """Action button with soft lilac background and deep purple text."""
    def __init__(self, text="Button", font_size=13, bold=True, color=None, **kwargs):
        kwargs.pop("font_size", None)
        kwargs.pop("bold", None)
        kwargs.pop("color", None)
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        with self.canvas.before:
            Color(*C_LILAC_BTN_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            Color(*C_LILAC_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)), width=1.0)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.btn_lbl = Label(
            text=text,
            font_size=font_size,
            bold=bold,
            color=color or C_PURPLE,
            halign="center",
            valign="middle"
        )
        self.add_widget(self.btn_lbl)

    @property
    def text(self):
        return self.btn_lbl.text

    @text.setter
    def text(self, val):
        self.btn_lbl.text = str(val)

    def set_text(self, val):
        self.btn_lbl.text = str(val)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(12))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.75
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class LogoutOutlineButton(ButtonBehavior, BoxLayout):
    """Clean outline logout button matching the design reference."""
    def __init__(self, text="Log Out", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(38)

        with self.canvas.before:
            Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(*C_DANGER_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=1.1)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.lbl = Label(
            text=f"[b]↳  {text}[/b]",
            markup=True,
            font_size=13,
            color=C_DANGER_TEXT,
            halign="center",
            valign="middle"
        )
        self.add_widget(self.lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(10))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.7
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class LanguageOptionChip(ButtonBehavior, BoxLayout):
    """Language selection chip in a 2-column grid matching the reference design."""
    def __init__(self, lang_data, is_active=False, on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.lang_data = lang_data
        self.is_active = is_active
        self.on_select = on_select
        self.orientation = "horizontal"
        self.size_hint = (0.48, None)
        self.height = dp(44)
        self.padding = [dp(10), dp(4), dp(10), dp(4)]
        self.spacing = dp(8)

        with self.canvas.before:
            self.bg_color = Color(*C_LILAC_BTN_BG) if is_active else Color(*C_CARD_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            self.border_color = Color(*C_PURPLE) if is_active else Color(*C_CARD_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)), width=1.5 if is_active else 1.0)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # Badge container
        self.badge_box = BoxLayout(size_hint=(None, None), size=(dp(34), dp(26)), pos_hint={"center_y": 0.5})
        with self.badge_box.canvas.before:
            self.badge_bg_color = Color(*C_LILAC_BORDER) if is_active else Color(0.95, 0.94, 0.98, 1)
            self.badge_bg = RoundedRectangle(pos=self.badge_box.pos, size=self.badge_box.size, radius=[dp(6)])
        self.badge_box.bind(pos=lambda *_: setattr(self.badge_bg, "pos", self.badge_box.pos),
                            size=lambda *_: setattr(self.badge_bg, "size", self.badge_box.size))

        self.badge_lbl = Label(
            text=f"[b]{lang_data['badge']}[/b]",
            markup=True,
            font_size=12,
            color=C_PURPLE if is_active else C_TEXT_SECONDARY,
            halign="center",
            valign="middle"
        )
        self.badge_box.add_widget(self.badge_lbl)
        self.add_widget(self.badge_box)

        # Name label
        self.name_lbl = Label(
            text=f"[b]{lang_data['native']}[/b]" if is_active else lang_data["native"],
            markup=True,
            font_size=13,
            color=C_TEXT_PRIMARY,
            halign="left",
            valign="middle",
            size_hint=(1, 1)
        )
        self.name_lbl.bind(size=self.name_lbl.setter("text_size"))
        self.add_widget(self.name_lbl)

        # Checkmark
        self.check_lbl = Label(
            text="[b]✔[/b]" if is_active else "",
            markup=True,
            font_size=13,
            color=C_PURPLE,
            size_hint=(None, 1),
            width=dp(20),
            halign="center",
            valign="middle"
        )
        self.add_widget(self.check_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(12))

    def set_active(self, active):
        self.is_active = active
        self.bg_color.rgba = C_LILAC_BTN_BG if active else C_CARD_BG
        self.border_color.rgba = C_PURPLE if active else C_CARD_BORDER
        self.border_line.width = 1.5 if active else 1.0
        self.badge_bg_color.rgba = C_LILAC_BORDER if active else (0.95, 0.94, 0.98, 1)
        self.badge_lbl.color = C_PURPLE if active else C_TEXT_SECONDARY
        self.name_lbl.text = f"[b]{self.lang_data['native']}[/b]" if active else self.lang_data["native"]
        self.check_lbl.text = "[b]✔[/b]" if active else ""

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.on_select:
                self.on_select(self.lang_data["code"])
            return True
        return super().on_touch_down(touch)


class SettingsScreen(Screen):
    """Preferences dashboard with clean simple UI/UX matching the design reference."""

    def __init__(self, settings, tts, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.tts = tts
        self.lang_chips = {}
        self._build_ui()

    def _build_ui(self):
        root_layout = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(12), dp(16), dp(12)],
            spacing=dp(10)
        )

        with root_layout.canvas.before:
            Color(*C_BG)
            self.bg_rect = RoundedRectangle(pos=root_layout.pos, size=root_layout.size)

        root_layout.bind(pos=lambda _, v: setattr(self.bg_rect, "pos", v),
                         size=lambda _, v: setattr(self.bg_rect, "size", v))

        # -------------------------------------------------------------
        # TOP BAR: BACK BUTTON & TITLE
        # -------------------------------------------------------------
        top_bar = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(46), spacing=dp(8))

        back_btn = BackButton(icon_path=ICON_BACK)
        back_btn.bind(on_press=self.go_back)

        self.title_lbl = Label(
            text="Settings & Preferences",
            font_size=18,
            bold=True,
            color=C_TEXT_PRIMARY,
            halign="center",
            valign="middle",
            size_hint=(1, 1)
        )
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))

        spacer = BoxLayout(size_hint=(None, None), size=(dp(92), dp(38)))

        top_bar.add_widget(back_btn)
        top_bar.add_widget(self.title_lbl)
        top_bar.add_widget(spacer)
        root_layout.add_widget(top_bar)

        # -------------------------------------------------------------
        # SCROLLABLE PREFERENCES
        # -------------------------------------------------------------
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=dp(3))
        content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(12), padding=[0, dp(4), 0, dp(14)])
        content.bind(minimum_height=content.setter("height"))

        # --- CARD 1: SELECT LANGUAGE & VOICE ---
        lang_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(195),
                              padding=[dp(14), dp(12), dp(14), dp(12)], spacing=dp(8))

        lang_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(26), spacing=dp(8))
        globe_icon = Image(source=ICON_GLOBE, size_hint=(None, 1), width=dp(20), fit_mode="contain", color=C_PURPLE)
        self.sec_lang_title = Label(
            text="Select Language & Voice",
            font_size=13.5,
            bold=True,
            color=C_TEXT_PRIMARY,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.sec_lang_title.bind(size=self.sec_lang_title.setter("text_size"))
        lang_header.add_widget(globe_icon)
        lang_header.add_widget(self.sec_lang_title)
        lang_card.add_widget(lang_header)

        # Grid of supported languages (2 per row)
        current_lang = self.settings.language or "en"
        langs = SUPPORTED_LANGUAGES

        for i in range(0, len(langs), 2):
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(42), spacing=dp(10))
            for j in range(2):
                if i + j < len(langs):
                    l_data = langs[i + j]
                    chip = LanguageOptionChip(
                        lang_data=l_data,
                        is_active=(l_data["code"] == current_lang),
                        on_select=self.on_language_select
                    )
                    self.lang_chips[l_data["code"]] = chip
                    row.add_widget(chip)
                else:
                    row.add_widget(BoxLayout(size_hint=(0.48, 1)))
            lang_card.add_widget(row)

        content.add_widget(lang_card)

        # --- CARD 2: VOICE & SPEECH SYNTHESIS ---
        audio_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(220),
                               padding=[dp(16), dp(12), dp(16), dp(14)], spacing=dp(6))

        audio_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24), spacing=dp(8))
        mic_icon = Image(source=ICON_MIC, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.sec_audio_title = Label(
            text="Voice & Speech Synthesis",
            font_size=13.5,
            bold=True,
            color=C_TEXT_PRIMARY,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.sec_audio_title.bind(size=self.sec_audio_title.setter("text_size"))
        audio_header.add_widget(mic_icon)
        audio_header.add_widget(self.sec_audio_title)
        audio_card.add_widget(audio_header)

        # Volume row
        vol_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(22))
        self.vol_lbl = Label(text="Voice Volume", font_size=13, color=C_TEXT_PRIMARY, halign="left", valign="middle")
        self.vol_lbl.bind(size=self.vol_lbl.setter("text_size"))
        self.vol_val_lbl = Label(text=f"{self.settings.volume}%", font_size=13, bold=True,
                                 color=C_TEXT_PRIMARY, size_hint=(None, 1), width=dp(60), halign="right", valign="middle")
        self.vol_val_lbl.bind(size=self.vol_val_lbl.setter("text_size"))
        vol_header.add_widget(self.vol_lbl)
        vol_header.add_widget(self.vol_val_lbl)
        audio_card.add_widget(vol_header)

        self.volume_slider = Slider(
            min=0, max=100, value=self.settings.volume, size_hint=(1, None), height=dp(28),
            value_track=True, value_track_color=C_PURPLE, value_track_width=dp(4),
            cursor_size=(dp(18), dp(18))
        )
        self.volume_slider.bind(value=self.on_volume_change)
        audio_card.add_widget(self.volume_slider)

        # Speed row
        spd_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(22))
        self.spd_lbl = Label(text="Speech Speed", font_size=13, color=C_TEXT_PRIMARY, halign="left", valign="middle")
        self.spd_lbl.bind(size=self.spd_lbl.setter("text_size"))
        self.spd_val_lbl = Label(text=self._format_speed(self.settings.rate), font_size=13, bold=True,
                                 color=C_TEXT_PRIMARY, size_hint=(None, 1), width=dp(85), halign="right", valign="middle")
        self.spd_val_lbl.bind(size=self.spd_val_lbl.setter("text_size"))
        spd_header.add_widget(self.spd_lbl)
        spd_header.add_widget(self.spd_val_lbl)
        audio_card.add_widget(spd_header)

        self.speed_slider = Slider(
            min=-10, max=10, value=self.settings.rate, size_hint=(1, None), height=dp(28),
            value_track=True, value_track_color=C_PURPLE, value_track_width=dp(4),
            cursor_size=(dp(18), dp(18))
        )
        self.speed_slider.bind(value=self.on_speed_change)
        audio_card.add_widget(self.speed_slider)

        # Test Voice Button
        self.test_voice_btn = GradientButton(
            text="▶  Play Voice Sample",
            font_size=13,
            bold=True,
            size_hint=(1, None),
            height=dp(38)
        )
        self.test_voice_btn.bind(on_press=self.play_voice_sample)
        audio_card.add_widget(self.test_voice_btn)

        content.add_widget(audio_card)

        # --- CARD 3: SAFETY & PROXIMITY ALERTS ---
        obstacle_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(110),
                                  padding=[dp(16), dp(12), dp(16), dp(14)], spacing=dp(6))

        obs_title_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24), spacing=dp(8))
        shield_icon = Image(source=ICON_SHIELD, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.sec_obs_title = Label(
            text="Safety & Proximity Alerts",
            font_size=13.5,
            bold=True,
            color=C_TEXT_PRIMARY,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.sec_obs_title.bind(size=self.sec_obs_title.setter("text_size"))
        obs_title_row.add_widget(shield_icon)
        obs_title_row.add_widget(self.sec_obs_title)
        obstacle_card.add_widget(obs_title_row)

        obs_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(22))
        self.obs_lbl = Label(text="Proximity Alert Threshold", font_size=13, color=C_TEXT_PRIMARY, halign="left", valign="middle")
        self.obs_lbl.bind(size=self.obs_lbl.setter("text_size"))
        self.obs_val_lbl = Label(text=f"{int(self.settings.obstacle_threshold * 100)}%", font_size=13, bold=True,
                                 color=C_TEXT_PRIMARY, size_hint=(None, 1), width=dp(60), halign="right", valign="middle")
        self.obs_val_lbl.bind(size=self.obs_val_lbl.setter("text_size"))
        obs_header.add_widget(self.obs_lbl)
        obs_header.add_widget(self.obs_val_lbl)
        obstacle_card.add_widget(obs_header)

        self.obstacle_slider = Slider(
            min=0.10, max=0.50, value=self.settings.obstacle_threshold,
            size_hint=(1, None), height=dp(28),
            value_track=True, value_track_color=C_PURPLE, value_track_width=dp(4),
            cursor_size=(dp(18), dp(18))
        )
        self.obstacle_slider.bind(value=self.on_obstacle_change)
        obstacle_card.add_widget(self.obstacle_slider)

        content.add_widget(obstacle_card)

        # --- CARD 4: HANDS-FREE ASSISTANCE ---
        voice_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(86),
                               padding=[dp(16), dp(12), dp(16), dp(12)], spacing=dp(8))

        voice_title_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24), spacing=dp(8))
        voice_icon = Image(source=ICON_MIC, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.sec_voice_title = Label(
            text="Hands-Free Assistance",
            font_size=13.5,
            bold=True,
            color=C_TEXT_PRIMARY,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.sec_voice_title.bind(size=self.sec_voice_title.setter("text_size"))
        voice_title_row.add_widget(voice_icon)
        voice_title_row.add_widget(self.sec_voice_title)
        voice_card.add_widget(voice_title_row)

        voice_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(32), spacing=dp(10))
        self.voice_desc = Label(
            text="Voice Recognition",
            font_size=13,
            color=C_TEXT_PRIMARY,
            halign="left",
            valign="middle"
        )
        self.voice_desc.bind(size=self.voice_desc.setter("text_size"))

        self.voice_toggle = ToggleButton(
            text="Enabled" if self.settings.voice_enabled else "Disabled",
            state="down" if self.settings.voice_enabled else "normal",
            font_size=12,
            bold=True,
            size_hint=(None, 1),
            width=dp(96),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )
        self._update_toggle_style(self.voice_toggle, self.settings.voice_enabled)
        self.voice_toggle.bind(state=self.on_voice_toggle)

        voice_row.add_widget(self.voice_desc)
        voice_row.add_widget(self.voice_toggle)
        voice_card.add_widget(voice_row)

        content.add_widget(voice_card)

        # --- CARD 5: AI SERVER CONNECTION (CLOUD / PC) ---
        server_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(168),
                                padding=[dp(16), dp(12), dp(16), dp(14)], spacing=dp(8))

        server_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24), spacing=dp(8))
        server_icon = Image(source=ICON_RADAR, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.sec_server_title = Label(
            text="AI Server Connection (Cloud / PC)",
            font_size=13.5,
            bold=True,
            color=C_TEXT_PRIMARY,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.sec_server_title.bind(size=self.sec_server_title.setter("text_size"))
        server_header.add_widget(server_icon)
        server_header.add_widget(self.sec_server_title)
        server_card.add_widget(server_header)

        # Input Wrapper with link icon
        input_wrap = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40), padding=[dp(8), dp(2), dp(8), dp(2)], spacing=dp(6))
        with input_wrap.canvas.before:
            Color(*C_CARD_BG)
            self.input_bg = RoundedRectangle(pos=input_wrap.pos, size=input_wrap.size, radius=[dp(10)])
            Color(*C_CARD_BORDER)
            self.input_border = Line(rounded_rectangle=(input_wrap.x, input_wrap.y, input_wrap.width, input_wrap.height, dp(10)), width=1.1)
        input_wrap.bind(pos=lambda *_: (setattr(self.input_bg, "pos", input_wrap.pos), setattr(self.input_border, "rounded_rectangle", (input_wrap.x, input_wrap.y, input_wrap.width, input_wrap.height, dp(10)))),
                        size=lambda *_: (setattr(self.input_bg, "size", input_wrap.size), setattr(self.input_border, "rounded_rectangle", (input_wrap.x, input_wrap.y, input_wrap.width, input_wrap.height, dp(10)))))

        link_lbl = Label(text="🔗", font_size=14, size_hint=(None, 1), width=dp(24), halign="center", valign="middle")
        self.server_input = TextInput(
            text=self.settings.server_url,
            multiline=False,
            font_size=13,
            foreground_color=C_TEXT_PRIMARY,
            hint_text="http://127.0.0.1:8000",
            hint_text_color=C_TEXT_MUTED,
            cursor_color=C_PURPLE,
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            size_hint=(1, 1),
            padding=[dp(2), dp(8), dp(4), dp(4)]
        )
        input_wrap.add_widget(link_lbl)
        input_wrap.add_widget(self.server_input)
        server_card.add_widget(input_wrap)

        self.server_status_lbl = Label(
            text=f"Current: {self.settings.server_url}",
            font_size=11,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(16),
            halign="center",
            valign="middle"
        )
        self.server_status_lbl.bind(size=self.server_status_lbl.setter("text_size"))
        server_card.add_widget(self.server_status_lbl)

        self.server_test_btn = GradientButton(
            text="((•))  Test & Save Connection",
            font_size=13,
            bold=True,
            size_hint=(1, None),
            height=dp(38)
        )
        self.server_test_btn.bind(on_press=self.test_server_connection)
        server_card.add_widget(self.server_test_btn)

        content.add_widget(server_card)

        # --- CARD 6: ACCOUNT & PROFILE ---
        account_card = LilacCard(radius=16, orientation="vertical", size_hint=(1, None), height=dp(118),
                                 padding=[dp(16), dp(12), dp(16), dp(14)], spacing=dp(8))

        acc_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24), spacing=dp(8))
        acc_icon = Image(source=ICON_USER, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PURPLE)
        self.acc_title = Label(
            text="Account & Profile",
            font_size=13.5,
            bold=True,
            color=C_TEXT_PRIMARY,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.acc_title.bind(size=self.acc_title.setter("text_size"))
        acc_header.add_widget(acc_icon)
        acc_header.add_widget(self.acc_title)
        account_card.add_widget(acc_header)

        user_info = self.settings.current_user or {"name": "sonal", "email": "sonal@visionaid.ai"}
        user_name = user_info.get('name', 'sonal')
        lang_name = language_manager.get_language_info(self.settings.language)['name']
        self.user_lbl = Label(
            text=f"User: {user_name}   |   Language: {lang_name}",
            font_size=12.5,
            color=C_TEXT_SECONDARY,
            size_hint=(1, None),
            height=dp(18),
            halign="left",
            valign="middle"
        )
        self.user_lbl.bind(size=self.user_lbl.setter("text_size"))
        account_card.add_widget(self.user_lbl)

        # Clean Red Outline Logout Button
        self.logout_btn = LogoutOutlineButton(text="Log Out")
        self.logout_btn.bind(on_press=self._handle_logout)
        account_card.add_widget(self.logout_btn)

        content.add_widget(account_card)

        # --- FOOTER TAGLINE (MATCHING REFERENCE IMAGE) ---
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
        content.add_widget(footer_wrap)

        scroll.add_widget(content)
        root_layout.add_widget(scroll)

        self.add_widget(root_layout)

    def on_language_select(self, lang_code):
        """Immediately apply language change across settings, TTS engine, and UI."""
        self.settings.set_language(lang_code)
        language_manager.set_language(lang_code)
        self.tts.set_language(lang_code)

        for code, chip in self.lang_chips.items():
            chip.set_active(code == lang_code)

        info = language_manager.get_language_info(lang_code)
        self.tts.speak(info["confirmation"], interrupt=True)
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        """Update labels on the settings screen while preserving clean typography."""
        lang = self.settings.language
        user_info = self.settings.current_user or {"name": "sonal", "email": "sonal@visionaid.ai"}
        user_name = user_info.get('name', 'sonal')
        lang_name = language_manager.get_language_info(lang)['name']
        self.user_lbl.text = f"User: {user_name}   |   Language: {lang_name}"

    def test_server_connection(self, *args):
        url = self.server_input.text.strip().rstrip("/")
        if not url:
            url = "http://127.0.0.1:8000"
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.server_input.text = url
        self.settings.set_server_url(url)
        self.server_status_lbl.text = "Checking connection..."
        self.server_status_lbl.color = C_PURPLE

        def _ping():
            health_url = f"{url}/api/health"
            try:
                import ssl
                ctx = None
                try:
                    ctx = ssl._create_unverified_context()
                except Exception:
                    pass
                req = urllib.request.Request(health_url, headers={'User-Agent': 'VisionAid-Mobile'})
                with urllib.request.urlopen(req, timeout=6.0, context=ctx) as resp:
                    if resp.status == 200:
                        Clock.schedule_once(lambda dt: self._on_ping_success(url))
                        return
            except Exception as e:
                err_str = str(e)
                print("Server ping exception:", err_str)
                Clock.schedule_once(lambda dt: self._on_ping_failed(err_str))

        threading.Thread(target=_ping, daemon=True).start()

    def _on_ping_success(self, url):
        msg = language_manager.get_string("server_connected", self.settings.language)
        self.server_status_lbl.text = f"● {msg}"
        self.server_status_lbl.color = (0.10, 0.70, 0.35, 1)
        if self.tts:
            self.tts.speak("Server connected successfully", interrupt=True)

    def _on_ping_failed(self, err_str):
        msg = language_manager.get_string("server_offline", self.settings.language)
        self.server_status_lbl.text = f"● {msg}"
        self.server_status_lbl.color = C_DANGER_TEXT
        if self.tts:
            self.tts.speak("Connection failed. Check server IP address.", interrupt=True)

    def _format_speed(self, rate):
        rate = int(rate)
        if rate == 0:
            return "Normal (0)"
        elif rate > 0:
            return f"+{rate} Fast"
        return f"{rate} Slow"

    def _update_toggle_style(self, btn, is_on):
        btn.canvas.before.clear()
        bg_col = C_PURPLE if is_on else (0.88, 0.85, 0.93, 1)
        text_col = (1.0, 1.0, 1.0, 1) if is_on else C_TEXT_SECONDARY

        with btn.canvas.before:
            Color(*bg_col)
            btn.bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(12)])

        btn.color = text_col

        btn.bind(pos=lambda *_: setattr(btn.bg, "pos", btn.pos),
                 size=lambda *_: setattr(btn.bg, "size", btn.size))

    def on_volume_change(self, instance, value):
        val = int(value)
        self.settings.set_volume(val)
        self.tts.set_volume(val)
        self.vol_val_lbl.text = f"{val}%"

    def on_speed_change(self, instance, value):
        val = int(value)
        self.settings.set_rate(val)
        self.tts.set_rate(val)
        self.spd_val_lbl.text = self._format_speed(val)

    def on_obstacle_change(self, instance, value):
        val = round(float(value), 2)
        self.settings.set_obstacle_threshold(val)
        self.obs_val_lbl.text = f"{int(val * 100)}%"

    def on_voice_toggle(self, instance, state):
        is_on = state == "down"
        self.settings.set_voice_enabled(is_on)
        instance.text = "Enabled" if is_on else "Disabled"
        self._update_toggle_style(instance, is_on)

    def play_voice_sample(self, instance):
        msg = language_manager.get_string("preview_speech", self.settings.language)
        self.tts.speak(msg, interrupt=True)

    def go_back(self, instance):
        if self.manager:
            if self.manager.has_screen("main"):
                main_scr = self.manager.get_screen("main")
                if hasattr(main_scr, "update_language"):
                    main_scr.update_language()
            self.manager.transition.direction = "right"
            self.manager.current = "main"

    def on_enter(self):
        current_lang = self.settings.language or "en"
        language_manager.set_language(current_lang)
        self.tts.set_language(current_lang)

        for code, chip in self.lang_chips.items():
            chip.set_active(code == current_lang)

        self.refresh_ui_texts()

    def _goto_language(self, *args):
        if self.manager:
            self.manager.transition.direction = "left"
            self.manager.current = "language_select"

    def _handle_logout(self, *args):
        self.settings.logout()
        logout_msg = language_manager.get_string("logged_out", self.settings.language)
        self.tts.speak(logout_msg, interrupt=True)
        if self.manager:
            self.manager.transition.direction = "right"
            self.manager.current = "login"
