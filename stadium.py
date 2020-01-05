import typer
import pygame
import math
from pygame.locals import *


class Stadium:
    def __init__(self, left, top, width, height, text):
        self.rectangle = pygame.Rect(left, top, width, height)
        self.left_circle = pygame.Rect(left - height / 2, top, height, height)
        self.right_circle = pygame.Rect(left + width - height / 2, top, height, height)
        self.text = text
        self.colour = (18, 18, 18)

    def drawer(self, screen):
        pygame.draw.rect(screen, self.colour, self.rectangle)
        pygame.draw.ellipse(screen, self.colour, self.left_circle)
        pygame.draw.ellipse(screen, self.colour, self.right_circle)
        typer.menu_options(screen, (self.rectangle.centerx, self.rectangle.centery), self.text)
        pygame.display.update()
        print('ok')

    def check_collision(self, mouse_position):
        if self.rectangle.collidepoint(mouse_position):
            return True
        elif circle_collidepoint(self.left_circle, mouse_position):
            return True
        elif circle_collidepoint(self.right_circle, mouse_position):
            return True
        else:
            return False

    def change_text(self, text):
        self.text = text

def circle_collidepoint(circle, mouse_position):  # improve this function
    distance = math.sqrt(
        math.pow(circle.centerx - mouse_position[0], 2) + math.pow(circle.centery - mouse_position[1], 2))
    if distance < circle.width / 2:
        return True
    else:
        return False
