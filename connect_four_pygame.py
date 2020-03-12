# np.zeros(x,y) creates a board for you using zeroes


import numpy as np


ROW_COUNT = 0
COLUMN_COUNT = 0

while ROW_COUNT * COLUMN_COUNT < 16:
    while ROW_COUNT < 4:
        ROW_COUNT = int(
            input("Please select the size of the rows (Must be greater or equal to 4): "))
        if type(ROW_COUNT) != "int":
            print("error: Please select an integer value")
            continue
        elif ROW_COUNT < 4:
            print("Row size is too low\n")
    while COLUMN_COUNT < 4:
        COLUMN_COUNT = int(
            input("Please select the size of the columns (Must be greater or equal to 4): "))
        if type(COLUMN_COUNT) != "int":
            print("error: Please select an integer value")
        elif COLUMN_COUNT < 4:
            print("\nColumn size is too low\n")


def create_board(x, y):
    board = np.zeros((x, y))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col, row):
    if col < COLUMN_COUNT and col >= 0:
        return (board[row - 1][col] == 0)


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

    while board[row][last_location_col] != piece and row < ROW_COUNT:
        row += 1
    while board[row][last_location_col] == piece and row < ROW_COUNT:
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

    # checks from last piece position and checks matching piece going to top right

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
turn = 0

while not game_over:

    turn = 1
    # Ask for player 1 input
    while turn == 1 and game_over == False:
        col = int(
            input("Player 1 make your selection (0 - {}): ".format(COLUMN_COUNT - 1)))
        check = is_valid_location(board, col, ROW_COUNT)
        if check == True and col < COLUMN_COUNT:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            turn = 2
            print_board(board)
        elif (col >= COLUMN_COUNT):
            print(
                f"\nerror: Column choice is outside of range. Please select another spot between 0 and {COLUMN_COUNT - 1}\n")
        elif check == False:
            print("\nerror: This column is full. Please select another spot\n")
        if col < COLUMN_COUNT and col >= 0 and check == True:
            if check_win(board, row, col, 1) >= 4:
                print_board(board)
                print("\nPlayer 1 wins!")
                game_over = True

    # Ask for player 2 input
    while turn == 2 and game_over == False:
        col = int(
            input("Player 2 make your selection (0 - {}): ".format(COLUMN_COUNT - 1)))
        check = is_valid_location(board, col, ROW_COUNT)
        if check == True and col < COLUMN_COUNT:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            turn = 1
            print_board(board)
        elif (col >= COLUMN_COUNT):
            print(
                f"\nerror: Column choice is outside of range. Please select another spot between 0 and {COLUMN_COUNT}\n")
        elif check == False:
            print("\nerror: This column is full. Please select another spot\n")
        if col < COLUMN_COUNT and col >= 0 and check == True:
            if check_win(board, row, col, 2) >= 4:
                print_board(board)
                print("\nPlayer 2 wins!")
                game_over = True
