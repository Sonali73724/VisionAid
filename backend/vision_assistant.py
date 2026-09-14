import cv2
from ultralytics import YOLO
import win32com.client
import time

# Load YOLO model
model = YOLO("yolo11n.pt")

# Initialize Windows Speech
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Speech speed
speaker.Rate = 0

# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ VisionAid started")
print("Press Q to quit")

# Speech control
last_spoken = ""
last_speech_time = 0

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Failed to read camera")
        break

    # YOLO detection
    results = model(frame, verbose=False)

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    # Store objects
    detected_objects = []

    for box in results[0].boxes:

        confidence = float(box.conf[0])

        if confidence >= 0.30:

            class_id = int(box.cls[0])

            object_name = model.names[class_id]

            if object_name not in detected_objects:
                detected_objects.append(object_name)

    # Sort for stable output
    detected_objects.sort()

    if detected_objects:

        objects_text = ", ".join(detected_objects)

        current_time = time.time()

        # Speak only when object list changes
        if (
            objects_text != last_spoken
            and current_time - last_speech_time >= 2
        ):

            message = f"I can see {objects_text}"

            print("🔊", message)

            speaker.Speak(message)

            last_spoken = objects_text
            last_speech_time = current_time

    # Show camera
    cv2.imshow(
        "VisionAid - AI Assistant",
        annotated_frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()