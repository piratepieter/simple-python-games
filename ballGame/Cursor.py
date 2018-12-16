import arcade


class Cursor():
    """
        A mouse cursor with 2 modes and visual appearances.

        1. Create mode: a dark brown circle
        2. Draw mode: a dark brown square.
    """

    CREATE = 1
    DRAW = 2

    def __init__(self):
        """
            Define the cursor in create mode outside the window.
        """
        self.x = -1
        self.y = -1
        self.type = self.CREATE
        self.size = 6

    def set_position(self, x, y):
        """ Update the cursor's position. """
        self.x = x
        self.y = y

    def set_create_mode(self):
        """ Change the cursor to create mode. """
        self.type = self.CREATE

    def set_draw_mode(self):
        """ Change the cursor to draw mode. """
        self.type = self.DRAW

    def is_draw_mode(self):
        """ Whether the cursor is in draw mode. """
        return (self.type is self.DRAW)

    def draw(self):
        """
            Draw the cursor on the currrent active
            arcade window.
        """
        if self.type is self.CREATE:
            arcade.draw_circle_filled(
                self.x,
                self.y,
                self.size,
                arcade.color.BLACK_BEAN)
        elif self.type is self.DRAW:
            arcade.draw_lrtb_rectangle_filled(
                self.x - self.size,
                self.x + self.size,
                self.y + self.size,
                self.y - self.size,
                arcade.color.BLACK_BEAN)
