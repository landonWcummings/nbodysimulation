import pygame
from model import Game

class model:
    def __init__(self, window, width, height,bodies,walls=False,consume=False):
        self.window = window
        self.width = width
        self.height = height
        self.bodies = bodies
        self.walls = walls
        self.consume = consume
    def play(self):
        window = pygame.display.set_mode((self.width, self.height))
        game = Game(self.window,self.width,self.height,
                    self.bodies,walls=self.walls,consume=self.consume)

        run = True
        clock = pygame.time.Clock()
        
        while run:
            clock.tick(150)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game.reset()
            game.loop()
            game.draw()
            pygame.display.update()
        pygame.quit()

width, height = 1400, 750
window = pygame.display.set_mode((width, height))
n = 100
m = model(window,width,height,n,walls=True,consume=True)
m.play()
