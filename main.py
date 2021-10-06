from pynput.keyboard import Key, Listener
from playsound import playsound
from pydub import AudioSegment  
import json
import random
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item
from threading import Thread
import time 
import os
def keyHandling(args):
    json_content = ""
    with(open("config.json", "r")) as file:
        json_content = file.read()

    def updateVolume(sounds, volume):
        for i in sounds:
            song = AudioSegment.from_mp3(i)
            newVolume = song + volume
            updated_string = i[:6] + 'buffer/updated' + i[6:]
            newVolume.export(updated_string, format="mp3")


    config = json.loads(json_content)
    volume = config["volume"]
    char_sound = config["char_sound"]
    enter_sound = config["enter_sound"]
    space_sound = config["space_sound"]
    back_sound = config["backspace_sound"]
    sounds = []
    sounds.extend(char_sound.split(","))
    sounds.extend(enter_sound.split(","))
    sounds.extend(space_sound.split(","))
    sounds.extend(back_sound.split(","))
    updateVolume(sounds, volume)

    special_keys = [Key.backspace, Key.space, Key.enter]

    def show(key):
            
        if key == Key.backspace:
            sounds = back_sound.split(",")
        elif key == Key.enter:
            sounds = enter_sound.split(",")
        elif key == Key.space:
            sounds = space_sound.split(",")
        else:
            sounds = char_sound.split(",")

        playSound = sounds[random.randint(0, len(sounds) - 1)]
        updated_string = playSound[:6] + 'buffer/updated' + playSound[6:]
        playsound(updated_string, False)

    
    with Listener(on_press = show) as listener:   
        listener.join()

def setup(icon):
    icon.visible = True
    while icon.visible:
        time.sleep(5)
def action(icon):
    icon.visible = False
    icon.stop()
    os._exit(1)

def displayIcon():
    image = Image.open("favicon.ico")
    menu = (item('Stop Program', action),)
    icon = pystray.Icon(name="smh", icon=image, title ="smh", menu = menu)
    icon.run(setup)


thread = Thread(target=keyHandling, args=(12, ))
thread.start()
displayIcon()
