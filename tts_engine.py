import platform
import threading
import sys

# Ensure UTF-8 output on Windows consoles without charmap crash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass



import os

try:
    from kivy.utils import platform as kivy_platform
    IS_ANDROID = (kivy_platform == 'android') or ('ANDROID_ARGUMENT' in os.environ) or ('ANDROID_ROOT' in os.environ)
except Exception:
    IS_ANDROID = ('ANDROID_ARGUMENT' in os.environ) or ('ANDROID_ROOT' in os.environ)


class TTSEngine:
    """Robust, non-blocking Text-To-Speech engine with multi-language voice support."""

    def __init__(self, language="en"):
        self.system = platform.system()
        self.is_android = IS_ANDROID
        self.speaker = None
        self.volume = 100
        self.rate = 0
        self.language = language or "en"
        self._lock = threading.Lock()

        if self.is_android:
            try:
                from plyer import tts
                self.speaker = tts
                print("✅ Android Plyer TTS initialized successfully")
            except Exception as e:
                print("Android TTS error:", e)
        elif self.system == "Windows":
            try:
                import win32com.client
                import pythoncom
                pythoncom.CoInitialize()
                self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
                self.speaker.Rate = self.rate
                self.speaker.Volume = self.volume
                self.set_language(self.language)
                print(f"Windows SAPI TTS initialized (Async mode, Lang: {self.language})")
            except Exception as e:
                print("SAPI initialization error, falling back to pyttsx3:", e)
                try:
                    import pyttsx3
                    self._pyttsx_engine = pyttsx3.init()
                except Exception as py_e:
                    print("pyttsx3 fallback error:", py_e)
                    self._pyttsx_engine = None

    def _find_voice_token_for_language(self, lang_code):
        """Find the best matching Windows OneCore or SAPI voice token for the requested language."""
        if self.system != "Windows":
            return None

        import winreg

        # Language keywords to look for in token IDs
        patterns = {
            "hi": ["hiin", "hindi", "kalpana", "hemant"],
            "en": ["enin", "heera", "ravi", "enus", "david", "zira", "mark", "english"],
            "es": ["eses", "esmx", "spanish", "helena", "sabina", "pablo"],
            "fr": ["frfr", "frca", "french", "paul", "hortense", "julie"],
            "de": ["dede", "german", "stefan", "hedda", "katja"],
            "ja": ["jajp", "japanese", "ayumi", "haruka", "ichiro"],
            "ta": ["tain", "tamil", "valluvar"],
        }
        keywords = patterns.get(lang_code.lower(), [lang_code.lower()])

        search_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Speech\Voices\Tokens"),
        ]

        for root_key, path in search_paths:
            try:
                k = winreg.OpenKey(root_key, path)
                count = winreg.QueryInfoKey(k)[0]
                for i in range(count):
                    sub = winreg.EnumKey(k, i)
                    sub_lower = sub.lower()
                    if any(kw in sub_lower for kw in keywords):
                        return f"HKEY_LOCAL_MACHINE\\{path}\\{sub}"
            except Exception:
                continue

        return None

    def set_language(self, lang_code):
        """Switch speech voice to match the selected language code."""
        if not lang_code:
            return
        self.language = lang_code.strip().lower()

        if self.system == "Windows" and self.speaker:
            try:
                token_id = self._find_voice_token_for_language(self.language)
                if token_id:
                    import win32com.client
                    import pythoncom
                    pythoncom.CoInitialize()
                    tok = win32com.client.Dispatch("SAPI.SpObjectToken")
                    tok.SetId(token_id)
                    self.speaker.Voice = tok
                    self.voice_name = self.speaker.Voice.GetDescription()
                    print(f"TTS voice set to: {self.voice_name} (Language: {self.language})")
                else:
                    print(f"No specific voice token found for '{self.language}', keeping current voice.")
            except Exception as e:
                print(f"Failed to switch TTS voice for language '{self.language}':", e)

    def speak(self, text, interrupt=False):
        """Speak text asynchronously without blocking the UI main thread."""
        if not text:
            return

        text = str(text).strip()
        if not text:
            return

        try:
            print("TTS Speak:", text)
        except Exception:
            pass

        if self.is_android:
            try:
                from plyer import tts
                threading.Thread(target=tts.speak, args=(text,), daemon=True).start()
            except Exception as e:
                print("Android TTS error:", e)
        elif self.system == "Windows" and self.speaker:
            try:
                import pythoncom
                pythoncom.CoInitialize()
                # SVSFlagsAsync = 1, SVSFPurgeBeforeSpeak = 2
                flags = 1  # asynchronous
                if interrupt:
                    flags = 1 | 2  # async + purge current speech
                self.speaker.Speak(text, flags)
            except Exception as e:
                print("SAPI Async Speak error:", e)
        else:
            # Fallback thread runner
            def _fallback_speak():
                with self._lock:
                    try:
                        import pyttsx3
                        eng = pyttsx3.init()
                        eng.setProperty('rate', 150 + self.rate * 10)
                        eng.setProperty('volume', max(0.0, min(1.0, self.volume / 100.0)))
                        eng.say(text)
                        eng.runAndWait()
                    except Exception as err:
                        print("Fallback speak error:", err)

            threading.Thread(target=_fallback_speak, daemon=True).start()

    def stop(self):
        """Stop any currently playing speech immediately."""
        if self.system == "Windows" and self.speaker:
            try:
                import pythoncom
                pythoncom.CoInitialize()
                # SVSFPurgeBeforeSpeak = 2, SVSFlagsAsync = 1
                self.speaker.Speak("", 1 | 2)
            except Exception as e:
                print("TTS stop error:", e)

    def set_volume(self, volume):
        """Set volume 0-100."""
        self.volume = max(0, min(100, int(volume)))
        if self.system == "Windows" and self.speaker:
            try:
                self.speaker.Volume = self.volume
            except Exception as e:
                print("Volume set error:", e)

    def set_rate(self, rate):
        """Set rate -10 to +10."""
        self.rate = max(-10, min(10, int(rate)))
        if self.system == "Windows" and self.speaker:
            try:
                self.speaker.Rate = self.rate
            except Exception as e:
                print("Rate set error:", e)


if __name__ == "__main__":
    tts = TTSEngine(language="hi")
    tts.speak("नमस्ते! विज़नएड वॉइस इंजन तैयार है।")
    print("TTS test launched.")