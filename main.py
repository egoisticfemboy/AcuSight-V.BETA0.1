import tkinter as tk
from crosshair_overlay import CrosshairOverlay
from track_kill import detect_kills

if __name__ == "__main__":
    root = tk.Tk()
    crosshair_paths = {
        'default': "ressources/crosshair/default_crosshair.png",
        'kill1': "ressources/crosshair/kill1_crosshair.png",
        'kill2': "ressources/crosshair/kill2_crosshair.png",
        'kill3': "ressources/crosshair/kill3_crosshair.png",
        'kill4': "ressources/crosshair/kill4_crosshair.png",
        'kill5': "ressources/crosshair/kill5_crosshair.png",
        'miss': "ressources/crosshair/miss_crosshair.png"
    }

    app = CrosshairOverlay(root, crosshair_paths)
    
    root.after(100, lambda: detect_kills(app))
    root.mainloop()
