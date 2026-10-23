"""
VisionAid - Language & Localization Engine
Supports multi-language selection, native scripts, localized speech announcements,
YOLO object translation, and spatial audio directions.
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
        # Auth & Onboarding
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
        "logged_out": "Logged out successfully.",

        # Top Bar & HUD
        "app_subtitle": "AI Accessibility Companion",
        "status_standby": "STANDBY",
        "status_active": "ACTIVE",
        "status_cam_error": "CAM ERROR",
        "status_listening": "LISTENING",
        "banner_standby": "System ready to assist you.",
        "banner_monitoring": "Monitoring path for obstacles...",
        "banner_detecting": "Identifying objects in surroundings...",
        "banner_reading": "Align camera with text...",
        "banner_radar": "Scanning spatial proximity...",
        "banner_face": "Scanning for faces & expressions...",
        "cam_standby_title": "Vision Camera Standby",
        "cam_standby_sub": "Select an AI mode below to activate vision assistance",

        # Cards
        "card_find_title": "Find Object",
        "card_find_sub": "Target locator with audio feedback",
        "card_object_title": "Object Guidance",
        "card_object_sub": "Identifies items, people & vehicles",
        "card_radar_title": "Spatial Radar",
        "card_radar_sub": "Directional pulses alert to obstacles",
        "card_face_title": "Face Companion",
        "card_face_sub": "Identify familiar contacts & expressions",
        "card_text_title": "Read Text",
        "card_text_sub": "Recognize documents, signage & books",
        "card_obstacle_title": "Obstacle Guidance",
        "card_obstacle_sub": "Real-time proximity warnings & alerts",
        "card_voice_title": "Voice Assistant",
        "card_voice_sub": "Hands-free voice control",
        "card_stop_title": "Stop Camera",
        "card_stop_sub": "Turn off video feed & pause vision",

        # Settings
        "settings_title": "SETTINGS & PREFERENCES",
        "settings_subtitle": "Personalize audio, safety and vision assistance",
        "lang_selector_title": "SELECT LANGUAGE & VOICE",
        "audio_title": "VOICE & SPEECH SYNTHESIS",
        "vol_title": "Voice Volume",
        "spd_title": "Speech Speed",
        "play_sample": "Play Voice Sample",
        "obs_title": "SAFETY & PROXIMITY ALERTS",
        "obs_thresh": "Proximity Alert Threshold",
        "voice_assist": "HANDS-FREE ASSISTANCE",
        "voice_rec": "Voice Recognition",
        "account_lang": "Account & Preferences",
        "user_lbl_prefix": "User",
        "back": "BACK",

        # Speech announcements
        "guidance_ready": "System ready to assist you.",
        "mode_obstacle": "Obstacle guidance started",
        "mode_obstacle_stopped": "Obstacle guidance stopped",
        "mode_object": "Object detection started",
        "mode_radar": "Spatial radar navigation started",
        "mode_face": "Face and contact recognition started",
        "mode_text": "Text reading mode started. Hold text steady in front of camera.",
        "camera_stopped": "Camera stopped",
        "camera_error": "Could not access camera device",
        "listening": "Listening for command...",
        "unrecognized": "Sorry, command not recognized",
        "voice_disabled": "Voice commands are disabled in settings",
        "preview_speech": "This is a preview of your VisionAid speech settings.",
    },
    "hi": {
        # Auth & Onboarding
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
        "logged_out": "सफलतापूर्वक लॉग आउट हो गया।",

        # Top Bar & HUD
        "app_subtitle": "एआई सुगमता साथी",
        "status_standby": "स्टैंडबाय",
        "status_active": "सक्रिय",
        "status_cam_error": "कैमरा त्रुटि",
        "status_listening": "सुन रहा है",
        "banner_standby": "सिस्टम आपकी सहायता के लिए तैयार है।",
        "banner_monitoring": "रास्ते में बाधाओं की निगरानी जारी है...",
        "banner_detecting": "आस-पास की वस्तुओं की पहचान जारी है...",
        "banner_reading": "कैमरे को टेक्स्ट के सामने रखें...",
        "banner_radar": "दूरी और दिशा स्कैन की जा रही है...",
        "banner_face": "चेहरे और भाव स्कैन किए जा रहे हैं...",
        "cam_standby_title": "कैमरा स्टैंडबाय",
        "cam_standby_sub": "मार्गदर्शन शुरू करने के लिए नीचे कोई मोड चुनें",

        # Cards
        "card_find_title": "वस्तु खोजें",
        "card_find_sub": "आवाज़ मार्गदर्शन से लक्ष्य खोजें",
        "card_object_title": "वस्तु पहचान",
        "card_object_sub": "सामान, लोग और वाहनों की पहचान",
        "card_radar_title": "दिशात्मक रडार",
        "card_radar_sub": "बाधाओं के लिए दिशात्मक आवाज़",
        "card_face_title": "चेहरा साथी",
        "card_face_sub": "परिचित लोगों और भावों की पहचान",
        "card_text_title": "टेक्स्ट पढ़ें",
        "card_text_sub": "दस्तावेज़, बोर्ड और किताबें पढ़ें",
        "card_obstacle_title": "बाधा चेतावनी",
        "card_obstacle_sub": "समीप की बाधाओं की तुरंत चेतावनी",
        "card_voice_title": "वॉइस सहायक",
        "card_voice_sub": "आवाज़ से हैंड्स-फ्री नियंत्रण",
        "card_stop_title": "कैमरा रोकें",
        "card_stop_sub": "कैमरा बंद करें और विश्लेषण रोकें",

        # Settings
        "settings_title": "सेटिंग्स और प्राथमिकताएं",
        "settings_subtitle": "आवाज़, सुरक्षा और विज़न मार्गदर्शन अनुकूलित करें",
        "lang_selector_title": "भाषा और आवाज़ चुनें",
        "audio_title": "आवाज़ और वाक् संश्लेषण",
        "vol_title": "आवाज़ की मात्रा",
        "spd_title": "बोलने की गति",
        "play_sample": "आवाज़ का नमूना सुनें",
        "obs_title": "सुरक्षा और निकटता चेतावनी",
        "obs_thresh": "चेतावनी दूरी सीमा",
        "voice_assist": "हैंड्स-फ्री सहायता",
        "voice_rec": "आवाज़ पहचान",
        "account_lang": "खाता और प्राथमिकताएं",
        "user_lbl_prefix": "उपयोगकर्ता",
        "back": "पीछे",

        # Speech announcements
        "guidance_ready": "सिस्टम सहायता के लिए तैयार है।",
        "mode_obstacle": "बाधा चेतावनी शुरू हो गई",
        "mode_obstacle_stopped": "बाधा चेतावनी रोक दी गई",
        "mode_object": "वस्तु पहचान शुरू हो गई",
        "mode_radar": "दिशात्मक रडार नेविगेशन शुरू",
        "mode_face": "चेहरा पहचान साथी शुरू",
        "mode_text": "टेक्स्ट पठन मोड शुरू। कैमरे के सामने टेक्स्ट को स्थिर रखें।",
        "camera_stopped": "कैमरा बंद कर दिया गया",
        "camera_error": "कैमरा डिवाइस कनेक्ट नहीं हो सका",
        "listening": "कमांड सुन रहा हूँ...",
        "unrecognized": "क्षमा करें, कमांड समझ नहीं आया",
        "voice_disabled": "सेटिंग्स में वॉइस कमांड बंद है",
        "preview_speech": "यह आपकी विज़नएड आवाज़ सेटिंग्स का पूर्वावलोकन है।",
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
        "logged_out": "Sesión cerrada.",

        "app_subtitle": "Asistente Visual IA",
        "status_standby": "EN ESPERA",
        "status_active": "ACTIVO",
        "status_cam_error": "ERROR CÁMARA",
        "status_listening": "ESCUCHANDO",
        "banner_standby": "Sistema listo para ayudarle.",
        "card_find_title": "Buscar Objeto",
        "card_object_title": "Detección de Objetos",
        "card_radar_title": "Radar Espacial",
        "card_face_title": "Reconocimiento Facial",
        "card_text_title": "Leer Texto",
        "card_obstacle_title": "Guía de Obstáculos",
        "card_voice_title": "Asistente de Voz",
        "card_stop_title": "Detener Cámara",
        "settings_title": "AJUSTES Y PREFERENCIAS",
        "lang_selector_title": "SELECCIONAR IDIOMA Y VOZ",
        "play_sample": "Probar Voz",
        "back": "ATRÁS",

        "guidance_ready": "Sistema listo para ayudarle.",
        "mode_obstacle": "Guía de obstáculos iniciada",
        "mode_obstacle_stopped": "Guía de obstáculos detenida",
        "mode_object": "Detección de objetos iniciada",
        "mode_radar": "Navegación por radar iniciada",
        "mode_face": "Reconocimiento facial iniciado",
        "mode_text": "Lectura de texto iniciada.",
        "camera_stopped": "Cámara detenida",
        "camera_error": "No se pudo acceder a la cámara",
        "listening": "Escuchando comando...",
        "unrecognized": "Comando no reconocido",
        "voice_disabled": "Comandos de voz desactivados",
        "preview_speech": "Esta es una vista previa de la voz de VisionAid.",
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
        "logged_out": "Déconnexion réussie.",

        "app_subtitle": "Compagnon Visuel IA",
        "status_standby": "EN ATTENTE",
        "status_active": "ACTIF",
        "status_cam_error": "ERREUR CAM",
        "status_listening": "ÉCOUTE",
        "banner_standby": "Système prêt à vous assister.",
        "card_find_title": "Trouver Objet",
        "card_object_title": "Détection d'Objets",
        "card_radar_title": "Radar Spatial",
        "card_face_title": "Compagnon Visage",
        "card_text_title": "Lire le Texte",
        "card_obstacle_title": "Alerte Obstacles",
        "card_voice_title": "Assistant Vocal",
        "card_stop_title": "Arrêter Caméra",
        "settings_title": "PARAMÈTRES & PRÉFÉRENCES",
        "lang_selector_title": "LANGUE ET VOIX",
        "play_sample": "Écouter la Voix",
        "back": "RETOUR",

        "guidance_ready": "Système prêt à vous assister.",
        "mode_obstacle": "Guidage d'obstacles démarré",
        "mode_obstacle_stopped": "Guidage d'obstacles arrêté",
        "mode_object": "Détection d'objets démarrée",
        "mode_radar": "Navigation radar démarrée",
        "mode_face": "Reconnaissance faciale démarrée",
        "mode_text": "Lecture de texte démarrée.",
        "camera_stopped": "Caméra arrêtée",
        "camera_error": "Impossible d'accéder à la caméra",
        "listening": "Écoute de commande...",
        "unrecognized": "Commande non reconnue",
        "voice_disabled": "Commandes vocales désactivées",
        "preview_speech": "Aperçu de la voix VisionAid.",
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
        "logged_out": "Erfolgreich abgemeldet.",

        "app_subtitle": "KI-Barrierefreiheits-Assistent",
        "status_standby": "BEREIT",
        "status_active": "AKTIV",
        "status_cam_error": "KAMERA-FEHLER",
        "status_listening": "HÖREN",
        "banner_standby": "System bereit zu helfen.",
        "card_find_title": "Objekt Suchen",
        "card_object_title": "Objekterkennung",
        "card_radar_title": "Raum-Radar",
        "card_face_title": "Gesichtserkennung",
        "card_text_title": "Text Vorlesen",
        "card_obstacle_title": "Hindernis-Führung",
        "card_voice_title": "Sprachassistent",
        "card_stop_title": "Kamera Stoppen",
        "settings_title": "EINSTELLUNGEN & OPTIONEN",
        "lang_selector_title": "SPRACHE & STIMME WÄHLEN",
        "play_sample": "Sprachprobe",
        "back": "ZURÜCK",

        "guidance_ready": "System bereit zu helfen.",
        "mode_obstacle": "Hindernisführung gestartet",
        "mode_obstacle_stopped": "Hindernisführung gestoppt",
        "mode_object": "Objekterkennung gestartet",
        "mode_radar": "Radarnavigation gestartet",
        "mode_face": "Gesichtserkennung gestartet",
        "mode_text": "Textlesen gestartet.",
        "camera_stopped": "Kamera gestoppt",
        "camera_error": "Kein Zugriff auf Kamera",
        "listening": "Warte auf Sprachbefehl...",
        "unrecognized": "Befehl nicht erkannt",
        "voice_disabled": "Sprachbefehle deaktiviert",
        "preview_speech": "Vorschau der VisionAid-Stimme.",
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
        "logged_out": "ログアウトしました。",

        "app_subtitle": "AI視覚支援パートナー",
        "status_standby": "待機中",
        "status_active": "作動中",
        "status_cam_error": "カメラエラー",
        "status_listening": "聞き取り中",
        "banner_standby": "アシスタントの準備が完了しました。",
        "card_find_title": "物を探す",
        "card_object_title": "物体認識",
        "card_radar_title": "空間レーダー",
        "card_face_title": "顔・表情認識",
        "card_text_title": "文字読み上げ",
        "card_obstacle_title": "障害物ガイダンス",
        "card_voice_title": "音声アシスタント",
        "card_stop_title": "カメラ停止",
        "settings_title": "設定と環境設定",
        "lang_selector_title": "言語と音声の選択",
        "play_sample": "音声をテスト",
        "back": "戻る",

        "guidance_ready": "アシスタントの準備が完了しました。",
        "mode_obstacle": "障害物案内を開始しました",
        "mode_obstacle_stopped": "障害物案内を停止しました",
        "mode_object": "物体検出を開始しました",
        "mode_radar": "空間レーダーを開始しました",
        "mode_face": "顔認識を開始しました",
        "mode_text": "テキスト読み上げを開始しました。",
        "camera_stopped": "カメラを停止しました",
        "camera_error": "カメラにアクセスできません",
        "listening": "コマンドをお待ちしています...",
        "unrecognized": "認識できませんでした",
        "voice_disabled": "音声操作は無効です",
        "preview_speech": "VisionAidの音声プレビューです。",
    }
}

# YOLO Object Translations (English to Hindi & other languages)
YOLO_OBJECT_TRANSLATIONS = {
    "hi": {
        "person": "व्यक्ति",
        "bicycle": "साइकिल",
        "car": "गाड़ी",
        "motorcycle": "मोटरसाइकिल",
        "airplane": "हवाई जहाज़",
        "bus": "बस",
        "train": "ट्रेन",
        "truck": "ट्रक",
        "boat": "नाव",
        "traffic light": "ट्रैफिक लाइट",
        "fire hydrant": "फायर हाइड्रेंट",
        "stop sign": "स्टॉप साइन",
        "parking meter": "पार्किंग मीटर",
        "bench": "बेंच",
        "bird": "पक्षी",
        "cat": "बिल्ली",
        "dog": "कुत्ता",
        "horse": "घोड़ा",
        "sheep": "भेड़",
        "cow": "गाय",
        "elephant": "हाथी",
        "bear": "भालू",
        "zebra": "ज़ेबरा",
        "giraffe": "जिराफ़",
        "backpack": "बैग",
        "umbrella": "छाता",
        "handbag": "हैंडबैग",
        "tie": "टाई",
        "suitcase": "सूटकेस",
        "bottle": "बोतल",
        "wine glass": "ग्लास",
        "cup": "कप",
        "fork": "कांटा",
        "knife": "चाकू",
        "spoon": "चम्मच",
        "bowl": "कटोरा",
        "banana": "केला",
        "apple": "सेब",
        "sandwich": "सैंडविच",
        "orange": "संतरा",
        "broccoli": "ब्रोकोली",
        "carrot": "गाजर",
        "pizza": "पिज़्ज़ा",
        "donut": "डोनट",
        "cake": "केक",
        "chair": "कुर्सी",
        "couch": "सोफ़ा",
        "sofa": "सोफ़ा",
        "potted plant": "गमला",
        "bed": "बिस्तर",
        "dining table": "मेज़",
        "table": "मेज़",
        "toilet": "शौचालय",
        "tv": "टीवी",
        "tvmonitor": "टीवी",
        "laptop": "लैपटॉप",
        "mouse": "माउस",
        "remote": "रिमोट",
        "keyboard": "कीबोर्ड",
        "cell phone": "मोबाइल फोन",
        "phone": "मोबाइल",
        "microwave": "माइक्रोवेव",
        "oven": "ओवन",
        "toaster": "टोस्टर",
        "sink": "सिंक",
        "refrigerator": "फ्रिज",
        "book": "किताब",
        "clock": "घड़ी",
        "vase": "फूलदान",
        "scissors": "कैंची",
        "teddy bear": "टेडी बियर",
        "hair drier": "हेयर ड्रायर",
        "toothbrush": "टूथब्रश",
        "glasses": "चश्मा",
        "sunglasses": "धूप का चश्मा",
        "keys": "चाबी",
        "key": "चाबी",
        "pen": "पेन",
        "pencil": "पेंसिल",
        "notebook": "कॉपी",
        "copy": "कॉपी",
        "door": "दरवाज़ा",
        "stairs": "सीढ़ियाँ",
        "wall": "दीवार",
        "window": "खिड़की",
        "obstacle": "बाधा",
        "object": "वस्तु",
    }
}


class LanguageManager:
    """Manages language choices, UI string lookups, and spoken guidance formatting."""

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

    def t(self, key, code=None):
        """Short alias for get_string."""
        return self.get_string(key, code)

    def get_language_info(self, code=None):
        c = code or self.current_code
        for l in SUPPORTED_LANGUAGES:
            if l["code"] == c:
                return l
        return SUPPORTED_LANGUAGES[0]

    def translate_label(self, label, code=None):
        c = code or self.current_code
        lbl_clean = str(label).lower().strip()
        if c in YOLO_OBJECT_TRANSLATIONS:
            return YOLO_OBJECT_TRANSLATIONS[c].get(lbl_clean, label)
        return label

    def translate_position(self, pos_str, code=None):
        c = code or self.current_code
        p = str(pos_str).lower().strip()
        if c == "hi":
            if "left" in p:
                return "आपके बाईं ओर"
            elif "right" in p:
                return "आपके दाईं ओर"
            elif "directly in front" in p:
                return "सीधे आपके सामने"
            elif "front" in p or "center" in p:
                return "आपके सामने"
            return p
        return pos_str

    def translate_distance(self, dist_str, code=None):
        c = code or self.current_code
        d = str(dist_str).lower().strip()
        if c == "hi":
            if "very close" in d:
                return "बहुत पास"
            elif "close" in d:
                return "पास"
            elif "ahead" in d or "meters" in d or "away" in d:
                return "आगे"
            return d
        return dist_str

    def format_obstacle_warning(self, label, pos="directly in front of you", dist="very close", code=None):
        c = code or self.current_code
        lbl = self.translate_label(label, c)
        if c == "hi":
            p = self.translate_position(pos, c)
            d = self.translate_distance(dist, c)
            return f"सावधान! {lbl} {p} {d} है।"
        return f"Warning! {label} is very close directly in front of you."

    def format_detection(self, label, dist="close", pos="in front of you", code=None):
        c = code or self.current_code
        lbl = self.translate_label(label, c)
        if c == "hi":
            p = self.translate_position(pos, c)
            d = self.translate_distance(dist, c)
            return f"मुझे {p} {d} पर {lbl} दिख रहा है।"
        return f"I see a {label} {dist} {pos}."

    def format_target_found(self, target, pos="in front of you", dist="close", code=None):
        c = code or self.current_code
        tgt = self.translate_label(target, c)
        if c == "hi":
            p = self.translate_position(pos, c)
            d = self.translate_distance(dist, c)
            return f"{tgt} मिल गया! यह {p}, {d} है।"
        return f"Found {target}! It is {pos}, {dist}."

    def format_text_reading(self, text, code=None):
        c = code or self.current_code
        if c == "hi":
            return f"यहाँ लिखा है: {text}"
        return f"I can read: {text}"

    def format_face_found(self, name, pos="in front of you", code=None):
        c = code or self.current_code
        if c == "hi":
            p = self.translate_position(pos, c)
            return f"{name} {p} मौजूद हैं।"
        return f"Found {name}, {pos}."

    def get_ask_what_to_find(self, code=None):
        c = code or self.current_code
        prompts = {
            "hi": "आप क्या खोजना चाहते हैं?",
            "en": "What would you like to find?",
            "es": "¿Qué desea buscar?",
            "fr": "Que souhaitez-vous trouver?",
            "de": "Was möchten Sie suchen?",
            "ja": "何を探しますか？",
            "ar": "ما الذي تريد البحث عنه؟"
        }
        return prompts.get(c, prompts["en"])

    def format_search_prompt(self, target, code=None):
        c = code or self.current_code
        tgt = self.translate_label(target, c)
        if c == "hi":
            return f"{tgt} खोज रहे हैं। कैमरा धीरे घुमाएं।"
        elif c == "es":
            return f"Buscando {tgt}. Mueva la cámara despacio."
        elif c == "fr":
            return f"Recherche de {tgt}. Déplacez la caméra lentement."
        elif c == "de":
            return f"Suche nach {tgt}. Bewegen Sie die Kamera langsam."
        elif c == "ja":
            return f"{tgt}を探しています。カメラをゆっくり動かしてください。"
        elif c == "ar":
            return f"جاري البحث عن {tgt}. حرك الكاميرا ببطء."
        return f"Searching for {target}. Pan camera slowly."

    def get_sr_language(self, code=None):
        c = code or self.current_code
        sr_map = {
            "hi": "hi-IN",
            "en": "en-IN",
            "es": "es-ES",
            "fr": "fr-FR",
            "de": "de-DE",
            "ja": "ja-JP",
            "ar": "ar-SA"
        }
        return sr_map.get(c, "en-US")

    def detect_object_in_text(self, text, code=None):
        """Checks if text contains an explicit object name without needing find/search prefixes."""
        if not text:
            return None
        t = str(text).lower()

        # Explicit Hindi/Hinglish/English synonym dictionary
        mappings = {
            "cell phone": ["phone", "mobile", "cell phone", "smartphone", "फ़ोन", "फोन", "मोबाइल", "सेलफोन"],
            "pen": ["pen", "ballpen", "pencil", "पेन", "कलम", "पेंसिल"],
            "cup": ["cup", "mug", "कप", "प्याला", "मिल्क मग", "चाय का कप", "चाय कप"],
            "bottle": ["bottle", "water bottle", "flask", "बोतल", "पानी की बोतल", "बॉटल", "pani"],
            "glasses": ["glasses", "sunglasses", "specs", "spectacles", "goggles", "chashma", "chashme", "chasma", "चश्मा", "चश्मे", "धूप का चश्मा", "चस्मा"],
            "keys": ["key", "keys", "chabi", "chabhi", "chabiyan", "चाबी", "चाबियां", "चाभी", "चाभियां"],
            "laptop": ["laptop", "computer", "लैपटॉप", "कंप्यूटर", "पीसी"],
            "chair": ["chair", "armchair", "kursi", "kursiya", "कुर्सी", "कुर्सियां"],
            "couch": ["couch", "sofa", "सोफ़ा", "सोफा"],
            "book": ["book", "notebook", "copy", "kitab", "pustak", "किताब", "किताबें", "पुस्तक", "कॉपी"],
            "clock": ["clock", "watch", "ghadi", "ghadiyan", "घड़ी", "घड़ी", "हाथ घड़ी"],
            "remote": ["remote", "controller", "रिमोट", "टीवी रिमोट"],
            "backpack": ["backpack", "bag", "basta", "बैग", "बस्ता", "स्कूल बैग"],
            "scissors": ["scissors", "kainchi", "कैंची", "कैची"],
            "person": ["person", "human", "someone", "man", "woman", "insan", "aadmi", "aurat", "व्यक्ति", "इंसान", "आदमी", "औरत", "दोस्त"],
            "cat": ["cat", "kitten", "billi", "billa", "बिल्ली", "बिल्ला"],
            "dog": ["dog", "puppy", "kutta", "pilla", "कुत्ता", "पिल्ला"],
        }
        for yolo_lbl, syns in mappings.items():
            for syn in syns:
                if syn in t:
                    return yolo_lbl

        # Check Hindi translation dictionary
        hi_dict = TRANSLATIONS.get("hi", {})
        for yolo_key, hi_val in hi_dict.items():
            if hi_val and hi_val in t and len(hi_val) > 1:
                return yolo_key

        return None

    def resolve_target_label(self, raw_input, code=None):
        """Map user speech (Devanagari, Hinglish, or English) to a canonical YOLO target."""
        if not raw_input:
            return "cup"
        t = str(raw_input).lower().strip()

        # 1. Direct object scan before stripping
        obj = self.detect_object_in_text(t)
        if obj:
            return obj

        # 2. Common stop phrases and affixes to strip
        for prefix in [
            "please find my", "please find", "please search my", "please search for", "please search", "please",
            "where is my", "where is", "search for my", "search for", "search my", "search", "find my", "find", "locate", "look for",
            "mera", "meri", "mere", "apna", "apni", "apne", "mujhe", "chahiye", "do", "karo", "dikhao",
            "dhundho", "dhundo", "dhund do", "dhund de", "dhund", "khojo", "khoj do", "khoj", "kahan hai", "kidhar hai", "lao", "dekho",
            "ढूंढो", "ढूंढ दो", "ढूंढ दे", "ढूंढ", "खोजो", "खोज दो", "खोज", "कहाँ है", "किधर है", "कहा है", "कहाँ", "लाओ", "देखो", "चाहिए",
            "मेरा", "मेरी", "मेरे", "मुझे", "अपना", "अपनी", "अपने", "दो", "कृपया", "प्लीज"
        ]:
            t = t.replace(prefix, " ")
        t = " ".join(t.split())
        if not t:
            return "cup"

        # 3. Check again after stop-phrase stripping
        obj = self.detect_object_in_text(t)
        if obj:
            return obj

        words = t.split()
        return words[0] if words else "cup"



# Global singleton instance
language_manager = LanguageManager()


def get_language_manager():
    return language_manager


# Module-level convenience functions
def detect_object_in_text(text, code=None):
    return language_manager.detect_object_in_text(text, code)


def resolve_target_label(raw_input, code=None):
    return language_manager.resolve_target_label(raw_input, code)


def get_string(key, code=None):
    return language_manager.get_string(key, code)


def translate_label(label, code=None):
    return language_manager.translate_label(label, code)


def get_sr_language(code=None):
    return language_manager.get_sr_language(code)


def get_ask_what_to_find(code=None):
    return language_manager.get_ask_what_to_find(code)


def format_search_prompt(target, code=None):
    return language_manager.format_search_prompt(target, code)
