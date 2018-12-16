import arcade
import pymunk


class Ball:
    """
        A dynamic black ball subject to gravity of variable size.
    """

    def __init__(self, x, y, radius, space):
        """
            Define a ball in space with initial position
            and collisions enabled.
        """
        self.x = x
        self.y = y
        self.radius = radius

        body = pymunk.Body()
        body.position = self.x, self.y
        self.shape = pymunk.Circle(body, self.radius, (0, 0))
        self.shape.density = 3
        self.shape.friction = 0.5
        self.shape.elasticity = 0.1
        space.add(body, self.shape)

    def push(self, force, *args):
        print('pushing', *args)
        self.shape.body.apply_impulse_at_local_point(force)

    def draw(self):
        """
            Draw the ball on the currrent active
            arcade window.
        """
        arcade.draw_circle_filled(
            self.x, self.y, self.radius, arcade.color.BLACK)

    def update(self):
        """
            Update end points based on pymunk's coordinate changes.
        """
        position = self.shape.body.position
        self.x = position.x
        self.y = position.y
