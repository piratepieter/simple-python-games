import arcade


class Vindue(arcade.Window):
    """
        Hele definition af vinduet.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.YELLOW)

    def on_draw(self):
        """
            Tegnefunktionen der bliver kalt flere gange hver sekund.
        """
        arcade.start_render()
        arcade.draw_point(100, 100, arcade.color.BLACK, 20)


if __name__ == "__main__":
    vindue = Vindue(800, 600)
    arcade.run()
