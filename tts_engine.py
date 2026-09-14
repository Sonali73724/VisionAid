import platform
import threading
import sys

# Ensure UTF-8 output on Windows consoles without charmap crash
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

class TTSEngine:
    """Robust, non-blocking Text-To-Speech engine for VisionAid."""

    def __init__(self):
        self.system = platform.system()
        self.speaker = None
        self.volume = 100
        self.rate = 0
        self._lock = threading.Lock()

        if self.system == "Windows":
            try:
                import win32com.client
                import pythoncom
                pythoncom.CoInitialize()
                self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
                self.speaker.Rate = self.rate
                self.speaker.Volume = self.volume
                print("Windows SAPI TTS initialized (Async mode)")
            except Exception as e:
                print("SAPI initialization error, falling back to pyttsx3:", e)
                try:
                    import pyttsx3
                    self._pyttsx_engine = pyttsx3.init()
                except Exception as py_e:
                    print("pyttsx3 fallback error:", py_e)
                    self._pyttsx_engine = None
        elif self.system == "Android":
            try:
                from plyer import tts
                self.speaker = tts
                print("Android TTS initialized")
            except Exception as e:
                print("Android TTS error:", e)

    def speak(self, text, interrupt=False):
        """Speak text asynchronously without blocking the UI main thread."""
        if not text:
            return

        text = str(text).strip()
        if not text:
            return

        print("TTS Speak:", text)

        if self.system == "Windows" and self.speaker:
            try:
                # SVSFlagsAsync = 1, SVSFPurgeBeforeSpeak = 2
                flags = 1  # asynchronous
                if interrupt:
                    flags = 1 | 2  # async + purge current speech
                self.speaker.Speak(text, flags)
            except Exception as e:
                print("SAPI Async Speak error:", e)
        elif self.system == "Android":
            try:
                from plyer import tts
                threading.Thread(target=tts.speak, args=(text,), daemon=True).start()
            except Exception as e:
                print("Android TTS error:", e)
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
    tts = TTSEngine()
    tts.speak("VisionAid asynchronous audio engine is working.")
    print("TTS test launched without blocking.")