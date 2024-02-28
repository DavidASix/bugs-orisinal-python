import pygame
from game import Game
from start_menu import StartMenu

def main():
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Create a Game instance and start the game loop
    #game = Game(screen)
    main_menu = StartMenu(screen)
    main_menu.start()
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
