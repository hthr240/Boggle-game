from view import *
from model import *
from boggle_board_randomizer import randomize_board


class Boggle:
    '''
    Boggle game controller
    '''

    def __init__(self, board, words):
        '''
        controller init
        '''
        self.model = Model(board, words)  # game logic object
        self.view = BoggleGui()  # game view object

        # attach commands form model to view object
        for btn_name in self.view.buttons:
            self.view.set_butt_cmd(btn_name, self.create_button_act(btn_name))

    def create_button_act(self, btn_name):
        '''
        this method attaches the commands
        '''
        def action():
            self.model.type_in(btn_name)
            self.view.update_display(self.model.get_real_info(), btn_name)
        return action

    def main(self):
        self.view.start()


if __name__ == '__main__':
    boggle = Boggle(board=randomize_board(), words=WORDS)
    boggle.main()
