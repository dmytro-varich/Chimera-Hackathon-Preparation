from vosk import Model, KaldiRecognizer
import wave

model_path = 'vosk-model-small-en-us-0.15/model' # The best practice is to download the large model on hd and use it
model = Model(model_path)

# Audio file path (Open)
af = wave.open('ch.wav', 'rb')
recognizer = KaldiRecognizer(model, af.getframerate())


while True:
    # Read 4000 frames of audio data
    data = af.readframes(4000)
    if len(data) == 0:
        break

    # Recognize the speech in the chunk
    recognizer.AcceptWaveform(data)

# Get the final result of the speech recognition
result = recognizer.FinalResult()
print(result)

