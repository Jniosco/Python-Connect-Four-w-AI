# np.zeros(x,y) creates a board for you using zeroes

import sys
import numpy as np
import pygame
import math

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ROW_COUNT = 0
COLUMN_COUNT = 0

while ROW_COUNT * COLUMN_COUNT < 16:
    while ROW_COUNT < 4:
        ROW_COUNT = int(
            input("Please select the size of the rows (Must be greater or equal to 4): "))
        if ROW_COUNT < 4:
            print("Row size is too low\n")
    while COLUMN_COUNT < 4:
        COLUMN_COUNT = int(
            input("Please select the size of the columns (Must be greater or equal to 4): "))
        if COLUMN_COUNT < 4:
            print("\nColumn size is too low\n")


def create_board(x, y):
    board = np.zeros((x, y))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col, row):
    if col < COLUMN_COUNT and col >= 0:
        return (board[row - 1][col] == 0)
    return False


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if (board[r][col] == 0):
            return (r)


def print_board(board):
    print(np.flip(board, 0))


def check_win(board, last_location_row, last_location_col, piece):

    # Check column of the piece's last row location
    col = 0
    count = 0

    # print last piece drop

    print(last_location_row, last_location_col)
    # checks horizontal win
    while board[last_location_row][col] != piece and col < COLUMN_COUNT:
        col += 1
    for y in range(col, COLUMN_COUNT):
        if board[last_location_row][y] != piece:
            break
        count += 1
        if count == 4:
            return count

    # Reset count. Check row of the piece's last column location

    count = 0
    row = 0
    # checks vertical win
    while board[last_location_row - row][last_location_col] == piece and last_location_row - row >= 0:
        count += 1
        row += 1
        if count == 4:
            return count

    # Reset Count. Checking diagonal from top left to bottom right

    # note: board is flipped over horizontal due to numpy.
    # row (0) starts from bottom row and goes up
    count = 0
    col = last_location_col
    row = last_location_row

    # checks from top left to bottom right

    for c in range(col, COLUMN_COUNT):
        if board[row][c] != piece:
            break
        row += 1
        count += 1
        if row >= ROW_COUNT or row < 0:
            break

    row = last_location_row - 1

    for c in range(col - 1, -1, -1):
        if board[row][c] != piece:
            break
        row -= 1
        count += 1
        if row < 0 or row >= ROW_COUNT:
            break

    if count >= 4:
        return count

    # Reset count. Checking diagonal from bottom left to top right

    # note: board is flipped over horizontal due to numpy.

    count = 0
    col = last_location_col
    row = last_location_row

    for c in range(col, COLUMN_COUNT):
        if board[row][c] != piece:
            break
        row -= 1
        count += 1
        if row < 0 or row >= ROW_COUNT:
            break

    row = last_location_row + 1
    if row >= ROW_COUNT:
        return count
    for c in range(col - 1, -1, -1):
        if board[row][c] != piece:
            break
        row += 1
        count += 1
        if row >= ROW_COUNT or row < 0:
            break

    return count


board = create_board(ROW_COUNT, COLUMN_COUNT)
print(board, "\nYour board is {} rows by {} columns\n".format(
    ROW_COUNT, COLUMN_COUNT))

game_over = False
turn = 1

pygame.init()
SQUARE_SIZE = 100
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE/2 - 5)
screen = pygame.display.set_mode(size)


def draw_board(board):

    for c in range(COLUMN_COUNT):

        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r *
                                            SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):

        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARE_SIZE + SQUARE_SIZE/2), height - int(r*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARE_SIZE + SQUARE_SIZE/2), height - int(r*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()


draw_board(board)
pygame.display.set_caption('Connect Four')
pygame.display.update()
font_size = COLUMN_COUNT * 10
myfont = pygame.font.SysFont("monospace", font_size)
if font_size > 80:
    font_size = 80


while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn % 2 == 1:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)

            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            print(event.pos)
            # Ask for player 1 input
            if turn % 2 == 1:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))
                check = is_valid_location(board, col,   ROW_COUNT)
                if check == True and col < COLUMN_COUNT:
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    print_board(board)
                    turn += 1
                if check == False:
                    print(
                        "\nerror: This column is full. Please select another spot\n")

                if col < COLUMN_COUNT and col >= 0 and check == True:
                    if check_win(board, row, col, 1) >= 4:
                        label = myfont.render('Player 1 wins!', True, RED)
                        game_over = True
            # Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(posx//SQUARE_SIZE)
                check = is_valid_location(board, col, ROW_COUNT)
                if check == True and col < COLUMN_COUNT:
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    print_board(board)
                    turn += 1
                elif check == False:
                    print("\nerror: This column is full. Please select another spot\n")
                if col < COLUMN_COUNT and col >= 0 and check == True:
                    if check_win(board, row, col, 2) >= 4:
                        label = myfont.render('Player 2 wins!', True, YELLOW)
                        game_over = True
            draw_board(board)
        if turn > (ROW_COUNT * COLUMN_COUNT):
            print("game over: no more spaces left!")
            game_over = True
        if game_over:
            text_rect = label.get_rect()
            text_rect.center = (COLUMN_COUNT * SQUARE_SIZE//2, SQUARE_SIZE//2)
            while True:
                screen.blit(label, text_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()
