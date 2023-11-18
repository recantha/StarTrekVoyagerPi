from gpiozero import Button
from signal import pause
from pygame import mixer
import time

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)
file_no = -1
files = ["VoyagerMainTitle.mp3", "VoyagerCore.mp3", "VoyagerRedAlert.mp3", "VoyagerTransporter.mp3", "VoyagerWarp.mp3"]

def stop_current_track():
    if mixer.get_busy():
        mixer.music.stop()

def play_track(filename):
    stop_current_track()

    print("Playing " + filename)

    mixer.music.load(filename)
    mixer.music.play()
    mixer.music.set_volume(0.4)

def next_track():
    global file_no

    print("Next track")

    file_no = file_no + 1

    if file_no == len(files):
        file_no = 0

    play_track(files[file_no])

def prev_track():
    global file_no

    print("Previous track")

    file_no = file_no - 1

    if file_no < 0:
        file_no = 0

    play_track(files[file_no])

def shutdown():
    if button_x.is_pressed and button_y.is_pressed:
        print("Shutdown")
        mixer.music.stop()

# Main

# Setup pyaudio
mixer.init()

# Setup button actions
button_a.when_pressed = prev_track
button_b.when_pressed = next_track
button_x.when_pressed = shutdown
button_y.when_pressed = pause

# Start initial track
next_track()

while True:
    if not mixer.music.get_busy():
        next_track()
    time.sleep(5)

pause()

