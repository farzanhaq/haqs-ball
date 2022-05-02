#!/usr/local/bin/python3

import pygame
import sys
import os
import gamemanager
import player
import opponent
import ball

'''
    General setup of the game
    Initializes the game and interprets user input
'''


class Haqsball:
    def main(self):
        # Reduce the buffer size to minimize sound delay
        pygame.mixer.pre_init(44100, -16, 2, 512)
        # Initialize PyGame modules and clock
        pygame.init()
        clock = pygame.time.Clock()

        # Window dimensions
        screen_width = 720
        screen_height = 457
        # Create a single display surface object of specified dimensions
        screen = pygame.display.set_mode((screen_width, screen_height))
        # Load the background image onto a regular surface
        background = pygame.image.load(os.path.join(os.path.dirname(__file__), "../assets/img/field.png"))
        # Provide a title
        pygame.display.set_caption("Haqsball")

        # Select font and color
        accent_color = (27, 35, 43)
        basic_font = pygame.font.Font('freesansbold.ttf', 24)
        # Load the shot sound
        shot_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "../assets/sound/shot.ogg"))
        # Load the score sound
        score_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "../assets/sound/score.ogg"))

        # Instantiate the player objects
        my_player = player.Player(os.path.join(os.path.dirname(__file__), "../assets/img/blue-ball.png"), \
            screen_width - 20, screen_height / 2, 3, 3)
        my_opponent = opponent.Opponent(os.path.join(os.path.dirname(__file__), "../assets/img/red-ball.png"), \
            20, screen_height / 2, 3, 3)
        # Create a group for the players and add the players to it
        player_group = pygame.sprite.Group()
        player_group.add(my_player, my_opponent)

        # Instantiate the ball object
        game_ball = ball.Ball(os.path.join(os.path.dirname(__file__), "../assets/img/grey-ball.png"), \
            screen_width / 2, screen_height / 2, 0, 0, player_group)
        # Create a group for the ball and add the ball to it
        ball_sprite = pygame.sprite.GroupSingle()
        ball_sprite.add(game_ball)

        # Instantiate the game manager object
        game_manager = gamemanager.GameManager(player_group, ball_sprite)  # Create the game manager

        while True:
            # Iterate through list of all user interactions
            for event in pygame.event.get():
                # Check if user exits the window
                if event.type == pygame.QUIT:
                    # Uninitialize the PyGame modules
                    pygame.quit()
                    # Exit the entire program
                    sys.exit()
                # Check if any key is pressed (note: if held down, no new event will be triggered)
                if event.type == pygame.KEYDOWN:
                    # Check if specified keys are pressed by player one
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT]:
                        if event.key == pygame.K_UP:
                            # Decrease vertical movement
                            my_player.movement_y -= my_player.speed_y
                        if event.key == pygame.K_DOWN:
                            # Increase vertical movement
                            my_player.movement_y += my_player.speed_y
                        if event.key == pygame.K_LEFT:
                            # Decrease horizontal movement
                            my_player.movement_x -= my_player.speed_x
                        if event.key == pygame.K_RIGHT:
                            # Increase horizontal movement
                            my_player.movement_x += my_player.speed_x
                        if event.key == pygame.K_RSHIFT:
                            # Set shot status to True
                            game_ball.is_shot = True
                            # Store shot time
                            game_ball.shot_time = pygame.time.get_ticks()
                # Check if any key is released (note: if untouched, no new event will be triggered)
                if event.type == pygame.KEYUP:
                    # Check if specified keys are released by player one
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT]:
                        if event.key == pygame.K_UP:
                            # Increase vertical movement
                            my_player.movement_y += my_player.speed_y
                        if event.key == pygame.K_DOWN:
                            # Decrease vertical movement
                            my_player.movement_y -= my_player.speed_y
                        if event.key == pygame.K_LEFT:
                            # Increase horizontal movement
                            my_player.movement_x += my_player.speed_x
                        if event.key == pygame.K_RIGHT:
                            # Decrease horizontal movement
                            my_player.movement_x -= my_player.speed_x
                        if event.key == pygame.K_RSHIFT:
                            # Set shot status to False
                            game_ball.is_shot = False

            # Draw the background surface at the center coordinates and display it on the screen
            screen.blit(background, (0, 0))
            # Run the game (note: successive elements in the loop are drawn on top of each other)
            game_manager.run_game(screen, screen_height, screen_width,
                                  basic_font, accent_color, score_sound, shot_sound)
            # Render a drawing of everything before this point in the loop
            pygame.display.flip()
            # Limit how fast the loop can run to 60 FPS
            clock.tick(60)


if __name__ == "__main__":
    hb = Haqsball()
    hb.main()
