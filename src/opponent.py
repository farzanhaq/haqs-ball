#!/usr/local/bin/python3

import block

'''
    The opponent can be moved and reset.
    It is constrained by the borders.
'''


class Opponent(block.Block):
    def __init__(self, path, pos_x, pos_y, speed_x, speed_y):
        super().__init__(path, pos_x, pos_y)
        # Fixed speed of the opponent
        self.speed_x = speed_x
        self.speed_y = speed_y
        # Current speed of the opponent
        self.movement_x = 0
        self.movement_y = 0
        # Initial position of the opponent
        self.initial_x = pos_x
        self.initial_y = pos_y

    def update(self, screen_height, screen_width, ball_group):
        # Update current position of the opponent while checking for constraints
        if self.rect.top >= ball_group.sprite.rect.bottom:
            if self.rect.top > ball_group.sprite.rect.bottom:
                self.movement_y = self.speed_y
                self.rect.y -= self.movement_y
            else:
                if ball_group.sprite.rect.y > screen_height / 2:
                   self.rect.y -= self.movement_y 
        if self.rect.bottom <= ball_group.sprite.rect.top:
            if self.rect.bottom < ball_group.sprite.rect.top:
                self.movement_y = self.speed_y
                self.rect.y += self.movement_y
            else:
                if ball_group.sprite.rect.y < screen_height / 2:
                   self.rect.y += self.movement_y 
        if self.rect.right <= ball_group.sprite.rect.left:
            if self.rect.right < ball_group.sprite.rect.left:
                self.movement_x = self.speed_x
                self.rect.x += self.movement_x
            else:
                if ball_group.sprite.rect.right < screen_width - ball_group.sprite.rect.width:
                    self.movement_x = self.speed_x
                    self.rect.x += self.movement_x
        if self.rect.left > ball_group.sprite.rect.right:
            self.movement_x = self.speed_x
            self.rect.x -= self.movement_x
        self.screen_constraint(screen_height, screen_width)

    def screen_constraint(self, screen_height, screen_width):
        # Constrain opponent movement to within boundaries
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
