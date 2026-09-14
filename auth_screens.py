"""
VisionAid - Mobile Authentication & Onboarding Screens
Includes Language Selection Screen, Login Screen, and Signup Screen.
Styled in the signature Lilac & Pink luxury accessibility aesthetic.
"""

import os
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.clock import Clock

from language_manager import language_manager, SUPPORTED_LANGUAGES
from auth_manager import auth_manager

BASE_DIR = os.path.dirname(__file__)
TEX_BG = os.path.join(BASE_DIR, "assets", "textures", "bg_grad.png")
TEX_CARD = os.path.join(BASE_DIR, "assets", "textures", "card_grad.png")
TEX_CARD_ACTIVE = os.path.join(BASE_DIR, "assets", "textures", "card_active_grad.png")
TEX_BTN = os.path.join(BASE_DIR, "assets", "textures", "btn_grad.png")

ICON_BACK = os.path.join(BASE_DIR, "assets", "icons", "icon_back.png")
ICON_GLOBE = os.path.join(BASE_DIR, "assets", "icons", "icon_globe.png")
ICON_USER = os.path.join(BASE_DIR, "assets", "icons", "icon_user.png")
ICON_LOCK = os.path.join(BASE_DIR, "assets", "icons", "icon_lock.png")
ICON_CHECK = os.path.join(BASE_DIR, "assets", "icons", "icon_check.png")

# Palette
C_LILAC = (0.75, 0.52, 0.98, 1)          # #C084FC Soft Radiant Lilac
C_PINK = (0.96, 0.45, 0.71, 1)           # #F472B6 Blossom Pink
C_MAGENTA = (0.91, 0.47, 0.97, 1)        # #E879F9 Orchid Fuchsia
C_CRIMSON = (0.96, 0.25, 0.37, 1)        # #F43F5E Soft Crimson
C_TEXT_WHITE = (0.99, 0.96, 1.0, 1)      # #FDF4FF Warm Lilac-White
C_TEXT_MUTED = (0.76, 0.70, 0.86, 1)      # #C4B5FD Soft Lavender
C_BORDER_DEFAULT = (0.40, 0.24, 0.56, 0.8)
C_BORDER_ACTIVE = (0.96, 0.45, 0.71, 0.95)


class GradientButton(ButtonBehavior, BoxLayout):
    """A pill button styled with the vibrant pink/lilac gradient."""

    def __init__(self, text, on_click=None, height_dp=50, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(height_dp)
        self.on_click = on_click

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)], source=TEX_BTN)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.lbl = Label(
            text=f"[b]{text}[/b]",
            markup=True,
            font_size=15,
            color=C_TEXT_WHITE,
            halign="center",
            valign="middle"
        )
        self.add_widget(self.lbl)

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def set_text(self, text):
        self.lbl.text = f"[b]{text}[/b]"

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.opacity = 0.85
            if self.on_click:
                self.on_click()
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.opacity = 1.0
        return super().on_touch_up(touch)


class StyledInput(BoxLayout):
    """A sleek input container with icon, label, and high-contrast text input."""

    def __init__(self, label_text, hint_text, icon_path=None, is_password=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = dp(76)
        self.spacing = dp(4)

        # Label
        self.label = Label(
            text=label_text,
            font_size=12,
            bold=True,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(18),
            halign="left"
        )
        self.label.bind(size=self.label.setter("text_size"))
        self.add_widget(self.label)

        # Input container with Lilac border
        input_box = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(48), spacing=dp(8), padding=[dp(12), dp(4), dp(8), dp(4)])
        with input_box.canvas.before:
            Color(0.18, 0.10, 0.28, 0.95)
            self.bg_rect = RoundedRectangle(pos=input_box.pos, size=input_box.size, radius=[dp(14)])
            self.border_color = Color(*C_BORDER_DEFAULT)
            self.border_line = Line(rounded_rectangle=(input_box.x, input_box.y, input_box.width, input_box.height, dp(14)), width=1.2)

        input_box.bind(pos=lambda *_: (setattr(self.bg_rect, "pos", input_box.pos),
                                       setattr(self.border_line, "rounded_rectangle", (input_box.x, input_box.y, input_box.width, input_box.height, dp(14)))),
                       size=lambda *_: (setattr(self.bg_rect, "size", input_box.size),
                                        setattr(self.border_line, "rounded_rectangle", (input_box.x, input_box.y, input_box.width, input_box.height, dp(14)))))

        if icon_path:
            icon = Image(source=icon_path, size_hint=(None, 1), width=dp(20), fit_mode="contain", color=C_LILAC)
            input_box.add_widget(icon)

        self.input_field = TextInput(
            hint_text=hint_text,
            password=is_password,
            multiline=False,
            font_size=14,
            foreground_color=C_TEXT_WHITE,
            hint_text_color=(0.60, 0.50, 0.72, 1),
            cursor_color=C_PINK,
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            size_hint=(1, 1),
            padding=[dp(6), dp(10), dp(6), dp(6)]
        )
        input_box.add_widget(self.input_field)

        # Show/Hide password toggle if password
        if is_password:
            self.toggle_btn = Button(
                text="SHOW",
                font_size=10,
                bold=True,
                color=C_PINK,
                background_normal="",
                background_color=(0, 0, 0, 0),
                size_hint=(None, 1),
                width=dp(46)
            )
            self.toggle_btn.bind(on_press=self._toggle_password)
            input_box.add_widget(self.toggle_btn)

        self.add_widget(input_box)

    def _toggle_password(self, *args):
        self.input_field.password = not self.input_field.password
        self.toggle_btn.text = "HIDE" if not self.input_field.password else "SHOW"

    @property
    def text(self):
        return self.input_field.text.strip()

    @text.setter
    def text(self, val):
        self.input_field.text = val


