from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):

        #create root widget
        self.__root = Tk()
        self.__root.title("My Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        #create and pack canvas for drawing
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False



    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.running = False