# required_utils.py

import os
import platform
import requests
import sys
import shutil
import subprocess
import zipfile

FFMPEG_DOWNLOAD_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

def check_ffmpeg_avconv():
    try:
        # Try running the FFmpeg command
        subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT)
        return True
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError as e:
        print(f"Failed to run FFmpeg: {e}")

    try:
        # Try running the avconv command
        subprocess.check_output(['avconv', '-version'], stderr=subprocess.STDOUT)
        return True
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError as e:
        print(f"Failed to run avconv: {e}")

    return False

def download_ffmpeg_installer():
    try:
        # Create the utility folder if it doesn't exist
        os.makedirs("utility", exist_ok=True)

        response = requests.get(FFMPEG_DOWNLOAD_URL)
        response.raise_for_status()
        # Save the content to a file
        with open("utility/ffmpeg-release-essentials.zip", "wb") as zip_file:
            zip_file.write(response.content)

        # Open the saved file with zipfile.ZipFile
        with zipfile.ZipFile("utility/ffmpeg-release-essentials.zip", "r") as zip_file:
            zip_file.extractall("utility")

        # Find the name of the extracted folder dynamically
        extracted_folder = None
        for item in os.listdir("utility"):
            if item.startswith("ffmpeg-"):
                extracted_folder = item
                break

        if extracted_folder is None:
            print("Failed to find extracted FFmpeg folder.")
            return False

        # Rename the extracted folder to "ffmpeg"
        os.rename(os.path.join("utility", extracted_folder), os.path.join("utility", "ffmpeg"))

        return True
    except Exception as e:
        print(f"Failed to download FFmpeg installer: {e}")
        return False

import winreg

def add_ffmpeg_to_path():
    try:
        # Get the user-specific PATH environment variable from the registry
        env_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_READ)
        current_path, _ = winreg.QueryValueEx(env_key, 'PATH')
        winreg.CloseKey(env_key)
 
        # Construct the full path to the FFmpeg binary directory
        ffmpeg_path = os.path.abspath("utility/ffmpeg/bin/")

        # If the FFmpeg binary directory is not already in the PATH, add it to the PATH in the registry
        if ffmpeg_path not in current_path:
            new_path = f"{ffmpeg_path};{current_path}"
            env_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(env_key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(env_key)
            print("FFmpeg added to user PATH.")
        else:
            print("FFmpeg is already in user PATH.")
    except Exception as e:
        print(f"Failed to add FFmpeg to user PATH: {e}")
