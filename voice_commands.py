import speech_recognition as sr
import pyttsx3

commands = {"silence alarm", "snooze alarm"}

# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to
# speech
def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Loop infinitely for user to
# speak

# while (1):
def get_voice_command(event):
    # Exception handling to handle
    # exceptions at the runtime
    my_text = ""
    while not event.is_set():
        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:

                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("say anything...")
                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                my_text = r.recognize_google(audio2)
                my_text = my_text.lower()

                print("Did you say ", my_text)
                speak_text(my_text)
                if my_text in commands:
                    break

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
    event.set()
    return my_text
