import pygame
from game import Game
from start_menu import StartMenu
import constants as c

def main():
    pygame.init()
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

    # Create a Game instance and start the game loop
    #game = Game(screen)
    main_menu = StartMenu(screen)
    main_menu.start()
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
