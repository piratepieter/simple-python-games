from PhysicsObjects import Ball
from PhysicsObjects import Line
from PhysicsObjects import space
from SendWindow import SendWindow
import arcade


class BallGame(SendWindow):
    """
    Single window ball game with levels.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AMAZON)

        self.level = 1
        self.setup_level()

    def setup_level(self):
        # Always initialize a new space.
        if self.level == 1:
            self.line = Line(100, 100, 200, 200)
            self.balls = [
                Ball(600, 500, 10),
                Ball(500, 500, 25),
                Ball(400, 500, 50),
            ]
        else:
            raise RuntimeError('Unknown level (%d)' % self.level)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.line.draw()
        for ball in self.balls:
            ball.draw()

    def on_update(self, delta_time):
        # First update all physics.
        space.step(delta_time)
        self.line.update()
        for ball in self.balls:
            ball.update()

        if len(self.balls) == 0:
            self.sendMessage('victory')

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
         Creat a new ball or line when using the left mouse button.
        """
        for i, ball in reversed(list(enumerate(self.balls))):
            if ball.isTouching(x, y):
                self.balls.pop(i)
                self.sendMessage('hit')
                return

        self.sendMessage('miss')


def main():
    """ Run the ball game. """
    game = BallGame(800, 600)
    arcade.run()


if __name__ == "__main__":
    main()
