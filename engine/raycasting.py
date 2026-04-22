import pygame
import math
from level.const import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.textures = self.load_wall_textures()
        self.ray_casting_result = []

    def load_wall_textures(self):
        try:
            return {
                1: pygame.image.load('assets/textures/wall_stone.png').convert(),
                2: pygame.image.load('assets/textures/wall_metal.png').convert(),
                3: pygame.image.load('assets/textures/wall_bricks.png').convert(),
                4: pygame.image.load('assets/textures/wall_tech.png').convert(),
            }
        except:
            dummy = pygame.Surface((256, 256))
            dummy.fill((100, 100, 100))
            return {1: dummy, 2: dummy, 3: dummy, 4: dummy}

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        texture_size = 256
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        
        for ray in range(NUM_RAYS):
            sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)
            
            texture_hor, texture_vert = 1, 1

            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx; y_hor += dy; depth_hor += delta_depth

            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx; y_vert += dy; depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture_id = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture_id = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.game.player.angle - ray_angle)
            proj_height = SCREEN_DIST / (depth + 0.0001)
            wall_column = self.textures[texture_id].subsurface(offset * (texture_size - 1), 0, 1, texture_size)
            wall_column = pygame.transform.scale(wall_column, (SCALE, int(proj_height)))
            self.game.screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
            self.ray_casting_result.append((depth, proj_height, texture_id, offset, ray))
            ray_angle += DELTA_ANGLE

    def check_hitscan(self):
        # Check for sprites in the center of the screen
        center_ray = NUM_RAYS // 2
        wall_depth = self.ray_casting_result[center_ray][0]
        
        target_sprite = None
        min_dist = wall_depth
        
        for sprite in self.game.sprite_renderer.sprites:
            if sprite.alive and sprite.is_enemy:
                # Check if sprite is centered horizontally
                if abs(sprite.screen_x - HALF_WIDTH) < sprite.sprite_half_width:
                    if sprite.dist < min_dist:
                        min_dist = sprite.dist
                        target_sprite = sprite
        
        if target_sprite:
            target_sprite.health -= 50 # Standard damage
            if target_sprite.health <= 0:
                target_sprite.alive = False
