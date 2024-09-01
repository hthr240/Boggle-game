from boggle_board_randomizer import randomize_board
from typing import List, Tuple
from resource_paths import create_words_dictionary


WORDS = create_words_dictionary()
SIZE = 4
VALID_COORD = [(i, j) for i in range(SIZE) for j in range(SIZE)]
POSSIBAL_MOVES = [(1, 0), (1, 1), (1, -1), (0, -1),
                  (0, 1), (-1, 0), (-1, 1), (-1, -1)]

Board = List[List[str]]
Path = List[Tuple[int, int]]


class Model():
    '''
    Boggel game model

    '''

    def __init__(self, board: List[List[str]], words: dict):
        '''
        model init
        '''

        self.board = board
        self.bank = []
        self.path = []
        self.current_word = ""
        self.valid_moves = []
        self.score = 0
        self.test_word = False
        self.word_dict = words

    def valid_cells(self, cell):
        '''
        creates valid moves list for next turn
        '''
        self.valid_moves = []

        for move in POSSIBAL_MOVES:
            move_coord = (cell[0]+move[0], cell[1]+move[1])
            if move_coord in VALID_COORD and move_coord not in self.path:
                self.valid_moves.append(move_coord)

    def choose_letter(self, coord: tuple):
        '''
        update current,path and valid_moves
        '''
        # valid_moves
        self.valid_cells(coord)

        # for empty path
        if not self.path:
            self.path.append(coord)
            self.current_word += self.board[coord[0]][coord[1]]

        # in middel of path
        else:
            for move in POSSIBAL_MOVES:
                row, col = self.path[len(self.path)-1]
                next_move = (row+move[0], col+move[1])
                if coord == next_move:
                    self.path.append(coord)
                    self.current_word += self.board[coord[0]][coord[1]]

    def check_word(self):
        '''
        this method checks if current is in words
        and update stat accordingly
        '''
        if self.current_word in self.word_dict:
            self.bank.append(self.current_word)
            self.score += len(self.path)**2
            self.test_word = True
        self.current_word = ""
        self.path = []
        self.valid_moves = []

    def refresh_word(self):
        '''
        this method clear current turn stats
        '''
        self.current_word = ""
        self.path = []
        self.valid_moves = []

    def reset(self, board):
        '''
        this method reset all stats
        '''
        self.board = board
        self.score = 0
        self.current_word = ""
        self.bank = []
        self.path = []
        self.valid_moves = []

    def type_in(self, btn_name: str):
        '''
        this function attaches command to model methods
        '''
        self.test_word = False
        if btn_name == "refresh":
            self.refresh_word()
        if btn_name == "reset" or btn_name == "return":
            self.reset(randomize_board())
        if btn_name == "check":
            self.check_word()
        if btn_name == "again":
            self.reset(randomize_board())
        if type(btn_name) is tuple:
            self.choose_letter(btn_name)

    def get_real_info(self) -> dict:
        '''
        this method returns the current stats of the model
        '''
        info = {
            "board": self.board,
            "bank": self.bank,
            "path": self.path,
            "current": self.current_word,
            "score": self.score,
            "valid_moves": self.valid_moves,
            "return": self.board,
            "test": self.test_word
        }
        return info
