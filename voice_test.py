import speech_recognition as sr

recognizer = sr.Recognizer()

print("🎤 Voice test started")
print("Speak something...")

with sr.Microphone() as source:

    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

    print("Listening...")

    try:

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5
        )

        print("Processing...")

        text = recognizer.recognize_google(
            audio
        )

        print("✅ You said:", text)

    except sr.WaitTimeoutError:

        print("❌ No speech detected")

    except sr.UnknownValueError:

        print("❌ Could not understand the speech")

    except sr.RequestError as e:

        print("❌ Speech recognition service error:")
        print(e)