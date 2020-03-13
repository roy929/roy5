import requests

newcall = {'src': 'yosi', 'operation': 'call', 'dst': 'moshe'}
r = requests.put('http://127.0.0.1:5000/call', data=newcall)
print(r.json())  # r.status_code
