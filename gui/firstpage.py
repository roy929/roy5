from tkinter import *
from tkinter.ttk import *
from gui.login import Login
from gui.register import Register


class FirstPage:

    def __init__(self, win=None):
        if win is None:
            self.win = Tk()
        else:
            self.win = win
        self.win.title('VoiceChat')
        self.style = Style(self.win)
        self.frame = Frame(self.win)
        self.button_login = Button(self.frame, text='login', command=self.login)
        self.button_register = Button(self.frame, text='register', command=self.register)
        center_window(self.win)

    def run(self):
        # grid & pack
        self.button_login.grid(row=0)
        self.button_register.grid(row=1)
        self.frame.pack()

        self.win.mainloop()

    def login(self):
        self.frame.destroy()
        Login(self.win).start()

    def register(self):
        self.frame.destroy()
        Register(self.win).start()


def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    f = FirstPage()
    f.run()
