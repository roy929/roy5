import socket
import tkinter.messagebox as tm
import tkinter
import time
from sockets import voice

SERVICE_PORT = 50003


def ask(name):
    root = tkinter.Tk()
    root.withdraw()
    result = tm.askyesno("VoiceChat", "Would you like to answer a call from {0}?".format(name))
    return result


def wait():
    in_chat = False
    print('Service Started!')
    server = socket.socket()
    server.bind(('0.0.0.0', SERVICE_PORT))
    server.listen(1)
    (client_socket, client_address) = server.accept()
    print("client accept from {0} at port {1}".format(client_address, SERVICE_PORT))

    while not in_chat:
        # waiting for request from a user to chat
        msg = client_socket.recv(1024)
        msg = msg.decode()
        if msg.startswith('CONNECTING'):  # now we got a call
            msg = msg.split(':')
            if len(msg) == 2:
                name = msg[1]
                print('{0} called'.format(name))
                ans = ask(name)  # ans = True/False
            else:
                ans = ask('')
            client_socket.send(str(ans).encode())
            time.sleep(1)
            client_socket.close()
            server.close()

            # TEST: chat server
            import server
            s = server.ChatServer()
            from threading import Thread
            t = Thread(target=s.run)
            t.start()

            print(client_address[0])

            # for now we enter chat from here
            if str(ans) == 'True':
                print('going to chat')
                in_chat = True
                a = voice.start()
                print(a)
                print('OVER')
                # while True:
                #     pass


# this is normal chat
def type_chat():
    from sockets.client import Client
    c = Client()
    c.start()


if __name__ == '__main__':
    while True:
        wait()
