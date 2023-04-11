# name voices_utils.py
import requests
from scripts.api_utils import get_api_key
from tkinter import ttk

def set_voice_id(self):
    selected_index = self.voices_listbox.curselection()
    if selected_index:
        selected_voice = self.voices_listbox.get(selected_index)
        self.voice_id = selected_voice.split(' ')[-1]  # Get the voice_id from the selected voice
        self.voice_name = selected_voice.split(',')[0].split(': ')[1]  # Get the voice_name from the selected voice

        self.status_label.config(text=f"Selected Voice ID: {self.voice_id}")

        # Update the voice_name_label text
        self.voice_name_label.config(text=f"Selected Voice: {self.voice_name}")

    else:
        self.status_label.config(text="No voice selected.")
        
def create_get_voices_button(tts_window_instance):
    tts_window_instance.get_API_voices_button = tk.Button(tts_window_instance.tab2_left, text="Get Voices", command=tts_window_instance.get_voices)
    tts_window_instance.get_API_voices_button.pack(side="top", pady=10)
		
def get_voices(self, tk):
    api_key = get_api_key()
    if not api_key:
        self.voices_listbox.delete(0, tk.END)
        self.voices_listbox.insert(tk.END, "No saved API key")
        return

    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {
        'accept': 'application/json',
        'xi-api-key': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        self.voices_listbox.delete(0, tk.END)  # Clear the Listbox before inserting new data
        for voice in data['voices']:
            voice_info = f"Name: {voice['name']}, Voice ID: {voice['voice_id']}"
            self.voices_listbox.insert(tk.END, voice_info)
    else:
        error_message = f"Error getting voices: {response.status_code}"
        self.voices_listbox.delete(0, tk.END)
        self.voices_listbox.insert(tk.END, error_message)
        
def refresh_voices(self):
    api_key = get_api_key()
    if not api_key:
        self.voices_listbox.delete(0, tk.END)
        self.voices_listbox.insert(tk.END, "No saved API key")
        return

    response = get_voices(api_key)
    if response.status_code == 200:
        data = response.json()
        self.voices_listbox.delete(0, tk.END)  # Clear the Listbox before inserting new data
        for voice in data['voices']:
            voice_info = f"Name: {voice['name']}, Voice ID: {voice['voice_id']}"
            self.voices_listbox.insert(tk.END, voice_info)
    else:
        error_message = f"Error getting voices: {response.status_code}"
        self.voices_listbox.delete(0, tk.END)
        self.voices_listbox.insert(tk.END, error_message)