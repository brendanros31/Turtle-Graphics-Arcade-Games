import sys
import random
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

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

EMPTY = 0

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


def evaluate_window (window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= -4

    return score

def score_position(board, piece):
    score = 0

    ## Score Center
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window =  row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)


    ## Score +ve Sloped Diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range (WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    ## Score -ve Sloped Diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax (board, depth, alpha, beta,  maximisingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else: #Game is over , no valid moves
                return (None, 0)
        else: #Depth is 0
            return None, score_position(board, AI_PIECE)

    if maximisingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                coloumn = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return column, value

    else: #minimisingPlayer
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
                beta = min(beta, value)
                if alpha <= beta:
                    break
        return column, value


def get_valid_locations (board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(Screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(Screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), Radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(Screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), Width - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), Radius)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(Screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), Width - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), Radius)
    pygame.display.update()



board = create_board()
print_board(board)
board = create_board()
game_over = False

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

turn = random.randint(PLAYER, AI)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(Screen, BLACK, (0, 0, Width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(Screen, RED, (posx, int(SQUARE_SIZE/2)), Radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)


            # Ask for Player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 WINS!", 1, WHITE)
                        Screen.blit(label, (155, 30))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)


               # print(selection) - to test

         # Ask for Player 2 input
    if turn == AI and not game_over:

        #col = random.randint(0, COLUMN_COUNT-1)
        #col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 8, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("AI WINS!", 2, WHITE)
                Screen.blit(label, (250, 30))
                game_over = True


            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)