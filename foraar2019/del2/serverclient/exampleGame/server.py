from socket import AF_INET, socket, SOCK_STREAM, timeout
from threading import Thread
from contextlib import contextmanager
import arcade

class ServerWindow(arcade.Window):
    PORT = 33001
    BUFSIZ = 1024
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
        self.server.bind((self.host, self.PORT))
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
        name = client.recv(self.BUFSIZ).decode("utf8")
        self.clients[client] = name

        while self.running:
            try:
                msg = client.recv(self.BUFSIZ).decode("utf8")
            except timeout:
                pass
            else:
                if msg == "{quit}":
                    print("{} is disconnecting.".format(name))
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del self.clients[client]
                    break
                else:
                    self.on_message_received(name, msg)

        client.close()

    def broadcast(self, msg, names=None):
        """Broadcasts a message to all the clients."""

        if names is None:
            names = list(self.clients.values())
        clients = [client for client, name in self.clients.items() if name in names]

        for sock in clients:
            sock.send(bytes(msg, "utf8"))

    def on_message_received(self, name, message):
        pass
