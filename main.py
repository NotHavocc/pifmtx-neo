import subprocess
import ffmpeg
import numpy as np
import os
import shutil
import threading
from pathlib import Path
from PIL import Image
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__, template_folder='web', static_folder='web', static_url_path='')

UPLOAD_FOLDER = 'uploads'
jammer_process = None
freq = "95.0"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    temp_path = Path("~/pifmtx-neo/pifmtx-neo/uploads/temp.wav").expanduser()
    sstv_path = Path("~/pifmtx-neo/pifmtx-neo/uploads/sstv.wav").expanduser()
    audio_data = request.files.get('audio_file')
    image_data = request.files.get('img_file')

    if audio_data and audio_data.filename != '':
        audio_path = os.path.join(UPLOAD_FOLDER, audio_data.filename)
        audio_data.save(audio_path)
        print(f"INFO: Processing audio: {audio_path}")
        audio_encode(audio_path)
        broadcast_audio(temp_path)
        return redirect(url_for('index'))

    if image_data and image_data.filename != '':
        img_path = os.path.join(UPLOAD_FOLDER, image_data.filename)
        image_data.save(img_path)
        print(f"INFO: Processing Image: {img_path}")
        sstv_encode(img_path)
        broadcast_audio(sstv_path)
        return redirect(url_for('index'))
        
    return """
    <script>
        alert('ERROR : check if uploaded file is valid.');
        window.location.href = '/';
    </script>
    """

@app.route('/freq', methods=['POST'])
def set_freq():
    global freq
    data = request.get_json()
    new_val = str(data.get('freq')) 
    freq = new_val
    return f"INFO: Success: {freq}"

def audio_encode(path):
    with open(path, 'r') as f:
        print(f"INFO: Reading: {path}")

        path_obj = Path(path)
        extension = path_obj.suffix

        if extension != ".wav" :
            print("INFO: File is not .wav, converting...")
            input_file = path
            output_file = Path("~/pifmtx-neo/pifmtx-neo/uploads/temp.wav").expanduser()

            try:
                (
                    ffmpeg
                    .input(input_file)
                    .output(output_file)
                    .run()
                )
                print("INFO: Conversion complete!")
            except ffmpeg.Error as e:
                print(f"ERROR: {e.stderr.decode()}")

@app.route('/sstv', methods=['POST'])
def sstv_encode(img_path):
    sstv_path = Path("~/pifmtx-neo/pifmtx-neo/uploads/sstv.wav").expanduser()
    img = Image.open(img_path)
    mode_var = request.form.get('sstv_mode')
    print(f"INFO: Using {mode_var} transmission mode...")

    if mode_var == "Robot36":
        from pysstv.color import Robot36 as SelectedMode
    elif mode_var == "MartinM1":
        from pysstv.color import MartinM1 as SelectedMode
    elif mode_var == "Robot24BW":
        from pysstv.grayscale import Robot24BW as SelectedMode
    elif mode_var == "ScottieS1":
        from pysstv.color import ScottieS1 as SelectedMode
    elif mode_var == "PD120":
        from pysstv.color import PD120 as SelectedMode
    else:
        raise ValueError("ERROR: Unknown mode!")
    
    sstv = SelectedMode(img, 44100, 16)

    with open(sstv_path, "wb") as f:
        sstv.write_wav(f)

def broadcast_audio(file_path):
    command = ["sudo", "pi_fm_rds", "-freq", str(freq), "-audio", file_path]
    
    try:
        print(f"INFO: Broadcasting {file_path} on {freq}MHz...")
        subprocess.run(command)
    except KeyboardInterrupt:
        print("\nINFO: Stopping broadcast.")

def generate_static(process):
    try:
        if not process.stdin:
            return

        while process.poll() is None:
            samples = np.random.randint(-32768, 32767, 2048, dtype=np.int16)
            
            process.stdin.write(samples.tobytes())
            process.stdin.flush() 
            
    except (BrokenPipeError, AttributeError, OSError):
        print("WARNING: Transmission pipe closed.")
    finally:
        try:
            process.stdin.close()
        except:
            pass

@app.route('/jammer')
def start_jammer():
    global jammer_process
    if jammer_process is None:
        cmd = ["sudo", "pi_fm_rds", "-freq", str(freq), "-audio", "-"]
        jammer_process = subprocess.Popen(cmd, stdin=subprocess.PIPE)

        threading.Thread(target=generate_static, args=(jammer_process), daemon=True).start()
        
    return redirect(url_for('index'))

@app.route('/stop')
def stop_all():
    temp_path = Path("~/pifmtx-neo/pifmtx-neo/uploads/temp.wav").expanduser()
    global jammer_process
    if jammer_process:
        jammer_process.terminate()
        jammer_process.wait()       
        jammer_process = None
    try:
        subprocess.run(["sudo", "pkill", "pi_fm_rds"], check=True)
        print("INFO: All transmitter processes terminated.")
        if os.path.isfile(temp_path):
            os.remove(temp_path)
        return redirect(url_for('index'))
    except subprocess.CalledProcessError:
        print("INFO: No active transmitter processes found to kill.")
        if os.path.isfile(temp_path):
            os.remove(temp_path)
        return redirect(url_for('index'))
    
if __name__ == "__main__":
    uploads_path = Path("~/pifmtx-neo/pifmtx-neo/uploads").expanduser()
    print("INFO: Removing upload cache...")
    if os.path.exists(uploads_path):
        shutil.rmtree(uploads_path)
        os.mkdir(uploads_path)
    else:
        os.mkdir(uploads_path)
    app.run(host="0.0.0.0", port="5000")

