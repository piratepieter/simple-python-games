from serverclient import ServerWindow
import arcade
import random
import math


class Player:
    def __init__(self, name, x, y, r, id, color):
        self.name = name
        self.x = x
        self.y = y
        self.r = r
        self.id = id
        self.color = color


class Bullet:
    def __init__(self, name, player):
        self.shooter = name
        self.x = player.x
        self.y = player.y
        self.r = player.r
        self.color = player.color
        self.age = 0


class MyWindow(ServerWindow):
    def __init__(self):
        super().__init__('localhost', 400, 400)
        arcade.set_background_color(arcade.color.BLACK)

        self.players = {}
        self.bullets = []
        self.score = {}

        self.radius = 8
        self.bullet_radius = 2

    def move_player(self, name, move):
        player = self.players[name]

        rotate_unit = 10
        step_unit = 10

        if move == 'a':
            player.r += rotate_unit
        elif move == 'd':
            player.r -= rotate_unit
        elif move == 'w':
            r_rad = math.radians(player.r)
            player.x += math.cos(r_rad) * step_unit
            player.y += math.sin(r_rad) * step_unit
        elif move == 's':
            r_rad = math.radians(player.r)
            player.x -= math.cos(r_rad) * step_unit
            player.y -= math.sin(r_rad) * step_unit

        self.boundary_checks(player)

    def boundary_checks(self, obj):
        if obj.x > self.width:
            obj.x -= self.width
        elif obj.x < 0:
            obj.x += self.width

        if obj.y > self.height:
            obj.y -= self.height
        elif obj.y < 0:
            obj.y += self.height

    def draw_player(self, name):
        player = self.players[name]

        arcade.draw_circle_filled(
            player.x,
            player.y,
            self.radius,
            player.color)

        r_rad = math.radians(player.r)
        arcade.draw_line(
            player.x,
            player.y,
            player.x + self.radius * math.cos(r_rad),
            player.y + self.radius * math.sin(r_rad),
            arcade.color.BLACK,
            2.0)

    def draw_bullet(self, bullet):
        arcade.draw_circle_filled(
            bullet.x,
            bullet.y,
            self.bullet_radius,
            bullet.color)

    def on_draw(self):
        arcade.start_render()
        for name in self.players:
            self.draw_player(name)

        for bullet in self.bullets:
            self.draw_bullet(bullet)

    def touching_player(self, bullet):
        for name, player in self.players.items():
                if name == bullet.shooter:
                    continue
                distance = (player.x - bullet.x) ** 2 + (player.y - bullet.y) ** 2
                if distance < (self.radius + self.bullet_radius) ** 2:
                    return name
        return None

    def on_update(self, delta):
        bullet_speed = 70
        for bullet in self.bullets:
            r_rad = math.radians(bullet.r)
            bullet.x += math.cos(r_rad) * bullet_speed * delta
            bullet.y += math.sin(r_rad) * bullet_speed * delta
            bullet.age += delta

            self.boundary_checks(bullet)

        score_updated = False

        for i, bullet in reversed(list(enumerate(self.bullets))):
            touching_player = self.touching_player(bullet)
            if touching_player is not None:
                self.bullets.pop(i)
                self.score[touching_player] -= 1
                self.score[bullet.shooter] += 1
                score_updated = True

        if score_updated:
            self.send_score()

        self.bullets = [bullet for bullet in self.bullets if bullet.age < 10]

    def send_score(self):
        msg = 'score:'
        for name, score in self.score.items():
            msg += '%s=%d,' % (name, score)
        self.broadcast(msg)

    def on_connection_establised(self, name):
        new_player = Player(
            name=name,
            x=random.randint(0, self.width),
            y=random.randint(0, self.height),
            r=random.randint(0, 360),
            id=len(self.players) + 1,
            color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        self.players[name] = new_player
        self.score[name] = 5
        self.broadcast(
            'id:%d' % new_player.id,
            [name])
        self.broadcast(
            'color:%d-%d-%d' % new_player.color,
            [name])
        self.send_score()

    def on_message_received(self, name, message):
        if 'move:' in message:
            move = message[5:]
            self.move_player(name, move)
        elif message == 'shoot':
            new_bullet = Bullet(name, self.players[name])
            self.bullets.insert(0, new_bullet)


s = MyWindow()
arcade.run()
