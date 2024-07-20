import sounddevice as sd
import numpy as np

# Read threshold value from file
threshold = int(open(r"keys\threshold", "r").readline().strip())
Clap = False

def detect_clap(indata, frames, time, status):
    global Clap
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > threshold:
        print("Clapped!")
        Clap = True

def listen_for_claps():
    with sd.InputStream(callback=detect_clap):
        sd.sleep(1000)

def main_clap_exe():
    print("Waiting for clap to run the JARVIS")
    while True:
        listen_for_claps()
        if Clap:
            break

if __name__ == "__main__":
    main_clap_exe()
