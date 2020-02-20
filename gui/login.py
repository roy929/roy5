from tkinter import *
from tkinter.ttk import *
from sql import Sql


class Login:
    MY_USER_NAME = ""

    def __init__(self, win=None):
        if win is None:
            self.win = Tk()
        else:
            self.win = win
        self.win.title('Login')
        self.style = Style(self.win)
        self.frame = Frame(self.win)
        self.entry_name = Entry(self.frame)
        self.entry_pas = Entry(self.frame, show='*')
        center_window(self.win)

    def start(self):
        # self.win.geometry('500x500')
        name = Label(self.frame, text='Name')
        pas = Label(self.frame, text='Password')
        enter = Button(self.frame, text='Enter', command=self.handle)
        self.frame.bind_all('<Return>', self.handle)

        self.entry_name.focus_set()

        # grid & pack
        name.grid(row=0, sticky=E)
        pas.grid(row=1, sticky=E)
        self.entry_name.grid(row=0, column=1)
        self.entry_pas.grid(row=1, column=1)
        enter.grid()
        self.frame.pack()
        self.win.mainloop()

    def handle(self, event=None):
        name = self.entry_name.get()
        pas = self.entry_pas.get()

        # check if exists in database
        database = Sql()
        check = database.check_account(name, pas)
        database.close_conn()
        if check:
            self.MY_USER_NAME = name
            pop_up_message("you're in, {}".format(self.MY_USER_NAME))
            # open chat page
            self.open_conn()
        else:
            self.entry_name.delete(0, len(name))
            self.entry_pas.delete(0, len(pas))
            pop_up_message("name or password in incorrect")

    def open_conn(self):
        from mainpage import MainPage
        self.frame.destroy()
        mp = MainPage(self.MY_USER_NAME, self.win)
        mp.to_run()


def pop_up_message(text):
    from time import sleep
    win = Tk()
    center_window(win, height=100)
    Style(win)
    Label(win, text=text).pack()
    win.update()
    sleep(1.5)
    win.destroy()


def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    login = Login()
    login.start()
