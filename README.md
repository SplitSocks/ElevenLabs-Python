# ElevenLabs-Python
I am crafting a GUI for ElevenLabs Useage.I am a fledgling scripter. I thought ElevenLabs was friggin awesome so I wanted an easy to use GUI. I love Skyrim and Fallout 4 mods and hoped ElevenLabs would bring a new spark.

Currenlty this will only process a formated CSV and spit out the audio. I plan to make it more encompasing as the months go.

1. Export dialouge lines following the same guide from https://www.nexusmods.com/fallout4/mods/59626?tab=file
2. Download this repository.
3. Open CMD from the main folder you downloaded and type "python tts_window.py"
4. This requires FFMPEG. Script will download/install it for you if you do not have it installed.
5. You may need to install a few pip libraries. I will eventually paste all that here. Forgive any slowness.
5a. pip install requests
6. Enter your ElevenLabs API on the API Tab and save it.
7. Voices tab is strictly for seeing the voices you have available.
8. CSV Tab is where the magic happens.
9. CSV setup is below. If any headers are missing, the script won't fire.

voice_id = The voice you want to use for this line. The GUI will allow you to pull a list of voices on your ElevenLabs account for easy retreival. <br>
text = This is where you place the text you want parsed by ElevenLabs<br>
out_path = I utilized the out_path for the name of the file when exported, so just put the name or w/e is exported to this column by the process.<br>

voice_id, text, out_path<br>
EXAVITQu4vr4xnSDxMaL,"I like butts", .\000323


I will edit this ReadMe to be more comprehensive as time goes on.
