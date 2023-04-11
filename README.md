# ElevenLabs-Python
Crafting a GUI for ElevenLabs Useage.

I am a fledgling scripter. I thought ElevenLabs was friggin awesome so I wanted an easy to use GUI. I love Skyrim and Fallout 4 mods and hoped ElevenLabs would bring a new spark.

Currently, this GUI/script is for exported Dialouge lines from xEDIT or the CreationKit.

Download the repository.
Open cmd in folder type "python tts_window.py"

You may need to install a few pip libraries. I will eventually paste all that here. Forgive any slowness.

CSV setup is below. If any headers are missing, the script won't fire.

voice_id = The voice you want to use for this line. The GUI will allow you to pull a list of voices on your ElevenLabs account for easy retreival. <br>
text = This is where you place the text you want parsed by ElevenLabs<br>
out_path = I utilized the out_path for the name of the file when exported, so just put the name or w/e is exported to this column by the process.<br>

voice_id, text, out_path<br>
EXAVITQu4vr4xnSDxMaL,"I like butts", .\000323

When you open the GUI enter your API on the API tab and save it.
You can look at the voices tab for retrieval of the ID
CSV tab is the magic. 
1. Pick the CSV (properly formated) 
2. then select the output folder. 
3. Click convert and watch your computer scream while it's processed. (My mouse stuttered as it processed)
