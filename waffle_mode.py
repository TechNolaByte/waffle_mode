import sys
import threading
import time
from io import BytesIO
from pathlib import Path
from tkinter import Tk, Canvas, NW
from PIL import Image, ImageTk, ImageSequence
import platform
import subprocess

import pygame
from pynput import keyboard, mouse

from assets import GIF_BYTES, MP3_BYTES, ON_SOUND_BYTES

def set_volume_30_percent():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["nircmd", "setsysvolume", "19660"])
        elif system == "Darwin":
            subprocess.run(["osascript", "-e", "set volume output volume 30"])
        elif system == "Linux":
            subprocess.run(["amixer", "sset", "Master", "30%"])
    except Exception:
        pass

class WaffleOverlay:
    def __init__(self, gif_bytes, mp3_bytes, on_sound_bytes):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.configure(bg="black")

        self.canvas = Canvas(self.root, width=self.width, height=self.height, highlightthickness=0, bg="black")
        self.canvas.pack()

        self.gif_image = Image.open(BytesIO(gif_bytes))
        self.frames = [ImageTk.PhotoImage(f.copy().convert("RGBA")) for f in ImageSequence.Iterator(self.gif_image)]
        self.gif_w, self.gif_h = self.gif_image.size
        self.current_frame = 0

        pygame.mixer.init()
        set_volume_30_percent()
        startup_sound = pygame.mixer.Sound(BytesIO(on_sound_bytes))
        startup_sound.play()
        self.sound = pygame.mixer.Sound(BytesIO(mp3_bytes))
        
        self.kb_listener = keyboard.Listener(on_press=self.on_keyboard, suppress=True)
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse, suppress=True)
        self.kb_listener.start()
        self.mouse_listener.start()

        self.update_frame()
        self.root.mainloop()

    def update_frame(self):
        self.canvas.delete("all")
        x = (self.width - self.gif_w) // 2
        y = (self.height - self.gif_h) // 2
        self.canvas.create_image(x, y, anchor=NW, image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(50, self.update_frame)

    def on_keyboard(self, key):
        try:
            if key == keyboard.Key.f15:
                self.sound.stop()
            else:
                self.play_sound()
        except AttributeError:
            pass

    def on_mouse(self, x, y, button, pressed):
        if pressed:
            self.play_sound()

    def play_sound(self):
        set_volume_30_percent()
        self.sound.stop()
        self.sound.play()

    def stop(self):
        self.kb_listener.stop()
        self.mouse_listener.stop()
        self.root.destroy()
        pygame.mixer.quit()
        sys.exit()

if __name__ == "__main__":
    WaffleOverlay(GIF_BYTES, MP3_BYTES, ON_SOUND_BYTES)
