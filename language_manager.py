"""
VisionAid - Language & Localization Engine
Supports multi-language selection, native scripts, and localized accessibility announcements.
"""

SUPPORTED_LANGUAGES = [
    {
        "code": "en",
        "name": "English",
        "native": "English",
        "badge": "EN",
        "greeting": "Welcome to VisionAid. Your AI accessibility companion.",
        "confirmation": "English selected."
    },
    {
        "code": "hi",
        "name": "Hindi",
        "native": "हिन्दी",
        "badge": "हि",
        "greeting": "विज़नएड में आपका स्वागत है। आपका एआई साथी।",
        "confirmation": "हिन्दी भाषा चुनी गई।"
    },
    {
        "code": "es",
        "name": "Spanish",
        "native": "Español",
        "badge": "ES",
        "greeting": "Bienvenido a VisionAid. Su asistente de visión artificial.",
        "confirmation": "Español seleccionado."
    },
    {
        "code": "fr",
        "name": "French",
        "native": "Français",
        "badge": "FR",
        "greeting": "Bienvenue sur VisionAid. Votre compagnon d'accessibilité IA.",
        "confirmation": "Français sélectionné."
    },
    {
        "code": "de",
        "name": "German",
        "native": "Deutsch",
        "badge": "DE",
        "greeting": "Willkommen bei VisionAid. Ihr KI-Begleiter für Barrierefreiheit.",
        "confirmation": "Deutsch ausgewählt."
    },
    {
        "code": "ja",
        "name": "Japanese",
        "native": "日本語",
        "badge": "JA",
        "greeting": "VisionAidへようこそ。AIアクセシビリティコンパニオン。",
        "confirmation": "日本語が選択されました。"
    }
]