# =====================================================================
# 1. LANGUAGE SELECTION SCREEN
# =====================================================================

class LanguageCard(ButtonBehavior, BoxLayout):
    """An accessible card for selecting a language."""

    def __init__(self, lang_data, is_selected=False, on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.lang_data = lang_data
        self.on_select = on_select
        self.is_selected = is_selected

        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = dp(64)
        self.padding = [dp(14), dp(8), dp(16), dp(8)]
        self.spacing = dp(14)

        with self.canvas.before:
            self.canvas_bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)],
                                              source=TEX_CARD_ACTIVE if is_selected else TEX_CARD)
            self.border_color = Color(*(C_BORDER_ACTIVE if is_selected else C_BORDER_DEFAULT))
            self.border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(16)),
                                    width=1.8 if is_selected else 1.2)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # 1. Flag / Badge Circle
        badge = BoxLayout(size_hint=(None, None), size=(dp(42), dp(42)), pos_hint={"center_y": 0.5})
        with badge.canvas.before:
            Color(0.32, 0.16, 0.46, 0.95)
            self.badge_bg = RoundedRectangle(pos=badge.pos, size=badge.size, radius=[dp(12)])
        badge.bind(pos=lambda *_: setattr(self.badge_bg, "pos", badge.pos),
                   size=lambda *_: setattr(self.badge_bg, "size", badge.size))
        
        badge_lbl = Label(text=f"[b]{lang_data['badge']}[/b]", markup=True, font_size=15, color=C_PINK)
        badge.add_widget(badge_lbl)
        self.add_widget(badge)

        # 2. Text info (Native script + English name)
        info = BoxLayout(orientation="vertical", spacing=dp(2), size_hint=(1, 1))
        self.native_lbl = Label(
            text=f"[b]{lang_data['native']}[/b]",
            markup=True,
            font_size=16,
            color=C_TEXT_WHITE,
            halign="left",
            valign="bottom",
            size_hint=(1, 0.58)
        )
        self.native_lbl.bind(size=self.native_lbl.setter("text_size"))

        self.english_lbl = Label(
            text=lang_data["name"],
            font_size=12,
            color=C_TEXT_MUTED,
            halign="left",
            valign="top",
            size_hint=(1, 0.42)
        )
        self.english_lbl.bind(size=self.english_lbl.setter("text_size"))

        info.add_widget(self.native_lbl)
        info.add_widget(self.english_lbl)
        self.add_widget(info)

        # 3. Selection Checkmark
        self.check_icon = Image(
            source=ICON_CHECK,
            size_hint=(None, None),
            size=(dp(24), dp(24)),
            pos_hint={"center_y": 0.5},
            opacity=1.0 if is_selected else 0.0
        )
        self.add_widget(self.check_icon)

    def _update_canvas(self, *args):
        self.canvas_bg.pos = self.pos
        self.canvas_bg.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(16))

    def set_selected(self, selected):
        self.is_selected = selected
        self.check_icon.opacity = 1.0 if selected else 0.0
        if selected:
            self.canvas_bg.source = TEX_CARD_ACTIVE
            self.border_color.rgba = C_BORDER_ACTIVE
            self.border_line.width = 1.8
        else:
            self.canvas_bg.source = TEX_CARD
            self.border_color.rgba = C_BORDER_DEFAULT
            self.border_line.width = 1.2

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.on_select:
                self.on_select(self.lang_data)
            return True
        return super().on_touch_down(touch)


