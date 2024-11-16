import pygame

from ui import UI
from ui.enums import UIList
from ui.ui_manager import UIManager


# Launch a pygame window
class GUI(UI):
    # Setup pygame
    def setup(self):
        #setup pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        #set the screen size
        self.screen = pygame.display.set_mode((800, 600))
        #set the window title
        pygame.display.set_caption("Game")
        #set the clock
        self.clock = pygame.time.Clock()

    def loop(self):
        #run the game loop
        running = True
        while running:
            #check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    UIManager.stop()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F12:
                        UIManager.change_ui(UIList.CLI)
            #clear the screen
            self.screen.fill((0, 0, 0))
            #update the screen
            pygame.display.flip()
            #tick the clock
            self.clock.tick(60)

    def cleanup(self):
        pygame.quit()