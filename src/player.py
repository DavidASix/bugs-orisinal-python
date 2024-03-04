import pygame
import math
import os

import constants as c

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.size = 25
        self.x = (c.WIDTH + self.size) / 2
        self.y = (c.HEIGHT + self.size) / 2

        self.direction = "S"

        self.moving = False
        self.jumping = False
        self.invincible = 0
        self.jump_timer = 1
        self.jump_index = 0
        self.ouch_animation = None
        self.moving_animation_index = 0
        self.play_field = pygame.Surface(screen.get_size())

        # Load sprites
        directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
        self.walking_animations = {}
        for direction in directions:
            animation_folder = f'./assets/sprites/player/{direction}'
            self.walking_animations[direction] = []
            for i in range(1, 16):
                image_path = f'{animation_folder}/{i}.png'
                image = pygame.image.load(image_path)
                self.walking_animations[direction].append(image)
        
        self.jumping_frames = []
        for i in range(32):
            image_path = f'./assets/sprites/player/jump/{i+1}.png'
            self.jumping_frames.append(pygame.image.load(image_path))


    def update_direction(self):
        # Get mouse and player positions, calculate angle (same as before)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_x, player_y = self.x, self.y
        dx, dy = mouse_x - player_x, player_y - mouse_y
        radians = math.atan2(-dy, dx)
        angle = math.degrees(radians)
        angle = (angle + 90) % 360

        # Define direction ranges and corresponding directions
        direction_ranges = {
            45: 'NE',
            90: 'E',
            135: 'SE',
            180: 'S',
            225: 'SW',
            270: 'W',
            315: 'NW'
        }

        # Find the closest direction based on the calculated angle
        closest_direction = min(direction_ranges.keys(), key=lambda x: abs(x - angle))

        # Direction buffer (same as before)
        direction_buffer = 22.5

        # Update direction if within the buffer range
        if abs(angle - closest_direction) <= direction_buffer:
            self.direction = direction_ranges[closest_direction]
        else:
            self.direction = 'N' 
    
    def move_toward_mouse(self, frame_height, current_mouse_pos):
        # Setup circular boundary for player
        circle_radius = frame_height / 2
        circle_center = (circle_radius, circle_radius)

        target_x, target_y = current_mouse_pos
        # Player should take 2.5 seconds to go from top to bottom of frame
        frame_speed = frame_height / 3.5 / c.FPS
        distance = math.hypot(target_x - self.x, target_y - self.y)
        # distance is compared against frame height to account for any variance
        # in movement when the frame is larger.
        if distance > math.floor(frame_height / 200):
            self.moving = True
            self.x += (target_x - self.x) * frame_speed / distance
            self.y += (target_y - self.y) * frame_speed / distance
        else:
            self.moving = False
        # Check if the player is outside the circle
        player_distance = math.hypot(self.x - circle_center[0], self.y - circle_center[1])
        if player_distance > circle_radius:
            # Move the player back towards the circle
            self.x -= (self.x - circle_center[0]) * (player_distance - circle_radius) / player_distance
            self.y -= (self.y - circle_center[1]) * (player_distance - circle_radius) / player_distance
    
    def calculate_jump(self):
        if self.jumping:
            # Calculate length of animation and current frame to display
            jump_length = 0.75
            jump_frame_length = c.FPS * jump_length
            jump_frame_interval = jump_frame_length / (len(self.jumping_frames) -1)
            self.jump_index = math.floor(self.jump_timer / jump_frame_interval)

            # Increment timer
            if (self.jump_timer < jump_frame_length):
                self.jump_timer += 1
        else:
            self.jump_timer = 0
    
    def animation(self):
        directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
        # Handle jumping animation
        if self.jumping:
            height = self.size * 4.5
            width = self.size * 4.5 * 0.75
            # Setup image
            image = self.jumping_frames[self.jump_index]
            image = pygame.transform.smoothscale(image, (width, height))
            self.screen.blit(image, (int(self.x - (width/2)), int(self.y - (height/3*2))))
            # Handle walking animation
        elif self.direction in directions:
            height = self.size * 2.25
            width = self.size * 2.25 * 0.75
            image = self.walking_animations[self.direction][self.moving_animation_index]
            image = pygame.transform.smoothscale(image, (width, height))
            self.screen.blit(image, (int(self.x - (width / 2)), int(self.y - (height / 2))))
            # Update animation frame
            if self.moving:
                self.moving_animation_index += 1
                self.moving_animation_index %= len(self.walking_animations[self.direction])
        # Handle the case where self.direction is not a valid direction
        else:
            pygame.draw.circle(self.screen, c.GREEN, (int(self.x), int(self.y)), self.size)

    def draw(self):
        flashing_seconds = 3
        flashing_frames = flashing_seconds * c.FPS
        flashing_interval = 3
        self.calculate_jump()
        # If the player is invincible, flash every 3 frames for 3 seconds
        if self.invincible and self.invincible < flashing_frames:
            if self.invincible % flashing_interval == 0:  
                self.animation()
            self.invincible += 1
        else:
            self.invincible = 0
            self.animation()