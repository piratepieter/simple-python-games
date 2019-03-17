import arcade
import random

class Vindue(arcade.Window):
    """
        Hele definition af vinduet.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.LIGHT_SKY_BLUE)
        self.y = 600
        self.set_update_rate(0.5)

    def on_draw(self):
        """
            Tegnefunktionen der bliver kalt flere gange hver sekund.
        """
        arcade.start_render()
        # Sne
        arcade.draw_rectangle_filled(400,30,800,60, arcade.color.WHITE)

        # Snemand
        arcade.draw_circle_filled(500, 100, 70, arcade.color.WHITE_SMOKE  )
        arcade.draw_circle_filled(500, 200, 50, arcade.color.WHITE_SMOKE  )
        arcade.draw_circle_filled(500, 280, 40, arcade.color.WHITE_SMOKE  )

        # Mund
        point_list_mund = ((485, 258),
                           (488, 256),
                           (510, 255),
                           (515, 260)
                          )
        arcade.draw_line_strip(point_list_mund, arcade.color.RED, 3)


        # Øjne
        arcade.draw_circle_filled(513, 283, 9, arcade.color.BLACK)
        arcade.draw_circle_filled(487, 283, 9, arcade.color.BLACK)
        arcade.draw_circle_filled(513, 283, 7, arcade.color.WHITE)
        arcade.draw_circle_filled(487, 283, 7, arcade.color.WHITE)
        arcade.draw_circle_filled(512, 281, 5, arcade.color.TROPICAL_RAIN_FOREST)
        arcade.draw_circle_filled(486, 281, 5, arcade.color.TROPICAL_RAIN_FOREST)

        # Næse
        point_list = ((500, 275),
                      (504, 273),
                      (505, 270),
                      (504, 267),
                      (500, 265),
                      (480, 259),
                      (480, 260),
                      )
        arcade.draw_polygon_filled(point_list, arcade.color.ORANGE_PEEL )

        # Venstre Arm
        arcade.draw_line(400, 280, 466, 224, arcade.color.BROWN, 3)
        # Fingre
        arcade.draw_line(400, 280, 385, 264, arcade.color.BROWN, 3)
        arcade.draw_line(400, 280, 383, 290, arcade.color.BROWN, 3)
        arcade.draw_line(400, 280, 395, 300, arcade.color.BROWN, 3)

        # Højre Arm
        arcade.draw_line(600, 270, 530, 224, arcade.color.BROWN, 3)
        # Fingre
        arcade.draw_line(600, 270, 615, 264, arcade.color.BROWN, 3)
        arcade.draw_line(600, 270, 613, 290, arcade.color.BROWN, 3)
        arcade.draw_line(600, 270, 620, 280, arcade.color.BROWN, 3)

        # træstamme
        arcade.draw_rectangle_filled(200, 50, 40, 50, arcade.color.BROWN)

        # Grønt
        point_list = ((150, 100),
                      (250, 100),
                      (300, 50),
                      (290, 45),
                      (105, 45),
                      (100, 50),
                      )
        arcade.draw_polygon_filled(point_list, arcade.color.DARK_GREEN )

        point_list = ((175, 150),
                      (225, 150),
                      (275, 100),
                      (265, 95),
                      (130, 95),
                      (125, 100),
                      )
        arcade.draw_polygon_filled(point_list, arcade.color.DEEP_MOSS_GREEN )

        point_list = ((199, 200),
                      (201, 200),
                      (250, 150),
                      (245, 145),
                      (155, 145),
                      (145, 150),
                      )
        arcade.draw_polygon_filled(point_list, arcade.color.GREEN )

        arcade.draw_circle_filled(400, self.y, 7, arcade.color.WHITE)
        self.y = self.y - 2

if __name__ == "__main__":
    vindue = Vindue(800, 600)
    arcade.run()
