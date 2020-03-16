from connection import handle_server
from data import voice
import time
from threading import Thread


# close chat
def check_if_chat_over():
    while True:
        time.sleep(0.5)
        if not handle_server.is_in_chat(user, my_name):
            voice.end()
            break


if __name__ == '__main__':
    my_name = 'kkk'
    print('waiting for a call')
    while True:
        time.sleep(0.5)
        if handle_server.look_for_call(my_name) != 'False':
            break
    user = handle_server.who_is_calling(my_name)
    print(user)
    handle_server.accept_call(user, my_name)

    t = Thread(target=voice.start, daemon=True)
    t.start()
    check_if_chat_over()

