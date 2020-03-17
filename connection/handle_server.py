import requests
import time

server_ip = '127.0.0.1'
server_port = 5000
users_url = f'http://{server_ip}:{server_port}/users'
call_url = f'http://{server_ip}:{server_port}/call'


# returns ip or False if user doesnt exist
def get_user_ip(name):
    data = {'name': name}
    r = requests.get(users_url, data=data)
    if r.json() == 'False':
        return False
    return r.json()  # r.status_code


def login(name, pas):
    data = {'name': name, 'password': pas}
    r = requests.get(users_url, data=data)
    if r.json() == 'True':
        return True
    return False


def register(name, pas):
    data = {'name': name, 'password': pas}
    r = requests.post(users_url, data=data)
    if r.json() == 'True':
        return True
    return False


# post calling
def call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'calling', 'dst': dst_name}
    r = requests.post(call_url, data=new_call)
    # print(r.json())  # r.status_code
    if r.json() == 'True':
        return True
    return False


# change to calling to call
def accept_call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'call', 'dst': dst_name}
    r = requests.put(call_url, data=new_call)
    if r.json() != 'go to chat':
        print(r.json())
    # print(r.json())  # r.status_code


def look_for_call(dst_name):
    check_call = {'operation': 'calling', 'dst': dst_name}
    r = requests.get(call_url, data=check_call)
    # print(r.json())  # r.status_code
    return r.json()  # return msg with name of src || False


def who_is_calling(dst_name):
    ans = look_for_call(dst_name)
    name = ans.split(':')[1]
    return name


# check if call accepted or call still alive
def is_in_chat(src, dst):
    data = {'src': src, 'dst': dst}
    r = requests.get(call_url, data=data)
    # json = operation
    if r.json() == 'call':
        return True
    # print(r.json())
    return False


# when calling
def stop_calling(src_name):
    msg = {'src': src_name, 'operation': 'calling'}
    r = requests.delete(call_url, data=msg)
    print(r.json())  # r.status_code


def stop_chat(name):
    check_call = {'src': name, 'operation': 'call', 'dst': name}
    r = requests.delete(call_url, data=check_call)
    print(r.json())  # r.status_code


if __name__ == '__main__':
    my_name = 'kkk'
    while True:
        if look_for_call(my_name) != 'False':
            break
    user = who_is_calling(my_name)
    print(user)
    accept_call(my_name, user)

    time.sleep(7)
    stop_chat(my_name)
