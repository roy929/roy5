import requests
import time

ip = '127.0.0.1'
port = 5000
users_url = f'http://{ip}:{port}/users'
call_url = f'http://{ip}:{port}/call'


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


def call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'calling', 'dst': dst_name}
    r = requests.post(call_url, data=new_call)
    # print(r.json())  # r.status_code
    if r.json() == 'error':
        return False
    return True


def accept_call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'call', 'dst': dst_name}
    r = requests.put(call_url, data=new_call)
    print(r.status_code)
    print(r.json())
    # print(r.json())  # r.status_code


def look_for_call(dst_name):
    check_call = {'operation': 'calling', 'dst': dst_name}
    r = requests.get(call_url, data=check_call)
    # print(r.json())  # r.status_code
    return r.json()


def who_is_calling(dst_name):
    check_call = {'operation': 'calling', 'dst': dst_name}
    r = requests.get(call_url, data=check_call)
    print(r.json())  # r.status_code

    name = r.json().split(':')[1]
    return name


def is_accepted(src, dst):
    data = {'src': src, 'dst': dst}
    r = requests.get(call_url, data=data)
    # json = operation
    if r.json() == 'call':
        return True
    # print(r.json())
    return False


# when calling
def stop_call(src_name):
    stop_calling = {'src': src_name, 'operation': 'calling'}
    r = requests.delete(call_url, data=stop_calling)
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
