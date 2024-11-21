import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    # Adjust for ambient noise and set pause threshold
    recognizer.adjust_for_ambient_noise(source)
    recognizer.pause_threshold = 1.0  # Adjust this value as needed
    
    print("Listening...")
    audio = recognizer.listen(source)

    try: 
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))