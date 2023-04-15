import warnings 
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", category=RuntimeWarning)

# Initial Imports
import sys
import subprocess

#Checking for proper packages
required_packages = ["requests", "tqdm", "pydub"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Attempting to install {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install it manually using 'pip install {package}' and try again.")
            sys.exit(1)

# Imports continued
import os
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, ttk
from tqdm import tqdm
from scripts.required_utils import check_ffmpeg_avconv, download_ffmpeg_installer, add_ffmpeg_to_path
from scripts.audio_utils import convert_to_audio
from scripts.api_utils import set_api_key, get_api_key
from scripts.voices_utils import get_voices
from scripts.csv_utils import convert_csv, select_csv_file, select_output_folder


class TTSWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Text-to-Speech Converter")
        self.pack(fill=tk.BOTH, expand=True)
        api_key = get_api_key()
        
        # Create a custom style for the Notebook tabs
        custom_notebook_style = ttk.Style()
        custom_notebook_style.configure("CustomNotebook.TNotebook", padding=[5, 5, 5, 5])
        custom_notebook_style.configure("CustomNotebook.TNotebook.Tab", font=('Helvetica', 12, 'bold'), padding=[10, 5, 10, 5])

        # Create a Notebook widget with the custom style
        self.notebook = ttk.Notebook(self, style="CustomNotebook.TNotebook")
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab1, text='CSV Conversion')
        self.notebook.add(self.tab2, text='Voices')
        self.notebook.add(self.tab3, text='API Setup')

        # Configure row and column weights for each tab
        for i in range(5):
            self.tab1.rowconfigure(i, weight=1)
            self.tab1.columnconfigure(0, weight=1)
            self.tab1.columnconfigure(3, weight=1)
            self.tab2.rowconfigure(i, weight=1)
            self.tab2.columnconfigure(0, weight=1)
            self.tab2.columnconfigure(3, weight=1)
            self.tab3.rowconfigure(i, weight=1)
            self.tab3.columnconfigure(0, weight=1)
            self.tab3.columnconfigure(2, weight=1)
            
        # Tab 1 - CSV File
        ## Create the widgets for the CSV conversion tab
        csvHeader = tk.Label(self.tab1, text="Utilize the Voices tab if you want a quick way to nab a voice ID for the CSV file. Remember, you must format the CSV file correctly or this won't work", font=("Arial", 12), pady=10, wraplength=400)
        csv_file_label = ttk.Label(self.tab1, text="CSV File:")
        self.csv_file_entry = ttk.Entry(self.tab1, state="readonly")
        csv_file_button = ttk.Button(self.tab1, text="Select CSV File", command=lambda: select_csv_file(self))

        csv_voice_id_label = ttk.Label(self.tab1, text="Voice ID:")
        self.csv_voice_id_entry = ttk.Entry(self.tab1, state="readonly")

        csv_output_folder_label = ttk.Label(self.tab1, text="Output Folder:")
        self.csv_output_folder_entry = ttk.Entry(self.tab1, state="readonly")
        csv_output_folder_button = ttk.Button(self.tab1, text="Select Output Folder", command=lambda: select_output_folder(self))
        self.csv_output_folder_entry = ttk.Entry(self.tab1, state="readonly")
        
        def update_output_folder_entry():
                    output_folder = select_output_folder()
                    if output_folder:
                        self.csv_output_folder_entry.delete(0, tk.END)
                        self.csv_output_folder_entry.insert(0, output_folder)
                        self.csv_output_folder_entry.config(state='readonly')
                    
        csv_convert_button = ttk.Button(self.tab1, text="Convert CSV", command=convert_csv)
        
        ## Add the widgets to the CSV conversion tab
        csvHeader.grid(row=0, column=1, columnspan=2)
        csv_file_button.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        csv_file_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.csv_file_entry.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W+tk.E)

        csv_voice_id_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.csv_voice_id_entry.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W+tk.E)

        csv_output_folder_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        csv_output_folder_label.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.csv_output_folder_entry.grid(row=5, column=2, padx=5, pady=5, sticky=tk.W+tk.E)        

        csv_convert_button.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
       
        # Tab 2 - Voices
        voicesHeader = tk.Label(self.tab2, text="View your voices available on Eleven Labs.", font=("Arial", 12), pady=10, wraplength=400)
        voicesHeader.grid(row=0, column=1)

        ## Get Voices Button
        self.get_voices_button = tk.Button(self.tab2, text="View Voices", command=lambda: get_voices(self, tk))
        self.get_voices_button.grid(row=1, column=1, pady=10, sticky=tk.W+tk.E)

        ## Add these lines to create a Listbox for voices and a Scrollbar
        self.voices_listbox = tk.Listbox(self.tab2, width=50, height=10)
        self.voices_listbox.grid(row=2, column=1, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        self.voices_scrollbar = tk.Scrollbar(self.tab2)
        self.voices_scrollbar.grid(row=2, column=2, sticky=tk.N+tk.S)
        
        ## Configure the Listbox to use the Scrollbar
        self.voices_listbox.config(yscrollcommand=self.voices_scrollbar.set)
        self.voices_scrollbar.config(command=self.voices_listbox.yview)
        
        ## Add a button to set the selected voice_id
        #self.set_voice_id_button = tk.Button(self.tab2, text="Set Voice ID", command=lambda: set_voice_id(self))
        #self.set_voice_id_button.grid(row=3, column=1, pady=10, sticky=tk.W+tk.E)

        # Initialize the voice_id variable
        self.voice_id = None

        # Tab 3 - API
        ## Create widget for API key
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.api_key_label = tk.Label(self.tab3, text=f"Current API Key: {get_api_key()}")
        self.api_key_label.grid(row=0, column=1, columnspan=3, pady=10, sticky=tk.W+tk.E)

        self.api_key_entry = tk.Entry(self.tab3, width=50)
        self.api_key_entry.insert(0, "Enter new API Key")
        self.api_key_entry.grid(row=1, column=1, pady=10, sticky=tk.W+tk.E)

        def save_api_key():
            # get the text entered in the Entry widget
            new_api_key = self.api_key_entry.get()
            # set the new API key in the ConfigParser object
            config.set('API_KEYS', 'ElevenLABS', new_api_key)
            # write the changes back to the INI file
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            # update label
            self.api_key_label.config(text=f"Current API Key: {new_api_key}")
            self.api_key_entry.delete('0', 'end')

        self.save_api_key_button = tk.Button(self.tab3, text="Save API Key", command=save_api_key)
        self.save_api_key_button.grid(row=2, column=1, pady=10, sticky=tk.W+tk.E)

        ## Status Area
        self.api_status_label = tk.Label(self.tab3, text="")
        self.api_status_label.grid(row=3, column=1, pady=10, sticky=tk.W+tk.E)

if __name__ == "__main__":
    if not check_ffmpeg_avconv():
        print("FFmpeg not found.")
        choice = input("Do you want to download the FFmpeg installer? (Windows 10/11 ONLY) Otherwise NO (y/n): ")

        if choice.lower() == "y":
            print("Downloading FFmpeg installer...")
            if download_ffmpeg_installer():
                print("FFmpeg installer downloaded successfully.")
                # Extract the downloaded file
                os.remove("utility/ffmpeg-release-essentials.zip")
                add_ffmpeg_to_path()
                root = tk.Tk()
                app = TTSWindow(master=root)
                app.mainloop()
            else:
                print("Failed to download FFmpeg installer. Please try again later.")
                print("Go to https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip to download and extract it yourself.")
                print("Be sure to add the ffmpeg/bin to your path")
            print("Please install FFmpeg before running the application.")
            print("Go to https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip to download and extract it yourself.")
            print("Be sure to add the ffmpeg/bin to your path")
            sys.exit(1)
    else:
        print("FFmpeg is installed. Launching GUI")
        root = tk.Tk()
        app = TTSWindow(master=root)
        app.mainloop()