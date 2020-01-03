import pygame
from pygame.locals import *
class Stadium:
    def __init__(self, left, top, width, height):
        self.rectangle = pygame.Rect(left, top, width, height)
        self.left_circle = pygame.Rect(left - height / 2, top, height, height)
        self.right_circle = pygame.Rect(left + width - height / 2, top, height, height)
