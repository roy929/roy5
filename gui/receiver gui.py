from tkinter import *
from tkinter.ttk import *
from threading import Thread
import time
from connection import handle_server
from gui.general_gui_methods import pop_up_message, center_window
from data import voice


class Receiver:
    MY_USER_NAME = ""

    def __init__(self, my_user_name, win=None):
        self.MY_USER_NAME = my_user_name
        if win:
            self.win = win
        else:
            self.win = Tk()
        self.win.title('RECEIVE')
        self.style = Style(self.win)
        self.frame = Frame(self.win)
        self.yes = Button(self.frame, text='yes', command=self.yes_m)
        self.no = Button(self.frame, text='no', command=self.no_m)
        center_window(self.win)

    def main(self):
        msg = Label(self.frame, text='waiting for a call')
        msg.pack()
        print('waiting for a call')
        t = Thread(target=self.wait_for_a_call)
        t.start()

        self.frame.pack()
        self.win.mainloop()

    def wait_for_a_call(self):
        while True:
            if handle_server.look_for_call(self.MY_USER_NAME) != 'False':
                break
            time.sleep(0.5)
        user = handle_server.who_is_calling(self.MY_USER_NAME)
        self.got_call(user)

    def got_call(self, name):
        # self.win.geometry('500x500')
        msg = Label(self.frame, text=f'you got a call from {name}')
        self.frame.bind_all('<Return>', self.yes_m)
        self.yes.focus_set()

        # grid & pack
        msg.pack()
        self.yes.pack()
        self.no.pack()

    def yes_m(self, name):
        print('yes')
        self.check_if_chat_over(name)

    def no_m(self):
        print('no')

        # close chat
    def check_if_chat_over(self, user):
        while True:
            time.sleep(0.5)
            if not handle_server.is_in_chat(user, self.MY_USER_NAME):
                voice.end()
                break


if __name__ == '__main__':
    r = Receiver('kkk')
    r.main()
