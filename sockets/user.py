import socket
import time
from gui.sql import Sql
from sockets import voice

SERVER_IP = 'localhost'
SERVER_PORT = 50002
SERVICE_PORT = 50005


def get_user_ip(name):
    s = Sql()
    ip = s.get_ip(name)
    s.close_conn()
    return ip


def call_service(name_of_calling_user, user_ip=""):
    if user_ip == "":
        user_ip = SERVER_IP
    client = socket.socket()
    try:
        client.connect((user_ip, SERVICE_PORT))
        # print('connected to service')
        msg = 'Connecting:{0}'.format(name_of_calling_user)
        client.send(msg.encode())
        print('Waiting for an answer')
        time.sleep(1)
        answer = client.recv(1024)
        client.close()
        if answer.decode() == 'different':
            return 'different'
        return bool(answer.decode())
    except socket.error:
        print('---socket error---')


def handle_ans(answer):
    if answer:
        voice.start()
    elif not answer:
        print("sorry, the user can't speak right now")
    elif answer == 'different':
        print('different')
    else:
        print("sorry, an error occurred")


# this is normal chat
def type_chat():
    from sockets.client import Client
    c = Client()
    c.start()


def end_chat():
    voice.end()


def check_if_name_exists(user_name_1):
    database = Sql()
    exist = database.does_exist(user_name_1)  # return True or False
    database.close_conn()
    return exist


if __name__ == '__main__':
    user_name = 'roy'
    my_name = 'random_name'
    user_ip = get_user_ip(user_name)
    ans = call_service(my_name, user_ip)
    handle_ans(ans)

