# -*- coding: utf-8 -*-
# Kig på http://arcade.academy/examples/drawing_primitives.html
import arcade

# Áben vindue
window = arcade.open_window(800, 500, 'Example')

# Vælg bagrundsfarve
arcade.set_background_color(arcade.color.LIGHT_SKY_BLUE)

# Begyn tegningen
arcade.start_render()

# Græs
arcade.draw_rectangle_filled(400,30,800,60, arcade.color.GREEN)

# Krop
arcade.draw_line(400,300,400,150, arcade.color.LIGHT_PINK, 4)

# Hoved
arcade.draw_circle_filled(400, 300, 40, arcade.color.LIGHT_PINK)

# Mund
point_list_mund = ((385, 282),
	               (390, 278),
	               (410, 280),
	               (412, 282)
	              )
arcade.draw_line_strip(point_list_mund, arcade.color.RED, 3)

# Øjne
arcade.draw_circle_filled(413, 303, 9, arcade.color.BLACK)
arcade.draw_circle_filled(387, 303, 9, arcade.color.BLACK)
arcade.draw_circle_filled(413, 303, 7, arcade.color.WHITE)
arcade.draw_circle_filled(387, 303, 7, arcade.color.WHITE)
arcade.draw_circle_filled(414, 301, 5, arcade.color.TROPICAL_RAIN_FOREST)
arcade.draw_circle_filled(388, 301, 5, arcade.color.TROPICAL_RAIN_FOREST)

# Ben
arcade.draw_line(400, 150, 350, 20, arcade.color.LIGHT_PINK, 4)
arcade.draw_line(400, 150, 450, 20, arcade.color.LIGHT_PINK, 4)

# Arme
point_list_arme = ((300, 300),
	               (340, 240),
	               (400, 250),
	               (450, 210),
	               (410, 170)
	              )
arcade.draw_line_strip(point_list_arme, arcade.color.LIGHT_PINK, 3)


# Afslut tegningen
arcade.finish_render()

# Vis vindue
arcade.run()