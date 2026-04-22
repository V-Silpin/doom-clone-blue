import pygame
import sys
from level.const import *
from engine.map import Map
from bio_entity.Player import Player
from bio_entity.Item import Item
from engine.raycasting import RayCasting
from engine.effects import PostProcess
from engine.ui import UI
from engine.sprite_renderer import SpriteRenderer, SpriteObject

# States
MENU, PLAYING, WIN = 0, 1, 2

class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.current_level = 1
        self.state = MENU
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = RayCasting(self)
        self.effects = PostProcess(self)
        self.sprite_renderer = SpriteRenderer(self)
        self.ui = UI(self)
        self.map.generate_new_map()
        self.player.reset_position()
        self.map.reveal_area(self.player.map_pos, 3)

    def next_level(self):
        self.current_level += 1
        if self.current_level > 10:
            self.state = WIN
        else:
            self.map.generate_new_map()
            self.player.reset_position()
            self.map.reveal_area(self.player.map_pos, 3)

    def update(self):
        if self.state == PLAYING:
            self.player.update()
            self.sprite_renderer.update()
            self.effects.update()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'DOOM CLONE BLUE - FPS: {self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == PLAYING:
            pygame.draw.rect(self.screen, (20, 20, 40), (0, 0, WIDTH, HALF_HEIGHT))
            pygame.draw.rect(self.screen, (40, 40, 40), (0, HALF_HEIGHT, WIDTH, HEIGHT))
            self.raycasting.ray_cast()
            self.sprite_renderer.update()
            self.map.draw()
            self.player.draw()
            self.effects.draw()
            self.ui.draw_weapon()
            self.ui.draw_hud()
        elif self.state == MENU: self.ui.draw_menu()
        elif self.state == WIN: self.ui.draw_win()
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == MENU and event.key == pygame.K_RETURN: self.state = PLAYING
                elif self.state == WIN and event.key == pygame.K_RETURN:
                    self.current_level = 1; self.new_game(); self.state = PLAYING

    def run(self):
        while True:
            self.check_events(); self.update(); self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()