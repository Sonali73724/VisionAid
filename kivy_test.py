from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


# Window size for desktop testing
Window.size = (400, 700)


class VisionAidApp(App):

    def build(self):

        # Main layout
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        # Title
        title = Label(
            text="VISIONAID",
            font_size=32,
            bold=True,
            size_hint=(1, 0.15)
        )

        # Subtitle
        subtitle = Label(
            text="AI Assistant for Blind People",
            font_size=18,
            size_hint=(1, 0.10)
        )

        # Object Detection button
        object_button = Button(
            text="👁️  OBJECT DETECTION",
            font_size=20,
            size_hint=(1, 0.18)
        )

        # Read Text button
        text_button = Button(
            text="📖  READ TEXT",
            font_size=20,
            size_hint=(1, 0.18)
        )

        # Stop button
        stop_button = Button(
            text="🔊  STOP SPEECH",
            font_size=20,
            size_hint=(1, 0.18)
        )

        # Status
        status = Label(
            text="Ready",
            font_size=18,
            size_hint=(1, 0.15)
        )

        # Button actions
        def object_detection(instance):

            status.text = "Object Detection Mode"
            print("Object Detection clicked")


        def read_text(instance):

            status.text = "Text Reading Mode"
            print("Read Text clicked")


        def stop_speech(instance):

            status.text = "Speech stopped"
            print("Stop Speech clicked")


        object_button.bind(
            on_press=object_detection
        )

        text_button.bind(
            on_press=read_text
        )

        stop_button.bind(
            on_press=stop_speech
        )


        # Add widgets
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(object_button)
        layout.add_widget(text_button)
        layout.add_widget(stop_button)
        layout.add_widget(status)

        return layout


if __name__ == "__main__":
    VisionAidApp().run()