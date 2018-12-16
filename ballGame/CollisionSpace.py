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
        self.gravity = 0.0, -900.0

    def add_ball_collision_handler(self, ball_type_1, ball_type_2, handler):
        """
            Set a custom collision handler between two types of balls.
        """
        collision_handler = self.add_collision_handler(
            ball_type_1.COLLISION_TYPE,
            ball_type_2.COLLISION_TYPE,
        )

        collision_handler.begin = handler
