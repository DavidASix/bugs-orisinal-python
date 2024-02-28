import pygame
import random
import math
import constants as c
import os

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
        self.speed = 1.15 # pixels per frame to move
        self.angle = random.randint(0, 360)
        self.color = ['red', 'blue', 'green', 'yellow', 'orange'][random.randint(0, 4)]
        self.size = 15
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, f'assets/sprites/bugs/{self.color}.png')
        self.image = pygame.transform.scale(pygame.image.load(image_path), (self.size, self.size))

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        screen_padding = self.size * 2
        width = self.screen_width + screen_padding
        height = self.screen_height + screen_padding
        min_location = -screen_padding/2
        self.x = (self.x - min_location + width) % width - screen_padding / 2
        self.y = (self.y - min_location + height) % height - screen_padding / 2

        self.angle += random.randint(-2, 2)
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, 90-self.angle)
        screen.blit(rotated_image, (self.x - self.size / 2, self.y - self.size / 2))