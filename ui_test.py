from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


Window.size = (400, 750)


class VisionAidUI(App):

    def build(self):

        main = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=15
        )

        title = Label(
            text="VISIONAID",
            font_size=32,
            bold=True,
            size_hint=(1, 0.12)
        )

        subtitle = Label(
            text="AI Assistant for Visually Impaired",
            font_size=16,
            size_hint=(1, 0.08)
        )

        see_button = Button(
            text="👁  SEE OBJECTS",
            font_size=20,
            size_hint=(1, 0.15)
        )

        text_button = Button(
            text="📖  READ TEXT",
            font_size=20,
            size_hint=(1, 0.15)
        )

        obstacle_button = Button(
            text="🚨  OBSTACLE ASSISTANCE",
            font_size=20,
            size_hint=(1, 0.15)
        )

        voice_button = Button(
            text="🎤  VOICE COMMAND",
            font_size=20,
            size_hint=(1, 0.15)
        )

        status = Label(
            text="Ready to assist you",
            font_size=15,
            size_hint=(1, 0.10)
        )

        main.add_widget(title)
        main.add_widget(subtitle)
        main.add_widget(see_button)
        main.add_widget(text_button)
        main.add_widget(obstacle_button)
        main.add_widget(voice_button)
        main.add_widget(status)

        return main


if __name__ == "__main__":
    VisionAidUI().run()