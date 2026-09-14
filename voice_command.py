import speech_recognition as sr


class VoiceCommand:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        # Microphone select karo
        self.microphone = sr.Microphone()


    def listen(self):

        print("\n🎤 Listening...")

        try:

            with self.microphone as source:

                # Background noise adjust
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )


            print("⚙️ Processing voice...")


            # Speech → Text
            text = self.recognizer.recognize_google(
                audio
            )


            text = text.lower().strip()


            print("🗣️ You said:", text)


            return self.get_command(text)


        except sr.WaitTimeoutError:

            print("❌ No speech detected")

            return None


        except sr.UnknownValueError:

            print(
                "❌ Sorry, I could not understand."
            )

            return None


        except sr.RequestError as e:

            print(
                "❌ Speech recognition error:",
                e
            )

            return None


    # =====================================================
    # COMMAND DETECTION
    # =====================================================

    def get_command(self, text):

        # -----------------------------------------------
        # OBJECT DETECTION
        # -----------------------------------------------

        if (
            "what can you see" in text
            or "detect objects" in text
            or "detect object" in text
            or "objects" in text
        ):

            return "object"


        # -----------------------------------------------
        # READ TEXT
        # -----------------------------------------------

        elif (
            "read text" in text
            or "read this" in text
            or "read" in text
            or "text" in text
        ):

            return "text"


        # -----------------------------------------------
        # OBSTACLE
        # -----------------------------------------------

        elif (
            "obstacle" in text
            or "obstacles" in text
            or "help me walk" in text
            or "navigation" in text
        ):

            return "obstacle"


        # -----------------------------------------------
        # STOP
        # -----------------------------------------------

        elif (
            "stop" in text
            or "stop camera" in text
            or "close camera" in text
            or "exit" in text
        ):

            return "stop"


        # -----------------------------------------------
        # UNKNOWN
        # -----------------------------------------------

        else:

            print(
                "❓ Unknown command:",
                text
            )

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

            print(
                "👁️ Command detected: OBJECT DETECTION"
            )


        elif command == "text":

            print(
                "📖 Command detected: READ TEXT"
            )


        elif command == "obstacle":

            print(
                "🚨 Command detected: OBSTACLE ASSISTANCE"
            )


        elif command == "stop":

            print(
                "⏹️ Command detected: STOP"
            )

            break


        elif command == "unknown":

            print(
                "❓ Command not recognized"
            )


        print()