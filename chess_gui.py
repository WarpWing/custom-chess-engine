#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import chess_engine
import pygame as py

from enums import Player

"""Variables"""
WIDTH = HEIGHT = 512            # width and height of the chess board
DIMENSION = 8                   # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION   # the size of each of the squares in the board
MAX_FPS = 15                    # FPS for animations
IMAGES = {}                     # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]

def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r,c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()], py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))
            for move in valid_moves:
                screen.blit(s, (move[1]*SQ_SIZE,  move[0]*SQ_SIZE))

def main():
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    game_state = chess_engine.game_state()
    load_images()
    running = True
    square_selected = ()                        # keeps track of the last selected square
    player_clicks = []                          # keeps track of player clicks (two tuples)
    valid_moves = []
    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                location = py.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:
                    # this if is useless right now
                    if not game_state.is_valid_piece(player_clicks[0][0], player_clicks[0][1]):
                        square_selected = ()
                        player_clicks = []
                    else:
                        game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                              (player_clicks[1][0], player_clicks[1][1]), game_state)
                        square_selected = ()
                        player_clicks = []
                        valid_moves = []
                else:
                    valid_moves = game_state.get_valid_moves(game_state, row, col)

        draw_game_state(screen, game_state, valid_moves, square_selected)
        clock.tick(MAX_FPS)
        py.display.flip()


if __name__ == "__main__":
    main()