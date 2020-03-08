import requests

new_call = {'src': 'kkk', 'operation': 'call', 'dst': 'roy'}
r = requests.post("http://127.0.0.1:5000/call", data=new_call)
print(r.json())  # r.status_code
