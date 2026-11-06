import os
import sys
import tkinter as tk
from PIL import Image, ImageTk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MapAndPawns:
    def __init__(self, root, map_path):
        self.root = root
        self.root.title("Suspended(1983) Map Assistant")
        try:
            map_image = Image.open(map_path)
            self.width, self.height = map_image.size
            self.background = ImageTk.PhotoImage(map_image)
        except FileNotFoundError:
            self.width, self.height = 1024, 768
            self.background = None
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="lightgrey")
        self.canvas.pack()
        if self.background:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        else:
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill="lightblue", outline="black")
        icon_files = [
            resource_path("icons/iris.png"),
            resource_path("icons/poet.png"),
            resource_path("icons/whiz.png"),
            resource_path("icons/sensa.png"),
            resource_path("icons/auda.png"),
            resource_path("icons/waldo.png")
        ]
        self.pawns = []
        self.pawn_images = []
        positions = [
            (50, 245), (100, 245),
            (50, 345), (100, 345),
            (50, 445), (100, 445)
            ]
        for i in range(6):
            x, y = positions[i]
            img = Image.open(icon_files[i])
            img = img.resize((32, 32), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.pawn_images.append(tk_img)
            pawn = self.canvas.create_image(
                x, y,
                image=tk_img,
                tags=f"pawn_{i}"
                )
            self.pawns.append(pawn)
            # assign event bindings for dragging
            self.canvas.tag_bind(pawn, "<ButtonPress-1>", self.start_drag)
            self.canvas.tag_bind(pawn, "<B1-Motion>", self.drag)
            self.canvas.tag_bind(pawn, "<ButtonRelease-1>", self.end_drag)

    def start_drag(self, event):
        # Find the pawn that was clicked
        self.current_pawn = self.canvas.find_withtag("current")[0]
        x, y = self.canvas.coords(self.current_pawn)
        self.offset_x = event.x - x
        self.offset_y = event.y - y

    def drag(self, event):
        if self.current_pawn:
            # Calculate new position based on mouse movement and offset
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y
            # Keep pawn within the canvas boundaries
            radius = 20
            new_x = max(radius, min(new_x, self.width - radius))
            new_y = max(radius, min(new_y, self.height - radius))
            # Move the pawn
            self.canvas.coords(
                self.current_pawn,
                new_x, new_y
            )

    def end_drag(self, event):
        self.current_pawn = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MapAndPawns(
        root,
        resource_path("map/suspended_big.png")
        )
    root.mainloop()