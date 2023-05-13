# Adapted from: https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/

import speech_recognition as sr
import pyttsx3
from threading import Thread

COMMANDS = {"silence alarm", "snooze alarm"}


# Function to convert text to speech
def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


class VoiceCommands(Thread):
    def __init__(self, event, allow_snoozing=True):
        # execute the base constructor
        Thread.__init__(self)

        self.event = event
        self.allow_snoozing = allow_snoozing

        # Initialize the recognizer
        self.r = sr.Recognizer()

        self.command_is_snooze = False

    def run(self):
        my_text = ""
        while not self.event.is_set():
            try:

                # use the microphone as source for input.
                with sr.Microphone() as source2:

                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    self.r.adjust_for_ambient_noise(source2, duration=0.2)
                    print("say anything...")
                    # listens for the user's input
                    audio2 = self.r.listen(source2)

                    # Using google to recognize audio
                    my_text = self.r.recognize_google(audio2)
                    my_text = my_text.lower()

                    print("Did you say ", my_text)
                    speak_text(my_text)
                    if my_text == "silence alarm":
                        break
                    elif my_text == "snooze alarm":
                        if self.allow_snoozing:
                            self.command_is_snooze = True
                            break
                        else:
                            speak_text("Snoozing not allowed.")

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occurred")
        self.event.set()
        return
