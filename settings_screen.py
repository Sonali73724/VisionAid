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
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp

BASE_DIR = os.path.dirname(__file__)
TEX_BG = os.path.join(BASE_DIR, "assets", "textures", "bg_grad.png")
TEX_CARD = os.path.join(BASE_DIR, "assets", "textures", "card_grad.png")
TEX_BTN = os.path.join(BASE_DIR, "assets", "textures", "btn_grad.png")
ICON_BACK = os.path.join(BASE_DIR, "assets", "icons", "icon_back.png")
ICON_GLOBE = os.path.join(BASE_DIR, "assets", "icons", "icon_globe.png")
ICON_USER = os.path.join(BASE_DIR, "assets", "icons", "icon_user.png")

from language_manager import language_manager, SUPPORTED_LANGUAGES

# Lilac & Pink Theme Colors
C_LILAC = (0.75, 0.52, 0.98, 1)        # #C084FC Soft Radiant Lilac
C_PINK = (0.96, 0.45, 0.71, 1)         # #F472B6 Blossom Pink
C_ROSE = (0.98, 0.44, 0.52, 1)         # #FB7185 Coral Rose
C_TEXT_WHITE = (0.99, 0.96, 1.0, 1)    # #FDF4FF Warm Lilac-White
C_TEXT_MUTED = (0.75, 0.68, 0.85, 1)    # #C4B5FD Soft Lavender
C_BORDER = (0.45, 0.28, 0.62, 0.8)     # Lilac Border Glow


class BackButton(ButtonBehavior, BoxLayout):
    """An elegant pill button displaying a back chevron icon and BACK text."""

    def __init__(self, icon_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.size = (dp(98), dp(38))
        self.pos_hint = {"center_y": 0.5}
        self.padding = [dp(8), dp(6), dp(10), dp(6)]
        self.spacing = dp(6)

        with self.canvas.before:
            self.canvas_bg = Color(0.24, 0.14, 0.38, 0.95)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            self.canvas_border = Color(*C_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=1.3)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.back_icon = Image(
            source=icon_path,
            size_hint=(None, 1),
            width=dp(18),
            fit_mode="contain"
        )
        self.text_lbl = Label(
            text="BACK",
            font_size=13,
            bold=True,
            color=C_TEXT_WHITE,
            halign="center",
            valign="middle"
        )

        self.add_widget(self.back_icon)
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


class LilacCard(BoxLayout):
    """Card with gradient texture, rounded corners, and glowing lilac border."""
    def __init__(self, radius=16, **kwargs):
        super().__init__(**kwargs)
        self.card_radius = [dp(radius)]

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.card_radius, source=TEX_CARD)
            self.canvas_border = Color(*C_BORDER)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(radius)), width=1.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.card_radius[0])


