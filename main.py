import colours
import logic
import pygame_textinput
import copy
import time
import fingers
import pygame
from pygame.locals import *


class Board:
    def __init__(self, window=None):
        self.value = [[1, 1],
                      [1, 1]]
        self.rotate = False  # add here
        self.window = window

    def print_board(self):
        print(self.value[0])
        print(self.value[1])

    def rotate_board(self):
        if self.rotate:
            self.value[0][0], self.value[1][1] = self.value[1][1], self.value[0][0]
            self.value[0][1], self.value[1][0] = self.value[1][0], self.value[0][1]

    def game_over(self):
        if self.value[0] == [0, 0]:
            return True, 0
        elif self.value[1] == [0, 0]:
            return True, 1
        else:
            return False, None

    def empty_hand(self, hand):
        if self.value_in(hand) == 0:
            return True
        else:
            return False

    def value_in(self, hand):
        return self.value[hand[0]][hand[1]]

    @staticmethod
    def set_value_in_to(board, hand, value):
        board.value[hand[0]][hand[1]] = value


class Players:

    def __init__(self):
        self.names = []
        self.current = 0

    # def accept_name(self, number):
    #     print('Please Enter Player ' + str(number) + '\'s name')
    #     self.name = input()

    def switch_player(self):
        self.current = int(not self.current)


# Maybe change how it assigns
class Move:
    def __init__(self, hand_from, hand_to, value):
        self.hand_from = hand_from
        self.hand_to = hand_to
        self.value = value

    def print_move(self):
        print('Hand from:' + str(self.hand_from))
        print('Hand to:' + str(self.hand_to))
        print('Value:' + str(self.value))

    def make_move(self, board):
        if self.hand_from[0] == self.hand_to[0]:
            # print('entered switch')
            if self.value == -1:  # if real player
                # options = self.get_switch_options(board)
                # board.window.draw_amounts(options)
                # print('Choose from these:' + str(options))
                # self.value = int(input())
                # self.value=board.window.get_move(options)
                self.switch(board)
            else:
                self.switch(board)
        else:
            self.value = board.value_in(self.hand_from)
            self.give(board)
        # board.rotate_board()
        # board.print_board()

    def switch(self, board):
        value_in_hand_to = board.value_in(self.hand_to)
        value_in_hand_from = board.value_in(self.hand_from)
        value_in_hand_to += self.value
        value_in_hand_from -= self.value
        value_in_hand_to %= 5
        board.set_value_in_to(board, self.hand_to, value_in_hand_to)
        board.set_value_in_to(board, self.hand_from, value_in_hand_from)

    def give(self, board):
        value_in_hand_to = board.value_in(self.hand_to)
        value_in_hand_from = board.value_in(self.hand_from)

        value_in_hand_to += value_in_hand_from
        value_in_hand_to %= 5

        board.set_value_in_to(board, self.hand_to, value_in_hand_to)

    def get_switch_options(self, board):
        import copy

        value_in_hand_to = board.value_in(self.hand_to)
        value_in_hand_from = board.value_in(self.hand_from)

        options = list(range(1, value_in_hand_from + 1))
        options_copy = copy.deepcopy(options)
        for x in options_copy:
            if x + value_in_hand_to >= 5:
                options.remove(x)
        if value_in_hand_from > value_in_hand_to:
            options.remove(value_in_hand_from - value_in_hand_to)

        return options

    def is_valid(self, click, board, window):

        if click == 1:
            if board.empty_hand(self.hand_from):
                window.type('This hand has zero points')
                return False
            if self.is_upper_half():
                window.type('Try again on the lower half of the screen')
                return False

        elif click == 2:
            if self.hand_to[0] != self.hand_from[0]:
                if board.empty_hand(self.hand_to):
                    window.type('This hand has zero points')
                    return False
            else:
                if self.is_same():
                    window.type('Cannot add to the same hand')
                    return False
                if len(self.options) == 0:
                    window.type('Switches not possible at all')
                    return False

        return True  # if no returns happen, it is good

    def is_same(self):
        if self.hand_to == self.hand_from:
            return True
        else:
            return False

    def is_upper_half(self):
        if self.hand_from[0] == 0:
            return True
        else:
            return False


