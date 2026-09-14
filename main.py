# import cv2
# from ultralytics import YOLO
# import easyocr
# import win32com.client
# import time


# # =========================================================
# # INITIALIZATION
# # =========================================================

# print("====================================")
# print("        VISIONAID AI ASSISTANT")
# print("====================================")

# print("Loading YOLO model...")
# yolo_model = YOLO("yolo11n.pt")
# print("✅ YOLO ready")

# print("Loading OCR model...")
# ocr_reader = easyocr.Reader(['en'])
# print("✅ OCR ready")

# # Windows Speech
# speaker = win32com.client.Dispatch("SAPI.SpVoice")
# speaker.Rate = 0

# # Camera
# camera = cv2.VideoCapture(0)

# if not camera.isOpened():
#     print("❌ Camera could not be opened")
#     exit()

# print("✅ Camera ready")

# print("\nControls:")
# print("O → Object Detection")
# print("R → Read Text")
# print("Q → Quit")


# # =========================================================
# # VARIABLES
# # =========================================================

# mode = "object"

# last_spoken = ""
# last_speech_time = 0

# SPEECH_INTERVAL = 3


# # =========================================================
# # SPEECH FUNCTION
# # =========================================================

# def speak(message):

#     print("🔊", message)

#     speaker.Speak(message)


# # =========================================================
# # OBJECT DETECTION
# # =========================================================

# def detect_objects(frame):

#     global last_spoken
#     global last_speech_time

#     results = yolo_model(frame, verbose=False)

#     detected_objects = []

#     for box in results[0].boxes:

#         confidence = float(box.conf[0])

#         if confidence >= 0.30:

#             class_id = int(box.cls[0])

#             object_name = yolo_model.names[class_id]

#             if object_name not in detected_objects:

#                 detected_objects.append(object_name)

#     detected_objects.sort()

#     annotated_frame = results[0].plot()

#     if detected_objects:

#         objects_text = ", ".join(detected_objects)

#         current_time = time.time()

#         if (
#             objects_text != last_spoken
#             and current_time - last_speech_time >= SPEECH_INTERVAL
#         ):

#             message = f"I can see {objects_text}"

#             speak(message)

#             last_spoken = objects_text
#             last_speech_time = current_time

#     return annotated_frame


# # =========================================================
# # OCR / TEXT READING
# # =========================================================

# def read_text(frame):

#     global last_spoken
#     global last_speech_time

#     results = ocr_reader.readtext(frame)

#     detected_text = []

#     for detection in results:

#         text = detection[1]

#         confidence = detection[2]

#         if confidence >= 0.40:

#             detected_text.append(text)

#     if detected_text:

#         full_text = " ".join(detected_text)

#         current_time = time.time()

#         if (
#             full_text != last_spoken
#             and current_time - last_speech_time >= SPEECH_INTERVAL
#         ):

#             message = f"I can read: {full_text}"

#             speak(message)

#             last_spoken = full_text
#             last_speech_time = current_time

#     return frame


# # =========================================================
# # MAIN LOOP
# # =========================================================

# while True:

#     ret, frame = camera.read()

#     if not ret:

#         print("❌ Failed to read camera")

#         break


#     # -----------------------------
#     # Object Detection Mode
#     # -----------------------------

#     if mode == "object":

#         display_frame = detect_objects(frame)


#     # -----------------------------
#     # OCR Mode
#     # -----------------------------

#     elif mode == "ocr":

#         display_frame = read_text(frame)


#     # -----------------------------
#     # Display
#     # -----------------------------

#     cv2.imshow(
#         "VisionAid",
#         display_frame
#     )


#     # -----------------------------
#     # Keyboard Controls
#     # -----------------------------

#     key = cv2.waitKey(1) & 0xFF


#     if key == ord("o"):

#         mode = "object"

#         last_spoken = ""

#         print("\n👁️ Object Detection Mode")

#         speak("Object detection mode")


#     elif key == ord("r"):

#         mode = "ocr"

#         last_spoken = ""

#         print("\n📖 Text Reading Mode")

#         speak("Text reading mode")


#     elif key == ord("q"):

#         print("\n👋 VisionAid stopped")

#         break


# # =========================================================
# # CLEANUP
# # =========================================================

# camera.release()

# cv2.destroyAllWindows()

import cv2
from ultralytics import YOLO
import easyocr
import win32com.client
import time


# =========================================================
# VISIONAID - INITIALIZATION
# =========================================================

print("====================================")
print("        VISIONAID AI ASSISTANT")
print("====================================")


# =========================================================
# LOAD YOLO MODEL
# =========================================================

print("Loading YOLO model...")

yolo_model = YOLO("yolo11n.pt")

print("✅ YOLO ready")


# =========================================================
# LOAD OCR MODEL
# =========================================================

print("Loading OCR model...")

ocr_reader = easyocr.Reader(['en'])

print("✅ OCR ready")


# =========================================================
# WINDOWS TEXT-TO-SPEECH
# =========================================================

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Speech speed
speaker.Rate = 0

