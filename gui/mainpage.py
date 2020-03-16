from tkinter import *
from tkinter.ttk import *
from threading import Thread
import time
from gui.general_gui_methods import pop_up_message, center_window
from connection import handle_server
from data import voice



class MainPage:
    MY_USER_NAME = ""
    stop = False
    timeout = False

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

    def starting_page(self):
        # resets values
        self.stop = False
        self.timeout = False

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

    def run(self, user_name):
        pop_up_message("calling '{0}'".format(user_name))
        self.call.forget()
        self.user_to_call.forget()
        self.text1.forget()
        self.text2.configure(text='Calling {0}...'.format(user_name))
        self.text2.pack()
        self.end_call.pack()
        is_successful = handle_server.call(self.MY_USER_NAME, user_name)
        if is_successful:
            max_time = time.time() + 60 * 0.5  # 0.5 minutes from now

            # check if 'calling' changed to 'call'
            while not self.stop and not self.timeout:
                if time.time() > max_time:
                    pop_up_message('call stopped, waiting too long for answer')
                    self.timeout = True
                elif handle_server.is_in_chat(self.MY_USER_NAME, user_name):
                    print('call accepted')
                    break
                time.sleep(0.5)

            # need to delete calling or call if ended
            # find a way to break if waiting too long or if user wants to ?!!!!!
            if not self.stop and not self.timeout:
                self.end_call.forget()
                self.text2.configure(text='In chat with {0}'.format(user_name))
                self.end_chat.pack()
                # start chat
                voice.start()
            else:
                handle_server.stop_call(self.MY_USER_NAME)
        else:
            pop_up_message("sorry, couldn't call, some error occurred")

        self.starting_page()

    def close_chat(self):
        handle_server.stop_chat(self.MY_USER_NAME)
        voice.end()

    def stop_calling(self):
        self.stop = True
        pop_up_message("call stopped")

    def make_a_call(self, event=None):
        user_name = self.user_to_call.get()
        self.user_to_call.delete(0, len(user_name))
        if len(user_name) > 2 and user_name != self.MY_USER_NAME:
            user_ip = handle_server.get_user_ip(user_name)
            # replace ip with real check if the user exists
            if user_ip:
                # start call
                t = Thread(target=self.run, args=(user_name,))
                t.start()
            else:
                pop_up_message("sorry, the user '{0}' is not registered yet".format(user_name))
        elif len(user_name) < 3:
            pop_up_message('sorry, the name is too short, at least 3 characters')
        else:
            pop_up_message("you can't call yourself")


# this is normal chat
def type_chat():
    from data.type_chat_client import Client
    c = Client()
    c.start()


if __name__ == '__main__':
    my_name = 'roy'
    conn = MainPage(my_name)
    conn.starting_page()
