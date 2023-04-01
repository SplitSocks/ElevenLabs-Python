#Name tts_window.py
# FFMPEG = https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
import sys
print(sys.executable)

import os
import sys
import requests
import configparser
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk
from GetAudio import convert_to_audio
from pydub import AudioSegment

class TTSWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Text-to-Speech Converter")
        self.pack()  # Add missing pack method for the frame
        
        # Create a custom style for the Notebook tabs
        custom_notebook_style = ttk.Style()
        custom_notebook_style.configure("CustomNotebook.TNotebook", padding=[5, 5, 5, 5])
        custom_notebook_style.configure("CustomNotebook.TNotebook.Tab", font=('Helvetica', 12, 'bold'), padding=[10, 5, 10, 5])
        
        # Create a Notebook widget with the custom style
        self.notebook = ttk.Notebook(self.master, style="CustomNotebook.TNotebook")
        self.notebook.pack(fill='both', expand=True)

        # Create five tabs
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        self.tab4 = tk.Frame(self.notebook)
        self.tab5 = tk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab1, text='Main')
        self.notebook.add(self.tab2, text='API and VoiceID')
        self.notebook.add(self.tab3, text='Tab 3')
        self.notebook.add(self.tab4, text='Tab 4')
        self.notebook.add(self.tab5, text='Tab 5')

        # Create widgets for the first tab
        # Initialized attributes
        self.voice_name = None        
        self.text_file_path = None
        
        ## Select Text File
        self.select_button = tk.Button(self.tab1, text="Select Text File", command=self.select_file)
        self.select_button.pack(side="top", pady=10)        
        ## File Selected Label
        self.file_selected_label = tk.Label(self.tab1, text="")
        self.file_selected_label.pack(side="top", pady=5)   
        ## Clear Text File Button
        self.clear_button = tk.Button(self.tab1, text="Clear Text File", command=self.clear_file)
        self.clear_button.pack(side="top", pady=10)        
        ## Enter Text Instead
        self.text_entry = tk.Entry(self.tab1, width=50)
        self.text_entry.pack(side="top", pady=10)        
         ## Status Area
        self.status_label = tk.Label(self.tab1, text="")
        self.status_label.pack(side="top", pady=10)
        ## Add this block to create the voice_name_label
        self.voice_name_label = tk.Label(self.tab1, text="No voice selected")
        self.voice_name_label.pack(side="top", pady=10)
        ## Audio Request Button
        self.convert_button = tk.Button(self.tab1, text="Convert to Audio", command=self.convert_text)
        self.convert_button.pack(side="top", pady=10)
        ## Convert to XMW
        self.convert_mp3_to_xwm_button = tk.Button(self.tab1, text="Convert MP3 to XWM", command=self.convert_mp3_to_xwm)
        self.convert_mp3_to_xwm_button.pack(pady=5)
        ## Status Aarea
        self.status_label = tk.Label(self.tab1, text="")
        self.status_label.pack(side="top", pady=10)
        

        # Create widgets for the second tab
        ## Create widget for API key
        self.api_key_label = tk.Label(self.tab2, text="API Key:")
        self.api_key_label.pack(side="top", pady=10)
        
        saved_api_key = self.get_api_key()  # Load the saved API key
        self.api_key_entry = tk.Entry(self.tab2, width=50)
        self.api_key_entry.insert(0, saved_api_key)  # Set the saved API key as the default value
        self.api_key_entry.pack(side="top", pady=10)
        
        self.save_api_key_button = tk.Button(self.tab2, text="Save API Key", command=self.save_api_key_to_file)
        self.save_api_key_button.pack(side="top", pady=10)
        
        ## Voices Button and List
        
        self.get_API_voices_button = tk.Button(self.tab2, text="Get Voices", command=self.get_API_voices)
        self.get_API_voices_button.pack(side="top", pady=10)
        
        ## Add these lines to create a Listbox for voices and a Scrollbar
        self.voices_listbox = tk.Listbox(self.tab2, width=50, height=10)
        self.voices_listbox.pack(side="left", pady=10)
        self.voices_scrollbar = tk.Scrollbar(self.tab2)
        self.voices_scrollbar.pack(side="left", fill="y")

        ## Configure the Listbox to use the Scrollbar
        self.voices_listbox.config(yscrollcommand=self.voices_scrollbar.set)
        self.voices_scrollbar.config(command=self.voices_listbox.yview)

        ## Add a button to set the selected voice_id
        self.set_voice_id_button = tk.Button(self.tab2, text="Set Voice ID", command=self.set_voice_id)
        self.set_voice_id_button.pack(side="top", pady=10)

        self.voice_id = None  # Initialize the voice_id variable
        
    # API Configuration
    def get_api_key(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('DEFAULT', 'api_key')
        
    def save_api_key(self, api_key):
        config = configparser.ConfigParser()  # Instantiate the config object before using it
        config.read('config.ini')  # Read the config file before modifying it
        config.set('DEFAULT', 'api_key', api_key)
        with open('config.ini', 'w') as f:
            config.write(f)
        
    def save_api_key_to_file(self):
        api_key = self.api_key_entry.get()
        if api_key:
            self.save_api_key(api_key)
            self.status_label.config(text="API key saved successfully.")
        else:
            self.status_label.config(text="Error: No API key input.")
        
    def select_file(self):
        self.text_file_path = filedialog.askopenfilename(initialdir="Text", title="Select Text File",
                                                    filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        self.file_selected_label.config(text=f"Selected file: {os.path.basename(self.text_file_path)}")
        
    def clear_file(self):
        self.text_file_path = No
        ne  # Update this line to clear text_file_path
        self.file_selected_label.config(text="Cleared selected file")
    
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
            
    ## Should move this to its own PY
    def get_API_voices(self):
        api_key = self.get_api_key()
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
                
    def convert_text(self):
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
            
    # Conversion Process form MP3 to XWM
    def convert_mp3_to_wav(self, mp3_path, wav_path):  # Added 'self' as the first parameter
        try:
            command = f"ffmpeg -i {mp3_path} {wav_path}"
            subprocess.run(command, check=True, shell=True)
            print(f"Successfully converted {mp3_path} to {wav_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {mp3_path} to {wav_path}: {e}")
            
    def convert_wav_to_xwm(self, wav_path, xwm_path, xwmaencode_path):
        try:
            command = f'"{xwmaencode_path}" -i "{wav_path}" -o "{xwm_path}"'
            result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Output: {result.stdout.decode('utf-8')}")
            print(f"Error output: {result.stderr.decode('utf-8')}")
            print(f"Successfully converted {wav_path} to {xwm_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {wav_path} to {xwm_path}: {e}")
            print(f"Error output: {e.stderr.decode('utf-8')}")

            
    def perform_mp3_to_xwm_conversion(self, mp3_path, xwm_file_name, xwmaencode_path):
        # Convert MP3 to WAV
        wav_file_path = os.path.splitext(mp3_path)[0] + ".wav"
        self.convert_mp3_to_wav(mp3_path, wav_file_path)

        # Convert WAV to XWM
        xwm_file_path = os.path.splitext(mp3_path)[0] + ".xwm"
        self.convert_wav_to_xwm(wav_file_path, xwm_file_path, xwmaencode_path)
    
    def convert_mp3_to_xwm(self):
        if not self.mp3_file_path:
            self.status_label.config(text="Error: No MP3 file to convert")
            return

        xwm_file_name = os.path.splitext(os.path.basename(self.mp3_file_path))[0] + ".xwm"
        xwmaencode_path = "C:\\Program Files (x86)\\Microsoft DirectX SDK (June 2010)\\Utilities\\bin\\x86\\xWMAEncode.exe"

        try:
            # Update the method call inside the convert_mp3_to_xwm method
            self.perform_mp3_to_xwm_conversion(self.mp3_file_path, xwm_file_name, xwmaencode_path)
            self.status_label.config(text="Successfully converted MP3 to XWM")
        except Exception as e:
            self.status_label.config(text=f"Error converting MP3 to XWM: {e}")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = TTSWindow(master=root)
    app.mainloop()
