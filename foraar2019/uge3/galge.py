import arcade


class MyWindow(arcade.Window):

    def __init__(self, width, height):
        super().__init__(width, height, 'Example')
        arcade.set_background_color(arcade.color.GREEN)

        self.word = 'piratskib'
        self.tried = set()
        self.errors = 0

        self.won = False
        self.lost = False

    def on_draw(self):

        arcade.start_render()

        for i, letter in enumerate(self.word):
            to_print = letter if letter in self.tried else '_'

            arcade.draw_text(
                to_print, 110 + i * 20, 350, arcade.color.BLACK, 24)

        if self.errors > 0:
            arcade.draw_line(100, 50, 150, 50, arcade.color.BLACK)
        if self.errors > 1:
            arcade.draw_line(125, 50, 125, 300, arcade.color.BLACK)
        if self.errors > 2:
            arcade.draw_line(125, 300, 300, 300, arcade.color.BLACK)
        if self.errors > 3:
            arcade.draw_line(220, 300, 220, 250, arcade.color.BLACK)
        if self.errors > 4:
            arcade.draw_circle_outline(220, 220, 30, arcade.color.BLACK)
        if self.errors > 5:
            arcade.draw_line(220, 190, 220, 120, arcade.color.BLACK)
        if self.errors > 6:
            arcade.draw_line(220, 120, 190, 80, arcade.color.BLACK)
            arcade.draw_line(220, 120, 250, 80, arcade.color.BLACK)
        if self.errors > 7:
            arcade.draw_line(190, 155, 250, 155, arcade.color.BLACK)
        if self.errors > 8:
            arcade.draw_line(205, 215, 215, 225, arcade.color.BLACK)
            arcade.draw_line(205, 225, 215, 215, arcade.color.BLACK)
            arcade.draw_line(230, 215, 240, 225, arcade.color.BLACK)
            arcade.draw_line(230, 225, 240, 215, arcade.color.BLACK)

        if self.lost:
            arcade.draw_text('DEAD', 150, 50, arcade.color.RED, 36)
        if self.won:
            arcade.draw_text('VICTORY', 100, 5, arcade.color.ARMY_GREEN, 36)

        arcade.finish_render()

    def on_key_press(self, key, key_modifiers):
        if self.won or self.lost:
            return

        letter = chr(key)
        self.tried.add(letter)
        if letter not in self.word:
            self.errors += 1
            if self.errors == 9:
                self.lost = True
        else:
            if len(set(self.word) - self.tried) == 0:
                self.won = True


window = MyWindow(400, 400)
arcade.run()
