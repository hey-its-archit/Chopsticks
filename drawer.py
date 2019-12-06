import pygame
import numpy
# from pygame.locals import *
import colours
import time
import fingers
import rotator
import typer

pygame.init()

font_size = 32
offset = 0
clock = pygame.time.Clock()


def runner(points, player, screen, screen_size):
    draw_points(points, not player, screen, screen_size)
    pygame.image.save(screen, 'screenshots/screenshot.png')
    screenshot = pygame.image.load('screenshots/screenshot.png')
    rotator.rotate(screenshot, screen)
    draw_points(points, player, screen, screen_size)
    typer.turn(player, screen, screen_size)


def draw_points(points, player, screen, screen_size):
    global clock
    screen.fill(colours.BACKGROUND)
    font = pygame.font.SysFont('comicsansms', 32)
    offset_x = -75
    offset_y = -75
    images = []

    # text_top_left = font.render(str(points[not player][1]), False, colours.RED)
    # text_top_right = font.render(str(points[not player][0]), False, colours.RED)
    # text_bot_left = font.render(str(points[player][0]), False, colours.RED)
    # text_bot_right = font.render(str(points[player][1]), False, colours.RED)

    # image_top_left=pygame.transform.flip(fingers.fingers[points[not player][1]],True,True)
    # image_top_right=pygame.transform.flip(fingers.fingers[points[not player][0]],False,True)
    # image_bot_left=pygame.transform.flip(fingers.fingers[points[player][0]],True,False)
    # image_bot_right=pygame.transform.flip(fingers.fingers[points[player][1]],False,False)
    images.append(pygame.transform.flip(fingers.fingers[points[not player][1]], True, True))
    images.append(pygame.transform.flip(fingers.fingers[points[not player][0]], False, True))
    images.append(pygame.transform.flip(fingers.fingers[points[player][0]], True, False))
    images.append(pygame.transform.flip(fingers.fingers[points[player][1]], False, False))

    rectangles = []
    for i in range(0, 4):
        rectangles.append(images[i].get_rect().center)

    screen.blit(images[0], numpy.subtract((screen_size[0] / 4, screen_size[1] / 4), rectangles[0]))
    screen.blit(images[1], numpy.subtract((3 * screen_size[0] / 4, screen_size[1] / 4), rectangles[1]))
    screen.blit(images[2], numpy.subtract((screen_size[0] / 4, 3 * screen_size[1] / 4), rectangles[2]))
    screen.blit(images[3], numpy.subtract((3 * screen_size[0] / 4, 3 * screen_size[1] / 4), rectangles[3]))
    pygame.display.flip()

    clock.tick(60)


def draw_amounts(amounts, screen, screen_size):
    global font_size
    global offset
    global clock
    print('in d_A')
    number = len(amounts)
    font_size = 32
    offset = number * font_size / 2
    font = pygame.font.SysFont('comicsansms', 32)
    for i in range(0, number):
        text = font.render(str(amounts[i]), False, colours.RED)
        screen.blit(text, (screen_size[0] / 4 - offset + (i * font_size), screen_size[1] / 2))
    pygame.display.flip()

    clock.tick(60)


def highlight(hand_from, screen, screen_size):
    vertical_offset = 50
    rect_size = (screen_size[0] / 2, screen_size[1] / 2 - vertical_offset)

    if hand_from == 0:
        rect_info = [0, screen_size[1] / 2 + vertical_offset]
        rect_info.extend(rect_size)
        pygame.draw.rect(screen, colours.WHITE, rect_info, 2)
    else:
        rect_info = [screen_size[0] / 2, screen_size[1] / 2 + vertical_offset]
        rect_info.extend(rect_size)
        pygame.draw.rect(screen, colours.WHITE, rect_info, 2)
    pygame.display.flip()
