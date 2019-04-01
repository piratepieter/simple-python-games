import socket

s = socket.socket()
s.connect(('192.168.1.102', 8040))
message = None
while message != 'q':
    message = input('? ')
    s.send(message.encode('utf-8'))

s.close()

_
