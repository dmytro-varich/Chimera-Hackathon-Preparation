import os
from speechmatics.models import *
import speechmatics

PATH_TO_FILE = "C:/Users/admin/T-mobile-Hackathon-2024/SpeechMaticsUsage/ch.wav"
LANGUAGE = "en"

API_KEY = os.environ.get("API_KEY")

sm_client = speechmatics.client.WebsocketClient(API_KEY)

sm_client.add_event_handler(
    event_name = ServerMessageType.AddPartialTranscript, 
    event_handler = print,
)

sm_client.add_event_handler(
    event_name=ServerMessageType.AddTranscript,
    event_handler=print,
)

conf = TranscriptionConfig(
    language=LANGUAGE, enable_partials=True, max_delay=5, enable_entities=True,
)

print("Starting transcription (type Ctrl-C to stop):")
with open(PATH_TO_FILE, "rb") as fd:
    try: 
        sm_client.run_synchronously(fd, conf)
    except KeyboardInterrupt:
        print("\nTranscription stopped.")