class GradientButton(ButtonBehavior, BoxLayout):
    """An interactive action button with vibrant pink gradient and rounded corners."""
    def __init__(self, text="Button", font_size=14, bold=True, color=None, **kwargs):
        # Remove label-specific properties from kwargs before passing to BoxLayout
        kwargs.pop("font_size", None)
        kwargs.pop("bold", None)
        kwargs.pop("color", None)
        super().__init__(**kwargs)
        self.orientation = "horizontal"

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)], source=TEX_BTN)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.btn_lbl = Label(
            text=text,
            font_size=font_size,
            bold=bold,
            color=color or C_TEXT_WHITE,
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

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.82
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class LanguageOptionChip(ButtonBehavior, BoxLayout):
    """Interactive chip for selecting a language immediately on the settings screen."""

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
            self.bg_color = Color(0.34, 0.17, 0.48, 0.95) if is_active else Color(0.18, 0.11, 0.26, 0.90)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            self.border_color = Color(*(C_PINK if is_active else (0.38, 0.24, 0.52, 0.7)))
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)), width=1.6 if is_active else 1.0)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.badge_lbl = Label(
            text=f"[b]{lang_data['badge']}[/b]",
            markup=True,
            font_size=13,
            color=C_PINK if is_active else C_TEXT_MUTED,
            size_hint=(None, 1),
            width=dp(26)
        )
        self.name_lbl = Label(
            text=f"[b]{lang_data['native']}[/b]" if is_active else lang_data["native"],
            markup=True,
            font_size=13,
            color=C_TEXT_WHITE if is_active else C_TEXT_MUTED,
            halign="left",
            valign="middle"
        )
        self.name_lbl.bind(size=self.name_lbl.setter("text_size"))

        self.add_widget(self.badge_lbl)
        self.add_widget(self.name_lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(12))

    def set_active(self, active):
        self.is_active = active
        self.bg_color.rgba = (0.34, 0.17, 0.48, 0.95) if active else (0.18, 0.11, 0.26, 0.90)
        self.border_color.rgba = C_PINK if active else (0.38, 0.24, 0.52, 0.7)
        self.border_line.width = 1.6 if active else 1.0
        self.badge_lbl.color = C_PINK if active else C_TEXT_MUTED
        self.name_lbl.color = C_TEXT_WHITE if active else C_TEXT_MUTED
        self.name_lbl.text = f"[b]{self.lang_data['native']}[/b]" if active else self.lang_data["native"]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.on_select:
                self.on_select(self.lang_data["code"])
            return True
        return super().on_touch_down(touch)


