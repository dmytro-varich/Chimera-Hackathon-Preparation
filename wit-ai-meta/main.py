import requests

WIT_AI_TOKEN = "2PKTNYRIBWQP3B5LFAZV2KCFVDPKKG4V"

def process_speech(input_text: str):
    headers = {
        'Authorization': f'Bearer {WIT_AI_TOKEN}',
    }

    response = requests.get(
        f'"https://api.wit.ai/message?v=20241121&q={input_text}', 
        headers=headers
    )

# Example Input
user_input = "Add a task to write a report for tommorow."
response = process_speech(user_input)

# Print the extracted intent and entities
print("Inntent:", response['intents'][0]['name'] if response['intents'] else "No Intent Detected")
print("Entities:", response.get('entities', {}))