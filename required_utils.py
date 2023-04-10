# required_utils.py
import os
import sys
import subprocess
import requests

def check_ffmpeg_avconv():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def download_ffmpeg_installer():
    url = "https://github.com/GyanD/codexffmpeg/releases/download/6.0/ffmpeg-6.0-full_build.7z"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open("ffmpeg-6.0-full_build.7z", "wb") as file:
            file.write(response.content)
        return True
    else:
        return False

def main():
    if not check_ffmpeg_avconv():
        print("FFmpeg not found.")
        choice = input("Do you want to download the FFmpeg installer? (y/n): ")
        
        if choice.lower() == "y":
            print("Downloading FFmpeg installer...")
            if download_ffmpeg_installer():
                print("FFmpeg installer downloaded successfully. Please install FFmpeg and try again.")
            else:
                print("Failed to download FFmpeg installer. Please try again later.")
    else:
        print("FFmpeg is installed.")

if __name__ == "__main__":
    main()
