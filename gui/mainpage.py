from tkinter import *
from tkinter.ttk import *
import sockets.user as user
from threading import Thread


class MainPage(Thread):
    MY_USER_NAME = ""
    USER_TO_CALL = ""

    def __init__(self, my_user_name, win=None):
        super().__init__()
        self.MY_USER_NAME = my_user_name
        if win is None:
            self.win = Tk()
        else:
            self.win = win

        self.win.title('User')
        self.style = Style(self.win)
        self.frame = Frame(self.win)
        self.name = Label(self.frame, text='Call to').pack(side=TOP)
        self.user_to_call = Entry(self.frame)
        self.call = Button(self.frame, text='Call', command=self.collect_viable_name)
        self.end_call = Button()

    def try_call(self):
        pop_up_message("calling '{0}'".format(self.USER_TO_CALL))
        self.call.forget()
        self.user_to_call.forget()
        # self.win.withdraw()
        self.start()  # threaded, the chat function
        # find a way to know when chat ended
        self.end_call = Button(self.frame, text='End Call', command=user.end_chat)
        self.end_call.pack()
        # self.win.update()
        # self.win.deiconify()

    def collect_viable_name(self, event=None):
        user_name = self.user_to_call.get()
        self.user_to_call.delete(0, len(user_name))
        if len(user_name) > 2 and user_name != self.MY_USER_NAME:
            if user.check_if_name_exists(user_name):  # check if the name database
                self.USER_TO_CALL = user_name
                self.try_call()
            else:
                pop_up_message("sorry, the user '{0}' is not registered yet".format(user_name))
        elif len(user_name) < 3:
            pop_up_message('sorry, the name is too short, at least 3 characters')
        else:
            pop_up_message("sorry, you can't call yourself")

    def to_run(self):
        # packing and set up
        self.user_to_call.pack()
        self.call.pack()
        self.frame.pack()
        self.frame.bind_all('<Return>', self.collect_viable_name)
        self.user_to_call.focus_set()
        center_window(self.win)
        self.win.mainloop()

    def run(self):
        user.call_user(self.USER_TO_CALL, self.MY_USER_NAME)


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
    name = 'test'
    conn = MainPage(name)
    conn.to_run()
    print('here')
    while not True:
        pass
    # now chat
