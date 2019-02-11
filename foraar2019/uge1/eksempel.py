# -*- coding: utf-8 -*-
# Kig på http://arcade.academy/examples/drawing_primitives.html
import arcade

# Áben vindue
window = arcade.open_window(800, 800, 'Example')

# Vælg bagrundsfarve
arcade.set_background_color(arcade.color.YELLOW)

# Begyn tegningen
arcade.start_render()

# Båd
arcade.draw_line(200, 100, 600, 100, arcade.color.BLACK, 2)
arcade.draw_line(200, 100, 100, 300, arcade.color.BLACK, 2)
arcade.draw_line(600, 100, 700, 300, arcade.color.BLACK, 2)

# Ben
arcade.draw_line(400, 200, 350, 120, arcade.color.BLACK, 2)
arcade.draw_line(400, 200, 450, 120, arcade.color.BLACK, 2)

# Arme
arcade.draw_line(400, 250, 300, 300, arcade.color.BLACK, 2)
arcade.draw_line(400, 250, 500, 300, arcade.color.BLACK, 2)


# Krop
arcade.draw_ellipse_filled(400, 250, 40, 70, arcade.color.GREEN)

# Hoved
arcade.draw_circle_filled(400, 350, 40, arcade.color.AMBER)

# Afslut tegningen
arcade.finish_render()

# Vis vindue
arcade.run()
