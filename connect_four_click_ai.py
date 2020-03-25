# np.zeros(x,y) creates a board for you using zeroes

import sys
import numpy as np
import pygame
import math
import random

# Colors used for the connect four board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Inititalize ROW_COUNT and COLUMN_COUNT as zero until porgram recieves user input
ROW_COUNT = 0
COLUMN_COUNT = 0

# determines the game mode to be played. Either  Player versus Player or Player vs AI
GAME_MODE = 0
PLAYER2 = True
AI_PLAYER = False

# AI input for level of difficulty
AI_LVL = 0
AI_LVL_DEPTH = 1

# Window length is used for the AI score_position function. This determines the range of pieces the function checks to see what pieces fill that row, column, or diagonals.
WINDOW_LENGTH = 4

# Player pieces determined by numbers to differentiate between each other. AI share's the same number as player 2 since player 2 is not in the player vs AI game mode. The empty position determines what spaces have not been filled yet
PLAYER_ONE_PIECE = 1
PLAYER_TWO_PIECE = 2
AI_PIECE = 2
EMPTY = 0

# Asking for user input on game mode

while GAME_MODE <= 0 or GAME_MODE > 2:
    x = 0
    if x == 0:
        GAME_MODE = int(input(
            "Please select game mode number:\n 1. player1 versus player2\n 2. player1 vs AI\n"))

# if game mode Player vs AI is selected, then it will ask the level of difficulty the AI should be.
    # Options are: easy, medium, and hard
if GAME_MODE == 2:
    AI_PLAYER = True
    PLAYER2 = False
    while AI_LVL <= 0 or AI_LVL > 4:
        AI_LVL = int(
            input("Please select AI difficulty:\n 1. easy\n 2. medium\n 3. hard\n"))
    if AI_LVL == 2:
        AI_LVL_DEPTH = 3
    elif AI_LVL == 3:
        AI_LVL_DEPTH = 5

# Asks for user input on size of board for rows and columns. Minimum lengths must be 4. This will replace global variable ROW_COUNT and COLUMN_COUNT.
while ROW_COUNT * COLUMN_COUNT < 16:
    # Row count
    while ROW_COUNT < 4:
        ROW_COUNT = int(
            input("Please select the size of the rows (Must be greater or equal to 4): "))
        if ROW_COUNT < 4:
            print("Row size is too low\n")
    # Column count
    while COLUMN_COUNT < 4:
        COLUMN_COUNT = int(
            input("Please select the size of the columns (Must be greater or equal to 4): "))
        if COLUMN_COUNT < 4:
            print("\nColumn size is too low\n")

# Uses library numpy to create an array of zeroes based on ROW_COUNT and COLUMN_COUNT.


def create_board(x, y):
    board = np.zeros((x, y))
    return board


# Verifies if the top row or the last array in the board to see if a piece can be dropped there


def is_valid_location(board, col):
    if col < COLUMN_COUNT and col >= 0:
        return (board[ROW_COUNT - 1][col] == 0)
    return False

# Puts together list of valid locations for a piece to drop using is_valid_location function


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
# starting from the first array in the list, keeps checking in that column where the EMPTY piece is located. Returns that position on the board as board[row][column]


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if (board[r][col] == 0):
            return (r)

# Drops piece in the designated area on the connect 4 board after being confirmed by the get_next_open_row function.


def drop_piece(board, row, col, piece):
    board[row][col] = piece

# To visualize in the terminal, the board is printed using numpy library function flip to simulate a connect four board and how the pieces get placed.


def print_board(board):
    print(np.flip(board, 0))

# After each piece is dropped, confirms if the last piece dropped has mad a connect four in horizontal, vertical, or diagonal fashion.


def check_win(board, last_location_row, last_location_col, piece):

    # Check column of the piece's last row location
    col = 0
    count = 0

    # print last piece drop

    print(last_location_row, last_location_col)
    # checks horizontal win
    for r in range(ROW_COUNT):
        count = 0
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            count = row_array[c:c+WINDOW_LENGTH]
            if count.count(piece) == 4:
                return count.count(piece)

    # Reset count. Check row of the piece's last column location

    count = 0
    row = 0
    # checks vertical win

    while board[last_location_row - row][last_location_col] == piece and last_location_row - row >= 0:
        count += 1
        row += 1
        if count == 4:
            return count

    # Reset Count, col, and row. Checking diagonal from TOP LEFT to BOTTOM RIGHT

    # note: board is flipped over horizontal due to numpy.flip
    # row (0) starts from bottom row and goes up
    count = 0
    col = last_location_col
    row = last_location_row
    # lol

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

    # Reset count, col, and row. Checking diagonal from BOTTOM LEFT to TOP RIGHT

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


# score_counter used to add points in position.


def score_counter(window, piece):

    score = 0

    if window.count(piece) == 4:
        score += 50
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 30
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 20
    elif window.count(piece) == 1 and window.count(EMPTY) == 3:
        score += 10
    return score

# have to change score position so it takes points based on the point it drops on


