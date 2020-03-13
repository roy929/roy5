import requests

login = {'name': 'yosi', 'password': '1234'}
r = requests.get('http://127.0.0.1:5000/users', data=login)
print(r.json())  # r.status_code
