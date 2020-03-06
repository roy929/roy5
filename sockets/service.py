import socket
import tkinter.messagebox as tm
import tkinter
import time
from data import voice
from socket import socket

SERVICE_PORT = 50005
SERVICE_IP = '0.0.0.0'


def ask(name):
    root = tkinter.Tk()
    root.withdraw()
    result = tm.askyesno("VoiceChat", "Would you like to answer a call from {0}?".format(name))
    return result


def service():
    server = socket()
    server.bind(('', SERVICE_PORT))
    server.listen(5)
    print('Service Started!')
    client_socket, client_address = server.accept()
    print("client accept from {0} at port {1}".format(client_address, SERVICE_PORT))

    # waiting for request from a user to chat
    msg = client_socket.recv(1024)
    msg = msg.decode()
    if msg.startswith('Connecting'):  # now we got a call
        msg = msg.split(':')
        name = msg[1]
        print('{0} calling'.format(name))
        ans = ask(name)  # ans = True/False
    else:
        ans = ask('different')
    client_socket.send(str(ans).encode())
    time.sleep(0.12)
    client_socket.close()
    server.close()
    # go to main server
    if ans:
        print('starting chat, going to server')
        voice.start()
        # find a way to know when the other user leaves, and leave as well
    else:
        print(ans)


# this is normal chat
def type_chat():
    from data.type_chat_client import Client
    c = Client()
    c.start()


def main_server():
    # TEST: chat server
    import server
    s = server.ChatServer()
    from threading import Thread
    t = Thread(target=s.run)
    t.start()


if __name__ == '__main__':
    while True:
        service()
