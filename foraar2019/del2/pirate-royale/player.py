from serverclient import ClientWindow
import arcade
import sys


class MyWindow(ClientWindow):
    def __init__(self, name):
        super().__init__('localhost', name, 300, 300)

        self.name = name
        self.id = None
        self.color = arcade.color.BLACK

        self.score = {}

    def on_draw(self):
        arcade.set_background_color(self.color)
        arcade.start_render()
        if self.id is not None:
            arcade.draw_text(
                '{} (id={})'.format(self.name, self.id),
                self.width / 2, self.height - 20,
                arcade.color.BLACK, 15,
                align='center',
                anchor_x='center',
            )

        arcade.draw_text(
            'Score: ',
            5, self.height - 55,
            arcade.color.BLACK, 15,
        )
        for i, (name, score) in enumerate(self.score.items()):
            arcade.draw_text(
                "%s => %s" % (name, score),
                75, self.height - 55 - i * 20,
                arcade.color.BLACK, 15,
            )

        if self.is_hyperjump_active():
            arcade.draw_text(
                'Hyperjump activated!',
                5, 20,
                arcade.color.RED, 15,
            )

    def on_message_received(self, message):
        if 'id:' in message:
            self.id = message[3:]
        if 'color:' in message:
            color_str = message[6:].split('-')
            self.color = (int(color_str[0]), int(color_str[1]), int(color_str[2]))
        if 'score:' in message:
            self.score = {}
            score_str = message[6:].split(',')
            for name_score in score_str:
                if '=' in name_score:
                    name, score = name_score.split('=')
                    self.score[name] = score

    def on_key_press(self, key, key_modifiers):
        letter = chr(key).lower()
        if letter in ['a', 'w', 's', 'd']:
            self.send('move:' + letter)
        if self.is_hyperjump_active() and letter == 'h':
            self.send('move:' + letter)
        elif key == arcade.key.SPACE:
            self.send('shoot')

    def on_connection_aborted(self):
        self.id = None

    def is_hyperjump_active(self):
        try:
            return int(self.score[self.name]) <= 2
        except KeyError:
            return False


s = MyWindow(sys.argv[1])
arcade.run()
