import pyttsx3 

engine = pyttsx3.init()

# Set the voice to English
# We must to download voices in Microsoft Speech Platform SDK
# https://github.com/BogCiu/TextToSpeech_Configuration_pyttsx3
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'Alex':
        engine.setProperty('voice', voice.id)
        print("Voice changed to Alex")
        break

# Open and read the text file
with open('file.txt', 'r') as file:
    text = file.read()

# Converts text to speech
engine.say(text)
engine.runAndWait()

engine.say("The text has been converted to speech successfully.")
engine.runAndWait()