import pygame
import math
from level.const import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = 1.5, 1.5
        self.angle = 0
        self.shot = False
        self.health = 100
        self.inventory = {"sonar": 3}
        self.shot = False
        self.fire_timer = 0
        self.fire_cooldown = 200 # ms

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pygame.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pygame.K_d]:
            dx -= speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

        if keys[pygame.K_SPACE]:
            self.use_sonar()

    def use_sonar(self):
        if self.inventory["sonar"] > 0:
            self.inventory["sonar"] -= 1
            self.game.effects.trigger_sonar_flash()
            self.game.map.reveal_area(self.map_pos, radius=5)

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        size = 8
        pygame.draw.circle(self.game.screen, 'green', (self.x * size, self.y * size), 4)

    def update(self):
        self.movement()
        self.check_goal()
        self.update_timers()

    def update_timers(self):
        if self.fire_timer > 0:
            self.fire_timer -= self.game.delta_time
            if self.fire_timer <= 0:
                self.shot = False

    def fire(self):
        if not self.shot:
            self.shot = True
            self.fire_timer = self.fire_cooldown
            # Hitscan check will go here once SpriteRenderer is updated
            self.game.raycasting.check_hitscan()

    def check_goal(self):
        if self.map_pos == self.game.map.goal:
            self.game.next_level()

    def reset_position(self):
        self.x, self.y = 1.5, 1.5
        self.angle = 0

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)