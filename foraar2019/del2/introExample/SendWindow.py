from BallPhysics import Ball
from BallPhysics import PrizeBall
import arcade
import socket


class SendWindow(arcade.Window):
    """
    Single window ball game with levels.
    """
    def __init__(self, width, height):
        super().__init__(width, height)

        self.socket = socket.socket()
        self.socket.connect(('localhost', 8040))

    def sendMessage(self, message):
        self.socket.send(message.encode('utf-8'))

    def close(self):
        self.socket.close()
        super().close()
