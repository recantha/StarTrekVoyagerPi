from gpiozero import Button
from signal import pause
from pygame import mixer
from PIL import Image, ImageDraw, ImageFont
import ST7789 as ST7789
import time
import os

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)
file_no = -1
folder = "/home/pi/StarTrekVoyagerPi"

files = ["VoyagerMainTitle.mp3", "VoyagerCore.mp3", "VoyagerRedAlert.mp3", "VoyagerTransporter.mp3", "VoyagerWarp.mp3"]

def stop_current_track():
    if mixer.get_busy():
        mixer.music.stop()

def play_track(filename):
    stop_current_track()

    print("Playing " + filename)

    mixer.music.load(folder + "/" + filename)
    mixer.music.play()
    mixer.music.set_volume(0.3)

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

def display_text(the_text):
    global disp

    # Draw black square
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    size_x, size_y = draw.textsize(the_text, font)
    text_x = 0
    text_y = 0

    draw.text((text_x, text_y), the_text, font=font, fill=(255, 0, 0))
    disp.display(img)

def shutdown():
    global shutting_down

    shutting_down = True

    if button_x.is_pressed and button_y.is_pressed:
        display_text("Shutdown")
        time.sleep(3)
        mixer.music.stop()
        os.system('sudo shutdown now')

def display_image(filename):
    global disp

    image = Image.open(folder + "/" + filename)
    disp.display(image)

    print("Displayed image: " + filename)

# Main

# Setup pyaudio
mixer.init()

# Setup screen

HEIGHT = 240
WIDTH = 240

disp = ST7789.ST7789(
    height = HEIGHT,
    rotation = 90,
    port = 0,
    cs = 1,
    dc = 9,
    backlight = 13,
    spi_speed_hz = 80*1000*1000,
    offset_left = 0,
    offset_top = 0
)

WIDTH = disp.width
HEIGHT = disp.height
disp.begin()

image_files = [
    "Starfleet_Command_Insignia.png",
    "LCARS_wallpaper.png",
    "Starfleet_Command_simple_insignia.png",
    "Voyager_Full_LCARS.jpg"
]
image_num = -1

display_text("Starting up...")

# Setup button actions
button_a.when_pressed = prev_track
button_b.when_pressed = next_track
button_x.when_pressed = shutdown
button_y.when_pressed = pause

# Start initial track
next_track()

shutting_down = False

while True:
    image_num = image_num + 1
    if image_num == len(image_files):
        image_num = 0

    if not shutting_down:
        display_image(image_files[image_num])

    if not mixer.music.get_busy():
        next_track()

    time.sleep(7)

pause()

