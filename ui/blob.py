__author__ = 'vladvalt'


from Tkinter import *

class Blob:

    def __init__(self, canvas, xy, ink, delta):

        self.canvas = canvas

        self.id = self.canvas.create_oval(
            -10-abs(delta), -10,
            11+abs(delta), 11,
            fill=ink
            )

        self.canvas.move(self.id, xy[0], xy[1])

        if delta > 0:
            self.delta = delta
            self.start = self.right
        else:
            self.delta = -delta
            self.start = self.left

    def __call__(self):
        return self.start # get things going

    def right(self):

        xy = self.canvas.coords(self.id)
        if xy[2] >= self.canvas.winfo_width():
            return self.left()

        self.canvas.move(self.id, self.delta, 0)

        return self.right

    def left(self):

        xy = self.canvas.coords(self.id)
        if xy[0] <= 0:
            return self.right()

        self.canvas.move(self.id, -self.delta, 0)

        return self.left

root = Tk()
root.title("Blobs")
root.resizable(0, 0)

frame = Frame(root, bd=5, relief=SUNKEN)
frame.pack()

canvas = Canvas(frame, width=500, height=200, bd=0, highlightthickness=0)
canvas.pack()

items = [
    Blob(canvas, (100, 50), "red", 5),
    Blob(canvas, (100, 80), "blue", -5),
    Blob(canvas, (100, 120), "green", 1),
    Blob(canvas, (100, 150), "gold", 20)
    ]

root.update() # fix geometry

# loop over items

try:
    while 1:
        for i in range(len(items)):
            items[i] = items[i]()
            root.update_idletasks() # redraw
        root.update() # process events
except TclError:
    pass # to avoid errors when the window is closed