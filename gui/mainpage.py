from tkinter import *
from tkinter.ttk import *
from threading import Thread
import time
from gui.general_gui_methods import pop_up_message, center_window
from connection import handle_server
from data import voice


class MainPage:
    MY_USER_NAME = ""
    cancel = False
    timed_out = False

    def __init__(self, my_user_name, win=None):
        self.MY_USER_NAME = my_user_name
        if win:
            self.win = win
        else:
            self.win = Tk()
        self.win.title('Call Page')
        self.style = Style(self.win)
        self.start_frame = Frame(self.win)
        self.in_chat_frame = Frame(self.win)
        self.text1 = Label(self.start_frame, text='Call to')
        self.text2 = Label(self.in_chat_frame)
        self.user_to_call = Entry(self.start_frame)
        self.call = Button(self.start_frame, text='Call', command=self.make_a_call)
        self.end_call = Button(self.in_chat_frame, text='Stop calling', command=self.stop_calling)
        self.end_chat = Button(self.in_chat_frame, text='End Chat', command=self.close_chat)
        center_window(self.win)

    def main(self):
        # packing and set up
        # frame1
        self.text1.pack(side=TOP)
        self.user_to_call.pack()
        self.call.pack()
        self.start_frame.bind_all('<Return>', self.make_a_call)
        self.user_to_call.focus_set()
        self.start_frame.pack()
        # frame2
        self.text2.pack(side=TOP)
        self.end_call.pack()

        self.win.mainloop()

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

    def wait_for_answer(self, user_name, timeout=1):
        max_time = time.time() + 60 * timeout  # 1 minutes from now
        # check if 'calling' changed to 'call'
        while not self.cancel:
            if time.time() > max_time:
                self.timed_out = True
                return False
            if handle_server.is_in_chat(self.MY_USER_NAME, user_name):
                return True
            time.sleep(0.5)
        return False

    def run(self, user_name):
        self.text2.configure(text=f'Calling {user_name}...')
        self.start_frame.forget()
        self.in_chat_frame.pack()
        is_posted = handle_server.call(self.MY_USER_NAME, user_name)
        if is_posted:
            print('call posted')
            if self.wait_for_answer(user_name, 2):
                print('call accepted')
                self.end_call.forget()
                self.text2.configure(text='In chat with {0}'.format(user_name))
                self.end_chat.pack()
                voice.start()  # start chat
                # set frame back
                self.end_call.pack()
                self.end_chat.forget()
            elif self.timed_out:  # # waited too long for response from the call target
                handle_server.stop_calling(self.MY_USER_NAME)
                pop_up_message('call canceled, waiting too long for answer')
                print('call canceled, waiting too long for answer')
            elif self.cancel:  # user canceled his call
                pop_up_message('call was canceled')
                print('call was canceled')
        else:  # couldn't call
            pop_up_message("error, call already exists, please try again")
            handle_server.stop_calling(self.MY_USER_NAME)

        # reset page
        self.cancel = False
        self.timed_out = False
        self.in_chat_frame.forget()
        self.start_frame.pack()

    def close_chat(self):
        handle_server.stop_chat(self.MY_USER_NAME)
        voice.end()

    def stop_calling(self):
        handle_server.stop_calling(self.MY_USER_NAME)
        self.cancel = True


# this is normal chat
# def type_chat():
#     from data.type_chat_client import Client
#     c = Client()
#     c.start()


if __name__ == '__main__':
    my_name = 'roy'
    conn = MainPage(my_name)
    conn.main()
