import pygame
from level import map

pygame.init()
screen = pygame.display.set_mode((720, 720))
level = map.Map(screen)
level.get_map()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #screen.fill("purple")
    level.draw()
    pygame.display.flip()

pygame.quit()

