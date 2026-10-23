import sys
import speech_recognition as sr
import language_manager as lm

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class VoiceCommand:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1.0
        self.microphone = sr.Microphone()

    def listen(self, primary_lang="hi-IN"):
        print("\n🎤 Listening...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=10
                )

            print("⚙️ Processing voice...")

            text = None
            try:
                text = self.recognizer.recognize_google(audio, language=primary_lang)
            except Exception:
                text = None

            if not text:
                alt = "en-IN" if primary_lang.startswith("hi") else "hi-IN"
                try:
                    text = self.recognizer.recognize_google(audio, language=alt)
                except Exception:
                    text = None

            if not text:
                try:
                    text = self.recognizer.recognize_google(audio, language="en-US")
                except Exception:
                    text = None

            if not text:
                print("❌ Sorry, I could not understand.")
                return None

            text = text.lower().strip()
            print("🗣️ You said:", text)
            return self.get_command(text)

        except sr.WaitTimeoutError:
            print("❌ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Sorry, could not understand speech.")
            return None
        except sr.RequestError as e:
            print("❌ Speech recognition network error:", e)
            return None

    # =====================================================
    # COMMAND DETECTION
    # =====================================================

    def get_command(self, text):
        t = str(text).lower().strip()

        # 1. Stop / Close
        stop_keywords = [
            "stop", "close camera", "exit", "pause", "shut down", "turn off", "quit",
            "band karo", "ruko", "ruk jao", "chhod do", "khatam", "band",
            "बंद करो", "रुक जाओ", "बंद", "रोको"
        ]
        if any(w in t for w in stop_keywords):
            return "stop"

        # 2. Camera Start
        start_keywords = [
            "start camera", "open camera", "turn on camera", "camera on", "start", "open",
            "camera chalu", "chalu karo", "camera on karo", "shuru karo", "camera kholo",
            "कैमरा चालू", "चालू करो", "कैमरा खोलो", "शुरू करो", "कैमरा ऑन"
        ]
        if any(w in t for w in start_keywords):
            return "start"

        # 3. Read Text (OCR)
        read_keywords = [
            "read text", "read this", "read", "reading", "text", "ocr", "sign", "document", "page",
            "padho", "padh do", "kya likha", "likha hua", "padh kar", "padhna", "padhke", "padhiye",
            "पढ़ो", "पढ़", "पढ़िए", "क्या लिखा है", "टेक्स्ट", "किताब पढ़ो", "दस्तावेज़"
        ]
        if any(w in t for w in read_keywords) and not any(w in t for w in ["find", "search", "dhund", "khoj", "ढूंढ", "खोज"]):
            return "text"

        # 4. Face Recognition
        face_keywords = [
            "face", "faces", "emotion", "companion", "who is that", "who is here", "identify person",
            "chehra", "kaun hai", "pehchano", "insan", "dost",
            "चेहरा", "कौन है", "पहचानो", "इंसान", "दोस्त", "साथी"
        ]
        if any(w in t for w in face_keywords) and not any(w in t for w in ["find", "search", "dhund", "khoj", "ढूंढ", "खोज"]):
            return "face"

        # 5. Obstacle Navigation
        obstacle_keywords = [
            "obstacle", "obstacles", "walk", "walking", "navigation", "danger", "hazard", "safety", "warning",
            "khatra", "badha", "rasta", "chalo", "chalna", "alert", "guidance", "rasta batao", "rasta dikhao",
            "बाधा", "खतरा", "रास्ता", "अलर्ट", "नेविगेशन", "सावधानी", "मार्गदर्शन"
        ]
        if any(w in t for w in obstacle_keywords) and not any(w in t for w in ["find", "search", "dhund", "khoj", "ढूंढ", "खोज"]):
            return "obstacle"

        # 6. Object Detection
        object_keywords = [
            "what can you see", "detect objects", "object detection", "what is around", "what is in front",
            "kya dikh raha hai", "kya hai samne", "samne kya hai", "vastu", "dekho", "dekhiye", "batao kya hai", "kuch dikh raha hai",
            "surroundings", "aaspas", "dikh raha",
            "वस्तु", "क्या दिख रहा", "सामने क्या है", "बताओ", "देखो", "आसपास"
        ]
        if any(w in t for w in object_keywords) and not any(w in t for w in ["find", "search", "dhund", "khoj", "ढूंढ", "खोज"]):
            return "object"

        # 7. Find / Search
        find_triggers = [
            "find", "search", "locate", "where is", "look for", "get me", "track",
            "dhundho", "dhundo", "dhund do", "dhund de", "dhund", "khojo", "khoj do", "khoj", "kahan hai", "kidhar hai", "lao", "dikhao",
            "ढूंढो", "ढूंढ दो", "ढूंढ दे", "ढूंढ", "खोजो", "खोज दो", "खोज", "कहाँ है", "किधर है", "कहा है", "कहाँ", "लाओ", "दिखाओ"
        ]
        detected_object = lm.detect_object_in_text(t)
        if detected_object:
            return ("find", detected_object)

        if any(w in t for w in find_triggers):
            cleaned = t
            for trig in find_triggers:
                cleaned = cleaned.replace(trig, " ")
            for sw in ["please", "my", "the", "a", "an", "mera", "meri", "mere", "apna", "apni", "mujhe", "chahiye", "do", "karo", "मेरा", "मेरी", "मेरे", "मुझे", "दो", "कृपया"]:
                cleaned = cleaned.replace(sw, " ")
            cleaned = " ".join(cleaned.split())
            if not cleaned:
                return "ask_target"
            target = lm.resolve_target_label(cleaned, "hi")
            return ("find", target)

        # 8. Fallback: Any recognized object or single word is treated as an item to find
        target = lm.resolve_target_label(t, "hi")
        if target and target not in ["unknown", "unrecognized", "what"]:
            return ("find", target)

        return "unknown"


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":
    voice = VoiceCommand()

    print("=" * 45)
    print("       VISIONAID VOICE COMMAND TEST")
    print("=" * 45)

    while True:
        command = voice.listen()

        if command == "object":
            print("👁️ Command detected: OBJECT DETECTION")
        elif command == "text":
            print("📖 Command detected: READ TEXT")
        elif command == "obstacle":
            print("🚨 Command detected: OBSTACLE ASSISTANCE")
        elif command == "face":
            print("👤 Command detected: FACE COMPANION")
        elif command == "start":
            print("📷 Command detected: START CAMERA")
        elif isinstance(command, tuple) and command[0] == "find":
            print(f"🔍 Command detected: FIND OBJECT -> {command[1]}")
        elif command == "ask_target":
            print("🔍 Command detected: FIND MODE (Asking what to find...)")
        elif command == "stop":
            print("⏹️ Command detected: STOP")
            break
        elif command == "unknown":
            print("💡 Suggestion: Say 'find pen', 'what can you see', or 'read text'")

        print()