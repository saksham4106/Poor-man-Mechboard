from pynput.keyboard import Key, Listener
from pydub import AudioSegment  
import json
import random
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item
from threading import Thread
import time 
import os
import tkinter as tk
import pygame

def strip(string):
    return string.replace(" ", "")
json_content = ""
with(open("config.json", "r")) as file:
    json_content = file.read()

shouldPlay = True
config = json.loads(json_content)
volume = config["volume"]
# char_sound = strip(config["char_sound"])
# enter_sound = strip(config["enter_sound"])
# space_sound = strip(config["space_sound"])
# back_sound = strip(config["backspace_sound"])
# sounds = []
# sounds.extend(char_sound.split(","))
# sounds.extend(enter_sound.split(","))
# sounds.extend(space_sound.split(","))
# sounds.extend(back_sound.split(","))
sounds = []
char_sound = enter_sound = space_sound = back_sound = ""
def update_sounds():
    global sounds, char_sound, enter_sound, back_sound, space_sound
    char_sound = strip(config["char_sound"])
    enter_sound = strip(config["enter_sound"])
    space_sound = strip(config["space_sound"])
    back_sound = strip(config["backspace_sound"])
    sounds.extend(char_sound.split(","))
    sounds.extend(enter_sound.split(","))
    sounds.extend(space_sound.split(","))
    sounds.extend(back_sound.split(","))

update_sounds()
def keyHandling(args):
    def updateVolume(sounds, volume):
        try:
            for i in sounds:
                song = AudioSegment.from_mp3(i)
                newVolume = song + volume
                updated_string = i[:6] + 'buffer/updated' + i[6:]
                newVolume.export(updated_string, format="mp3")
        except FileNotFoundError:
            pass

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
        pygame.mixer.init()
        pygame.mixer.music.load(updated_string)
        if(shouldPlay):
            pygame.mixer.music.play()

    
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
def action2(icon):
    win = tk.Tk()
    global volume, char_sound, enter_sound, back_sound, space_sound
    def volume_changed():
        global volume, shouldPlay
        n_vol = vol_slid.get()
        n_cso = strip(c_so.get())
        n_eso = strip(e_so.get())
        n_bso = strip(b_so.get())
        n_sso = strip(s_so.get())
        config["volume"] = n_vol
        volume = n_vol
        config["char_sound"] = n_cso
        config["enter_sound"] = n_eso
        config["backspace_sound"] = n_bso
        config["space_sound"] = n_sso

        update_sounds()

        if(switch.get() == 0):
            shouldPlay = False
        else:
            shouldPlay = True

        with open("config.json", "w") as f:
            f.write(json.dumps(config))

        try:
            for i in sounds:
                song = AudioSegment.from_mp3(i)
                newVolume = song + volume
                updated_string = i[:6] + 'buffer/updated' + i[6:]
                newVolume.export(updated_string, format="mp3")
        except FileNotFoundError:
            pass
        
    win.title("ALL THE CONFIGURATION YOU WILL EVER NEED")
    tk.Label(win, text = "Volume: ").grid(row=1, column = 0)
    vol_slid = tk.Entry(win, width = 40)
    vol_slid.delete(0, "end")
    vol_slid.insert(0, volume)
    vol_slid.grid(row = 1, column = 1)
    
    switch = tk.Scale(win,label = "Stop           Start", from_ = 0, to = 1, orient = tk.HORIZONTAL, showvalue = 0)
    switch.set(1)
    switch.grid(row = 0, column = 0)


    tk.Label(win, text = "Char key sounds: ").grid(row = 3, column = 0)
    c_so = tk.Entry(win, width = 40)
    c_so.insert(0, char_sound)
    c_so.grid(row = 3, column = 1)

    tk.Label(win, text = "Space key sounds: ").grid(row = 4, column = 0)
    s_so = tk.Entry(win, width = 40)
    s_so.insert(0, space_sound)
    s_so.grid(row = 4, column = 1)

    tk.Label(win, text = "Enter key sounds: ").grid(row = 5, column = 0)
    e_so = tk.Entry(win, width = 40)
    e_so.insert(0, enter_sound)
    e_so.grid(row = 5, column = 1)

    tk.Label(win, text = "Backspace key sounds: ").grid(row = 6, column = 0)
    b_so = tk.Entry(win, width = 40)
    b_so.insert(0, back_sound)
    b_so.grid(row = 6, column = 1)

    save_button = tk.Button(win, text = "Save", command = volume_changed)
    save_button.grid(row = 10, column = 0)

    win.mainloop()

def displayIcon():
    image = Image.open("favicon.ico")
    menu = (item("Config", action2), item('Stop Program', action),)
    icon = pystray.Icon(name="smh", icon=image, title ="smh", menu = menu)
    icon.run(setup)


thread = Thread(target=keyHandling, args=(12, ))
thread.start()
displayIcon()
