from server import ServerWindow
import arcade


class MyWindow(ServerWindow):
    def __init__(self):
        super().__init__('localhost', 400, 300)
        self.last_msg = 'Nothing'

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.last_msg, 10, 150, arcade.color.RED, 24)
        arcade.finish_render()

    def on_message_received(self, name, message):
        self.last_msg = '{}: {}'.format(name, message)

s = MyWindow()
arcade.run()
