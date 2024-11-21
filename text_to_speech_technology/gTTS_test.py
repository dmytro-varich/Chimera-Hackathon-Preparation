from gtts import gTTS
import os

import pygame

# Text to be converted to speech
mytext = "Hello, I am a text to speech conversion system."

language = 'en'

# Passing the text and language to the engine, here we have marked slow=False. Which tells the module that the converted audio should have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named welcome
myobj.save("welcome.mp3")

# Playing the converted file
os.system("start welcome.mp3")

# Initialize the pygame mixer
# pygame.mixer.init()

# Load the mp3 file
path = '/c/Users/admin/T-mobile-Hackathon-2024/text_to_speech_technology/welcome.mp3'
# pygame.mixer.music.load(path)

# Play the loaded mp3 file
# pygame.mixer.music.play()