class LanguageSelectionScreen(Screen):
    """Mobile language selection screen with accessible cards and audio greetings."""

    def __init__(self, settings, tts, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.tts = tts
        self.selected_code = self.settings.language or "en"
        self.cards = []

        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(24), dp(20), dp(20)], spacing=dp(16))
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size, source=TEX_BG)
        root.bind(pos=lambda *_: setattr(self.bg_rect, "pos", root.pos),
                  size=lambda *_: setattr(self.bg_rect, "size", root.size))

        # Top Header
        header = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(90), spacing=dp(6))
        globe_icon = Image(source=ICON_GLOBE, size_hint=(None, None), size=(dp(36), dp(36)), color=C_PINK)
        
        self.title_lbl = Label(
            text="[b]Choose Language[/b]",
            markup=True,
            font_size=24,
            color=C_TEXT_WHITE,
            size_hint=(1, None),
            height=dp(28),
            halign="left"
        )
        self.title_lbl.bind(size=self.title_lbl.setter("text_size"))

        self.sub_lbl = Label(
            text="Select your preferred language for voice and guidance",
            font_size=13,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(20),
            halign="left"
        )
        self.sub_lbl.bind(size=self.sub_lbl.setter("text_size"))

        header.add_widget(globe_icon)
        header.add_widget(self.title_lbl)
        header.add_widget(self.sub_lbl)
        root.add_widget(header)

        # Scrollable Language List
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.card_list = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        self.card_list.bind(minimum_height=self.card_list.setter("height"))

        for l in SUPPORTED_LANGUAGES:
            card = LanguageCard(
                lang_data=l,
                is_selected=(l["code"] == self.selected_code),
                on_select=self._on_card_select
            )
            self.cards.append(card)
            self.card_list.add_widget(card)

        scroll.add_widget(self.card_list)
        root.add_widget(scroll)

        # Continue Button
        self.continue_btn = GradientButton(
            text="CONTINUE",
            on_click=self._on_continue,
            height_dp=52
        )
        root.add_widget(self.continue_btn)

        self.add_widget(root)

    def on_enter(self):
        # Audio introduction on screen entrance
        self.tts.speak("Please choose your language. Then press continue.", interrupt=True)

    def _on_card_select(self, lang_data):
        self.selected_code = lang_data["code"]
        for c in self.cards:
            c.set_selected(c.lang_data["code"] == self.selected_code)

        # Update language manager & announce
        language_manager.set_language(self.selected_code)
        self.title_lbl.text = f"[b]{language_manager.get_string('lang_title')}[/b]"
        self.sub_lbl.text = language_manager.get_string("lang_subtitle")
        self.continue_btn.set_text(language_manager.get_string("continue"))

        self.tts.speak(lang_data["confirmation"], interrupt=True)

    def _on_continue(self):
        self.settings.set_language(self.selected_code)
        
        # Route to Login if not logged in, else to Main
        if self.manager:
            self.manager.transition = SlideTransition(direction="left")
            if self.settings.current_user:
                self.manager.current = "main"
            else:
                self.manager.current = "login"


# =====================================================================
# 2. LOGIN SCREEN
# =====================================================================

