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

    def __init__(self, start_x, start_y, end_x, end_y, space):
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
        self.shape.friction = 0
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
