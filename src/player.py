import pygame
import math

import constants as c

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.size = 20
        self.x = (c.WIDTH + self.size) / 2
        self.y = (c.HEIGHT + self.size) / 2
        self.color = c.GREEN
        self.direction = "S"
        self.jumping = False
        self.invincible = 0
        self.ouch_animation = None
        self.jump_animation = None
        self.play_field = pygame.Surface(screen.get_size())

    def update_direction(self, last_mouse_pos, current_mouse_pos):
        if (last_mouse_pos and current_mouse_pos):
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            ew = "E" if dx > 0 else "W" if dx < 0 else ""
            ns = "S" if dy > 0 else "N" if dy < 0 else ""
            self.direction = ns + ew

    def move_toward_mouse(self, frame_height, current_mouse_pos):
        # Setup circular boundary for player
        circle_radius = frame_height / 2
        circle_center = (circle_radius, circle_radius)

        target_x, target_y = current_mouse_pos
        # Player should take 2.5 seconds to go from top to bottom of frame
        frame_speed = frame_height / 2.5 / c.FPS
        distance = math.hypot(target_x - self.x, target_y - self.y)
        # distance is compared against frame height to account for any variance
        # in movement when the frame is larger.
        if distance > math.floor(frame_height / 200):
            self.x += (target_x - self.x) * frame_speed / distance
            self.y += (target_y - self.y) * frame_speed / distance

        # Check if the player is outside the circle
        player_distance = math.hypot(self.x - circle_center[0], self.y - circle_center[1])
        if player_distance > circle_radius:
            # Move the player back towards the circle
            self.x -= (self.x - circle_center[0]) * (player_distance - circle_radius) / player_distance
            self.y -= (self.y - circle_center[1]) * (player_distance - circle_radius) / player_distance
    
    
    def animation(self):
        self.color = c.RED if self.jumping else c.GREEN
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)


    def draw(self):
        flashing_seconds = 3
        flashing_frames = flashing_seconds * c.FPS
        flashing_interval = 3

        # If the player is invincible, flash every 3 frames for 3 seconds
        if self.invincible and self.invincible < flashing_frames:
            if self.invincible % flashing_interval == 0:  
                self.animation()
            self.invincible += 1
        else:
            self.invincible = 0
            self.animation()