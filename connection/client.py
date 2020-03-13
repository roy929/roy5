from connection.handle_server import look_for_call, who_is_calling, accept_call
from data import voice

my_name = 'guyc'
print('waiting for a call')
while True:
    if look_for_call(my_name) != 'False':
        break
user = who_is_calling(my_name)
print(user)
accept_call(user, my_name)

voice.start()

