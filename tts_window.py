#Name tts_window.py

import os
import sys
import requests
import configparser
import tkinter as tk
from tkinter import filedialog, ttk
from TTSCurlConversion import convert_to_audio

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
        ## Convert Button
        self.convert_button = tk.Button(self.tab1, text="Convert to Audio", command=self.convert_text)
        self.convert_button.pack(side="top", pady=10)
        ## Status Aarea
        self.status_label = tk.Label(self.tab1, text="")
        self.status_label.pack(side="top", pady=10)
        
        self.text_file_path = None  # Initialize text_file_path to None

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
            self.status_label.config(text=f"Selected Voice ID: {self.voice_id}")
        else:
            self.status_label.config(text="No voice selected.")
            
    ## Should move this to its own PY
    def get_API_voices(self):
        url = 'https://api.elevenlabs.io/v1/voices'
        headers = {
            'accept': 'application/json',
            'xi-api-key': self.get_api_key()
        }

        response = requests.get(url, headers=headers)  # Add the headers parameter

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
            # Pass the voice_id to the convert_to_audio function
            convert_to_audio(text=text, voice_id=self.voice_id)
            self.status_label.config(text="Conversion successful")
        except Exception as e:
            self.status_label.config(text=f"Error converting text to audio: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSWindow(master=root)
    app.mainloop()
