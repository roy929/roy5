import socket
import pyaudio
# import _thread
from threading import Thread

run_chat = True
# record
CHUNK = 1024  # 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
SERVER_PORT = 50002
SERVER_IP = "127.0.0.1"


def set_up():
    global s, receive_stream, send_stream, run_chat

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

    p = pyaudio.PyAudio()

    receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Voice chat running")


def receive_data():
    while run_chat:
        try:
            data = s.recv(1024)
            receive_stream.write(data)
        except:
            pass


def send_data():
    while run_chat:
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
    print('running')
    recv.join()
    s.close()
    print('voice closed')


def end():
    global run_chat
    run_chat = False


def time_end(t=15):
    from time import sleep
    sleep(t)
    print('closing voice')
    end()
