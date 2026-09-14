# import pyttsx3

# engine = pyttsx3.init()

# engine.setProperty("rate", 150)
# engine.setProperty("volume", 1.0)

# text = "I can see a toothbrush, a bottle, and a person."

# print("Speaking:", text)

# engine.say(text)
# engine.runAndWait()

# print("Speech completed.")

import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

text = "I can see a toothbrush, a bottle, and a person."

print("Speaking:", text)

speaker.Speak(text)

print("Speech completed.")