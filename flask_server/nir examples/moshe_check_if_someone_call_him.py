import requests

checkcall = {'operation':'calling','dst':'moshe'}
r = requests.get('http://127.0.0.1:5000/call', data=checkcall)
print(r.json())  # r.status_code
