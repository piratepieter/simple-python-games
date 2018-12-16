from Ball import Ball
from Line import Line
import arcade
import pymunk
from speech_recognition import Microphone
from speech_recognition import Recognizer


class MyWindow(arcade.Window):
    """
    Single window ball game with levels.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.AMAZON)
        self.microphone = Microphone()
        self.recognizer = Recognizer()

        # with self.microphone as source:
        #     self.recognizer.adjust_for_ambient_noise(source, duration=2.0)
        self.recognizer.energy_threshold = 5000

        self.stop_listening = None

    def cleanup(self):
        if self.stop_listening is not None:
            self.stop_listening(False)

    def setup(self):
        def process_sound(recognizer, audio_data):
            try:
                result = self.recognizer.recognize_google(audio_data)
            except Exception:
                return

            force = 0.
            if result.lower().startswith('l'):
                force = -10000
            elif result.lower().startswith('r'):
                force = 10000
            self.ball.push((force, 0), result)

        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            process_sound,
            phrase_time_limit=1.,
        )

        self.space = pymunk.Space()
        self.space.gravity = 0.0, -900.0
        self.bottom_line = Line(100, 100, 400, 100, self.space)
        self.left_line = Line(100, 100, 100, 200, self.space)
        self.right_line = Line(400, 100, 400, 200, self.space)
        self.ball = Ball(200, 200, 10, self.space)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self.bottom_line.draw()
        self.left_line.draw()
        self.right_line.draw()
        self.ball.draw()

    def on_update(self, delta_time):
        # First update all physics.
        self.space.step(delta_time)

        self.bottom_line.update()
        self.left_line.update()
        self.right_line.update()
        self.ball.update()


def main():
    """ Run the ball game. """
    game = MyWindow(800, 600)
    game.setup()
    arcade.run()
    game.cleanup()


if __name__ == "__main__":
    main()
