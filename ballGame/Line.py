import arcade
import pymunk


class Line:
    """
        Static straight line.

        Has 2 modes:
            1. Not fixed: the endpoint has not been set. In this
               mode, collision detection is not active.
            2. Fixed: The endpoint can no longer change. Other
               pymunk bodies can collide with the line.
    """

    def __init__(self, start_x, start_y, space):
        """
            Define a straight line in space with initial
            begin and end points.
        """
        self.x0 = start_x
        self.y0 = start_y
        self.x1 = start_x
        self.y1 = start_y
        self.thickness = 3

        self.fixed = False

        self.space = space

    def set_fixed(self):
        """
            Fix the line's end point and enable collision
            detection.
        """
        if self.is_fixed():
            return
        self.fixed = True

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(
            body=body,
            a=(self.x0, self.y0),
            b=(self.x1, self.y1),
            radius=self.thickness,
        )
        self.shape.density = 3
        self.shape.friction = 1.0
        self.space.add(body, self.shape)

    def is_fixed(self):
        """
            Whether the end point has been fixed.
        """
        return self.fixed

    def set_endpoint(self, end_x, end_y):
        """
            Move the end point of the line.
        """
        if self.fixed:
            raise RuntimeError('Cannot move fixed line')

        self.x1 = end_x
        self.y1 = end_y

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
        if not self.is_fixed():
            return
        shape = self.shape
        body = shape.body
        self.x0, self.y0 = body.position + shape.a.rotated(body.angle)
        self.x1, self.y1 = body.position + shape.b.rotated(body.angle)
