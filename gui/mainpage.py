from tkinter import *
from tkinter.ttk import *
from connection import handle_server
from data import voice
from threading import Thread
import time


class MainPage:
    MY_USER_NAME = ""
    stop = False
    error = False

    def __init__(self, my_user_name, win=None):
        self.MY_USER_NAME = my_user_name
        if win:
            self.win = win
        else:
            self.win = Tk()
        self.win.title('Call Page')
        self.style = Style(self.win)
        self.frame = Frame(self.win)
        self.text1 = Label(self.frame, text='Call to')
        self.text2 = Label(self.frame)
        self.user_to_call = Entry(self.frame)
        self.call = Button(self.frame, text='Call', command=self.make_a_call)
        self.end_call = Button(self.frame, text='End Call', command=self.stop_calling)
        self.end_chat = Button(self.frame, text='End Chat', command=self.close_chat)

    def run(self, user_name, user_ip):
        pop_up_message("calling '{0}'".format(user_name))
        self.call.forget()
        self.user_to_call.forget()
        self.text1.forget()
        self.text2.configure(text='Calling {0}...'.format(user_name))
        self.text2.pack()
        self.end_call.pack()
        is_successful = handle_server.call(self.MY_USER_NAME, user_name)

        if not is_successful:
            self.error = True

        # check if 'calling' changed to 'call'

        timeout = time.time() + 60 * 0.5  # 0.5 minutes from now
        # print(timeout)

        while not self.error and not self.stop:
            if time.time() > timeout:
                pop_up_message('call stopped, waiting too long for answer')
                self.error = True

            time.sleep(0.1)
            if handle_server.is_accepted(self.MY_USER_NAME, user_name):
                print('accepted')
                break
            # need to delete calling or call if ended

        # get ok from service
        # to_call = user.call_service(self.MY_USER_NAME, user_ip)
        # find a way to break if waiting too long or if user wants to ?!!!!!

        if not self.error and not self.stop:
            self.end_call.forget()
            self.text2.configure(text='In chat with {0}'.format(user_name))
            self.end_chat.pack()
            # start chat
            voice.start()

        elif self.stop:
            pop_up_message("call stopped")
        elif self.error:
            pop_up_message('sorry, an error occurred')
        handle_server.stop_call(self.MY_USER_NAME)
        self.starting_page()

    def close_chat(self):
        handle_server.stop_chat(self.MY_USER_NAME)
        voice.end()

    def stop_calling(self):
        self.stop = True
        voice.end()

    def make_a_call(self, event=None):
        user_name = self.user_to_call.get()
        self.user_to_call.delete(0, len(user_name))
        if len(user_name) > 2 and user_name != self.MY_USER_NAME:
            user_ip = handle_server.get_user_ip(user_name)
            if user_ip:
                # start call
                t = Thread(target=self.run, args=(user_name, user_ip))
                t.start()
            else:
                pop_up_message("sorry, the user '{0}' is not registered yet".format(user_name))
        elif len(user_name) < 3:
            pop_up_message('sorry, the name is too short, at least 3 characters')
        else:
            pop_up_message("you can't call yourself")

    def starting_page(self):
        # resets values
        self.stop = False
        self.error = False

        self.end_call.forget()
        self.text2.forget()
        self.end_chat.forget()

        # packing and set up
        self.text1.pack(side=TOP)
        self.user_to_call.pack()
        self.call.pack()
        self.frame.pack()
        self.frame.bind_all('<Return>', self.make_a_call)
        self.user_to_call.focus_set()
        center_window(self.win)
        self.win.mainloop()


# this is normal chat
def type_chat():
    from data.type_chat_client import Client
    c = Client()
    c.start()


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
    my_name = 'roy'
    conn = MainPage(my_name)
    conn.starting_page()
