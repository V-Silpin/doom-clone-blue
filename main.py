import pygame
from level.gen import Spark

def main():
    clock = pygame.time.Clock()
    grid = None
    running = True
    obj = Spark()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid = obj.prim()

        if grid is None:
            grid = obj.prim()
        
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()