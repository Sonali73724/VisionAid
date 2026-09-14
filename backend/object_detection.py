import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ VisionAid Object Detection Started")
print("Press Q to quit")

while True:
    ret, frame = camera.read()

    if not ret:
        print("❌ Failed to read camera frame")
        break

    # Run YOLO detection
    results = model(frame, verbose=False)

    # Draw detection results
    annotated_frame = results[0].plot()

    # Display result
    cv2.imshow("VisionAid - Object Detection", annotated_frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()