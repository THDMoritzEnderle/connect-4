from copy import deepcopy

from termtables import to_string, styles
import main_menu
import datetime
import os

class GameElement:
    """
    The base class for all game elements.
    """

    def __init__(self):
        pass


class Checker(GameElement):
    """
    A checker.
    """

    def __init__(self):
        super().__init__()


class GameBoard(GameElement):
    """
    The game board.
    """

    def __init__(self, cols: int = 7, rows: int = 6):
        super().__init__()
        self.player_one_start = True
        self._cols = cols
        self._rows = rows
        self._game_board = [[-1 for _ in range(cols)] for _ in range(rows)]
        self.has_ended = False

    def __getitem__(self, item):
        return self._game_board[item]

    def game_save(self, game_mode):   # [1, 2, 3, 4, 5, 6]
        # create gamestring
        save = ""
        for column in self._game_board:
            save = save + str(column)[1:-1] + ";"  # take away the []
        save = save[:-1]
        date = datetime.datetime(2022, 6, 22)
        date = date.now()
        print(str(date).replace(' ', '_').replace('-', '_').replace(':', '_').split('.'))
        file = str(date).replace(' ', '_').replace('-', '_').replace(':', '_').split('.')[0] + '_' + game_mode

        with open(f'save_games/{file}.txt', 'w') as file:
            file.write(save + '|' + game_mode)

    def load_save(self, game_index):
        games = os.popen("ls save_games").read().split('\n')[:-1]
        file_name = games[int(game_index)-1]
        self._game_board = [[-1 for _ in range(self._cols)] for _ in range(self._rows)]   # to empty the game if game is loaded after another game
        with open(f'save_games/{file_name}', 'r') as file:
            game_info = file.read().split('|')
        saved_games = game_info[0].split(";")
        i = 0
        checkers = 0
        for rows in saved_games:
            rows = rows.split(', ')
            j = 0
            for element in rows:
                self._game_board[i][j] = int(element)
                if element != '-1':
                    checkers += 1
                j += 1
            i += 1
        if (checkers % 2) == 1:
            self.player_one_start = False
        return [file_name, game_info[1]]

    def check_valid_move(self, col: int) -> bool:
        """
        Check if a move is valid.
        :param col: column to check
        :return: True if valid, False otherwise
        """

        return (0 <= col < self._cols) and self._game_board[0][col] == -1

    def make_move(self, col: int, player: int) -> bool:
        """
        Make a move.
        :param col: column to make the move in
        :param player: player to make the move
        :return: True if move was made, False otherwise
        """

        if self.check_valid_move(col):
            for row in range(self._rows - 1, -1, -1):
                if self._game_board[row][col] == -1:
                    self._game_board[row][col] += player
                    break
            return True
        return False

    def __str__(self):
        """
        String representation of the game board.
        :return: game board string
        """

        return to_string(
            [[" " if self._game_board[row][col] == -1 else ("○" if self._game_board[row][col] == 1
                                                            else "✗")
              for col in range(self._cols)] for row in range(self._rows)],
            header=list(range(1, self._cols + 1)),
            style=styles.ascii_thin_double,
        )

    def check_win(self, player) -> bool:
        """
        check if a player has won.
        :return: False if no one has won, True otherwise
        """
        
        self.has_ended = True
        for x in range(self._cols):
            for y in range(self._rows):
                try:
                    if self._game_board[y][x] == \
                            self._game_board[y][x + 1] == \
                            self._game_board[y][x + 2] == \
                            self._game_board[y][x + 3] == player - 1:

                        return True
                    if self._game_board[y][x] == \
                            self._game_board[y + 1][x] == \
                            self._game_board[y + 2][x] == \
                            self._game_board[y + 3][x] == player - 1:
                        return True
                    if self._game_board[y][x] == \
                            self._game_board[y + 1][x + 1] == \
                            self._game_board[y + 2][x + 2] == \
                            self._game_board[y + 3][x + 3] == player - 1:
                        return True
                    if self._game_board[y][x] == \
                            self._game_board[y + 1][x - 1] == \
                            self._game_board[y + 2][x - 2] == \
                            self._game_board[y + 3][x - 3] == player - 1:
                        return True
                    if self._game_board[y][x] == \
                            self._game_board[y - 1][x + 1] == \
                            self._game_board[y - 2][x + 1] == \
                            self._game_board[y - 3][x + 1] == player - 1:
                        return True
                except IndexError:
                    pass
        self.has_ended = False
        return False

    def check_draw(self) -> bool:
        """
        check if the game is a draw.
        :return: True if draw, False otherwise
        """
        for x in range(self._cols):
            for y in range(self._rows):
                if self._game_board[y][x] == -1:
                    return False
        self.has_ended = True
        return True
      
    @property
    def cols(self):
        return self._cols

    def deepcopy(self):
        """
        deepcopy the game board.
        :return: deepcopy of the game board
        """
        return deepcopy(self)


class Player(GameElement):
    """
    The player.
    """

    def __init__(self, player_id, game_board: GameBoard, checkers: int = 21):
        super().__init__()
        self._checkers = checkers
        self._game_board = game_board
        self._player_id = player_id

    def _use_checker(self, col: int) -> bool:
        """
        Use a checker.
        :param col: column to use the checker in
        :return: True if checker was used, False otherwise
        """

        if self._check_checkers():
            self._checkers -= 1
            return self._game_board.make_move(col, self._player_id)
        return False

    def _check_checkers(self) -> bool:
        """
        Check if the player has any checkers left.
        """

        return self._checkers > 0

    def play(self, filename) -> bool:
        """
        Plays a move.
        :return: True if game is still running, False if game is over.
        """
        print(str(self._game_board) + f'\nPlayer {self._player_id}, its your turn. Which column do you want ' \
                                        f'to place your checker?\n')
        while True:
            options = [f'{i + 1}' for i in range(self._game_board._cols)] + ["quit"]
            index = main_menu.navigate_game(options)
            if index == len(options) - 1:
                if filename is not None:
                    os.popen(f"rm save_games/{filename}")
                return False
            if self._use_checker(index):
                if self._game_board.check_win(self._player_id):
                    print(str(self._game_board))
                    main_menu.win_menu(self._player_id)
                    if filename is not None:
                        os.popen(f"rm save_games/{filename}")
                    return False
                if self._game_board.check_draw():
                    print(str(self._game_board))
                    main_menu.draw_menu()
                    if filename is not None:
                        os.popen(f"rm save_games/{filename}")
                    return False
                return True
            else:
                title = str(self._game_board) + f"\n\nthis column is already full!\nplayer {self._player_id}, its " \
                                                f"your turn. Which column do you want to place your checker? "
