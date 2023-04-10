# Name csv_utils.py
import csv
import tkinter as tk
from tkinter import filedialog

def select_csv_file():
    csv_file_path = filedialog.askopenfilename(initialdir="CSV", title="Select CSV File", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    return csv_file_path

def convert_csv():
    csv_file_path = select_csv_file()
    if csv_file_path:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                text = row['text']
                voice_id = row['voice_id']
                out_path = row['out_path']
    else:
        print("No CSV file selected.")
