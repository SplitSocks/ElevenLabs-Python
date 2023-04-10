#name audio_utils.py
import os
import sys
import json
import requests

def convert_to_audio(text=None, voice_id=None, api_key=None, speed=1.0, pitch=1.0, output_folder="Audio"):
    api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    data = {
        "text": text,
        "voice_id": voice_id,
        "speed": speed,
        "pitch": pitch
    }

    # send the API call
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    # check if the API call was successful
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None

    # get the content of the audio file and save it to disk
    audio_content = response.content
    audio_folder = "Audio"
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    audio_file = os.path.join(audio_folder, "audio_file.mp3")

    # check if the audio file already exists and append a number to the filename if it does
    i = 1
    while os.path.exists(audio_file):
        audio_file = os.path.join(audio_folder, f"audio_file({i}).mp3")
        i += 1

    # write the audio content to the file
    with open(audio_file, "wb") as f:
        f.write(audio_content)

    return audio_file
    return output_file_path

if __name__ == '__main__':
    voice_id = input("Enter voice id: ")
    if not voice_id:
        print("No voice ID")
        sys.exit()

    text = "Hello, how are you doing?"
    audio_file = convert_to_audio(text=text, voice_id=voice_id)

    print(f"Audio file saved as: {audio_file}")