class LoginScreen(Screen):
    """Mobile Login screen with high-contrast inputs and guest mode option."""

    def __init__(self, settings, tts, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.tts = tts

        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(24), dp(20), dp(20)], spacing=dp(12))
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size, source=TEX_BG)
        root.bind(pos=lambda *_: setattr(self.bg_rect, "pos", root.pos),
                  size=lambda *_: setattr(self.bg_rect, "size", root.size))

        # Brand Logo Header
        header = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(110), spacing=dp(4))
        brand = Label(
            text="[b][color=C084FC]VISION[/color][color=F472B6]AID[/color][/b]",
            markup=True,
            font_size=28,
            size_hint=(1, None),
            height=dp(34),
            halign="center"
        )
        self.title_lbl = Label(
            text="[b]Welcome Back[/b]",
            markup=True,
            font_size=20,
            color=C_TEXT_WHITE,
            size_hint=(1, None),
            height=dp(26),
            halign="center"
        )
        self.sub_lbl = Label(
            text="Sign in to access your customized vision assistance",
            font_size=12,
            color=C_TEXT_MUTED,
            size_hint=(1, None),
            height=dp(20),
            halign="center"
        )
        header.add_widget(brand)
        header.add_widget(self.title_lbl)
        header.add_widget(self.sub_lbl)
        root.add_widget(header)

        # Form fields
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        form_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        form_box.bind(minimum_height=form_box.setter("height"))

        self.email_input = StyledInput(
            label_text="Email or Username",
            hint_text="user@visionaid.ai",
            icon_path=ICON_USER
        )
        self.pass_input = StyledInput(
            label_text="Password",
            hint_text="Enter your password",
            icon_path=ICON_LOCK,
            is_password=True
        )

        form_box.add_widget(self.email_input)
        form_box.add_widget(self.pass_input)

        # Status / Feedback label
        self.status_lbl = Label(
            text="",
            font_size=12,
            color=C_PINK,
            size_hint=(1, None),
            height=dp(22),
            halign="center"
        )
        form_box.add_widget(self.status_lbl)

        # Login button
        self.login_btn = GradientButton(text="LOG IN", on_click=self._handle_login, height_dp=50)
        form_box.add_widget(self.login_btn)

        # Divider
        div_box = BoxLayout(size_hint=(1, None), height=dp(24), spacing=dp(10))
        or_lbl = Label(text="───  OR  ───", font_size=11, color=C_TEXT_MUTED)
        div_box.add_widget(or_lbl)
        form_box.add_widget(div_box)

        # Guest access button
        self.guest_btn = Button(
            text="CONTINUE AS GUEST",
            font_size=13,
            bold=True,
            color=C_TEXT_WHITE,
            background_normal="",
            background_color=(0.24, 0.14, 0.36, 0.95),
            size_hint=(1, None),
            height=dp(48)
        )
        with self.guest_btn.canvas.before:
            Color(*C_BORDER_DEFAULT)
            self.guest_border = Line(rounded_rectangle=(self.guest_btn.x, self.guest_btn.y, self.guest_btn.width, self.guest_btn.height, dp(14)), width=1.2)
        self.guest_btn.bind(pos=lambda *_: setattr(self.guest_border, "rounded_rectangle", (self.guest_btn.x, self.guest_btn.y, self.guest_btn.width, self.guest_btn.height, dp(14))),
                            size=lambda *_: setattr(self.guest_border, "rounded_rectangle", (self.guest_btn.x, self.guest_btn.y, self.guest_btn.width, self.guest_btn.height, dp(14))))
        self.guest_btn.bind(on_press=self._handle_guest)
        form_box.add_widget(self.guest_btn)

        # Sign up link
        self.signup_link = Button(
            text="Don't have an account? Sign Up",
            font_size=13,
            color=C_PINK,
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(1, None),
            height=dp(38)
        )
        self.signup_link.bind(on_press=self._goto_signup)
        form_box.add_widget(self.signup_link)

        scroll.add_widget(form_box)
        root.add_widget(scroll)

        self.add_widget(root)

    def on_enter(self):
        # Update texts based on current language
        self.title_lbl.text = f"[b]{language_manager.get_string('login_title')}[/b]"
        self.sub_lbl.text = language_manager.get_string("login_subtitle")
        self.login_btn.set_text(language_manager.get_string("login_btn"))
        self.guest_btn.text = language_manager.get_string("guest_btn")
        self.signup_link.text = language_manager.get_string("no_account")
        self.status_lbl.text = ""

        self.tts.speak("VisionAid Login screen. Enter your details or continue as guest.", interrupt=True)

    def _handle_login(self):
        email = self.email_input.text
        pwd = self.pass_input.text

        ok, user_info, msg = auth_manager.authenticate_user(email, pwd)
        if ok:
            self.status_lbl.color = (0.45, 0.90, 0.55, 1)
            self.status_lbl.text = msg
            self.settings.set_current_user(user_info)
            self.tts.speak(f"Welcome back {user_info['name']}", interrupt=True)
            Clock.schedule_once(lambda dt: self._goto_main(), 0.3)
        else:
            self.status_lbl.color = C_CRIMSON
            self.status_lbl.text = msg
            self.tts.speak(msg, interrupt=True)

    def _handle_guest(self, *args):
        guest_info = auth_manager.guest_login()
        self.settings.set_current_user(guest_info)
        self.tts.speak("Continuing as guest explorer.", interrupt=True)
        self._goto_main()

    def _goto_signup(self, *args):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "signup"

    def _goto_main(self):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "main"


