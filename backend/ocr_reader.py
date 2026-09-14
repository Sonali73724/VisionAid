import cv2
import easyocr
import win32com.client
import time

# -----------------------------
# Open Camera FIRST
# -----------------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ Camera opened successfully")

# -----------------------------
# Initialize OCR
# -----------------------------
print("⏳ Loading EasyOCR model...")

reader = easyocr.Reader(['en'])

print("✅ EasyOCR ready")

# -----------------------------
# Initialize Windows Speech
# -----------------------------
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 0

print("✅ VisionAid OCR started")
print("Press Q to quit")

last_text = ""
last_speech_time = 0

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Failed to read camera")
        break

    # Run OCR
    results = reader.readtext(frame)

    detected_text = []

    for detection in results:

        text = detection[1]
        confidence = detection[2]

        if confidence >= 0.40:
            detected_text.append(text)

    if detected_text:

        full_text = " ".join(detected_text)

        current_time = time.time()

        if (
            full_text != last_text
            and current_time - last_speech_time >= 2
        ):

            print("📖 Detected Text:", full_text)

            message = f"I can read: {full_text}"

            print("🔊", message)

            speaker.Speak(message)

            last_text = full_text
            last_speech_time = current_time

    # Show camera
    cv2.imshow("VisionAid - Text Reader", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()