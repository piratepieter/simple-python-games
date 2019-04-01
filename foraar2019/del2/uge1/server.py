import socket

s = socket.socket()
s.setblocking(False)
s.bind(('192.168.1.102', 8040))
s.listen(10)

connections = []
ips = {}

try:
    while True:
        try:
            c, address = s.accept()
            ips[c] = address[0]
            c.setblocking(False)
        except BlockingIOError:
            pass
        else:
            name = 'Unknown'
            if '192.168.1.118' == address[0]:
                name = 'Terkel'
            elif '192.168.1.103' == address[0]:
                name = 'Bertram'
            elif '192.168.1.107' == address[0]:
                name = 'Alvin'
            elif '192.168.1.100' == address[0]:
                name = 'Vivien'
            elif '192.168.1.117' == address[0]:
                name = 'Martin'
            print('Hej ', name)
            connections.append(c)
            print('Number of connections', len(connections))

        for c in connections:
            try:
                print(ips[c], c.recv(4096).decode('utf-8'))
            except BlockingIOError:
                pass
finally:
    s.close()

