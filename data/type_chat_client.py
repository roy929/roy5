import socket
import _thread
from queue import Queue
from threading import Thread


class Client(Thread):
    recv_q = Queue()
    send_q = Queue()

    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                if data != "":
                    print(data.decode())
                    self.recv_q.put(data.decode())

            except Exception as e:
                print('error:', e)
                break

    def send_data(self):
        while True:
            if not self.send_q.empty():
                try:
                    data = self.send_q.get()
                    self.s.send(data.encode())
                except Exception as e:
                    print('error:', e)
                    break

    def run(self, ip=None):
        ip = "127.0.0.1"
        flag = 0
        try:
            self.s.connect((ip, 50000))
            print("client chat running")
            flag = 1
        except Exception as e:
            print(e)
        if flag == 1:
            # RECV
            self.s_recv()
            # SEND
            self.s_send()
            # WRITE TO SEND
            self.write_msg()
            # continue

    def s_recv(self):
        _thread.start_new_thread(self.receive_data, ())

    def s_send(self):
        _thread.start_new_thread(self.send_data, ())

    def add_to_q(self, data):
        self.send_q.put(data)

    def write_msg(self):
        while True:
            msg = input()
            if msg != "":
                self.add_to_q(msg)
            if msg == 'quit':
                break


if __name__ == '__main__':
    c = Client()
    c.start()
    print('now we write code')
