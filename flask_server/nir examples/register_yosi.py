import requests

newuser = {'name': 'roy', 'password': '1234'}
r = requests.post('http://127.0.0.1:5000/users', data=newuser)
print(r)  # r.status_code
