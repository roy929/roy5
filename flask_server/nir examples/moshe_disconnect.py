import requests

checkcall = {'operation':'call','dst':'moshe'}
r = requests.delete('http://127.0.0.1:5000/call', data=checkcall)
print(r.json()) #r.status_code

