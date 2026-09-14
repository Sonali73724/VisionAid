import cv2
import time
import threading
import win32com.client
import easyocr
import speech_recognition as sr

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window

from ultralytics import YOLO


# =========================================================
# WINDOW
# =========================================================

Window.size = (400, 750)


# =========================================================
# LOAD YOLO
# =========================================================

print("Loading YOLO model...")

model = YOLO("yolo11n.pt")

print("YOLO ready")


# =========================================================
# LOAD EASY OCR
# =========================================================

print("Loading EasyOCR...")

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

print("EasyOCR ready")


# =========================================================
# SAPI TEXT TO SPEECH
# =========================================================

print("Loading SAPI...")

speaker = win32com.client.Dispatch(
    "SAPI.SpVoice"
)

speaker.Rate = 0
speaker.Volume = 100

print("SAPI ready")


# =========================================================
# SPEECH RECOGNITION
# =========================================================

recognizer = sr.Recognizer()

microphone = sr.Microphone()


# =========================================================
# TEXT TO SPEECH
# =========================================================

def speak(text):

    def speech_thread():

        try:

            print("🔊", text)

            speaker.Speak(text)

        except Exception as e:

            print("TTS Error:", e)


    threading.Thread(
        target=speech_thread,
        daemon=True
    ).start()


# =========================================================
# VISIONAID APP
# =========================================================

