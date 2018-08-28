# Credit to Symon: https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it
import csv
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk

class ui_controls:
    def __init__(self, dim=50, offset=5, x=0, y=0, lines=[], to_save=[], is_car=True, file_path="./image_data/images/2018/08/fd10484b-fa1d-4df0-b394-431e17b9ec44.jpg"):
        self.dim = IntVar()
        self.dim.set(dim)
        self.offset = offset
        self.x = IntVar()
        self.x.set(x)
        self.y = IntVar()
        self.y.set(y)
        self.lines = lines
        self.to_save = to_save
        self.is_car = BooleanVar()
        self.is_car.set(is_car)
        self.file_path = file_path

    def make_smaller(self):
        if self.dim.get() >= self.offset:
            self.dim.set(self.dim.get() - self.offset)

    def make_bigger(self):
        self.dim.set(self.dim.get() + self.offset)

    def toggle_is_car(self):
        self.is_car.set(not self.is_car.get())

    def save(self):
        self.to_save.append([1 if self.is_car.get() else 0, self.x.get(), self.y.get(), self.dim.get()])
        _ = [self.lines.pop(-1) for _ in self.lines[-4:]]

    def draw_rect(self, canvas, x, y):
        self.x.set(x)
        self.y.set(y)
        dim = self.dim.get()
        coords = [
            [x - dim, y - dim, x + dim, y - dim],
            [x + dim, y - dim, x + dim, y + dim],
            [x - dim, y + dim, x + dim, y + dim],
            [x - dim, y - dim, x - dim, y + dim]
        ]
        color = "green" if self.is_car.get() else "red"
        for c in coords:
            l = canvas.create_line(c[0], c[1], c[2], c[3], fill=color)
            self.lines.append(l)

    def clear_lines(self, canvas):
        for l in self.lines:
            canvas.after(1, canvas.delete, l)
        self.lines = []

    def export_selections(self):
        save_file_path = "image_data/image_selections/" + self.file_path.split('/')[-1] + ".csv"
        print save_file_path
        with open(save_file_path, 'w+') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for s in self.to_save:
                datawriter.writerow(s)

    def handle_key_press(self, root, canvas, char):
        if char == 'q':
            print "making selection rect smaller"
            self.make_smaller()
        elif char == 'w':
            print "making selection rect bigger"
            self.make_bigger()
        elif char == 's':
            print "saving last selection"
            self.save()
        elif char == 'd':
            print "deleting unsaved lines"
            self.clear_lines(canvas)
        elif char == 'e':
            print "exporting saved lines"
            self.export_selections()
        elif char == 'a':
            print "toggling is_car"
            self.toggle_is_car()
        elif char == 'f':
            print "exiting"
            root.quit()

    def print_usage(self):
        print "**************************************************"
        print "Press 'q' to make the selection square smaller"
        print "Press 'w' to make the selection square bigger"
        print "Press 'a' to toggle is_car"
        print "Press 's' to save the latest square"
        print "Press 'd' to delete all unsaved squares"
        print "Press 'e' to export saved squares to a csv file"
        print "Press 'f' to finish and close the window"
        print "**************************************************"


if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    # File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    File = "./image_data/images/2018/08/fd10484b-fa1d-4df0-b394-431e17b9ec44.jpg"
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    cntrls = ui_controls()

    #function to be called when mouse is clicked
    def draw_rect(event):
        cntrls.draw_rect(canvas, event.x, event.y)


    def key(event):
        cntrls.handle_key_press(root, canvas, event.char)


    #mouseclick event
    canvas.bind("<Button 1>",draw_rect)
    canvas.focus_set()
    canvas.bind('<Key>', key)

    cntrls.print_usage()


    root.mainloop()
