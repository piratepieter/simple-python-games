from client import ClientWindow
import arcade


class MyWindow(ClientWindow):
    def __init__(self, name):
        super().__init__('localhost', name, 400, 300)

        self.last_msg = 'Nothing'
        self.count = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.last_msg, 10, 150, arcade.color.RED, 24)
        arcade.finish_render()

    def on_message_received(self, message):
        self.last_msg = message

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.count += 1
        self.send('%d' % self.count)


s = MyWindow('Pieter')
s = MyWindow('Martin')
arcade.run()
