# required_utils.py
import os
import sys
import requests
import subprocess
import shutil
import subprocess

def check_ffmpeg_avconv():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

def check_ffmpeg_avconv():
    return shutil.which("ffmpeg") is not None or shutil.which("avconv") is not None

def download_ffmpeg_installer():
    try:
        import requests
        import zipfile
        
        response = requests.get(FFMPEG_DOWNLOAD_URL)
        response.raise_for_status()

        with zipfile.ZipFile(response.content) as zip_file:
            zip_file.extractall()

        return True
    except Exception as e:
        print(f"Failed to download FFmpeg installer: {e}")
        return False

def add_ffmpeg_to_path():
    current_path = os.environ.get("PATH", "")
    ffmpeg_path = os.path.abspath("ffmpeg-4.4-essentials_build/bin")
    
    if ffmpeg_path not in current_path:
        os.environ["PATH"] = f"{ffmpeg_path};{current_path}"
        print("FFmpeg added to PATH.")
    else:
        print("FFmpeg is already in PATH.")

def main():
    if not check_ffmpeg_avconv():
        print("FFmpeg not found.")
        choice = input("Do you want to download the FFmpeg installer? (y/n): ")
        
        if choice.lower() == "y":
            print("Downloading FFmpeg installer...")
            if download_ffmpeg_installer():
                print("FFmpeg installer downloaded successfully.")
                subprocess.run(["7z", "x", "ffmpeg-release-essentials.zip"])
                os.remove("ffmpeg-release-essentials.zip")
                add_ffmpeg_to_path()
            else:
                print("Failed to download FFmpeg installer. Please try again later.")
    else:
        print("FFmpeg is installed.")

if __name__ == "__main__":
    main()