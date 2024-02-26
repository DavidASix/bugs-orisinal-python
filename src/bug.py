import pygame
import random
import math

class Bug:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(0, self.screen_height)
        self.speed = 1.8 # pixels per frame to move
        self.angle = random.randint(0, 360)
        self.size = 20

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

        self.x = (self.x + self.screen_width) % self.screen_width
        self.y = (self.y + self.screen_height) % self.screen_height

        self.angle += random.randint(-10, 10)
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y),  10)
        #pygame.draw.line(screen, (0, 0, 0), (self.x, self.y), (self.x + self.size * math.cos(math.radians(self.angle)), self.y + self.size * math.sin(math.radians(self.angle))), 2)