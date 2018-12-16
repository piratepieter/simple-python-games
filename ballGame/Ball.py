import arcade
import pymunk


class Ball:
    """
        A dynamic black ball subject to gravity of variable size.
    """

    COLLISION_TYPE = 1

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
        self.shape = pymunk.Circle(body, self.radius, (0,0))
        self.shape.density = 3
        self.shape.friction = 0.5
        self.shape.elasticity = 0.1
        self.shape.collision_type = self.COLLISION_TYPE
        space.add(body, self.shape)

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
        r = self.shape.radius
        v = self.shape.body.position
        rot = self.shape.body.rotation_vector
        self.x = v.x
        self.y = v.y


class PrizeBall:
    """
        A static pink ball of variable size.

        Has an initial value that decreases on each collision with
        ball of type Ball.
    """
    COLLISION_TYPE = 2

    def __init__(self, x, y, radius, points, space):
        """
            Define a ball in space with initial position.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.points = points

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = self.x, self.y
        self.shape = pymunk.Circle(body, self.radius, (0,0))
        self.shape.friction = 0.
        self.shape.elasticity = 0.
        self.shape.collision_type = self.COLLISION_TYPE
        space.add(body, self.shape)

        # Create an easy way for a shape to reference back
        # to the ball. Used in the collision handler.
        self.shape.prize_ball = self

    def draw(self):
        """
            Draw the ball on the currrent active
            arcade window.
        """
        arcade.draw_circle_filled(
            self.x, self.y, self.radius, arcade.color.PINK)
        arcade.draw_text(
            '%d' % self.points,
            self.x, self.y,
            arcade.color.BLACK,
            14,
            align='center',
            anchor_x='center',
            anchor_y='center',
        )

    def update(self):
        """ Ensure the ball is removed when it has no value. """
        if self.points < 1:
            self.shape.space.remove(self.shape)

    @classmethod
    def create_ball_collision_handler(cls):
        """
            Provides a custom collision handler for
            Ball-PrizeBall collision that lowers the
            value of the latter.
        """
        def handler(arbiter, space, data):
            _, prize_shape = arbiter.shapes
            prize_shape.prize_ball.points -= 1
            return True

        return handler