class VisionAidApp(App):

    def build(self):

        # -------------------------------------------------
        # MAIN LAYOUT
        # -------------------------------------------------

        main_layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=7
        )


        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = Label(
            text="VISIONAID",
            font_size=30,
            bold=True,
            size_hint=(1, 0.07)
        )


        subtitle = Label(
            text="AI Assistant for Blind People",
            font_size=15,
            size_hint=(1, 0.05)
        )


        # -------------------------------------------------
        # CAMERA
        # -------------------------------------------------

        self.camera_image = Image(
            size_hint=(1, 0.43)
        )


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        self.status_label = Label(
            text="Camera stopped",
            font_size=15,
            size_hint=(1, 0.07)
        )


        # -------------------------------------------------
        # OBJECT BUTTON
        # -------------------------------------------------

        object_button = Button(
            text="OBJECT DETECTION",
            font_size=16,
            size_hint=(1, 0.08)
        )

        object_button.bind(
            on_press=self.start_object_detection
        )


        # -------------------------------------------------
        # TEXT BUTTON
        # -------------------------------------------------

        text_button = Button(
            text="READ TEXT",
            font_size=16,
            size_hint=(1, 0.08)
        )

        text_button.bind(
            on_press=self.start_text_reader
        )


        # -------------------------------------------------
        # OBSTACLE BUTTON
        # -------------------------------------------------

        obstacle_button = Button(
            text="OBSTACLE ASSISTANCE",
            font_size=16,
            size_hint=(1, 0.08)
        )

        obstacle_button.bind(
            on_press=self.start_obstacle_assistance
        )


        # -------------------------------------------------
        # VOICE BUTTON
        # -------------------------------------------------

        voice_button = Button(
            text="🎤 VOICE COMMAND",
            font_size=16,
            size_hint=(1, 0.08)
        )

        voice_button.bind(
            on_press=self.start_voice_command
        )


        # -------------------------------------------------
        # STOP BUTTON
        # -------------------------------------------------

        stop_button = Button(
            text="STOP CAMERA",
            font_size=16,
            size_hint=(1, 0.08)
        )

        stop_button.bind(
            on_press=self.stop_camera
        )


        # -------------------------------------------------
        # ADD WIDGETS
        # -------------------------------------------------

        main_layout.add_widget(title)

        main_layout.add_widget(subtitle)

        main_layout.add_widget(
            self.camera_image
        )

        main_layout.add_widget(
            self.status_label
        )

        main_layout.add_widget(
            object_button
        )

        main_layout.add_widget(
            text_button
        )

        main_layout.add_widget(
            obstacle_button
        )

        main_layout.add_widget(
            voice_button
        )

        main_layout.add_widget(
            stop_button
        )


        # -------------------------------------------------
        # VARIABLES
        # -------------------------------------------------

        self.camera = None

        self.mode = None

        self.frame_count = 0

        self.process_every = 3


        # -------------------------------------------------
        # OBJECT SPEECH
        # -------------------------------------------------

        self.last_spoken_objects = ""

        self.last_speech_time = 0

        self.speech_interval = 4


        # -------------------------------------------------
        # OCR
        # -------------------------------------------------

        self.last_ocr_time = 0

        self.ocr_interval = 3

        self.last_read_text = ""


        # -------------------------------------------------
        # OBSTACLE
        # -------------------------------------------------

        self.last_obstacle_message = ""

        self.last_obstacle_time = 0

        self.obstacle_interval = 3


        # -------------------------------------------------
        # VOICE
        # -------------------------------------------------

        self.listening = False


        return main_layout


    # =====================================================
    # OPEN CAMERA
    # =====================================================

    def open_camera(self):

        if self.camera is not None:

            return True


        print("Starting camera...")


        self.camera = cv2.VideoCapture(0)


        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        self.camera.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )


        if not self.camera.isOpened():

            print("Camera could not be opened")

            self.status_label.text = (
                "Camera Error"
            )

            self.camera = None

            return False


        print("Camera opened")

        return True


    # =====================================================
    # START OBJECT DETECTION
    # =====================================================

    def start_object_detection(self, instance=None):

        if not self.open_camera():

            return


        self.mode = "object"

        self.frame_count = 0

        self.last_spoken_objects = ""

        self.last_speech_time = 0


        self.status_label.text = (
            "Object Detection Running"
        )


        speak(
            "Object detection started"
        )


        Clock.unschedule(
            self.update_camera
        )

        Clock.schedule_interval(
            self.update_camera,
            1.0 / 15.0
        )


    # =====================================================
    # START TEXT READER
    # =====================================================

    def start_text_reader(self, instance=None):

        if not self.open_camera():

            return


        self.mode = "text"

        self.frame_count = 0

        self.last_ocr_time = 0

        self.last_read_text = ""


        self.status_label.text = (
            "Text Reader Running"
        )


        speak(
            "Text reader started"
        )


        Clock.unschedule(
            self.update_camera
        )

        Clock.schedule_interval(
            self.update_camera,
            1.0 / 15.0
        )


    # =====================================================
    # START OBSTACLE ASSISTANCE
    # =====================================================

    def start_obstacle_assistance(
        self,
        instance=None
    ):

        if not self.open_camera():

            return


        self.mode = "obstacle"

        self.frame_count = 0

        self.last_obstacle_message = ""

        self.last_obstacle_time = 0


        self.status_label.text = (
            "Obstacle Assistance Running"
        )


        speak(
            "Obstacle assistance started"
        )


        Clock.unschedule(
            self.update_camera
        )

        Clock.schedule_interval(
            self.update_camera,
            1.0 / 15.0
        )


    # =====================================================
    # VOICE COMMAND
    # =====================================================

    def start_voice_command(
        self,
        instance
    ):

        if self.listening:

            return


        self.listening = True


        self.status_label.text = (
            "🎤 Listening..."
        )


        speak(
            "Listening"
        )


        # Run microphone in background
        threading.Thread(
            target=self.listen_for_command,
            daemon=True
        ).start()


    # =====================================================
    # LISTEN FOR COMMAND
    # =====================================================

    def listen_for_command(self):

        try:

            print("\n🎤 Listening...")


            with microphone as source:

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )


                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )


            print(
                "⚙️ Processing voice..."
            )


            text = recognizer.recognize_google(
                audio
            )


            text = text.lower().strip()


            print(
                "🗣️ You said:",
                text
            )


            command = self.get_command(
                text
            )


            # Kivy UI changes must happen
            # on the main thread
            Clock.schedule_once(
                lambda dt: self.execute_command(
                    command
                )
            )


        except sr.WaitTimeoutError:

            print(
                "❌ No speech detected"
            )


            Clock.schedule_once(
                lambda dt: self.voice_error(
                    "No speech detected"
                )
            )


        except sr.UnknownValueError:

            print(
                "❌ Could not understand"
            )


            Clock.schedule_once(
                lambda dt: self.voice_error(
                    "Sorry, I could not understand"
                )
            )


        except sr.RequestError as e:

            print(
                "❌ Speech recognition error:",
                e
            )


            Clock.schedule_once(
                lambda dt: self.voice_error(
                    "Speech recognition error"
                )
            )


    # =====================================================
    # GET COMMAND
    # =====================================================

    def get_command(self, text):

        # Object detection

        if (
            "what can you see" in text
            or "detect objects" in text
            or "detect object" in text
            or "objects" in text
        ):

            return "object"


        # Text reading

        if (
            "read text" in text
            or "read this" in text
            or "read" in text
            or "text" in text
        ):

            return "text"


        # Obstacle assistance

        if (
            "obstacle" in text
            or "obstacles" in text
            or "help me walk" in text
            or "navigation" in text
        ):

            return "obstacle"


        # Stop

        if (
            "stop" in text
            or "stop camera" in text
            or "close camera" in text
        ):

            return "stop"


        return "unknown"


    # =====================================================
    # EXECUTE COMMAND
    # =====================================================

    def execute_command(self, command):

        self.listening = False


        if command == "object":

            print(
                "👁️ Voice command: OBJECT"
            )

            self.start_object_detection()


        elif command == "text":

            print(
                "📖 Voice command: TEXT"
            )

            self.start_text_reader()


        elif command == "obstacle":

            print(
                "🚨 Voice command: OBSTACLE"
            )

            self.start_obstacle_assistance()


        elif command == "stop":

            print(
                "⏹️ Voice command: STOP"
            )

            self.stop_camera()


        else:

            self.status_label.text = (
                "Unknown command"
            )

            speak(
                "Sorry, command not recognized"
            )


    # =====================================================
    # VOICE ERROR
    # =====================================================

    def voice_error(self, message):

        self.listening = False

        self.status_label.text = message

        speak(message)


    # =====================================================
    # CAMERA UPDATE
    # =====================================================

    def update_camera(self, dt):

        if self.camera is None:

            return


        ret, frame = self.camera.read()


        if not ret:

            return


        self.frame_count += 1


        # =================================================
        # OBJECT DETECTION
        # =================================================

        if self.mode == "object":

            if (
                self.frame_count
                % self.process_every
                == 0
            ):

                results = model(
                    frame,
                    verbose=False
                )


                frame = results[0].plot()


                detected_objects = []


                for box in results[0].boxes:

                    confidence = float(
                        box.conf[0]
                    )


                    if confidence >= 0.30:

                        class_id = int(
                            box.cls[0]
                        )


                        object_name = model.names[
                            class_id
                        ]


                        if object_name not in detected_objects:

                            detected_objects.append(
                                object_name
                            )


                detected_objects.sort()


                if detected_objects:

                    objects_text = ", ".join(
                        detected_objects
                    )


                    self.status_label.text = (
                        "Detected: "
                        + objects_text
                    )


                    current_time = time.time()


                    if (
                        objects_text
                        != self.last_spoken_objects
                        and
                        current_time
                        - self.last_speech_time
                        >= self.speech_interval
                    ):

                        speech_text = (
                            self.create_object_sentence(
                                detected_objects
                            )
                        )


                        speak(
                            speech_text
                        )


                        self.last_spoken_objects = (
                            objects_text
                        )


                        self.last_speech_time = (
                            current_time
                        )


        # =================================================
        # TEXT READER
        # =================================================

        elif self.mode == "text":

            current_time = time.time()


            if (
                current_time
                - self.last_ocr_time
                >= self.ocr_interval
            ):

                self.last_ocr_time = (
                    current_time
                )


                ocr_results = reader.readtext(
                    frame
                )


                detected_text = []


                for result in ocr_results:

                    text = result[1]

                    confidence = result[2]


                    if confidence >= 0.40:

                        detected_text.append(
                            text
                        )


                if detected_text:

                    full_text = " ".join(
                        detected_text
                    )


                    self.status_label.text = (
                        "Text: "
                        + full_text[:45]
                    )


                    if (
                        full_text
                        != self.last_read_text
                    ):

                        speak(
                            "I can read: "
                            + full_text
                        )


                        self.last_read_text = (
                            full_text
                        )


        # =================================================
        # OBSTACLE ASSISTANCE
        # =================================================

        elif self.mode == "obstacle":

            if (
                self.frame_count
                % self.process_every
                == 0
            ):

                results = model(
                    frame,
                    verbose=False
                )


                frame = results[0].plot()


                frame_height, frame_width = (
                    frame.shape[:2]
                )


                detected_obstacles = []


                for box in results[0].boxes:

                    confidence = float(
                        box.conf[0]
                    )


                    if confidence < 0.35:

                        continue


                    x1, y1, x2, y2 = (
                        box.xyxy[0].tolist()
                    )


                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)


                    class_id = int(
                        box.cls[0]
                    )


                    object_name = model.names[
                        class_id
                    ]


                    center_x = (
                        x1 + x2
                    ) / 2


                    box_width = (
                        x2 - x1
                    )

                    box_height = (
                        y2 - y1
                    )


                    box_area = (
                        box_width
                        * box_height
                    )


                    frame_area = (
                        frame_width
                        * frame_height
                    )


                    area_ratio = (
                        box_area
                        / frame_area
                    )


                    # Mirror camera correction
                    if center_x < frame_width * 0.33:

                        position = "right"


                    elif center_x > frame_width * 0.66:

                        position = "left"


                    else:

                        position = "center"


                    detected_obstacles.append(
                        (
                            object_name,
                            position,
                            area_ratio
                        )
                    )


                if detected_obstacles:

                    largest_object = max(
                        detected_obstacles,
                        key=lambda x: x[2]
                    )


                    object_name = (
                        largest_object[0]
                    )

                    position = (
                        largest_object[1]
                    )

                    area_ratio = (
                        largest_object[2]
                    )


                    if position == "left":

                        direction_text = (
                            object_name
                            + " on your left."
                        )


                    elif position == "right":

                        direction_text = (
                            object_name
                            + " on your right."
                        )


                    else:

                        direction_text = (
                            object_name
                            + " in front of you."
                        )


                    if area_ratio > 0.25:

                        if position == "left":

                            message = (
                                "Warning! "
                                + object_name
                                + " is very close "
                                + "on your left."
                            )


                        elif position == "right":

                            message = (
                                "Warning! "
                                + object_name
                                + " is very close "
                                + "on your right."
                            )


                        else:

                            message = (
                                "Warning! "
                                + object_name
                                + " is very close "
                                + "in front of you."
                            )

                    else:

                        message = direction_text


                    self.status_label.text = message


                    current_time = time.time()


                    if (
                        message
                        != self.last_obstacle_message
                        and
                        current_time
                        - self.last_obstacle_time
                        >= self.obstacle_interval
                    ):

                        speak(message)


                        self.last_obstacle_message = (
                            message
                        )


                        self.last_obstacle_time = (
                            current_time
                        )


                else:

                    self.status_label.text = (
                        "Path appears clear"
                    )


        # =================================================
        # DISPLAY CAMERA
        # =================================================

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # Mirror camera
        frame = cv2.flip(
            frame,
            1
        )


        texture = Texture.create(
            size=(
                frame.shape[1],
                frame.shape[0]
            ),
            colorfmt="rgb"
        )


        texture.blit_buffer(
            frame.tobytes(),
            colorfmt="rgb",
            bufferfmt="ubyte"
        )


        texture.flip_vertical()


        self.camera_image.texture = texture


    # =====================================================
    # OBJECT SENTENCE
    # =====================================================

    def create_object_sentence(
        self,
        objects
    ):

        if len(objects) == 1:

            return (
                "I can see a "
                + objects[0]
            )


        elif len(objects) == 2:

            return (
                "I can see a "
                + objects[0]
                + " and a "
                + objects[1]
            )


        first_objects = ", ".join(
            [
                "a " + obj
                for obj in objects[:-1]
            ]
        )


        return (
            "I can see "
            + first_objects
            + ", and a "
            + objects[-1]
        )


    # =====================================================
    # STOP CAMERA
    # =====================================================

    def stop_camera(self, instance=None):

        print("Stopping camera...")


        self.mode = None


        Clock.unschedule(
            self.update_camera
        )


        if self.camera is not None:

            self.camera.release()

            self.camera = None


        self.camera_image.texture = None


        self.status_label.text = (
            "Camera stopped"
        )


        self.last_spoken_objects = ""

        self.last_read_text = ""

        self.last_obstacle_message = ""


        speak(
            "Camera stopped"
        )


        print("Camera stopped")


    # =====================================================
    # APP CLOSE
    # =====================================================

    def on_stop(self):

        if self.camera is not None:

            self.camera.release()

            self.camera = None


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    VisionAidApp().run()