def score_position(board, piece, col, row):

    score = 0

    # loop through the horizontal, vertical, and diagonals all at once at the point the piece is dropped

    # horizontal
    row_array = [int(i) for i in list(board[row, :])]
    if (col - 3) < 0:
        start = 0
    else:
        start = col - 3
    if (col + WINDOW_LENGTH) > COLUMN_COUNT:
        end = COLUMN_COUNT - 3
    else:
        end = col + 1
    for c in range(start, end):
        window = row_array[c: c + WINDOW_LENGTH]
        add_score = score_counter(window, piece)
        if add_score > score:
            score = add_score
    # vertical
    # add_score is a place holder from the previous score
    prev_score = score
    col_array = [int(i) for i in list(board[:, col])]
    if (row - 3) < 0:
        start = 0
    else:
        start = row - 3
    if (row + WINDOW_LENGTH) > ROW_COUNT:
        end = ROW_COUNT - 3
    else:
        end = row + 1
    for r in range(start, end):
        window = col_array[r: r + WINDOW_LENGTH]
        add_score = score_counter(window, piece)
        if (add_score + prev_score) > score:
            score = add_score + prev_score

    # Check diagonal from BOTTOM LEFT to TOP RIGHT
    # note the board will print upside down because of numpy.flip()
    # take in previous score
    prev_score = score

    # creates the start POINT of diagonal
    if (row - 3) <= 0 and (col >= row):
        point = [0, col - row]
    elif (row >= col) and (col - 3) <= 0:
        point = [row - col, 0]
    else:
        point = [row - 3, col - 3]

    # creates END point of diagonal

    if (row + WINDOW_LENGTH) >= ROW_COUNT and col <= row:
        end = [ROW_COUNT, col + (ROW_COUNT - row)]
    elif ((row < col) and (col + WINDOW_LENGTH >= COLUMN_COUNT)):
        end = [row + (COLUMN_COUNT - col), COLUMN_COUNT]
    else:
        end = [row + WINDOW_LENGTH, col + WINDOW_LENGTH]
    diagonal_array = []
    while point != end:
        diagonal_array.append(board[point[0]][point[1]])
        point[0] += 1
        point[1] += 1

    # checks created list of diagonal points. If it is less than 4, it skips the check

    if len(diagonal_array) >= 4:
        for diagonal in range(len(diagonal_array) - 3):
            window = diagonal_array[diagonal: diagonal + WINDOW_LENGTH]
            add_score = score_counter(window, piece)
            if (add_score + prev_score) > score:
                score = add_score + prev_score

    # Check diagonal from TOP LEFT to BOTTOM RIGHT
    # note the board will print upside down because of numpy.flip()

    prev_score = score

    # creates the start POINT of diagonal
    if row + col < ROW_COUNT and (col - 3 <= 0):
        point = [row + col, 0]
    elif (row + col) >= ROW_COUNT and (row + 3 >= ROW_COUNT):
        point = [ROW_COUNT - 1, col + 1 - (ROW_COUNT - row)]
    else:
        point = [row + 3, col - 3]

    # creates END point of diagonal
    if (row + WINDOW_LENGTH) >= ROW_COUNT and (col + row >= COLUMN_COUNT):
        end = [row - (COLUMN_COUNT - col), COLUMN_COUNT]
    elif (row - WINDOW_LENGTH < 0) and (col + row < COLUMN_COUNT):
        end = [-1, col + row + 1]
    else:
        end = [row - WINDOW_LENGTH, col + WINDOW_LENGTH]

    diagonal_array = []

    while point[1] != COLUMN_COUNT and point[0] >= 0:
        diagonal_array.append(board[point[0]][point[1]])
        point[0] -= 1
        point[1] += 1

    # checks created list of diagonal points. If it is less than 4, it skips the check

    if len(diagonal_array) >= 4:
        for diagonal in range(len(diagonal_array) - 3):
            window = diagonal_array[diagonal: diagonal + WINDOW_LENGTH]
            add_score = score_counter(window, piece)
            if (add_score + prev_score) > score:
                score = add_score + prev_score

    return score

# Used for AI to determine which column to drop the piece in based on the score it recieves in different positions. Will then choose the highest score with the col the piece will drop in.


def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        temp_board = board.copy()
        row = get_next_open_row(board, col)
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece, col, row)
        print(score)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


# def minimax(node_index, cur_depth, maximizing_player, scores, target_depth):
#     if cur_depth == target_depth:
#         return scores[node_index]
#     if (maximizing_player):
#         return max(minimax(cur_depth + 1, node_index * 2, False, scores, target_depth))


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

# draw board for pygame. added center to check positioning


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

# adding ai placeholder (temporary)
ai_dusty = False
if font_size > 80:
    font_size = 80


while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("No Contest")
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn % 2 == 1:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
            elif PLAYER2:
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
                check = is_valid_location(board, col)
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
            elif PLAYER2:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))
                check = is_valid_location(board, col)
                if check == True and col < COLUMN_COUNT:
                    if AI_PLAYER:
                        ai_dusty = True
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    print_board(board)
                    turn += 1
                if check == False:
                    print(
                        "\nerror: This column is full. Please select another spot\n")

                if col < COLUMN_COUNT and col >= 0 and check == True:
                    if check_win(board, row, col, 2) >= 4:
                        label = myfont.render('Player 2 wins!', True, YELLOW)
                        game_over = True
            draw_board(board)
    # A.I. turn
    if turn % 2 == 0 and AI_PLAYER and not game_over:
        col = pick_best_move(board, AI_PIECE)
        check = is_valid_location(board, col)
        if check == True and col < COLUMN_COUNT:
            # added delay for A.I. drop piece
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            print_board(board)
            turn += 1
        elif check == False:
            print("\nerror: This column is full. Please select another spot\n")
        if col < COLUMN_COUNT and col >= 0 and check == True:
            if check_win(board, row, col, 2) >= 4:
                label = myfont.render('AI_dusty wins!', True, YELLOW)
                game_over = True
        draw_board(board)

    if turn > (ROW_COUNT * COLUMN_COUNT):
        label = myfont.render("No more turns!", True, WHITE)
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
