import arcade


class GalgeVindue(arcade.Window):

    def __init__(self):
        super().__init__(400, 400, 'Galgen')
        arcade.set_background_color(arcade.color.GREEN)

        self.fejl = 0
        self.hit = 0
        self.victory = False

    def on_draw(self):

        arcade.start_render()

        if self.victory:
            arcade.draw_text('YOU WIN!', 100, 50, arcade.color.BLACK, 36)

        if self.fejl > 0:
            arcade.draw_line(100, 50, 150, 50, arcade.color.BLACK)
        if self.fejl > 1:
            arcade.draw_line(125, 50, 125, 300, arcade.color.BLACK)
        if self.fejl > 2:
            arcade.draw_line(125, 300, 300, 300, arcade.color.BLACK)
        if self.fejl > 3:
            arcade.draw_line(220, 300, 220, 250, arcade.color.BLACK)
        if self.fejl > 4:
            arcade.draw_circle_outline(220, 220, 30, arcade.color.BLACK)
        if self.fejl > 5:
            arcade.draw_line(220, 190, 220, 120, arcade.color.BLACK)
        if self.fejl > 6:
            arcade.draw_line(220, 120, 190, 80, arcade.color.BLACK)
            arcade.draw_line(220, 120, 250, 80, arcade.color.BLACK)
        if self.fejl > 7:
            arcade.draw_line(190, 155, 250, 155, arcade.color.BLACK)
        if self.fejl > 8:
            arcade.draw_line(205, 215, 215, 225, arcade.color.BLACK)
            arcade.draw_line(205, 225, 215, 215, arcade.color.BLACK)
            arcade.draw_line(230, 215, 240, 225, arcade.color.BLACK)
            arcade.draw_line(230, 225, 240, 215, arcade.color.BLACK)
            arcade.draw_text('DEAD', 150, 50, arcade.color.RED, 36)

        arcade.finish_render()
