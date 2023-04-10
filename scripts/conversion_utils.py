# Name conversion_utils.py
import os
import subprocess
from pydub import AudioSegment
      
def select_file():
    text_file_path = filedialog.askopenfilename(initialdir="Text", title="Select Text File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    file_selected_label.config(text=f"Selected file: {os.path.basename(text_file_path)}")
    
def clear_file():
    text_file_path = None
    file_selected_label.config(text="Cleared File")  
            
def convert_text():
    api_key = self.get_api_key()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    if self.text_file_path:
        try:
            with open(self.text_file_path, "r") as f:
                text = f.read()
        except Exception as e:
            self.status_label.config(text=f"Error reading file: {e}")
            return
    else:
        text = self.text_entry.get().strip()

    if not text:
        self.status_label.config(text="Error: No text input")
        return

    if not self.voice_id:
        self.status_label.config(text="Error: No voice_id selected")
        return

    try:
        # Pass the voice_id to the convert_to_audio function and store the output file path
        output_file_path = convert_to_audio(text=text, voice_id=self.voice_id)
        self.status_label.config(text="Conversion successful")

        # Store the output file path as an attribute
        self.mp3_file_path = output_file_path
    except Exception as e:
        self.status_label.config(text=f"Error converting text to audio: {e}")
        
def perform_mp3_to_wav_conversion():
    input_file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
    if input_file_path:
        output_file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
        if output_file_path:
            sound = AudioSegment.from_mp3(input_file_path)
            sound.export(output_file_path, format="wav")
            self.status_label.config(text="WAV conversion successful!")
        else:
            self.status_label.config(text="WAV conversion failed. Please try again.")
    else:
        self.status_label.config(text="WAV conversion failed. Please try again.")