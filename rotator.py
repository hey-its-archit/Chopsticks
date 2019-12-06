import pygame
import time
import colours

# from pygame.locals import  *
pygame.init()


def rotate(screenshot, screen):
    steps = 60
    time_to_rotate = 0
    rotation_angle = 180

    screen_rect = screen.get_rect()
    #rotated = screenshot.copy()
    rotated_rect = screenshot.get_rect(center=screen_rect.center)

    for i in range(0, steps):
        screen.fill(colours.BACKGROUND)
        rotated = pygame.transform.rotate(screenshot, rotation_angle / steps * i)
        rotated_rect = rotated.get_rect(center=rotated_rect.center)

        screen.blit(rotated, rotated_rect)
        pygame.display.flip()
        time.sleep(time_to_rotate / steps)
