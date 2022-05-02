#!/usr/local/bin/python3

import block

'''
    The player can be moved and reset.
    It is constrained by the borders.
'''


class Player(block.Block):
    def __init__(self, path, pos_x, pos_y, speed_x, speed_y):
        super().__init__(path, pos_x, pos_y)
        # Fixed speed of the player
        self.speed_x = speed_x
        self.speed_y = speed_y
        # Current speed of the player
        self.movement_x = 0
        self.movement_y = 0
        # Initial position of the player
        self.initial_x = pos_x
        self.initial_y = pos_y

    def update(self, screen_height, screen_width, ball_group):
        # Update current position of the player while checking for constraints
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y
        self.screen_constraint(screen_height, screen_width)

    def screen_constraint(self, screen_height, screen_width):
        # Constrain player movement to within boundaries
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height - 0:
            self.rect.bottom = screen_height - 0
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width - 0:
            self.rect.right = screen_width - 0

    def reset_player(self):
        # Teleport player to starting position
        self.rect.center = (self.initial_x, self.initial_y)
