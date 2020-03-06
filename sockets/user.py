import socket
import time
from sockets.sql import Sql

SERVER_IP = 'localhost'
SERVER_PORT = 50002
SERVICE_PORT = 50005


def get_user_ip(name):
    s = Sql()
    ip = s.get_ip(name)
    s.close_conn()
    return ip


def call_service(name_of_calling_user, ip=""):
    if ip == "":
        ip = SERVER_IP
    client = socket.socket()
    try:
        # connect to the user's service
        client.connect((ip, SERVICE_PORT))
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


# should be in server
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
