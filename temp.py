# encode_assets.py
import base64

def encode_file_to_pyvar(file_path, var_name, output_py):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    with open(output_py, "a") as out:
        out.write(f'{var_name} = base64.b64decode("""{b64}""")\n\n')

# Clear previous file
with open("assets.py", "w") as f:
    f.write("import base64\n\n")

encode_file_to_pyvar("assets/overlay.gif", "GIF_BYTES", "assets.py")
encode_file_to_pyvar("assets/sound.mp3", "MP3_BYTES", "assets.py")
encode_file_to_pyvar("assets/confirmed_turned_on.wav", "ON_SOUND_BYTES", "assets.py")
