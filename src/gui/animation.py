import tkinter as tk
from PIL import Image, ImageTk


class AnimatedGIF:
    """Simple GIF player for Tkinter canvas"""

    def __init__(self, canvas, gif_path, size=(400, 300)):
        self.canvas = canvas
        self.gif_path = gif_path
        self.size = size

        self.sequence = []
        self.delay = 100
        self.frame_index = 0
        self.is_running = False

        self._load_gif()

    def _load_gif(self):
        try:
            gif = Image.open(self.gif_path)

            for i in range(getattr(gif, "n_frames", 1)):
                gif.seek(i)
                frame = gif.copy().resize(self.size, Image.Resampling.LANCZOS)
                self.sequence.append(ImageTk.PhotoImage(frame))

            self.delay = gif.info.get("duration", 100)

        except FileNotFoundError:
            fallback = Image.new("RGB", self.size, "black")
            self.sequence = [ImageTk.PhotoImage(fallback)]

        except Exception as e:
            print("Error loading GIF:", e)
            fallback = Image.new("RGB", self.size, "black")
            self.sequence = [ImageTk.PhotoImage(fallback)]

    def start_animation(self):
        if not self.is_running:
            self.is_running = True
            self._animate()

    def stop_animation(self):
        self.is_running = False

    def _animate(self):
        if not self.is_running:
            return

        frame = self.sequence[self.frame_index]

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)

        # keep reference
        self.canvas.image = frame

        self.frame_index = (self.frame_index + 1) % len(self.sequence)

        self.canvas.after(self.delay, self._animate)
