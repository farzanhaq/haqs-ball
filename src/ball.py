#!/usr/local/bin/python3

import pygame
import block

'''
    The ball can be moved, reset, collided with, shot and scored.
    It is constrained by the borders.
'''


class Ball(block.Block):
    def __init__(self, path, pos_x, pos_y, speed_x, speed_y, players):
        super().__init__(path, pos_x, pos_y)
        # Fixed speed of the ball
        self.speed_x = speed_x
        self.speed_y = speed_y
        # Speed of the ball when shot
        self.movement_x = 0
        self.movement_y = 0
        # Group of players
        self.players = players
        # The collision with walls status
        self.is_collided_with_wall_x = False
        self.is_collided_with_wall_y = False
        # The shot trigger status
        self.is_shot = False
        # The shot progress status
        self.is_animating_shot = False
        # The ball active status
        self.active = False
        # The shot trigger time
        self.shot_time = 0
        # The score time
        self.score_time = 0

    def update(self, screen, screen_height, screen_width, basic_font, accent_color, shot_sound):
        if self.active:
            # Update current position of the ball while checking constraints and status
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions(screen_height, screen_width, shot_sound)
            if not self.is_collided_with_player and not self.is_animating_shot:
                # Halt the ball when there is no shot animation or collision occuring
                self.speed_x = 0
                self.speed_y = 0
                # Set the shot status to False
                self.is_shot = False
            elif self.is_animating_shot:
                # Perform the shot animation when it is set to True
                self.shot_animation(self.movement_x, self.movement_y,
                                    self.is_collided_with_wall_x, self.is_collided_with_wall_y)
        else:
            # Trigger countdown until ball status is active
            self.reset_counter(screen, screen_height, screen_width, basic_font, accent_color)

    def collisions(self, screen_height, screen_width, shot_sound):
        # Constrain player movement to within boundaries and set corresponding collision value to True
        if self.rect.top <= self.rect.height:
            self.rect.top = self.rect.height
            self.is_collided_with_wall_y = True
        if self.rect.bottom >= screen_height - self.rect.height:
            self.rect.bottom = screen_height - self.rect.height
            self.is_collided_with_wall_y = True
        if self.rect.left <= self.rect.width:
            self.rect.left = self.rect.width
            self.is_collided_with_wall_x = True
        if self.rect.right >= screen_width - self.rect.width:
            self.rect.right = screen_width - self.rect.width
            self.is_collided_with_wall_x = True

        if pygame.sprite.spritecollide(self, self.players, False):
            # When the ball collides with a player, store the player it collided with
            self.collision_player = pygame.sprite.spritecollide(self, self.players, False)[0]
            # Store the speed of the player at the time of the collision
            self.movement_x = self.collision_player.movement_x
            self.movement_y = self.collision_player.movement_y
            # Set the collision status to True
            self.is_collided_with_player = True

            # Check if the left of the player collides with the right of the ball
            if abs(self.rect.right - self.collision_player.rect.left) < 10:
                # Check if player has triggered the shot
                if self.is_shot:
                    # Play the shot sound and trigger the animation
                    self.shot_animation_with_sound(shot_sound)
                else:
                    # Move the ball in the same direction as the player
                    self.speed_x = self.movement_x
                    self.speed_y = self.movement_y
                    self.rect.right = self.collision_player.rect.left
            # Check if the right of the player collides with the left of the ball, and perform the same logic as above
            if abs(self.rect.left - self.collision_player.rect.right) < 10:
                if self.is_shot:
                    self.shot_animation_with_sound(shot_sound)
                else:
                    self.speed_x = self.movement_x
                    self.speed_y = self.movement_y
                    self.rect.left = self.collision_player.rect.right
            # Check if the bottom of the player collides with the top of the ball, and perform the same logic as above
            if abs(self.rect.top - self.collision_player.rect.bottom) < 10:
                if self.is_shot:
                    self.shot_animation_with_sound(shot_sound)
                else:
                    self.speed_x = self.movement_x
                    self.speed_y = self.movement_y
                    self.rect.top = self.collision_player.rect.bottom
            # Check if the top of the player collides with the bottom of the ball, and perform the same logic as above
            if abs(self.rect.bottom - self.collision_player.rect.top) < 10:
                if self.is_shot:
                    self.shot_animation_with_sound(shot_sound)
                else:
                    self.speed_x = self.movement_x
                    self.speed_y = self.movement_y
                    self.rect.bottom = self.collision_player.rect.top
        else:
            # Set the collision status to False
            self.is_collided_with_player = False

    def shot_animation_with_sound(self, shot_sound):
        pygame.mixer.Sound.play(shot_sound)
        self.shot_animation(self.collision_player.movement_x, self.collision_player.movement_y,
                            self.is_collided_with_wall_x, self.is_collided_with_wall_y)

    def shot_animation(self, movement_x, movement_y, is_collided_with_wall_x, is_collided_with_wall_y):
        # Set shot animation status to True
        self.is_animating_shot = True
        # Retrieve the current time this function was executed
        current_time = pygame.time.get_ticks()

        # Reverse the speed of the ball if collided with a boundary
        if is_collided_with_wall_x:
            movement_x *= -1
        if is_collided_with_wall_y:
            movement_y *= -1

        # Simulate a timer by taking the difference between shot time and current time, and update ball speed accordingly
        if current_time - self.shot_time <= 200:
            self.speed_x = movement_x * 2
            self.speed_y = movement_y * 2
        if 200 < current_time - self.shot_time <= 400:
            self.speed_x = movement_x * 1.5
            self.speed_y = movement_y * 1.5
        if 400 < current_time - self.shot_time <= 600:
            self.speed_x = movement_x * 1
            self.speed_y = movement_y * 1
        if current_time - self.shot_time >= 600:
            self.speed_x = 0
            self.speed_y = 0
            # Set the animation and boundary collision status to false after the animation is complete
            self.is_animating_shot = False
            self.is_collided_with_wall_x = False
            self.is_collided_with_wall_y = False

    def reset_ball(self, screen_height, screen_width):
        # Store the time a goal was scored
        self.score_time = pygame.time.get_ticks()
        # Teleport ball to starting position
        self.rect.center = (screen_width / 2, screen_height / 2)
        # Halt the ball
        self.speed_x = 0
        self.speed_y = 0
        # Set the ball active status to False
        self.active = False

    def reset_counter(self, screen, screen_height, screen_width, basic_font, accent_color):
        # Retrieve the current time this function was executed
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        # Simulate a timer by taking the difference between score time and current time, and update the countdown accordingly
        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time > 2100:
            # Set the ball active status to True after countdown is complete
            self.active = True

        # Return a text based surface with the time counter
        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        # Get the rectangular area of the time counter surface
        time_counter_rect = time_counter.get_rect(center=(screen_width/2, screen_height/2 + 50))
        # Draw the time counter surface onto the time counter rectangle surface and display it on the screen
        screen.blit(time_counter, time_counter_rect)
