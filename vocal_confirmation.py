import pyttsx3


# Function to convert text to
# speech
def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
