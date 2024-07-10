import tkinter as tk
from PIL import Image, ImageTk
import pygame
import time
from threading import Timer 

class AcuSightCrosshair:
    def __init__(self, root, crosshair_paths):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.5) # Set Transparency
        self.root.config(bg='systemTransparent')
        
        self.crosshair_images = {
            'default': ImageTk.PhotoImage(Image.open(crosshair_paths['default'])),
            'kill1' : ImageTk.PhotoImage(Image.open(crosshair_paths['kill1'])),
            'kill2' : ImageTk.PhotoImage(Image.open(crosshair_paths['kill2'])),
            'kill3': ImageTk.PhotoImage(Image.open(crosshair_paths['kill3'])),
            'kill4': ImageTk.PhotoImage(Image.open(crosshair_paths['kill4'])),
            'kill5': ImageTk.PhotoImage(Image.open(crosshair_paths['kill5'])),
            'miss': ImageTk.PhotoImage(Image.open(crosshair_paths['miss'])),
        }

        self.crosshair_label = tk.label(root, image=self.crosshair_images['default'], bg='systemTransparent')
        self.crosshair_laber.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.last_event_time = time.time()
        self.inactivity_timer = None
        self.reset_inactivity_timer()

    def change_crosshair(self, crosshair_type):
        self.crosshair_label.config(image=self.crosshair_images[crosshair_type])
        self.last_event_time = time.time()
        self.reset_inactivity_timer()

    def reset_inactivity_timer(self):
        if self.inactivity_timer:
            self.inactivity_timer.cancel()
        self.inactivity_timer = Timer(540, self.reset_to_default) # 9 min Timer to reset on default if inactivity
        self.inactivity_timer.start()

    def reset_to_default(self):
        self.change_crosshair('default')

# Initialize Pygame for sound effect

pygame.mixer.init()
miss_sound = pygame.mixer.Sound("ressources/sounds/miss.wav")
hit_sound = pygame.mixer.Sound("ressources/sounds/hit.wav")
multi_hit_sound = pygame.mixer.Sound("ressources/sounds/multi_kill.wav")

def play_miss_sound():
    miss_sound.play()

def play_hit_sound():
    hit_sound.play()

def play_multi_hit_sound():
    multi_hit_sound.play()