# =====================================================================
# 3. SIGNUP SCREEN
# =====================================================================

class SignupScreen(Screen):
    """Mobile Account Creation screen with validation and audio feedback."""

    def __init__(self, settings, tts, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.tts = tts

        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(18), dp(20), dp(20)], spacing=dp(10))
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(pos=root.pos, size=root.size, source=TEX_BG)
        root.bind(pos=lambda *_: setattr(self.bg_rect, "pos", root.pos),
                  size=lambda *_: setattr(self.bg_rect, "size", root.size))

        # Top Bar with Back Button
        top_bar = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(42), spacing=dp(10))
        back_btn = Button(
            size_hint=(None, 1),
            width=dp(42),
            background_normal="",
            background_color=(0, 0, 0, 0)
        )
        back_icon = Image(source=ICON_BACK, size_hint=(1, 1), fit_mode="contain")
        back_btn.add_widget(back_icon)
        back_btn.bind(on_press=self._goto_login)

        top_title = Label(
            text="[b]Create Account[/b]",
            markup=True,
            font_size=18,
            color=C_TEXT_WHITE,
            halign="left",
            valign="middle"
        )
        top_title.bind(size=top_title.setter("text_size"))

        top_bar.add_widget(back_btn)
        top_bar.add_widget(top_title)
        root.add_widget(top_bar)

        # Form ScrollView
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        form_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        form_box.bind(minimum_height=form_box.setter("height"))

        self.name_input = StyledInput(
            label_text="Full Name",
            hint_text="e.g. Sarah Jenkins",
            icon_path=ICON_USER
        )
        self.email_input = StyledInput(
            label_text="Email Address",
            hint_text="sarah@example.com",
            icon_path=ICON_USER
        )
        self.pass_input = StyledInput(
            label_text="Password",
            hint_text="At least 4 characters",
            icon_path=ICON_LOCK,
            is_password=True
        )
        self.confirm_input = StyledInput(
            label_text="Confirm Password",
            hint_text="Re-enter your password",
            icon_path=ICON_LOCK,
            is_password=True
        )

        form_box.add_widget(self.name_input)
        form_box.add_widget(self.email_input)
        form_box.add_widget(self.pass_input)
        form_box.add_widget(self.confirm_input)

        # Status label
        self.status_lbl = Label(
            text="",
            font_size=12,
            color=C_PINK,
            size_hint=(1, None),
            height=dp(22),
            halign="center"
        )
        form_box.add_widget(self.status_lbl)

        # Create Account Button
        self.signup_btn = GradientButton(
            text="CREATE ACCOUNT",
            on_click=self._handle_signup,
            height_dp=50
        )
        form_box.add_widget(self.signup_btn)

        # Already have account link
        login_link = Button(
            text="Already have an account? Log In",
            font_size=13,
            color=C_LILAC,
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(1, None),
            height=dp(38)
        )
        login_link.bind(on_press=self._goto_login)
        form_box.add_widget(login_link)

        scroll.add_widget(form_box)
        root.add_widget(scroll)

        self.add_widget(root)

    def on_enter(self):
        self.status_lbl.text = ""
        self.tts.speak("Create Account screen. Enter your name, email, and password.", interrupt=True)

    def _handle_signup(self):
        name = self.name_input.text
        email = self.email_input.text
        pwd = self.pass_input.text
        conf = self.confirm_input.text

        if pwd != conf:
            self.status_lbl.color = C_CRIMSON
            self.status_lbl.text = "Passwords do not match."
            self.tts.speak("Passwords do not match.", interrupt=True)
            return

        ok, user_info, msg = auth_manager.register_user(name, email, pwd)
        if ok:
            self.status_lbl.color = (0.45, 0.90, 0.55, 1)
            self.status_lbl.text = "Account created! Logging in..."
            self.settings.set_current_user(user_info)
            self.tts.speak(f"Account created successfully. Welcome to VisionAid, {name}.", interrupt=True)
            Clock.schedule_once(lambda dt: self._goto_main(), 0.5)
        else:
            self.status_lbl.color = C_CRIMSON
            self.status_lbl.text = msg
            self.tts.speak(msg, interrupt=True)

    def _goto_login(self, *args):
        if self.manager:
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "login"

    def _goto_main(self):
        if self.manager:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "main"
