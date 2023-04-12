#name audio_utils.py
import os
import sys
import json
import requests
from pydub import AudioSegment  
from scripts.api_utils import get_api_key

def convert_to_audio(text=None, voice_id=None, api_key=None, speed=0.25, pitch=0.25, out_folder=None, csv_out_path=None):
    api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": get_api_key(),
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
    audio_folder = out_folder
    
    # Save the MP3 content to a temporary file
    with open("temp.mp3", "wb") as f:
        f.write(audio_content)

    # Perform MP3 to WAV conversion
    sound = AudioSegment.from_mp3("temp.mp3")

    # Set the output file name using csv_out_path
    if csv_out_path:
        output_file_name = f"{csv_out_path}.wav"
    else:
        output_file_name = output_file_name

   # Combine the output folder path with the output file name
    if out_folder:
        output_file_path = os.path.join(out_folder, output_file_name)
    else:
        output_file_path = output_file_name

    sound.export(output_file_path, format="wav")

    # Remove the temporary MP3 file
    os.remove("temp.mp3")

    return output_file_path