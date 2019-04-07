from server import ServerWindow
import arcade
import random
import math
import collections


class MyWindow(ServerWindow):
    def __init__(self):
        super().__init__('localhost', 400, 400)
        arcade.set_background_color(arcade.color.AMAZON)

        self.scores = collections.defaultdict(lambda: 0)

        self.radius = 20
        self.x = self.width / 2
        self.y = self.height / 2

        self.vx = self.new_velocity(50)
        self.vy = self.new_velocity(50)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.BLACK)

        for i, (name, score) in enumerate(self.scores.items()):
            msg = '%s: %d' % (name, score)
            arcade.draw_text(msg, 10, 10 + i * 15, arcade.color.BLACK, 15)

        arcade.finish_render()

    def on_update(self, delta):
        new_x = self.x + self.vx * delta
        if new_x > self.width:
            new_x = 2 * self.width - new_x
            self.vx *= -1.
        elif new_x < 0:
            new_x *= -1
            self.vx *= -1.
        self.x = new_x

        new_y = self.y + self.vy * delta
        if new_y > self.height:
            new_y = 2 * self.height - new_y
            self.vy *= -1.
        elif new_y < 0:
            new_y *= -1
            self.vy *= -1.
        self.y = new_y

        self.vx = self.new_velocity(self.vx)
        self.vy = self.new_velocity(self.vy)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
         Creat a new ball or line when using the left mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.radius += 5.
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.radius -= 5.

    @staticmethod
    def new_velocity(v):
        v_min = 20.
        v_abs = abs(v)
        shift = 1.0 if v_abs <= v_min else 0.5

        new_v = max(
            v_min,
            (shift + random.random()) * v_abs
        )

        return math.copysign(new_v, v)

    def is_touching(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.radius ** 2

    def on_message_received(self, name, message):
        xy = message.split('-')
        x = int(xy[0])
        y = int(xy[1])
        if self.is_touching(x, y):
            self.scores[name] += 1
            self.broadcast('hit', [name])

s = MyWindow()
arcade.run()
