# Name csv_utils.py
import os
import csv
import tkinter as tk
from tkinter import filedialog
from scripts.audio_utils import convert_to_audio
from tqdm import tqdm

def select_csv_file(app_instance):
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(initialdir="CSV", title="Select CSV File", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if csv_file_path:
        try:
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                first_row = next(reader)
                if first_row:
                    voice_id = first_row['voice_id']
                    app_instance.csv_voice_id_entry.config(state='normal')
                    app_instance.csv_voice_id_entry.delete(0, tk.END)
                    app_instance.csv_voice_id_entry.insert(0, voice_id)
                    app_instance.csv_voice_id_entry.config(state='readonly')

                    app_instance.csv_file_entry.config(state='normal')
                    app_instance.csv_file_entry.delete(0, tk.END)
                    # extract the filename using os.path.basename()
                    filename = os.path.basename(csv_file_path)
                    # extract the parent directory using os.path.dirname()
                    parent_dir = os.path.basename(os.path.dirname(csv_file_path))
                    # concatenate the filename and parent directory
                    full_path = os.path.join(parent_dir, filename)
                    app_instance.csv_file_entry.insert(0, full_path)
                    app_instance.csv_file_entry.config(state='readonly')
                    
                    
        except StopIteration:
            app_instance.csv_voice_id_entry.config(state='normal')
            app_instance.csv_voice_id_entry.delete(0, tk.END)
            app_instance.csv_voice_id_entry.insert(0, "CSV File incorrectlly formatted")
            app_instance.csv_voice_id_entry.config(state='readonly')
            app_instance.csv_file_entry.config(state='normal')
            app_instance.csv_file_entry.delete(0, tk.END)
            app_instance.csv_file_entry.insert(0, "CSV File incorrectlly formatted")
            app_instance.csv_file_entry.config(state='readonly')

def select_output_folder(app_instance):
    global csv_output_folder
    csv_output_folder = filedialog.askdirectory(title="Select Output Folder")
    app_instance.csv_output_folder_entry.config(state='normal')
    app_instance.csv_output_folder_entry.delete(0, tk.END)
    # extract the filename using os.path.basename()
    filename = os.path.basename(csv_output_folder)
    # extract the parent directory using os.path.dirname()
    parent_dir = os.path.basename(os.path.dirname(csv_output_folder))
    # concatenate the filename and parent directory
    full_path = os.path.join(parent_dir, filename)
    app_instance.csv_output_folder_entry.insert(0, full_path)
    app_instance.csv_output_folder_entry.config(state='readonly')

def convert_csv():
    if csv_file_path:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                text = row['text']
                voice_id = row['voice_id']
                out_path = row['out_path']
                convert_to_audio(text=text, voice_id=voice_id, csv_out_path=out_path, out_folder=csv_output_folder)     
    else:
        print("No CSV file selected")