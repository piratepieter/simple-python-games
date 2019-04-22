import arcade
import struct
from socket import AF_INET, socket, SOCK_STREAM, timeout
from threading import Thread
import time


PORT = 33000


def send_text(socket, text):
    msg = bytes(text, 'utf8')
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    socket.sendall(msg)


def recv_text(socket):
    # Read message length and unpack it into an integer
    raw_msglen = recv_bytes(socket, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    msg = recv_bytes(socket, msglen)
    text = msg.decode('utf8')
    return text


def recv_bytes(socket, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = socket.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


class ClientWindow(arcade.Window):

    def __init__(self, host, name, width, height, title='Client'):
        super().__init__(width, height, title)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((host, PORT))

        self.receive_thread = Thread(target=self.receive, args=(name,))
        self.receive_thread.start()

    def close(self):
        self.send('{quit}')
        self.receive_thread.join()
        super().close()

    def receive(self, name):
        """Handles receiving of messages."""
        self.send(name)
        while True:
            try:
                msg = recv_text(self.client_socket)
                if msg is None:
                    continue
                elif msg == '{quit}':
                    self.send('{quitreceived}')
                    break
                else:
                    self.on_message_received(msg)
            except OSError:
                break

        self.client_socket.close()
        self.client_socket = None
        self.on_connection_aborted()

    def send(self, msg):
        """Handles sending of messages."""
        if self.client_socket is not None:
            send_text(self.client_socket, msg)

    def on_message_received(self, message):
        pass

    def on_connection_aborted(self):
        pass


class ServerWindow(arcade.Window):
    TIMEOUT = 0.5

    def __init__(self, host, width, height, title='Server'):
        super().__init__(width, height, title)
        self.clients = {}
        self.addresses = {}

        self.host = host
        self.running = False

        print("Waiting for connection...")
        self.running = True
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, PORT))
        self.server.listen(10)
        self.server.settimeout(self.TIMEOUT)
        self.accept_thread = Thread(target=self.accept_incoming_connections, args=(self.is_running,))
        self.accept_thread.start()

    def close(self):
        self.running = False
        self.broadcast('{quit}')

        self.accept_thread.join()
        self.server.close()
        self.accept_thread = None
        self.server = None
        super().close()

    def is_running(self):
        return self.running

    def accept_incoming_connections(self, is_running):
        """Sets up handling for incoming clients."""
        client_threads = []

        while is_running():
            try:
                client, client_address = self.server.accept()
                print("%s:%s has connected." % client_address)
                self.addresses[client] = client_address
                client.settimeout(self.TIMEOUT)
                thread = Thread(target=self.handle_client, args=(client,))
                client_threads.append(thread)
                thread.start()
            except timeout:
                pass

        for thread in client_threads:
            thread.join()

    def handle_client(self, client):
        """Handles a single client connection."""
        name = recv_text(client)
        print('Registering as {}'.format(name))
        self.clients[client] = name

        self.on_connection_establised(name)

        while self.running:
            try:
                msg = recv_text(client)
            except timeout:
                pass
            else:
                if msg is None:
                    continue
                elif msg == "{quit}":
                    print("{} is disconnecting.".format(name))
                    send_text(client, '{quit}')
                    confirmation = recv_text(client)
                    if confirmation != '{quitreceived}':
                        raise Exception('Disconnection protocol broken')
                    # Short wait to give the client time to properly close
                    # his end of the socket and send FIN and ACK packets.
                    time.sleep(0.5)
                    client.close()
                    del self.clients[client]
                    break
                else:
                    self.on_message_received(name, msg)

        self.on_connection_aborted(name)

    def broadcast(self, msg, names=None):
        """Broadcasts a message to all the clients."""

        if names is None:
            names = list(self.clients.values())
        clients = [client for client, name in self.clients.items() if name in names]

        for sock in clients:
            send_text(sock, msg)

    def on_connection_establised(self, name):
        pass

    def on_connection_aborted(self, name):
        pass

    def on_message_received(self, name, message):
        pass
