import colours
import pygame
import numpy
import os

pygame.init()
player_names = ["Archit", "Ashwini"]
print(os.getcwd())
font = pygame.font.Font('fonts\\roboto\\RobotoCondensed-Bold.ttf', 42)


def set_player_names(input_names):
    global player_names
    player_names = input_names


def turn(player, screen, screen_size):
    center = (screen_size[0] / 2, screen_size[1] / 2)
    print(center)
    global font
    text = font.render(player_names[player] + "'s turn", False, colours.RED)
    text_center = text.get_rect().center

    screen.blit(text, numpy.subtract(center, text_center))
    pygame.display.flip()
    print("font rendering")


def game_over(player, screen, screen_size):
    center = (screen_size[0] / 2, screen_size[1] / 2)

    global font
    text = font.render(player_names[player] + " wins", False, colours.RED)
    text_center = text.get_rect().center
    text_size = text.get_rect().size

    drawing_location = numpy.subtract(center, text_center)
    rect_info = drawing_location.tolist()
    # rect_info.append(text_size[0])
    rect_info[0] = 0  # bad stuff done so that rect starts at left of screen
    rect_info.append(screen_size[0])
    rect_info.append(text_size[1])
    print(text_size)
    print(drawing_location)
    print(rect_info)

    pygame.draw.rect(screen, colours.BACKGROUND, rect_info, 0)
    # screen.blit(text_background,drawing_location)
    screen.blit(text, drawing_location)
    pygame.display.flip()


def error_cant_suicide(screen, screen_size):
    global font
    center = (screen_size[0] / 2, screen_size[1] / 2)
    text = font.render("No suicides allowed! :)", False, colours.RED)
    text_center = text.get_rect().center
    drawing_location = numpy.subtract(center, text_center)
    screen.blit(text, drawing_location)
    pygame.display.flip()


def error_try_lower_half(screen, screen_size):
    global font
    center = (screen_size[0] / 2, screen_size[1] / 2)
    text = font.render("Try again on the lower half of the screen", False, colours.RED)
    text_center = text.get_rect().center
    drawing_location = numpy.subtract(center, text_center)
    screen.blit(text, drawing_location)
    pygame.display.flip()


def error_same_hand_add(screen, screen_size):
    global font
    center = (screen_size[0] / 2, screen_size[1] / 2)
    text = font.render("Cannot add to the same hand", False, colours.RED)
    text_center = text.get_rect().center
    drawing_location = numpy.subtract(center, text_center)
    screen.blit(text, drawing_location)
    pygame.display.flip()


def error_zero_points(screen, screen_size):
    global font
    center = (screen_size[0] / 2, screen_size[1] / 2)
    text = font.render("This hand has zero points", False, colours.RED)
    text_center = text.get_rect().center
    drawing_location = numpy.subtract(center, text_center)
    screen.blit(text, drawing_location)
    pygame.display.flip()


def menu_options(screen, location, text):
    global font

    text = font.render(text, False, (255, 127, 80))
    text_center = text.get_rect().center
    drawing_location = numpy.subtract(location, text_center)
    screen.blit(text, drawing_location)


def about(screen, screen_size):
    global font
    center = (screen_size[0] / 2, screen_size[1] / 2)
    screen.fill(colours.BACKGROUND)
    text = font.render('Game developed by Archit', False, (255, 127, 80))
    text_center = text.get_rect().center
    drawing_location = numpy.subtract((center[0], 400), text_center)
    screen.blit(text, drawing_location)

    text = font.render('github handle: hey-its-archit', False, (255, 127, 80))
    text_center = text.get_rect().center
    drawing_location = numpy.subtract((center[0], 450), text_center)
    screen.blit(text, drawing_location)

    text = font.render('Hand art Designed by-', False, (255, 127, 80))
    text_center = text.get_rect().center
    drawing_location = numpy.subtract((center[0], 600), text_center)
    screen.blit(text, drawing_location)

    text = font.render('macrovector_official / Freepik', False, (255, 127, 80))
    text_center = text.get_rect().center
    drawing_location = numpy.subtract((center[0], 650), text_center)
    screen.blit(text, drawing_location)

    pygame.display.flip()