class Window:
    def __init__(self, size, caption):
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.caption = pygame.display.set_caption(caption)
        self.center = (self.size[0] / 2, self.size[1] / 2)
        self.clock = pygame.time.Clock()
        self.font_size = 48
        self.font = pygame.font.SysFont('timesnewroman', self.font_size)

    def runner(self, board, players):  # remove later
        # player_names = ['Archit', 'AI']  # IMPORTANT REMOVE LATER
        players.switch_player()
        if board.rotate:
            board.rotate_board()
            pygame.image.save(self.screen, 'screenshots/screenshot.png')
            screenshot = pygame.image.load('screenshots/screenshot.png')
            self.rotate(screenshot)
        self.draw_points(board)
        self.type(players.names[players.current] + '\'s turn ')
        # pygame.time.wait(700)
        # self.clock.tick(5000)

    def type(self, sentence, offset=(0, 0)):
        import numpy

        text = self.font.render(sentence, False, colours.RED)
        text_center = text.get_rect().center
        text_size = text.get_rect().size
        drawing_location = numpy.subtract(self.center, text_center)
        drawing_location = numpy.subtract(drawing_location, offset)
        rect_info = drawing_location.tolist()
        rect_info[0] = 0  # bad stuff done so that rect starts at left of screen
        rect_info.append(self.size[0])
        rect_info.append(text_size[1])
        pygame.draw.rect(self.screen, colours.BACKGROUND, rect_info, 0)
        self.screen.blit(text, drawing_location)
        pygame.display.flip()
        return text_center

    def draw_points(self, board):
        import numpy

        self.screen.fill(colours.BACKGROUND)

        images = [[None, None], [None, None]]
        rectangles = [[None, None], [None, None]]
        fourth = [self.size[0] / 4, self.size[1] / 4]
        for i in range(0, 2):
            for j in range(0, 2):
                images[i][j] = pygame.transform.flip(fingers.fingers[board.value_in([i, j])], not j, not i)
                rectangles[i][j] = images[i][j].get_rect().center
                self.screen.blit(images[i][j],
                                 numpy.subtract(((2 * j + 1) * fourth[0], (2 * i + 1) * fourth[1]), rectangles[i][j]))
        pygame.display.flip()

        self.clock.tick(60)

    def rotate(self, screenshot):
        steps = 60
        time_to_rotate = 0
        rotation_angle = 180

        screen_rect = self.screen.get_rect()
        # rotated = screenshot.copy()
        rotated_rect = screenshot.get_rect(center=screen_rect.center)

        for i in range(0, steps):
            self.screen.fill(colours.BACKGROUND)
            rotated = pygame.transform.rotate(screenshot, rotation_angle / steps * i)
            rotated_rect = rotated.get_rect(center=rotated_rect.center)

            self.screen.blit(rotated, rotated_rect)
            pygame.display.flip()
            time.sleep(time_to_rotate / steps)

    def draw_amounts(self, amounts):

        print('in d_A')
        number = len(amounts)
        # font_size = 32  #  backup
        offset = number * self.font_size / 2

        for i in range(0, number):
            text = self.font.render(str(amounts[i]), False, colours.RED)
            self.screen.blit(text, (self.size[0] / 4 - offset + (i * self.font_size), self.size[1] / 2))
        pygame.display.flip()

        self.clock.tick(60)

    def highlight(self, hand_from):
        vertical_offset = 50
        rect_size = (self.size[0] / 2, self.size[1] / 2 - vertical_offset)

        if hand_from[1] == 0:
            rect_info = [0, self.size[1] / 2 + vertical_offset]
            rect_info.extend(rect_size)
            pygame.draw.rect(self.screen, colours.WHITE, rect_info, 2)
        else:
            rect_info = [self.size[0] / 2, self.size[1] / 2 + vertical_offset]
            rect_info.extend(rect_size)
            pygame.draw.rect(self.screen, colours.WHITE, rect_info, 2)
        pygame.display.flip()

    def get_switch_move(self, options):
        mouse_position = pygame.mouse.get_pos()
        offset = 0
        amount_clicked_index = int(
            (mouse_position[0] - (self.size[0] / 4 - offset)) / self.font_size)
        if 0 <= amount_clicked_index <= len(options) - 1:
            return options[amount_clicked_index]

    # def get_name(self):
    #
    #     text_input = pygame_textinput.TextInput()
    #     text_input.text_color = colours.WHITE
    #     text_input.cursor_color = colours.WHITE
    #
    #
    #
    #     self.screen.fill(colours.BACKGROUND)
    #     # text_enter_name = font.render('Enter name of player No.' + str(counter + 1), False, colours.RED)
    #     text_center = self.type('Enter name of player No.',(0,50))
    #     # aligned = numpy.subtract(window.center, text_center)
    #     # window.screen.blit(text_enter_name, (aligned[0], aligned[1] - 50))
    #     pygame.display.flip()
    #
    #     self.screen.blit(text_input.get_surface(), self.center)
    #     pygame.display.update()
    #     self.clock.tick(60)
    #     if text_input.update(events):
    #         counter = counter + 1
    #
    #         player_names.append(text_input.get_text())
    #         text_input.input_string = ''
    #
    #         if counter == 2:
    #             state = "INGAME"
    #             typer.set_player_names(player_names)
    #             drawer.draw_points(logic.points, player, window.screen, window.size)
    #             typer.turn(player, window.screen, window.size)


