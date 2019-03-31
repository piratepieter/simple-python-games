import arcade
import socket
import select
from GalgeVindue import GalgeVindue

class MyWindow(GalgeVindue):

    def __init__(self):
        super().__init__()

        self.socket = socket.socket()
        self.socket.setblocking(False)
        self.socket.bind(('localhost', 8040))
        self.socket.listen(1)

        self.connection = None
        self.ready_to_read = None

    def close(self):
        if self.connection is not None:
            self.connection.close()
        self.socket.close()
        super().close()

    def on_update(self, elapsed):
        if self.connection is None:
            try:
                self.connection, address = self.socket.accept()
                print('Establised connection:', address)
                self.ready_to_read, _, _ = select.select([self.connection], [], [])
            except:
                pass
        else:
            for read_socket in self.ready_to_read:
                message = read_socket.recv(4096).decode('utf-8')
                if message == 'miss':
                    self.fejl += 1
                elif message == 'hit':
                    self.hit += 1
                elif message == 'victory':
                    self.victory = True
                elif message == 'quit':
                    self.close()

        super().on_update(elapsed)



if __name__ == '__main__':
    window = MyWindow()
    arcade.run()
