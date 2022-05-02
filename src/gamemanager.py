#!/usr/local/bin/python3

import pygame

'''
    Organizes the entire game.
    Manages the loop, score and reset.
'''


class GameManager:
    def __init__(self, players_group, ball_group):
        # The score counters
        self.player = 0
        self.opponent = 0
        # The sprite groups
        self.players_group = players_group
        self.ball_group = ball_group

    def draw_score(self, screen, screen_height, screen_width, basic_font, accent_color):
        # Return text based surfaces with the scores
        player_score = basic_font.render(str(self.player), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent), True, accent_color)
        # Get the rectangular area of the score surfaces
        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))
        # Draw the score surfaces onto the score rectangle surfaces and display it on the screen
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

    def reset(self, screen_height, screen_width, score_sound):
        # Increment player one score when a goal is scored and reset all positions
        if (self.ball_group.sprite.rect.left <= self.ball_group.sprite.rect.width) and \
            (self.ball_group.sprite.rect.top >= 141 and self.ball_group.sprite.rect.bottom <= 285):
            pygame.mixer.Sound.play(score_sound)
            self.player += 1
            self.ball_group.sprite.reset_ball(screen_height, screen_width)
            for sprite in self.players_group.sprites():
                sprite.reset_player()
        # Increment player two score when a goal is scored and reset all positions
        if (self.ball_group.sprite.rect.right >= screen_width - self.ball_group.sprite.rect.width) and \
            (self.ball_group.sprite.rect.top >= 141 and self.ball_group.sprite.rect.bottom <= 285):
            pygame.mixer.Sound.play(score_sound)
            self.opponent += 1
            self.ball_group.sprite.reset_ball(screen_height, screen_width)
            for sprite in self.players_group.sprites():
                sprite.reset_player()

    def game_over(self, screen, screen_height, screen_width, basic_font, accent_color):
        # Generate the winner message based on winning criteria
        winner = ""
        if self.player == 5:
            winner = "Player"
        elif self.opponent == 5:
            winner = "Player"

        # Return a text based surface with the winner message
        winner_message = basic_font.render(str(f"Congratulations, {winner}!"), True, accent_color)
        # Get the rectangular area of the winner message surface
        winner_text_rect = winner_message.get_rect(center=(screen_width / 2, screen_height / 2))
        # Draw the winner message surface onto the winner message rectangle surface and display it on the screen
        screen.blit(winner_message, winner_text_rect)

    def run_game(self, screen, screen_height, screen_width, basic_font, accent_color, score_sound, shot_sound):
        # Continue the game until a player scores 5 goals
        if 5 not in [self.player, self.opponent]:
            # Draw the game objects
            self.players_group.draw(screen)
            self.ball_group.draw(screen)

            # Update the game objects
            self.players_group.update(screen_height, screen_width, self.ball_group)
            self.ball_group.update(screen, screen_height, screen_width, basic_font, accent_color, shot_sound)

            self.reset(screen_height, screen_width, score_sound)
            self.draw_score(screen, screen_height, screen_width, basic_font, accent_color)
        else:
            # Display the winner message
            self.game_over(screen, screen_height, screen_width, basic_font, accent_color)
