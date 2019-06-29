from serverclient import ServerWindow
import arcade
import random
import math


class Player:
    def __init__(self, name, x, y, r, id, color):
        self.name = name
        self.x = x
        self.y = y
        self.speed = 0
        self.rotation_speed = 0
        self.r = r
        self.radius = 8
        self.id = id
        self.color = color

    def draw(self):
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            self.color)

        r_rad = math.radians(self.r)
        arcade.draw_line(
            self.x,
            self.y,
            self.x + self.radius * math.cos(r_rad),
            self.y + self.radius * math.sin(r_rad),
            arcade.color.BLACK,
            2.0)

    def move(self, move):
        rotate_unit = 15
        speed_unit = 15

        if move == 'a':
            self.rotation_speed += rotate_unit
        elif move == 'd':
            self.rotation_speed -= rotate_unit
        elif move == 'w':
            self.speed += speed_unit
        elif move == 's':
            self.speed -= speed_unit

    def update(self, delta):
        self.r += self.rotation_speed * delta
        r_rad = math.radians(self.r)
        self.x += math.cos(r_rad) * self.speed * delta
        self.y += math.sin(r_rad) * self.speed * delta


class Bullet:
    def __init__(self, name, player):
        self.shooter = name
        self.x = player.x
        self.y = player.y
        self.r = player.r
        self.color = player.color
        self.radius = 2
        self.speed = 70 + player.speed
        self.age = 0

    def draw(self):
        arcade.draw_circle_filled(
            self.x,
            self.y,
            self.radius,
            self.color)

    def update(self, delta):
        r_rad = math.radians(self.r)
        self.x += math.cos(r_rad) * self.speed * delta
        self.y += math.sin(r_rad) * self.speed * delta
        self.age += delta


class MyWindow(ServerWindow):
    def __init__(self):
        super().__init__('localhost', 400, 400)
        arcade.set_background_color(arcade.color.BLACK)

        self.players = {}
        self.bullets = []
        self.score = {}

    def boundary_checks(self, obj):
        if obj.x > self.width:
            obj.x -= self.width
        elif obj.x < 0:
            obj.x += self.width

        if obj.y > self.height:
            obj.y -= self.height
        elif obj.y < 0:
            obj.y += self.height

    def on_draw(self):
        arcade.start_render()
        for player in self.players.values():
            player.draw()

        for bullet in self.bullets:
            bullet.draw()

    def touching_player(self, bullet):
        for name, player in self.players.items():
                if name == bullet.shooter:
                    continue
                distance = (player.x - bullet.x) ** 2 + (player.y - bullet.y) ** 2
                if distance < (player.radius + bullet.radius) ** 2:
                    return name
        return None

    def on_update(self, delta):
        for player in self.players.values():
            player.update(delta)
            self.boundary_checks(player)

        for bullet in self.bullets:
            bullet.update(delta)
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
            player = self.players[name]
            player.move(move)
        elif message == 'shoot':
            new_bullet = Bullet(name, self.players[name])
            self.bullets.insert(0, new_bullet)


s = MyWindow()
arcade.run()