TRANSLATIONS = {
    "en": {
        "lang_title": "Choose Language",
        "lang_subtitle": "Select your preferred language for voice and guidance",
        "continue": "CONTINUE",
        "login_title": "Welcome Back",
        "login_subtitle": "Sign in to access your customized VisionAid experience",
        "email_label": "Email or Username",
        "email_hint": "Enter your email or username",
        "password_label": "Password",
        "password_hint": "Enter your password",
        "login_btn": "LOG IN",
        "signup_btn": "CREATE ACCOUNT",
        "guest_btn": "CONTINUE AS GUEST",
        "no_account": "Don't have an account? Sign Up",
        "have_account": "Already have an account? Log In",
        "signup_title": "Create Account",
        "signup_subtitle": "Register for synchronized settings & contact profiles",
        "name_label": "Full Name",
        "name_hint": "Enter your full name",
        "confirm_password_label": "Confirm Password",
        "confirm_password_hint": "Re-enter your password",
        "guest_mode": "Guest Mode Active",
        "logout": "LOG OUT",
        "change_lang": "Change Language",
        "account_title": "Account & Profile",
        "logged_in_as": "Logged in as",
    },
    "hi": {
        "lang_title": "भाषा चुनें",
        "lang_subtitle": "आवाज़ और मार्गदर्शन के लिए अपनी पसंदीदा भाषा चुनें",
        "continue": "आगे बढ़ें",
        "login_title": "वापसी पर स्वागत है",
        "login_subtitle": "अपने विज़नएड खाते में साइन इन करें",
        "email_label": "ईमेल या यूज़रनेम",
        "email_hint": "अपना ईमेल दर्ज करें",
        "password_label": "पासवर्ड",
        "password_hint": "अपना पासवर्ड दर्ज करें",
        "login_btn": "लॉग इन करें",
        "signup_btn": "खाता बनाएं",
        "guest_btn": "अतिथि के रूप में जारी रखें",
        "no_account": "खाता नहीं है? साइन अप करें",
        "have_account": "पहले से खाता है? लॉग इन करें",
        "signup_title": "नया खाता बनाएं",
        "signup_subtitle": "संपर्क प्रोफाइल और सेटिंग्स के लिए पंजीकरण करें",
        "name_label": "पूरा नाम",
        "name_hint": "अपना पूरा नाम दर्ज करें",
        "confirm_password_label": "पासवर्ड की पुष्टि करें",
        "confirm_password_hint": "पुनः पासवर्ड दर्ज करें",
        "guest_mode": "अतिथि मोड सक्रिय",
        "logout": "लॉग आउट करें",
        "change_lang": "भाषा बदलें",
        "account_title": "खाता और प्रोफाइल",
        "logged_in_as": "लॉग इन:",
    },
    "es": {
        "lang_title": "Elegir Idioma",
        "lang_subtitle": "Seleccione su idioma preferido para voz y navegación",
        "continue": "CONTINUAR",
        "login_title": "Bienvenido",
        "login_subtitle": "Inicie sesión para acceder a su VisionAid",
        "email_label": "Correo o Usuario",
        "email_hint": "Ingrese su correo o usuario",
        "password_label": "Contraseña",
        "password_hint": "Ingrese su contraseña",
        "login_btn": "INICIAR SESIÓN",
        "signup_btn": "CREAR CUENTA",
        "guest_btn": "CONTINUAR COMO INVITADO",
        "no_account": "¿No tiene cuenta? Regístrese",
        "have_account": "¿Ya tiene cuenta? Iniciar Sesión",
        "signup_title": "Crear Cuenta",
        "signup_subtitle": "Regístrese para sincronizar preferencias",
        "name_label": "Nombre Completo",
        "name_hint": "Ingrese su nombre completo",
        "confirm_password_label": "Confirmar Contraseña",
        "confirm_password_hint": "Reingrese su contraseña",
        "guest_mode": "Modo Invitado",
        "logout": "CERRAR SESIÓN",
        "change_lang": "Cambiar Idioma",
        "account_title": "Cuenta y Perfil",
        "logged_in_as": "Conectado como",
    },
    "fr": {
        "lang_title": "Choisir la Langue",
        "lang_subtitle": "Sélectionnez votre langue préférée pour l'audio",
        "continue": "CONTINUER",
        "login_title": "Bienvenue",
        "login_subtitle": "Connectez-vous à votre compte VisionAid",
        "email_label": "Email ou Identifiant",
        "email_hint": "Entrez votre email",
        "password_label": "Mot de passe",
        "password_hint": "Entrez votre mot de passe",
        "login_btn": "SE CONNECTER",
        "signup_btn": "CRÉER UN COMPTE",
        "guest_btn": "CONTINUER EN INVITÉ",
        "no_account": "Pas de compte ? Inscrivez-vous",
        "have_account": "Déjà un compte ? Connexion",
        "signup_title": "Créer un Compte",
        "signup_subtitle": "Inscrivez-vous pour synchroniser vos profils",
        "name_label": "Nom Complet",
        "name_hint": "Entrez votre nom",
        "confirm_password_label": "Confirmer le mot de passe",
        "confirm_password_hint": "Retapez votre mot de passe",
        "guest_mode": "Mode Invité Actif",
        "logout": "DÉCONNEXION",
        "change_lang": "Changer de Langue",
        "account_title": "Compte et Profil",
        "logged_in_as": "Connecté en tant que",
    },
    "de": {
        "lang_title": "Sprache Wählen",
        "lang_subtitle": "Wählen Sie Ihre bevorzugte Sprache für Sprachführung",
        "continue": "WEITER",
        "login_title": "Willkommen Zurück",
        "login_subtitle": "Melden Sie sich bei Ihrem VisionAid-Konto an",
        "email_label": "E-Mail oder Benutzername",
        "email_hint": "E-Mail eingeben",
        "password_label": "Passwort",
        "password_hint": "Passwort eingeben",
        "login_btn": "ANMELDEN",
        "signup_btn": "KONTO ERSTELLEN",
        "guest_btn": "ALS GAST FORTFAHREN",
        "no_account": "Noch kein Konto? Registrieren",
        "have_account": "Bereits ein Konto? Anmelden",
        "signup_title": "Konto Erstellen",
        "signup_subtitle": "Registrieren Sie sich für Profile und Einstellungen",
        "name_label": "Vollständiger Name",
        "name_hint": "Name eingeben",
        "confirm_password_label": "Passwort bestätigen",
        "confirm_password_hint": "Passwort wiederholen",
        "guest_mode": "Gastmodus Aktiv",
        "logout": "ABMELDEN",
        "change_lang": "Sprache Ändern",
        "account_title": "Konto & Profil",
        "logged_in_as": "Angemeldet als",
    },
    "ja": {
        "lang_title": "言語を選択",
        "lang_subtitle": "音声とガイドの言語を選択してください",
        "continue": "次へ進む",
        "login_title": "おかえりなさい",
        "login_subtitle": "VisionAidにサインインしてください",
        "email_label": "メールアドレスまたはユーザー名",
        "email_hint": "メールアドレスを入力",
        "password_label": "パスワード",
        "password_hint": "パスワードを入力",
        "login_btn": "ログイン",
        "signup_btn": "新規登録",
        "guest_btn": "ゲストとして続行",
        "no_account": "アカウントをお持ちでないですか？登録",
        "have_account": "すでにアカウントをお持ちですか？ログイン",
        "signup_title": "アカウント作成",
        "signup_subtitle": "設定や連絡先プロファイルを保存します",
        "name_label": "氏名",
        "name_hint": "氏名を入力",
        "confirm_password_label": "パスワード再入力",
        "confirm_password_hint": "再度パスワードを入力",
        "guest_mode": "ゲストモード",
        "logout": "ログアウト",
        "change_lang": "言語を変更",
        "account_title": "アカウントとプロファイル",
        "logged_in_as": "ログイン中:",
    }
}


class LanguageManager:
    """Manages language choices and UI string lookups."""

    def __init__(self, current_code="en"):
        self.current_code = current_code

    def get_supported_languages(self):
        return SUPPORTED_LANGUAGES

    def set_language(self, code):
        if any(l["code"] == code for l in SUPPORTED_LANGUAGES):
            self.current_code = code

    def get_string(self, key, code=None):
        c = code or self.current_code
        lang_dict = TRANSLATIONS.get(c, TRANSLATIONS["en"])
        return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))

    def get_language_info(self, code=None):
        c = code or self.current_code
        for l in SUPPORTED_LANGUAGES:
            if l["code"] == c:
                return l
        return SUPPORTED_LANGUAGES[0]


# Global singleton instance
language_manager = LanguageManager()
