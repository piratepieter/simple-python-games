import socket

s = socket.socket()
s.connect(('localhost', 8040))
message = None
while message != 'q':
    message = input('hit/miss/victory/quit? ')
    s.send(message.encode('utf-8'))

s.close()

