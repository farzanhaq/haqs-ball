#!/usr/local/bin/python3

import pygame

'''
    Takes a surface and puts a rectangle around it.
    This class is not drawn on the screen, but other classes inherit it.
'''


class Block(pygame.sprite.Sprite):
    def __init__(self, path, pos_x, pos_y):
        super().__init__()
        # Load the image onto a surface
        self.image = pygame.image.load(path)
        # Get the rectangular area of the image surface
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
