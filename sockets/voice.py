import socket
import pyaudio
# import _thread
from threading import Thread

a = True
# record
CHUNK = 1024  # 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000


def set_up():
    global s, receive_stream, send_stream, a

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 50000))

    p = pyaudio.PyAudio()

    receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Voice chat running")


def receive_data():
    while a:
        try:
            data = s.recv(1024)
            receive_stream.write(data)
        except:
            pass


def send_data():
    while a:
        try:
            data = send_stream.read(CHUNK)
            s.sendall(data)
        except:
            pass


def start():
    set_up()
    recv = Thread(target=receive_data)
    send = Thread(target=send_data)
    recv.start()
    send.start()
    # _thread.start_new_thread(receive_data, ())
    # _thread.start_new_thread(send_data, ())
    print('waiting')
    while True:
        if a is False:
            return 'end'


def end():
    global a
    a = False


def time_end(t=15):
    from time import sleep
    sleep(t)
    print('closing voice')
    end()
