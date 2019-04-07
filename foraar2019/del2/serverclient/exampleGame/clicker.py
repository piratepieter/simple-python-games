from client import ClientWindow
import arcade


class MyWindow(ClientWindow):
    def __init__(self, name):
        super().__init__('localhost', name, 400, 400)
        arcade.set_background_color(arcade.color.AMAZON)

        self.score = 0

    def on_draw(self):
        arcade.start_render()
        msg = 'Score: %d' % self.score
        arcade.draw_text(msg, 10, 10, arcade.color.BLACK, 15)
        arcade.finish_render()

    def on_message_received(self, message):
        if message == 'hit':
            self.score += 1

    def on_mouse_press(self, x, y, button, key_modifiers):
        self.send('%d-%d' % (x, y))


s = MyWindow('Pieter')
s = MyWindow('Martin')
arcade.run()
