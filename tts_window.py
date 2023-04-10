# Name tts_window.py
# Curated by SplitSocks
# Need pip install pydub
# Need pip install requests

import os
import sys
import requests
import tkinter as tk
import scripts.api_utils
from tkinter import messagebox
from tkinter import filedialog, ttk
#from pydub import AudioSegment
from scripts.required_utils import check_ffmpeg_avconv
from scripts.audio_utils import convert_to_audio
from scripts.api_utils import set_api_key, get_api_key
from scripts.conversion_utils import perform_mp3_to_wav_conversion, select_file, clear_file, convert_text
from scripts.voices_utils import set_voice_id, get_API_voices
from scripts.csv_utils import convert_csv, select_csv_file
       
# Suppress CMD errors
import logging
logging.getLogger("pydub.converter").setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

class TTSWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Text-to-Speech Converter")        
        self.pack()  # Add missing pack method for the frame
        api_key = get_api_key()
        
        # Check for FFMPEG
        #if not check_ffmpeg_avconv():
        #    messagebox.showwarning("FFmpeg or Avconv not found", "Please install FFmpeg or Avconv and add it to #your system's PATH. This program will now close")
        #    self.master.destroy()
        #    sys.exit("FFmpeg not found. Please install FFmpeg and try again.")
        
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
        self.notebook.add(self.tab2, text='Voices')
        self.notebook.add(self.tab3, text='CSV Conversion')
        self.notebook.add(self.tab4, text='Tab 4')
        self.notebook.add(self.tab5, text='API Setup')

        # Create widgets for the first tab
        # Initialized attributes
        self.voice_name = None        
        self.text_file_path = None
        
        ## Select Text File
        self.select_button = tk.Button(self.tab1, text="Select Text File", command=select_file)
        self.select_button.pack(side="top", pady=10)        
        ## File Selected Label
        self.file_selected_label = tk.Label(self.tab1, text="")
        self.file_selected_label.pack(side="top", pady=5)   
        ## Clear Text File Button
        self.clear_button = tk.Button(self.tab1, text="Clear Text File", command=clear_file)
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
        self.convert_button = tk.Button(self.tab1, text="Convert to Audio", command=convert_text)
        self.convert_button.pack(side="top", pady=10)
        ## Convert to WAV
        self.perform_mp3_to_wav_conversion_button = tk.Button(self.tab1, text="Convert MP3 to WAV", command=perform_mp3_to_wav_conversion)
        self.perform_mp3_to_wav_conversion_button.pack(pady=5)
        ## Status Aarea
        self.status_label = tk.Label(self.tab1, text="")
        self.status_label.pack(side="top", pady=10)
        

        # Create widgets for the second tab
        ##Columns
        # create two columns in the second tab
        self.tab2_left = tk.Frame(self.tab2)
        self.tab2_left.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.tab2_right = tk.Frame(self.tab2)
        self.tab2_right.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Left Column
        ## Get API Button
        self.get_API_voices_button = tk.Button(self.tab2_left, text="Get Voices", command=get_API_voices)
        self.get_API_voices_button.pack(side="top", pady=10)
        ## Add a button to set the selected voice_id
        self.set_voice_id_button = tk.Button(self.tab2_left, text="Set Voice ID", command=set_voice_id)
        self.set_voice_id_button.pack(side="top", pady=10)
        
        ## Add these lines to create a Listbox for voices and a Scrollbar
        self.voices_listbox = tk.Listbox(self.tab2_right, width=50, height=10)
        self.voices_listbox.pack(side="left", pady=10)
        self.voices_scrollbar = tk.Scrollbar(self.tab2_right)
        self.voices_scrollbar.pack(side="left", fill="y")

        ## Configure the Listbox to use the Scrollbar
        self.voices_listbox.config(yscrollcommand=self.voices_scrollbar.set)
        self.voices_scrollbar.config(command=self.voices_listbox.yview)



        self.voice_id = None  # Initialize the voice_id variable
        
        # 3rd Tab
        ## Create the widgets for the CSV conversion tab
        csv_file_label = ttk.Label(self.tab3, text="CSV File:")
        self.csv_file_entry = ttk.Entry(self.tab3)
        csv_file_button = ttk.Button(self.tab3, text="Select CSV File", command=select_csv_file)

        csv_voice_id_label = ttk.Label(self.tab3, text="Voice ID:")
        self.csv_voice_id_entry = ttk.Entry(self.tab3)

        csv_output_folder_label = ttk.Label(self.tab3, text="Output Folder:")
        self.csv_output_folder_entry = ttk.Entry(self.tab3)

        csv_convert_button = ttk.Button(self.tab3, text="Convert CSV", command=convert_csv)

        ## Add the widgets to the CSV conversion tab
        csv_file_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.csv_file_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        csv_file_button.grid(row=0, column=2, padx=5, pady=5)

        csv_voice_id_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.csv_voice_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        csv_output_folder_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.csv_output_folder_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        csv_convert_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        
        #Tab 5 - API
        ## Create widget for API key
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.api_key_label = tk.Label(self.tab5, text=f"Current API Key: {get_api_key()}")
        self.api_key_label.pack(side="top", pady=10)
         
        self.api_key_entry = tk.Entry(self.tab5, width=50)
        self.api_key_entry.insert(0,"Enter new API Key")
        self.api_key_entry.pack(side="top", pady=10)  
        
        def save_api_key():
            # get the text entered in the Entry widget
            new_api_key = self.api_key_entry.get()
            # set the new API key in the ConfigParser object
            config.set('API_KEYS', 'ElevenLABS', new_api_key)
            # write the changes back to the INI file
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            #update label
            self.api_key_label.config(text=f"Current API Key: {new_api_key}")
            self.api_key_entry.delete('0', 'end')
       
        self.save_api_key_button = tk.Button(self.tab5, text="Save API Key", command=save_api_key)
        self.save_api_key_button.pack(side="top", pady=10)
        ## Status Aarea
        self.api_status_label = tk.Label(self.tab5, text="")
        self.api_status_label.pack(side="top", pady=10)
               
if __name__ == "__main__":
    root = tk.Tk()
    app = TTSWindow(master=root)
    app.mainloop()
