import pygame
from game import Game

def main():
    pygame.init()
    WIDTH, HEIGHT = 300, 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Create a Game instance and start the game loop
    game = Game(screen)
    game.game_loop()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
