from Ball import Ball
from Ball import PrizeBall
from CollisionSpace import BallCollisionSpace
from Cursor import Cursor
from Line import Line
import arcade
import pymunk
import time


class BallGame(arcade.Window):
    """
    Single window ball game with levels.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.cursor = Cursor()
        self.set_mouse_visible(False)

        self.level = 1
        self.setup_level()

    def setup_level(self):
        # Always initialize a new space.
        self.space = BallCollisionSpace()
        self.space.add_ball_collision_handler(
            ball_type_1=Ball,
            ball_type_2=PrizeBall,
            handler=PrizeBall.create_ball_collision_handler(),
        )

        if self.level == 1:
            self.balls_left = 5
            self.time_left = 60

            self.balls = []
            self.lines = []
            self.prizes = [
                PrizeBall(
                    self.width / 2.,
                    self.height / 2.,
                    radius=40,
                    points=5,
                    space=self.space
                ),
            ]
        elif self.level == 2:
            self.balls_left = 20
            self.time_left = 120

            # Create your sprites and sprite lists here
            self.balls = []
            self.lines = []
            self.prizes = [
                PrizeBall(400, 200, 40, 10, self.space),
                PrizeBall(200, 300, 40, 10, self.space),
                PrizeBall(250, 100, 40, 15, self.space),
            ]
        else:
            raise RuntimeError('Unknown level (%d)' % self.level)

        self.start_time = time.time()

    def active_line(self):
        """
            Returns the currenlty active not fixed line if it exists.
        """
        if len(self.lines) == 0:
            return None

        active_line = self.lines[-1]
        if not active_line.is_fixed():
            return active_line
        else:
            return None

    def fix_active_line(self):
        active_line = self.active_line()
        if active_line is not None:
            active_line.set_fixed()

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        for prize in self.prizes:
            prize.draw()

        for ball in self.balls:
            ball.draw()

        for line in self.lines:
            line.draw()

        self.cursor.draw()

        arcade.draw_text(
            'Balls left: %d' % self.balls_left,
            10,
            self.height - 20,
            arcade.color.BLACK,
            14
            )

        arcade.draw_text(
            'Time left: %d' % self.time_left,
            10,
            self.height - 40,
            arcade.color.BLACK,
            14
            )

    def on_update(self, delta_time):
        # First update all physics.
        self.space.step(delta_time)

        # Remove balls that left the window.
        for index, ball in reversed(list(enumerate(self.balls))):
            ball.update()
            if ball.y < 0:
                self.balls.pop(index)

        for line in self.lines:
            line.update()

        # Remove prize balls that have no value left.
        for index, prize in reversed(list(enumerate(self.prizes))):
            prize.update()
            if prize.points < 1:
                self.prizes.pop(index)

        self.time_left -= (time.time() - self.start_time) / 1e3

        if len(self.prizes) == 0:
            # Switch levels when all prize balls are cleared.
            self.level += 1
            self.setup_level()
        if self.time_left < 0 or (self.balls_left == 0 and len(self.balls) == 0):
            # Return to the first level if no time or balls are left.
            self.level = 1
            self.setup_level()

    def on_key_press(self, key, key_modifiers):
        """
            Switch to drawing mode when CTRL is pressed.
        """
        if key in (arcade.key.LCTRL, arcade.key.RCTRL):
            self.cursor.set_draw_mode()

    def on_key_release(self, key, key_modifiers):
        """
            Finally draw the current line if CTRL is released.
        """
        if key in (arcade.key.LCTRL, arcade.key.RCTRL):
            self.fix_active_line()
            self.cursor.set_create_mode()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Move the cursor and the active line's end point. """
        self.cursor.set_position(x, y)
        active_line = self.active_line()
        if active_line is not None:
            active_line.set_endpoint(x, y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
         Creat a new ball or line when using the left mouse button.
        """
        if button != 1:
            return

        if self.cursor.is_draw_mode():
            self.lines.append(Line(x, y, self.space))
        else:
            if self.balls_left > 0:
                self.balls.append(Ball(x, y, 10, self.space))
                self.balls_left -= 1

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
            Finally draw the current line when drawing and the
            left mouse button is released.
        """
        if button == 1 and self.cursor.is_draw_mode():
            self.fix_active_line()


def main():
    """ Run the ball game. """
    game = BallGame(800, 600)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
