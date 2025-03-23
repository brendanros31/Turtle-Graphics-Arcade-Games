import sys
import numpy as np
import turn as turn
import pygame
import math

# Colors For Board
BLUE = (173, 216, 231)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
YELLOW = (250, 250, 0)
WHITE = (250, 250, 250)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print (np.flip(board, 0))

def winning_move(board, piece):
    #Check all horozontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c +  1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check all Vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check Positively sloped Diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check Negatively sloped Diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(Screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(Screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), Radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(Screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), Width - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), Radius)
            elif board[r][c] == 2:
                pygame.draw.circle(Screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), Width - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), Radius)
    pygame.display.update()



board = create_board()
print_board(board)
board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100
Width = COLUMN_COUNT * SQUARE_SIZE
Height = ROW_COUNT+1 * SQUARE_SIZE

Size = (Width, Width)
Radius = int(SQUARE_SIZE/2 - 11)

Screen = pygame.display.set_mode(Size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(Screen, BLACK, (0, 0, Width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(Screen, RED, (posx, int(SQUARE_SIZE/2)), Radius)
            else:
                pygame.draw.circle(Screen, YELLOW, (posx, int(SQUARE_SIZE/2)), Radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)


            # Ask for Player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 WINS!", 1, WHITE)
                        Screen.blit(label, (110, 20))
                        game_over = True


               # print(selection) - to test

            # Ask for Player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 WINS!", 2, WHITE)
                        Screen.blit(label, (110, 20))
                        game_over = True


            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)