class SettingsScreen(Screen):
    """Preferences dashboard with instant multi-language selection, audio controls, and safety settings."""

    def __init__(self, settings, tts, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.tts = tts
        self.lang_chips = {}
        self._build_ui()

    def _build_ui(self):
        root_layout = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(16), dp(16), dp(16)],
            spacing=dp(12)
        )

        with root_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=root_layout.pos, size=root_layout.size, source=TEX_BG)

        root_layout.bind(pos=lambda _, v: setattr(self.bg_rect, "pos", v),
                         size=lambda _, v: setattr(self.bg_rect, "size", v))

        # -------------------------------------------------------------
        # TOP BAR: BACK BUTTON & TITLE
        # -------------------------------------------------------------
        top_bar = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))

        back_btn = BackButton(icon_path=ICON_BACK)
        back_btn.bind(on_press=self.go_back)

        self.title_lbl = Label(
            text=language_manager.get_string("settings_title", self.settings.language),
            font_size=18,
            bold=True,
            color=C_LILAC,
            halign="center",
            valign="middle",
            size_hint=(1, 1)
        )
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))

        spacer = BoxLayout(size_hint=(None, None), size=(dp(98), dp(38)))

        top_bar.add_widget(back_btn)
        top_bar.add_widget(self.title_lbl)
        top_bar.add_widget(spacer)
        root_layout.add_widget(top_bar)

        # -------------------------------------------------------------
        # SCROLLABLE PREFERENCES
        # -------------------------------------------------------------
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=dp(4))
        content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(14), padding=[0, dp(4), 0, dp(16)])
        content.bind(minimum_height=content.setter("height"))

        # --- CARD 1: VISUAL LANGUAGE SELECTOR (PROMINENT & EASY TO ACCESS) ---
        lang_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(195),
                              padding=dp(14), spacing=dp(8))

        lang_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24), spacing=dp(6))
        globe_icon = Image(source=ICON_GLOBE, size_hint=(None, 1), width=dp(20), fit_mode="contain", color=C_PINK)
        self.sec_lang_title = Label(
            text=language_manager.get_string("lang_selector_title", self.settings.language),
            font_size=12,
            bold=True,
            color=C_PINK,
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
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(44), spacing=dp(10))
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

        # --- CARD 2: SPEECH & AUDIO ---
        audio_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(230),
                               padding=dp(16), spacing=dp(10))

        self.sec_audio_title = Label(
            text=language_manager.get_string("audio_title", self.settings.language),
            font_size=12,
            bold=True,
            color=C_PINK,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.sec_audio_title.bind(size=self.sec_audio_title.setter("text_size"))
        audio_card.add_widget(self.sec_audio_title)

        # Volume row
        vol_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24))
        self.vol_lbl = Label(text=language_manager.get_string("vol_title", self.settings.language),
                             font_size=15, color=C_TEXT_WHITE, halign="left")
        self.vol_lbl.bind(size=self.vol_lbl.setter("text_size"))
        self.vol_val_lbl = Label(text=f"{self.settings.volume}%", font_size=14, bold=True,
                                 color=C_PINK, size_hint=(None, 1), width=dp(60), halign="right")
        self.vol_val_lbl.bind(size=self.vol_val_lbl.setter("text_size"))
        vol_header.add_widget(self.vol_lbl)
        vol_header.add_widget(self.vol_val_lbl)
        audio_card.add_widget(vol_header)

        self.volume_slider = Slider(min=0, max=100, value=self.settings.volume, size_hint=(1, None), height=dp(30))
        self.volume_slider.bind(value=self.on_volume_change)
        audio_card.add_widget(self.volume_slider)

        # Speed row
        spd_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24))
        self.spd_lbl = Label(text=language_manager.get_string("spd_title", self.settings.language),
                             font_size=15, color=C_TEXT_WHITE, halign="left")
        self.spd_lbl.bind(size=self.spd_lbl.setter("text_size"))
        self.spd_val_lbl = Label(text=self._format_speed(self.settings.rate), font_size=14, bold=True,
                                 color=C_LILAC, size_hint=(None, 1), width=dp(85), halign="right")
        self.spd_val_lbl.bind(size=self.spd_val_lbl.setter("text_size"))
        spd_header.add_widget(self.spd_lbl)
        spd_header.add_widget(self.spd_val_lbl)
        audio_card.add_widget(spd_header)

        self.speed_slider = Slider(min=-10, max=10, value=self.settings.rate, size_hint=(1, None), height=dp(30))
        self.speed_slider.bind(value=self.on_speed_change)
        audio_card.add_widget(self.speed_slider)

        # Test Voice Button
        self.test_voice_btn = GradientButton(
            text=language_manager.get_string("play_sample", self.settings.language),
            font_size=14,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(40)
        )
        self.test_voice_btn.bind(on_press=self.play_voice_sample)
        audio_card.add_widget(self.test_voice_btn)

        content.add_widget(audio_card)

        # --- CARD 3: OBSTACLE SENSITIVITY ---
        obstacle_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(130),
                                  padding=dp(16), spacing=dp(10))

        self.sec_obs_title = Label(
            text=language_manager.get_string("obs_title", self.settings.language),
            font_size=12,
            bold=True,
            color=C_ROSE,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.sec_obs_title.bind(size=self.sec_obs_title.setter("text_size"))
        obstacle_card.add_widget(self.sec_obs_title)

        obs_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24))
        self.obs_lbl = Label(text=language_manager.get_string("obs_thresh", self.settings.language),
                             font_size=15, color=C_TEXT_WHITE, halign="left")
        self.obs_lbl.bind(size=self.obs_lbl.setter("text_size"))
        self.obs_val_lbl = Label(text=f"{int(self.settings.obstacle_threshold * 100)}%", font_size=14, bold=True,
                                 color=C_ROSE, size_hint=(None, 1), width=dp(60), halign="right")
        self.obs_val_lbl.bind(size=self.obs_val_lbl.setter("text_size"))
        obs_header.add_widget(self.obs_lbl)
        obs_header.add_widget(self.obs_val_lbl)
        obstacle_card.add_widget(obs_header)

        self.obstacle_slider = Slider(min=0.10, max=0.50, value=self.settings.obstacle_threshold,
                                      size_hint=(1, None), height=dp(30))
        self.obstacle_slider.bind(value=self.on_obstacle_change)
        obstacle_card.add_widget(self.obstacle_slider)

        content.add_widget(obstacle_card)

        # --- CARD 4: HANDS-FREE VOICE ---
        voice_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(115),
                               padding=dp(16), spacing=dp(10))

        self.sec_voice_title = Label(
            text=language_manager.get_string("voice_assist", self.settings.language),
            font_size=12,
            bold=True,
            color=C_LILAC,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.sec_voice_title.bind(size=self.sec_voice_title.setter("text_size"))
        voice_card.add_widget(self.sec_voice_title)

        voice_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(44), spacing=dp(12))
        self.voice_desc = Label(
            text=language_manager.get_string("voice_rec", self.settings.language),
            font_size=15,
            color=C_TEXT_WHITE,
            halign="left",
            valign="middle"
        )
        self.voice_desc.bind(size=self.voice_desc.setter("text_size"))

        self.voice_toggle = ToggleButton(
            text="ENABLED" if self.settings.voice_enabled else "DISABLED",
            state="down" if self.settings.voice_enabled else "normal",
            font_size=13,
            bold=True,
            size_hint=(0.38, 1),
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            color=C_TEXT_WHITE
        )
        self._update_toggle_style(self.voice_toggle, self.settings.voice_enabled)
        self.voice_toggle.bind(state=self.on_voice_toggle)

        voice_row.add_widget(self.voice_desc)
        voice_row.add_widget(self.voice_toggle)
        voice_card.add_widget(voice_row)

        content.add_widget(voice_card)

        # --- CARD 5: AI SERVER CONNECTION ---
        server_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(230),
                                padding=dp(16), spacing=dp(8))

        self.sec_server_title = Label(
            text=language_manager.get_string("server_card_title", self.settings.language),
            font_size=12,
            bold=True,
            color=C_PINK,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.sec_server_title.bind(size=self.sec_server_title.setter("text_size"))
        server_card.add_widget(self.sec_server_title)

        self.server_desc = Label(
            text=language_manager.get_string("server_hint", self.settings.language),
            font_size=11,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(24),
            halign="left"
        )
        self.server_desc.bind(size=self.server_desc.setter("text_size"))
        server_card.add_widget(self.server_desc)

        input_wrap = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(42), padding=[dp(8), dp(2), dp(8), dp(2)])
        with input_wrap.canvas.before:
            Color(0.18, 0.10, 0.28, 0.95)
            self.input_bg = RoundedRectangle(pos=input_wrap.pos, size=input_wrap.size, radius=[dp(10)])
            Color(*C_BORDER)
            self.input_border = Line(rounded_rectangle=(input_wrap.x, input_wrap.y, input_wrap.width, input_wrap.height, dp(10)), width=1.1)
        input_wrap.bind(pos=lambda *_: (setattr(self.input_bg, "pos", input_wrap.pos), setattr(self.input_border, "rounded_rectangle", (input_wrap.x, input_wrap.y, input_wrap.width, input_wrap.height, dp(10)))),
                        size=lambda *_: (setattr(self.input_bg, "size", input_wrap.size), setattr(self.input_border, "rounded_rectangle", (input_wrap.x, input_wrap.y, input_wrap.width, input_wrap.height, dp(10)))))

        self.server_input = TextInput(
            text=self.settings.server_url,
            multiline=False,
            font_size=13,
            foreground_color=C_TEXT_WHITE,
            hint_text="http://192.168.1.15:8000",
            hint_text_color=(0.60, 0.50, 0.72, 1),
            cursor_color=C_PINK,
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            size_hint=(1, 1),
            padding=[dp(4), dp(8), dp(4), dp(4)]
        )
        input_wrap.add_widget(self.server_input)
        server_card.add_widget(input_wrap)

        preset_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(28), spacing=dp(8))
        wifi_btn = Button(text="PC WiFi: 192.168...", font_size=10, background_normal="", background_color=(0.28, 0.15, 0.40, 0.8), color=C_TEXT_MUTED)
        wifi_btn.bind(on_press=lambda _: setattr(self.server_input, "text", "http://192.168.1.15:8000"))
        local_btn = Button(text="Localhost: 127.0.0.1", font_size=10, background_normal="", background_color=(0.28, 0.15, 0.40, 0.8), color=C_TEXT_MUTED)
        local_btn.bind(on_press=lambda _: setattr(self.server_input, "text", "http://127.0.0.1:8000"))
        preset_row.add_widget(wifi_btn)
        preset_row.add_widget(local_btn)
        server_card.add_widget(preset_row)

        self.server_status_lbl = Label(
            text=f"Current: {self.settings.server_url}",
            font_size=11,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(18),
            halign="center"
        )
        self.server_status_lbl.bind(size=self.server_status_lbl.setter("text_size"))
        server_card.add_widget(self.server_status_lbl)

        self.server_test_btn = GradientButton(
            text=language_manager.get_string("server_test_btn", self.settings.language),
            font_size=13,
            bold=True,
            size_hint=(1, None),
            height=dp(38)
        )
        self.server_test_btn.bind(on_press=self.test_server_connection)
        server_card.add_widget(self.server_test_btn)

        content.add_widget(server_card)

        # --- CARD 6: ACCOUNT & PROFILE ---
        account_card = LilacCard(radius=16, orientation="vertical", size_hint=(1, None), height=dp(120),
                                 padding=[dp(16), dp(12), dp(16), dp(14)], spacing=dp(8))

        acc_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(26), spacing=dp(8))
        acc_icon = Image(source=ICON_USER, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PINK)
        self.acc_title = Label(
            text=language_manager.get_string("account_title", self.settings.language),
            font_size=15,
            bold=True,
            color=C_TEXT_WHITE,
            size_hint=(1, 1),
            halign="left",
            valign="middle"
        )
        self.acc_title.bind(size=self.acc_title.setter("text_size"))
        acc_header.add_widget(acc_icon)
        acc_header.add_widget(self.acc_title)
        account_card.add_widget(acc_header)

        user_info = self.settings.current_user or {"name": "Guest Explorer", "email": "guest@visionaid.ai"}
        self.user_lbl = Label(
            text=f"User: {user_info.get('name', 'Guest')} • {language_manager.get_language_info(self.settings.language)['native']}",
            font_size=12,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.user_lbl.bind(size=self.user_lbl.setter("text_size"))
        account_card.add_widget(self.user_lbl)

        # Logout Button
        logout_btn = Button(
            text=language_manager.get_string("logout", self.settings.language),
            font_size=12,
            bold=True,
            color=(0.98, 0.45, 0.55, 1),
            background_normal="",
            background_color=(0.32, 0.12, 0.22, 0.95),
            size_hint=(1, None),
            height=dp(36)
        )
        logout_btn.bind(on_press=self._handle_logout)
        account_card.add_widget(logout_btn)

        content.add_widget(account_card)

        # Footer Info
        info_lbl = Label(
            text="VisionAid • Intelligent AI Accessibility Companion\nPreferences are automatically saved.",
            font_size=12,
            color=C_TEXT_MUTED,
            halign="center",
            size_hint=(1, None),
            height=dp(42)
        )
        info_lbl.bind(size=info_lbl.setter("text_size"))
        content.add_widget(info_lbl)

        scroll.add_widget(content)
        root_layout.add_widget(scroll)

        self.add_widget(root_layout)

    def on_language_select(self, lang_code):
        """Immediately apply language change across settings, TTS engine, and UI."""
        self.settings.set_language(lang_code)
        language_manager.set_language(lang_code)
        self.tts.set_language(lang_code)

        # Update visual chip states
        for code, chip in self.lang_chips.items():
            chip.set_active(code == lang_code)

        # Localized spoken confirmation
        info = language_manager.get_language_info(lang_code)
        self.tts.speak(info["confirmation"], interrupt=True)

        # Refresh all labels on this screen
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        """Update all text labels on the settings screen to match the current language."""
        lang = self.settings.language
        self.title_lbl.text = language_manager.get_string("settings_title", lang)
        self.sec_lang_title.text = language_manager.get_string("lang_selector_title", lang)
        self.sec_audio_title.text = language_manager.get_string("audio_title", lang)
        self.vol_lbl.text = language_manager.get_string("vol_title", lang)
        self.spd_lbl.text = language_manager.get_string("spd_title", lang)
        self.test_voice_btn.btn_lbl.text = language_manager.get_string("play_sample", lang)
        self.sec_obs_title.text = language_manager.get_string("obs_title", lang)
        self.obs_lbl.text = language_manager.get_string("obs_thresh", lang)
        self.sec_voice_title.text = language_manager.get_string("voice_assist", lang)
        self.voice_desc.text = language_manager.get_string("voice_rec", lang)
        self.acc_title.text = language_manager.get_string("account_title", lang)
        if hasattr(self, "sec_server_title"):
            self.sec_server_title.text = language_manager.get_string("server_card_title", lang)
        if hasattr(self, "server_desc"):
            self.server_desc.text = language_manager.get_string("server_hint", lang)
        if hasattr(self, "server_test_btn"):
            self.server_test_btn.btn_lbl.text = language_manager.get_string("server_test_btn", lang)

        user_info = self.settings.current_user or {"name": "Guest Explorer", "email": "guest@visionaid.ai"}
        lang_info = language_manager.get_language_info(lang)
        self.user_lbl.text = f"User: {user_info.get('name', 'Guest')} • {lang_info['native']}"

    def test_server_connection(self, *args):
        url = self.server_input.text.strip().rstrip("/")
        if not url:
            url = "http://127.0.0.1:8000"
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.server_input.text = url
        self.settings.set_server_url(url)
        self.server_status_lbl.text = "Checking connection..."
        self.server_status_lbl.color = C_LILAC

        def _ping():
            health_url = f"{url}/api/health"
            try:
                req = urllib.request.Request(health_url, headers={'User-Agent': 'VisionAid-Mobile'})
                with urllib.request.urlopen(req, timeout=3.5) as resp:
                    if resp.status == 200:
                        Clock.schedule_once(lambda dt: self._on_ping_success(url))
                        return
            except Exception as e:
                err_str = str(e)
                Clock.schedule_once(lambda dt: self._on_ping_failed(err_str))

        threading.Thread(target=_ping, daemon=True).start()

    def _on_ping_success(self, url):
        msg = language_manager.get_string("server_connected", self.settings.language)
        self.server_status_lbl.text = f"● {msg}"
        self.server_status_lbl.color = (0.45, 0.90, 0.55, 1)
        if self.tts:
            self.tts.speak("Server connected successfully", interrupt=True)

    def _on_ping_failed(self, err_str):
        msg = language_manager.get_string("server_offline", self.settings.language)
        self.server_status_lbl.text = f"● {msg}"
        self.server_status_lbl.color = (0.96, 0.25, 0.37, 1)
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
        bg_col = (0.35, 0.16, 0.48, 1) if is_on else (0.18, 0.12, 0.25, 1)
        border_col = C_PINK if is_on else (0.35, 0.22, 0.48, 0.7)
        text_col = C_PINK if is_on else C_TEXT_MUTED

        with btn.canvas.before:
            Color(*bg_col)
            btn.bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(12)])
            Color(*border_col)
            btn.border_line = Line(rounded_rectangle=(btn.x, btn.y, btn.width, btn.height, dp(12)), width=1.3)

        btn.color = text_col

        btn.bind(pos=lambda *_: (setattr(btn.bg, "pos", btn.pos),
                                 setattr(btn.border_line, "rounded_rectangle",
                                         (btn.x, btn.y, btn.width, btn.height, dp(12)))),
                 size=lambda *_: (setattr(btn.bg, "size", btn.size),
                                  setattr(btn.border_line, "rounded_rectangle",
                                          (btn.x, btn.y, btn.width, btn.height, dp(12)))))

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
        instance.text = "ENABLED" if is_on else "DISABLED"
        self._update_toggle_style(instance, is_on)

    def play_voice_sample(self, instance):
        msg = language_manager.get_string("preview_speech", self.settings.language)
        self.tts.speak(msg, interrupt=True)

    def go_back(self, instance):
        if self.manager:
            # If main screen has update_language, call it
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