def list_moves(board, player):
    player = int(not player)  # inverting board, remove later
    moves = []
    for select_hand_from in range(0, 2):
        hand_from = [int(player), select_hand_from]
        # listing gives
        if not board.empty_hand(hand_from):
            for select_hand_to in range(0, 2):
                hand_to = [int(not player), select_hand_to]
                if not board.empty_hand(hand_to):  # removing empty hand to's
                    move = Move(hand_from, hand_to, board.value_in(hand_from))
                    moves.append(move)

        # listing switches
        hand_to = [int(player), int(not select_hand_from)]
        temp_move = Move(hand_from, hand_to, None)
        options = temp_move.get_switch_options(board)
        for option in options:
            move = Move(hand_from, hand_to, option)
            moves.append(move)
    return moves


def accept_input():
    input_str = input()
    list_formed = list(map(int, input_str.split(' ')))
    return list_formed


def minimax(board, depth, maximizingplayer):
    import math
    import copy

    game_over, player = board.game_over()

    if game_over:
        if maximizingplayer:
            return -1, None
        else:
            return 1, None
    if depth == 0:
        return 0, None
    temp_board = Board()
    if maximizingplayer:

        max_value = -math.inf
        moves = list_moves(board, maximizingplayer)
        for move in moves:
            temp_board.value = copy.deepcopy(board.value)
            move.make_move(temp_board)
            # temp_board.rotate_board()
            minimax_value, minimax_result = minimax(temp_board, depth - 1, not maximizingplayer)
            if minimax_value > max_value:
                max_value = minimax_value
                best_move = move

        return max_value, best_move
    else:
        min_value = math.inf
        moves = list_moves(board, maximizingplayer)
        for move in moves:
            temp_board.value = copy.deepcopy(board.value)

            move.make_move(temp_board)
            # temp_board.rotate_board()
            minimax_value, minimax_result = minimax(temp_board, depth - 1, not maximizingplayer)
            if minimax_value < min_value:
                min_value = minimax_value
                best_move = move

        return min_value, best_move


def testing_print(depth):
    for i in range(depth, 5):
        print(' ', end=' ')


# def main():
#     board = Board()
#     players = [Player(1), Player(2)]
#     player = players[PLAYER_1].index
#     board.print_board()
#     AI_ON = True
#     while not board.game_over()[0]:
#         if AI_ON and player == PLAYER_2:
#             print('AI\'s turn')
#             selected_move = minimax(board, 7, player)[1]
#             selected_move.print_move()
#             selected_move.make_move(board)
#         else:
#             move = Move(None, None, None)
#             print(players[player].name + '\'s turn')
#             print('Select hand to take from')
#             move.hand_from = accept_input()
#             print('Select hand to give to')
#             move.hand_to = accept_input()
#             move.value = -1
#             move.make_move(board)
#
#         board.print_board()
#         if board.game_over()[0]:
#             print(players[player].name + ' wins!!')
#             break
#
#         player = int(not player)


