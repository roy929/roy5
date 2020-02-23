import socket
import time
from gui.sql import Sql
from sockets import voice

SERVER_IP = 'localhost'
SERVER_PORT = 50000
SERVICE_PORT = 50001


def get_user_ip(name):
    s = Sql()
    ip = s.get_ip(name)
    s.close_conn()
    return ip


def call_service(name_of_calling_user, user_ip=""):
    if user_ip == "":
        user_ip = SERVER_IP
    try:
        client = socket.socket()
        print('trying to connect to service')
        client.connect((user_ip, SERVICE_PORT))
        print('connected to service')
        msg = 'CONNECTING:{0}'.format(name_of_calling_user)
        client.send(msg.encode())
        time.sleep(2)
        print('waiting for answer from other user')
        ans = client.recv(1024)
        ans = ans.decode()
        client.close()
        if ans == 'True':
            return 'yes'
        elif ans == 'False':
            return 'no'
        else:
            return 'socket error'
    except socket.error:
        print('---socket error---')


def check_if_name_exists(user_name_1):
    database = Sql()
    exist = database.does_exist(user_name_1)  # return True or False
    database.close_conn()
    return exist


def call_user(user_name_1, name_of_calling_user):
    user_ip = get_user_ip(user_name_1)
    ans = call_service(name_of_calling_user, user_ip)
    if ans == 'yes':
        # now we and user run chat
        a = voice.start()
        if a == 'end':
            print('OVER')
    elif ans == 'no':
        print("sorry, the user '{0}' can't speak right now".format(user_name_1))
    else:
        print("sorry, an error occurred".format(user_name_1))


# this is normal chat
def type_chat():
    from sockets.client import Client
    c = Client()
    c.start()


def end_chat():
    voice.end()


if __name__ == '__main__':
    user_name = 'roy'
    my_name = 'random_name'
    call_user(user_name, my_name)
