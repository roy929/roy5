from tkinter import *
from tkinter.ttk import *
from threading import Thread
import time
from connection import handle_server
from gui.general_gui_methods import center_window
from data import voice


class Receiver:
    MY_USER_NAME = ""

    def __init__(self, my_user_name, win=None):
        self.MY_USER_NAME = my_user_name
        if win:
            self.win = win
        else:
            self.win = Tk()
        self.win.title('Receive')
        self.style = Style(self.win)
        self.main_frame = Frame(self.win)
        self.called_frame = Frame(self.win)
        self.in_chat_frame = Frame(self.win)
        self.msg1 = Label(self.main_frame, text='waiting for a call')
        self.msg2 = Label(self.called_frame)
        self.msg3 = Label(self.in_chat_frame, text='in chat')
        self.cancel_button = Button(self.in_chat_frame, text='cancel', command=self.cancel)
        self.yes_button = Button(self.called_frame, text='yes', command=self.yes)
        self.no_button = Button(self.called_frame, text='no', command=self.no)
        center_window(self.win)

    def set(self):
        # grid & pack
        # # frame 1:
        self.msg1.pack()
        # frame 2:
        self.msg2.pack()
        self.called_frame.bind_all('<Return>', self.yes)
        self.yes_button.focus_set()
        self.yes_button.pack()
        self.no_button.pack()
        # frame 3:
        self.msg3.pack()
        self.cancel_button.pack()

    def main(self):
        self.set()  # need to run only one time
        self.main_frame.pack()
        wait_thread = Thread(target=self.wait_for_a_call)
        wait_thread.start()
        self.win.mainloop()

    def wait_for_a_call(self):
        while True:
            if handle_server.look_for_call(self.MY_USER_NAME) != 'False':
                break
            time.sleep(0.5)

        user = handle_server.who_is_calling(self.MY_USER_NAME)
        print(user, 'called')

        # self.main_frame.forget()
        self.called_frame.pack()
        self.msg2.configure(text=f'you got a call from {user}')

    def cancel(self):
        self.in_chat_frame.forget()
        # self.main_frame.pack()
        handle_server.stop_chat(self.MY_USER_NAME)
        print('end')
        wait_thread = Thread(target=self.wait_for_a_call)
        wait_thread.start()

    def yes(self):
        self.called_frame.forget()
        self.in_chat_frame.pack()
        user = handle_server.who_is_calling(self.MY_USER_NAME)
        handle_server.accept_call(user, self.MY_USER_NAME)
        end_thread = Thread(target=self.check_if_chat_over, args=[user])
        end_thread.start()
        voice_thread = Thread(target=voice.start)
        voice_thread.start()

    def no(self):
        self.called_frame.forget()
        self.main_frame.pack()
        handle_server.stop_chat(self.MY_USER_NAME)
        wait_thread = Thread(target=self.wait_for_a_call)
        wait_thread.start()

    def check_if_chat_over(self, user):
        while True:
            time.sleep(0.5)
            if not handle_server.is_in_chat(user, self.MY_USER_NAME):
                voice.end()
                break


if __name__ == '__main__':
    r = Receiver('roy')
    r.main()
