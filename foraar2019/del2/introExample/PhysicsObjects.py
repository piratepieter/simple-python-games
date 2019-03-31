import arcade
import pymunk


class BallCollisionSpace(pymunk.Space):
    """
        Custom pymunk space with gravity that simplifies
        collisions between balls.
    """

    def __init__(self):
        """
            Define the space with downwards vertical
            gravity enabled.
        """
        super().__init__()
        self.gravity = 0.0, -30.0

    def add_ball_collision_handler(self, ball_type_1, ball_type_2, handler):
        """
            Set a custom collision handler between two types of balls.
        """
        collision_handler = self.add_collision_handler(
            ball_type_1.COLLISION_TYPE,
            ball_type_2.COLLISION_TYPE,
        )

        collision_handler.begin = handler


space = BallCollisionSpace()


class Ball:
    """
        A dynamic black ball subject to gravity of variable size.
    """

    COLLISION_TYPE = 1

    def __init__(self, x, y, radius):
        """
            Define a ball in space with initial position
            and collisions enabled.
        """
        self.x = x
        self.y = y
        self.radius = radius

        mass = 10
        intertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, intertia)
        body.position = self.x, self.y
        self.shape = pymunk.Circle(body, self.radius, (0,0))
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
        v = self.shape.body.position
        self.x = v.x
        self.y = v.y

    def isTouching(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.radius**2


class PrizeBall:
    """
        A static pink ball of variable size.

        Has an initial value that decreases on each collision with
        ball of type Ball.
    """
    COLLISION_TYPE = 2

    def __init__(self, x, y, radius, points):
        """
            Define a ball in space with initial position.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.points = points
        self.visible = True

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
        if not self.visible:
            return

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
        if self.visible and self.points < 1:
            self.visible = False
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


class Line:
    """
        Static straight line.

        Has 2 modes:
            1. Not fixed: the endpoint has not been set. In this
               mode, collision detection is not active.
            2. Fixed: The endpoint can no longer change. Other
               pymunk bodies can collide with the line.
    """

    def __init__(self, start_x, start_y, end_x, end_y):
        """
            Define a straight line in space with initial
            begin and end points.
        """
        self.x0 = start_x
        self.y0 = start_y
        self.x1 = end_x
        self.y1 = end_y
        self.thickness = 3

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(
            body=body,
            a=(self.x0, self.y0),
            b=(self.x1, self.y1),
            radius=self.thickness,
        )
        self.shape.density = 3
        self.shape.friction = 1.0
        space.add(body, self.shape)

    def draw(self):
        """
            Draw the line on the currrent active
            arcade window.
        """
        arcade.draw_line(
            self.x0, self.y0, self.x1, self.y1,
            color=arcade.color.BLACK,
            border_width=self.thickness,
        )

    def update(self):
        """
            Update end points based on pymunk's coordinate changes.
        """
        shape = self.shape
        body = shape.body
        self.x0, self.y0 = body.position + shape.a.rotated(body.angle)
        self.x1, self.y1 = body.position + shape.b.rotated(body.angle)
