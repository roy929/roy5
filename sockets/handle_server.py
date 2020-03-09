import requests
import time


# returns ip or False if user doesnt exist
def get_user_ip(name):
    data = {'name': name}
    r = requests.get('http://127.0.0.1:5000/users', data=data)
    if r.json() == 'False':
        return False
    return r.json()  # r.status_code


def call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'calling', 'dst': dst_name}
    r = requests.post('http://127.0.0.1:5000/call', data=new_call)
    print(r.json())  # r.status_code


def accept_call(src_name, dst_name):
    new_call = {'src': src_name, 'operation': 'call', 'dst': dst_name}
    r = requests.put('http://127.0.0.1:5000/call', data=new_call)
    print(r.json())  # r.status_code


def look_for_call(dst_name):
    check_call = {'operation': 'calling', 'dst': dst_name}
    r = requests.get('http://127.0.0.1:5000/call', data=check_call)
    print(r.json())  # r.status_code


# when calling
def stop_call(src_name):
    stop_calling = {'src': src_name, 'operation': 'calling'}
    r = requests.delete('http://127.0.0.1:5000/call', data=stop_calling)
    print(r.json())  # r.status_code


def stop_chat(my_name):
    check_call = {'src': my_name, 'operation': 'call', 'dst': my_name}
    r = requests.delete('http://127.0.0.1:5000/call', data=check_call)
    print(r.json())  # r.status_code


if __name__ == '__main__':
    user_name = 'roy'
    my_name = 'kkk'
    stop_call(my_name)
    call(my_name, user_name)
    # time.sleep(2)
    look_for_call(user_name)
    accept_call(my_name, user_name)
    # time.sleep(2)
    stop_chat(user_name)
