import os
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp

BASE_DIR = os.path.dirname(__file__)
TEX_BG = os.path.join(BASE_DIR, "assets", "textures", "bg_grad.png")
TEX_CARD = os.path.join(BASE_DIR, "assets", "textures", "card_grad.png")
TEX_BTN = os.path.join(BASE_DIR, "assets", "textures", "btn_grad.png")
ICON_BACK = os.path.join(BASE_DIR, "assets", "icons", "icon_back.png")
ICON_GLOBE = os.path.join(BASE_DIR, "assets", "icons", "icon_globe.png")
ICON_USER = os.path.join(BASE_DIR, "assets", "icons", "icon_user.png")

from language_manager import language_manager

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


class GradientButton(Button):
    """Tactile button with smooth pink gradient texture."""
    def __init__(self, radius=14, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.btn_radius = [dp(radius)]

        with self.canvas.before:
            self.canvas_tint = Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.btn_radius, source=TEX_BTN)
            self.canvas_border = Color(1, 0.70, 0.85, 0.9)
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(radius)), width=1.3)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self.btn_radius[0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.canvas_tint.rgba = (0.85, 0.85, 0.85, 1)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.canvas_tint.rgba = (1, 1, 1, 1)
        return super().on_touch_up(touch)


class SettingsScreen(Screen):
    """Luxurious Lilac and Pinkish Settings screen."""

    def __init__(self, settings, tts, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.tts = tts
        self._build_ui()

    def _build_ui(self):
        root_layout = BoxLayout(orientation="vertical", padding=[dp(16), dp(14), dp(16), dp(16)], spacing=dp(12))

        # Canvas with deep midnight orchid gradient texture
        with root_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=root_layout.pos, size=root_layout.size, source=TEX_BG)

        root_layout.bind(pos=lambda _, v: setattr(self.bg_rect, "pos", v),
                         size=lambda _, v: setattr(self.bg_rect, "size", v))

        # -------------------------------------------------------------
        # TOP BAR: BACK BUTTON & TITLE
        # -------------------------------------------------------------
        top_bar = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))

        # Back Button with left chevron icon & BACK text (100% visible)
        back_btn = BackButton(icon_path=ICON_BACK)
        back_btn.bind(on_press=self.go_back)

        title_lbl = Label(
            text="SETTINGS",
            font_size=20,
            bold=True,
            color=C_LILAC,
            halign="center",
            valign="middle",
            size_hint=(1, 1)
        )
        title_lbl.bind(size=title_lbl.setter("text_size"))

        # Right balancing spacer so title stays centered
        spacer = BoxLayout(size_hint=(None, None), size=(dp(98), dp(38)))

        top_bar.add_widget(back_btn)
        top_bar.add_widget(title_lbl)
        top_bar.add_widget(spacer)
        root_layout.add_widget(top_bar)

        # -------------------------------------------------------------
        # SCROLLABLE PREFERENCES
        # -------------------------------------------------------------
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=dp(4))
        content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(14), padding=[0, dp(4), 0, dp(16)])
        content.bind(minimum_height=content.setter("height"))

        # --- CARD 1: SPEECH & AUDIO ---
        audio_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(230),
                               padding=dp(16), spacing=dp(10))

        sec_audio_title = Label(
            text="SPEECH & AUDIO PREFERENCES",
            font_size=12,
            bold=True,
            color=C_PINK,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        sec_audio_title.bind(size=sec_audio_title.setter("text_size"))
        audio_card.add_widget(sec_audio_title)

        # Volume row
        vol_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24))
        vol_lbl = Label(text="Voice Volume", font_size=15, color=C_TEXT_WHITE, halign="left")
        vol_lbl.bind(size=vol_lbl.setter("text_size"))
        self.vol_val_lbl = Label(text=f"{self.settings.volume}%", font_size=14, bold=True,
                                 color=C_PINK, size_hint=(None, 1), width=dp(60), halign="right")
        self.vol_val_lbl.bind(size=self.vol_val_lbl.setter("text_size"))
        vol_header.add_widget(vol_lbl)
        vol_header.add_widget(self.vol_val_lbl)
        audio_card.add_widget(vol_header)

        self.volume_slider = Slider(min=0, max=100, value=self.settings.volume, size_hint=(1, None), height=dp(30))
        self.volume_slider.bind(value=self.on_volume_change)
        audio_card.add_widget(self.volume_slider)

        # Speed row
        spd_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24))
        spd_lbl = Label(text="Speech Speed", font_size=15, color=C_TEXT_WHITE, halign="left")
        spd_lbl.bind(size=spd_lbl.setter("text_size"))
        self.spd_val_lbl = Label(text=self._format_speed(self.settings.rate), font_size=14, bold=True,
                                 color=C_LILAC, size_hint=(None, 1), width=dp(85), halign="right")
        self.spd_val_lbl.bind(size=self.spd_val_lbl.setter("text_size"))
        spd_header.add_widget(spd_lbl)
        spd_header.add_widget(self.spd_val_lbl)
        audio_card.add_widget(spd_header)

        self.speed_slider = Slider(min=-10, max=10, value=self.settings.rate, size_hint=(1, None), height=dp(30))
        self.speed_slider.bind(value=self.on_speed_change)
        audio_card.add_widget(self.speed_slider)

        # Test Voice Button with Pink Gradient
        test_voice_btn = GradientButton(
            text="Play Voice Sample",
            font_size=14,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(40)
        )
        test_voice_btn.bind(on_press=self.play_voice_sample)
        audio_card.add_widget(test_voice_btn)

        content.add_widget(audio_card)

        # --- CARD 2: OBSTACLE SENSITIVITY ---
        obstacle_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(130),
                                  padding=dp(16), spacing=dp(10))

        sec_obs_title = Label(
            text="SAFETY & PROXIMITY ALERTS",
            font_size=12,
            bold=True,
            color=C_ROSE,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        sec_obs_title.bind(size=sec_obs_title.setter("text_size"))
        obstacle_card.add_widget(sec_obs_title)

        obs_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(24))
        obs_lbl = Label(text="Proximity Alert Threshold", font_size=15, color=C_TEXT_WHITE, halign="left")
        obs_lbl.bind(size=obs_lbl.setter("text_size"))
        self.obs_val_lbl = Label(text=f"{int(self.settings.obstacle_threshold * 100)}%", font_size=14, bold=True,
                                 color=C_ROSE, size_hint=(None, 1), width=dp(60), halign="right")
        self.obs_val_lbl.bind(size=self.obs_val_lbl.setter("text_size"))
        obs_header.add_widget(obs_lbl)
        obs_header.add_widget(self.obs_val_lbl)
        obstacle_card.add_widget(obs_header)

        self.obstacle_slider = Slider(min=0.10, max=0.50, value=self.settings.obstacle_threshold,
                                      size_hint=(1, None), height=dp(30))
        self.obstacle_slider.bind(value=self.on_obstacle_change)
        obstacle_card.add_widget(self.obstacle_slider)

        content.add_widget(obstacle_card)

        # --- CARD 3: HANDS-FREE VOICE ---
        voice_card = LilacCard(orientation="vertical", size_hint_y=None, height=dp(115),
                               padding=dp(16), spacing=dp(10))

        sec_voice_title = Label(
            text="HANDS-FREE ASSISTANCE",
            font_size=12,
            bold=True,
            color=C_LILAC,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        sec_voice_title.bind(size=sec_voice_title.setter("text_size"))
        voice_card.add_widget(sec_voice_title)

        voice_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(44), spacing=dp(12))
        voice_desc = Label(
            text="Voice Recognition",
            font_size=15,
            color=C_TEXT_WHITE,
            halign="left",
            valign="middle"
        )
        voice_desc.bind(size=voice_desc.setter("text_size"))

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

        voice_row.add_widget(voice_desc)
        voice_row.add_widget(self.voice_toggle)
        voice_card.add_widget(voice_row)

        content.add_widget(voice_card)

        # -------------------------------------------------------------
        # 5. ACCOUNT & LANGUAGE PREFERENCES
        # -------------------------------------------------------------
        account_card = LilacCard(radius=16, orientation="vertical", size_hint=(1, None), height=dp(135),
                                 padding=[dp(16), dp(12), dp(16), dp(14)], spacing=dp(8))

        acc_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(26), spacing=dp(8))
        acc_icon = Image(source=ICON_USER, size_hint=(None, 1), width=dp(18), fit_mode="contain", color=C_PINK)
        self.acc_title = Label(
            text="Account & Language",
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
            text=f"User: {user_info.get('name', 'Guest')} • Lang: {language_manager.get_language_info(self.settings.language)['native']}",
            font_size=12,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.user_lbl.bind(size=self.user_lbl.setter("text_size"))
        account_card.add_widget(self.user_lbl)

        # Buttons row: Change Language & Log Out
        btn_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40), spacing=dp(10))
        lang_btn = Button(
            text="Change Language",
            font_size=12,
            bold=True,
            color=C_TEXT_WHITE,
            background_normal="",
            background_color=(0.28, 0.16, 0.42, 0.95),
            size_hint=(0.58, 1)
        )
        lang_btn.bind(on_press=self._goto_language)

        logout_btn = Button(
            text="Log Out",
            font_size=12,
            bold=True,
            color=(0.98, 0.45, 0.55, 1),
            background_normal="",
            background_color=(0.32, 0.12, 0.22, 0.95),
            size_hint=(0.42, 1)
        )
        logout_btn.bind(on_press=self._handle_logout)

        btn_row.add_widget(lang_btn)
        btn_row.add_widget(logout_btn)
        account_card.add_widget(btn_row)

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
        self.tts.speak("This is a preview of your VisionAid speech settings.", interrupt=True)

    def go_back(self, instance):
        if self.manager:
            self.manager.transition.direction = "right"
            self.manager.current = "main"

    def on_enter(self):
        user_info = self.settings.current_user or {"name": "Guest Explorer", "email": "guest@visionaid.ai"}
        lang_info = language_manager.get_language_info(self.settings.language)
        self.user_lbl.text = f"User: {user_info.get('name', 'Guest')} • Lang: {lang_info['native']}"

    def _goto_language(self, *args):
        if self.manager:
            self.manager.transition.direction = "left"
            self.manager.current = "language_select"

    def _handle_logout(self, *args):
        self.settings.logout()
        self.tts.speak("Logged out successfully.", interrupt=True)
        if self.manager:
            self.manager.transition.direction = "right"
            self.manager.current = "login"