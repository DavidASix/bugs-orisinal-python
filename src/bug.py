import pygame
import random
import math
import constants as c

class Bug:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        state_seed = random.randint(0, 3);
        initial_states = [
            (-20, random.randint(0, self.screen_height)),
            (self.screen_width + 20, random.randint(0, self.screen_height)),
            (random.randint(0, self.screen_width), -20),
            (random.randint(0, self.screen_width), self.screen_height + 20),
        ]
        self.x, self.y = initial_states[state_seed]
        self.speed = 1 # pixels per frame to move
        self.angle = random.randint(0, 360)
        self.color = [c.RED, c.BLUE, c.GREEN][random.randint(0, 2)]
        self.size = 20

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        screen_padding = self.size * 2
        width = self.screen_width + screen_padding
        height = self.screen_height + screen_padding
        min_location = -screen_padding/2
        self.x = (self.x - min_location + width) % width - screen_padding / 2
        self.y = (self.y - min_location + height) % height - screen_padding / 2

        self.angle += random.randint(-10, 10)
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y),  10)
        #pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x + self.size * math.cos(math.radians(self.angle)), self.y + self.size * math.sin(math.radians(self.angle))), 2)