# Volume
speaker.Volume = 100


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(0)

# Camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Reduce camera buffer
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)


if not camera.isOpened():

    print("❌ Camera could not be opened")

    exit()


print("✅ Camera ready")


# =========================================================
# CONTROLS
# =========================================================

print()
print("====================================")
print("          CONTROLS")
print("====================================")
print()
print("O → Object Detection")
print("R → Read Text")
print("Q → Quit")
print()


# =========================================================
# VARIABLES
# =========================================================

# Default mode
mode = "object"

# Last thing spoken
last_spoken = ""

# Last speech time
last_speech_time = 0


# Minimum time between speech
SPEECH_INTERVAL = 3


# Frame counter
frame_count = 0


# YOLO will run every 3rd frame
YOLO_SKIP = 3


# OCR will run every 10th frame
OCR_SKIP = 10


# =========================================================
# SPEECH FUNCTION
# =========================================================

def speak(message):

    print("🔊", message)

    speaker.Speak(message)


# =========================================================
# OBJECT DETECTION FUNCTION
# =========================================================

def detect_objects(frame):

    global last_spoken
    global last_speech_time

    # Run YOLO
    results = yolo_model(frame, verbose=False)

    # List of detected objects
    detected_objects = []

    # Process every detected box
    for box in results[0].boxes:

        # Confidence score
        confidence = float(box.conf[0])

        # Minimum confidence
        if confidence >= 0.30:

            # Class ID
            class_id = int(box.cls[0])

            # Object name
            object_name = yolo_model.names[class_id]

            # Avoid duplicate objects
            if object_name not in detected_objects:

                detected_objects.append(object_name)


    # Sort objects for stable speech
    detected_objects.sort()


    # Draw bounding boxes
    annotated_frame = results[0].plot()


    # If objects detected
    if detected_objects:

        objects_text = ", ".join(detected_objects)

        current_time = time.time()


        # Speak only when detection changes
        if (
            objects_text != last_spoken
            and current_time - last_speech_time >= SPEECH_INTERVAL
        ):

            message = f"I can see {objects_text}"

            speak(message)

            last_spoken = objects_text

            last_speech_time = current_time


    return annotated_frame


# =========================================================
# OCR / TEXT READING FUNCTION
# =========================================================

def read_text(frame):

    global last_spoken
    global last_speech_time

    # Run EasyOCR
    results = ocr_reader.readtext(frame)

    # Store detected text
    detected_text = []


    # Process OCR results
    for detection in results:

        text = detection[1]

        confidence = detection[2]


        # Confidence threshold
        if confidence >= 0.40:

            detected_text.append(text)


    # If text detected
    if detected_text:

        # Combine all detected text
        full_text = " ".join(detected_text)

        current_time = time.time()


        # Avoid repeating same text
        if (
            full_text != last_spoken
            and current_time - last_speech_time >= SPEECH_INTERVAL
        ):

            message = f"I can read: {full_text}"

            speak(message)

            last_spoken = full_text

            last_speech_time = current_time


    return frame


# =========================================================
# MAIN CAMERA LOOP
# =========================================================

while True:

    # Read camera frame
    ret, frame = camera.read()


    # Check camera
    if not ret:

        print("❌ Failed to read camera")

        break


    # Increase frame counter
    frame_count += 1


    # =====================================================
    # OBJECT DETECTION MODE
    # =====================================================

    if mode == "object":

        # Run YOLO only every 3rd frame
        if frame_count % YOLO_SKIP == 0:

            display_frame = detect_objects(frame)

        else:

            display_frame = frame


    # =====================================================
    # OCR MODE
    # =====================================================

    elif mode == "ocr":

        # Run OCR only every 10th frame
        if frame_count % OCR_SKIP == 0:

            display_frame = read_text(frame)

        else:

            display_frame = frame


    # =====================================================
    # DISPLAY CAMERA
    # =====================================================

    cv2.imshow(
        "VisionAid - AI Assistant",
        display_frame
    )


    # =====================================================
    # KEYBOARD INPUT
    # =====================================================

    key = cv2.waitKey(1) & 0xFF


    # -----------------------------------------------------
    # OBJECT DETECTION MODE
    # -----------------------------------------------------

    if key == ord("o"):

        mode = "object"

        # Reset speech
        last_spoken = ""

        last_speech_time = 0

        print()
        print("👁️ OBJECT DETECTION MODE")

        speak("Object detection mode")


    # -----------------------------------------------------
    # TEXT READING MODE
    # -----------------------------------------------------

    elif key == ord("r"):

        mode = "ocr"

        # Reset speech
        last_spoken = ""

        last_speech_time = 0

        print()
        print("📖 TEXT READING MODE")

        speak("Text reading mode")


    # -----------------------------------------------------
    # QUIT
    # -----------------------------------------------------

    elif key == ord("q"):

        print()
        print("👋 VisionAid stopped")

        break


# =========================================================
# CLEANUP
# =========================================================

camera.release()

cv2.destroyAllWindows()

print()
print("✅ Camera closed")
print("✅ VisionAid closed")