def main():
    pygame.init()

    # 0 is left and 1 is right

    text_input = pygame_textinput.TextInput()
    text_input.text_color = colours.WHITE
    text_input.cursor_color = colours.WHITE
    players = Players()

    window = Window((800, 800), 'Chopsticks')
    board = Board(window)
    ai_on = True

    stop = False
    clock = pygame.time.Clock()
    background = colours.BACKGROUND
    window.screen.fill(background)
    click = undo_click = 1
    undo_points = copy.deepcopy(logic.points)
    select_amount = False
    state = "MAIN MENU"
    # player_names = ['ABC', 'AI']
    counter = 0
    move = Move(None, None, None)
    while not stop:
        if ai_on and players.current == PLAYER_2:
            pygame.time.wait(700)
            selected_move = minimax(board, 7, players.current)[1]
            selected_move.print_move()
            selected_move.make_move(board)
            window.draw_points(board)
            board.rotate_board()

            window.runner(board, players)
            if board.game_over()[0]:
                window.type(players.names[board.game_over()[1]] + ' win\'s')
                state = "GAME OVER"

        events = pygame.event.get()
        if state == "MAIN MENU":

            window.screen.fill(background)
            window.type('Enter name of player No.' + str(counter + 1), (0, 50))
            pygame.display.flip()
            window.screen.blit(text_input.get_surface(), (400, 400))
            pygame.display.update()
            clock.tick(60)
            if text_input.update(events):
                counter = counter + 1
                players.names.append(text_input.get_text())
                text_input.input_string = ''
                if counter == 2:
                    state = "INGAME"
                    window.draw_points(board)
                    window.type(players.names[players.current] + '\'s turn ')
                elif ai_on:
                    players.names.append('Computer')
                    state = "INGAME"
                    window.draw_points(board)
                    window.type(players.names[players.current] + '\'s turn ')
        left_click = 1
        right_click = 3

        for event in events:

            if state == "GAME OVER":
                print("GAME OVER")
                state = ""

            if event.type == pygame.QUIT:
                print(event)
                stop = True

            elif state == "INGAME":
                if event.type == pygame.QUIT:
                    print(event)
                    stop = True
                elif event.type == MOUSEBUTTONDOWN:

                    if event.button == left_click:
                        window.draw_points(board)
                        mouse_position = pygame.mouse.get_pos()
                        # rows first columns next
                        mouse_quadrant = (
                            (2 * mouse_position[1] / window.size[1]), (2 * mouse_position[0] / window.size[0]),)
                        # undo_click = click
                        # undo_player = player
                        # undo_points = copy.deepcopy(logic.points)
                        # undo_hand_to = hand_to
                        # undo_hand_from = hand_from
                        print('og')
                        print(undo_points)
                        # print(player, click)

                        if select_amount:

                            move.value = board.window.get_switch_move(move.options)
                            move.make_move(board)  # make a function for this ??!!??
                            window.draw_points(board)
                            # board.rotate_board()
                            click = 1
                            # player = (player + 1) % 2
                            select_amount = False
                            window.runner(board, players)
                        else:
                            if click == 1:
                                move = Move(None, None, None)
                                move.hand_from = [int(_) for _ in mouse_quadrant]
                                if move.is_valid(click, board, window):
                                    window.highlight(move.hand_from)
                                    click = 2

                            elif click == 2:
                                window.highlight(move.hand_from)
                                move.hand_to = [int(_) for _ in mouse_quadrant]
                                if move.hand_to[0] == move.hand_from[0]:  # make work with rotate off
                                    move.options = move.get_switch_options(board)
                                    if move.is_valid(click, board, window):
                                        board.window.draw_amounts(move.options)
                                        select_amount = True

                                else:
                                    if move.is_valid(click, board, window):
                                        move.make_move(board)  # make a function for this ??!!??
                                        window.draw_points(board)
                                        # board.rotate_board()
                                        if board.game_over()[0]:
                                            window.type(players.names[board.game_over()[1]] + ' win\'s')
                                            state = 'GAME OVER'
                                            continue

                                        click = 1
                                        # player = (player + 1) % 2

                                        window.runner(board, players)

                                    # else:  # fix this later
                                    #     window.highlight(move.hand_from)
                    elif event.button == right_click:
                        pass
                        # print('undo')
                        # print(undo_points)
                        # print(logic.points)
                        #
                        # click = undo_click
                        # player = undo_player
                        # logic.points = copy.deepcopy(undo_points)
                        # hand_to = undo_hand_to
                        # hand_from = undo_hand_from
                        # if click == 2:
                        #     # drawer.runner(logic.points, player, window.screen, window.size)
                        #     window.runner(board, player)


PLAYER_1 = 0
PLAYER_2 = 1
if __name__ == '__main__':
    main()
