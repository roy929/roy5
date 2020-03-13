import requests

newcall = {'src': 'yosi', 'operation': 'calling', 'dst': 'moshe'}
r = requests.post('http://127.0.0.1:5000/call', data=newcall)
print(r.json())  # r.status_code
