from tkinter import *
from tkinter.font import BOLD
from resource_paths import *
import pygame


SIZE = 4
BOARD_COORDS = [(i, j) for i in range(SIZE) for j in range(SIZE)]
TIMES = {"1 min": 60, "3 min": 180, "5 min": 300}


class BoggleGui:
    '''
    Boggle game view

    '''

    def __init__(self):

        pygame.init()

        # root settings
        self.root = Tk()
        self.root.resizable(False, False)
        self.root["bg"] = "#1a1a1a"
        self.root.geometry("1000x700")
        self.buttons = dict()
        self.points = 0

        # sets default stats
        self.selected = StringVar(self.root)
        self.selected.set("3 min")

        # sets the frames
        self.home = HomePage(self.root)
        self.home_frame()  # pack
        self.bg_play(MENU_MUSIC)
        self.game = GamePage(self.root)
        self.end = EndPage(self.root)

        # update buttons dict
        self.buttons = self.game.buttons
        self.buttons["start"] = self.home.start_butt
        self.buttons["again"] = self.end.play_again

    def update_display(self, info: dict, btn_name):
        '''
        this method update the window according to the command given
        '''
        if btn_name == "start":
            self.start_game()
            self.set_board(info["board"])
            self.bg_stop()
            self.bg_play(GAME_MUSIC)

        if btn_name == "return":
            self.bg_stop()
            self.bg_play(MENU_MUSIC)
            self.time_label.destroy()
            self.clear(info)
            self.game.pack_forget()
            self.home_frame()

        if btn_name == "reset":
            self.clear(info)

        if btn_name == "again":
            self.refresh_turn()
            self.end.pack_forget()
            self.clear(info)
            self.set_board(info["return"])
            self.home_frame()

        if btn_name == "refresh":
            self.refresh_turn()

        if btn_name == "check":
            self.check(info)
            self.refresh_turn()
            if info["test"]:
                self.check_play(CHECK_SOUNDS)
            else:
                self.check_play(WRONG)

        if type(btn_name) is tuple:
            self.click_play()
            self.click_cell(info)

        self.points = info["score"]

    def clear(self, info):
        '''
        this method restart game stats
        '''
        self.time = TIMES[self.selected.get()]
        self.refresh_turn()
        self.set_board(info["board"])
        self.game.update_bank(info["bank"], info["score"])
        self.game.current["text"] = f"current word:"

    def click_cell(self, info):
        '''
        this method deals with
        '''
        self.game.current["text"] = info["current"]

        for coord in BOARD_COORDS:
            btn = self.game.buttons[coord]
            if coord not in info["valid_moves"]:
                btn["state"] = "disabled"
            else:
                btn["state"] = "normal"

    def refresh_turn(self):
        '''
        this method updates the turn(path and current)
        '''
        for btn in self.game.buttons.keys():
            if type(btn) == tuple:
                self.game.buttons[btn].config(state=NORMAL)
            self.game.current.config(text=f"current word:")

    def set_board(self, board):
        '''
        this method update the baord cells values
        '''
        for name in self.game.buttons:
            if type(name) == tuple:
                btn = self.game.buttons[name]
                btn["text"] = board[name[0]][name[1]]

    def check(self, info):
        '''
        this method update the status frame labels
        '''
        self.game.update_bank(info["bank"], info["score"])

####################################### timer ##############################################

    def clock(self):
        '''
        this method init the game timer
        when timer gets to 0 switches the frame to end game
        '''
        self.time = TIMES[self.selected.get()]
        self.minutes = int(self.time/60)
        self.seconds = 0

        self.time_label = Label(
            self.game, text=(f"{self.minutes:02}:{self.seconds:02}"), font=("fangsong ti", 50, BOLD), fg="white", bg="#1a1a1a", highlightthickness=0)
        self.time_label.place(x=760, y=500)
        self.clock_helper()

    def clock_helper(self):

        seconds = self.time % 60
        minutes = int((self.time / 60)) % 60
        self.time_label.config(text=(f"{minutes:02}:{seconds:02}"))
        if self.time == 0:
            self.time_up()

        # last 10 seconds color change
        if self.time <= 10:
            if self.time % 2 != 0:
                self.time_label["fg"] = "red"
            else:
                self.time_label["fg"] = "white"
        self.time_label.after(1000, self.clock_helper)
        self.time -= 1

    def time_up(self):
        '''
        switches the game to end frame
        '''
        self.game.pack_forget()
        self.time_label.place_forget()
        self.bg_stop()
        self.bg_play(MENU_MUSIC)
        self.end.score_label.config(text=f"your score: {self.points}")
        self.end.pack(pady=80, fill=BOTH, expand=TRUE)

################################## frame switch methods ####################################

    def return_button(self):
        '''
        this method switches from game frame to home frame
        '''
        self.game.pack_forget()
        self.home.tkraise()

    def start_game(self):
        '''
        this method switches from the home frame to game frame
        '''
        self.home.pack_forget()
        self.clock()
        self.game.pack(fill=BOTH, expand=TRUE)

    def again(self):
        '''
        this method switches to the home frame
        '''
        self.end.pack_forget()
        self.home_frame()

    def set_butt_cmd(self, btn_name, cmd):
        '''
        this sets the command of a given button
        '''
        btn = self.game.buttons[btn_name]
        btn["command"] = cmd

################################## sound methods #############################################

    def bg_play(self, path):
        # loading background music
        pygame.mixer.music.load(path)
        if path == GAME_MUSIC:
            pygame.mixer.music.set_volume(0.017)
        else:
            pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)

    def bg_stop(self):
        pygame.mixer.music.stop()

    def click_play(self):
        self.click_sound = pygame.mixer.Sound(CLICK_SOUND)
        self.click_sound.set_volume(0.018)
        self.click_sound.play()

    def check_play(self, path):
        '''
        check btn sounds
        '''
        if type(path) == list:
            self.correct_sound = pygame.mixer.Sound(get_check_sound(path))
        else:
            self.correct_sound = pygame.mixer.Sound(path)
        self.correct_sound.set_volume(0.08)
        self.correct_sound.play()

    def start(self):
        '''
        starts main loop
        '''
        self.root.title("boggle")
        self.root.mainloop()

    def home_frame(self):
        '''
        home frame pack
        '''
        self.home.pack(fill=BOTH, expand=TRUE)
        # choose time
        self.dropdown = OptionMenu(
            self.home, self.selected, *[option for option in TIMES.keys()])
        self.dropdown.config(bg="grey80", fg="#1a1a1a",
                             activebackground="#1a1a1a",
                             activeforeground="grey80",
                             width=6,
                             height=1,
                             font=("helvetica", 14, BOLD),
                             borderwidth=0)
        self.dropdown.place(x=438, y=220)


class HomePage(Frame):

    def __init__(self, parent):
        '''
        home frame init
        '''
        # home frame game starts
        super().__init__(parent)
        self.bg = PhotoImage(file=MENU_BG)
        self.bg_label = Label(self, image=self.bg)
        self.bg_label.pack(fill=BOTH, expand=TRUE)

        self["bg"] = "#1a1a1a"

        # header label
        self.head = Label(self.bg_label, text="Boggle Game", font=(
            "gothic", 60), bd=5, bg="#1a1a1a", fg="#b71228")
        self.head.pack(fill=BOTH)

        self.bg_label.pack(fill=BOTH, expand=TRUE)

        # start buttons config
        self.start_butt = Button(self.bg_label, text="Start Game!", font=(
            "courier", 20), bg="lightblue", bd=3, activebackground="RoyalBlue4")
        self.start_butt.place(x=388, y=130)

        # exit button config
        self.exit = Button(self.bg_label, text="exit", font=(
            "courier", 17), bg="firebrick3", activebackground="red", padx=10, command=lambda: exit(), bd=3, width=7)
        self.exit.place(x=430, y=630)


class GamePage(Frame):

    def __init__(self, parent):
        '''
        game frame init
        '''
        # init main game frame
        super().__init__(parent)
        self.bg = PhotoImage(file=MENU_BG)
        self.bg_label = Label(self, image=self.bg)
        self.bg_label.pack(fill=BOTH, expand=TRUE)

        self["bg"] = "#1a1a1a"
        # header label
        self.head = Label(self.bg_label, text="Boggle Game", font=(
            "gothic", 60), bd=5, bg="#1a1a1a", fg="#b71228")
        self.head.pack(fill=BOTH)
        pygame.init()

        # game buttons
        self.buttons = dict()

        # status frame
        self.status_frame()
        # board frame
        self.board = Frame(self.bg_label, width=400,
                           height=400, bg="floralwhite")
        self.board.place(x=290, y=150)
        self.board_frame()
        # hover_sound
        self.hover_sound = pygame.mixer.Sound(HOVER_SOUND_PATH)
        self.hover_sound.set_volume(0.015)

        # navigation buttons
        self.navigation_frame()
        # menu buttons
        self.menu_frame()

    def status_frame(self):
        '''
        pack buttuns to status frame
        '''
        # current word label
        self.current = Label(
            self.bg_label, text="current word:", font=("fixed", 15, BOLD), bg="#cb143e", bd=5, width=20)
        self.current.place(x=14, y=150)

        # bank of words label
        self.text = Text(self.bg_label, width=14, height=13,
                         bg="#cb143e", font=10, state=DISABLED)
        self.text.place(x=55, y=220)

        # score label
        self.score_label = Label(self.bg_label, text=f"score: 0", font=(
            "fangsong ti", 25, BOLD), bd=5, fg="white", bg="#1a1a1a", width=10)
        self.score_label.place(x=30, y=565)

    def update_bank(self, bank, points):
        '''
        this method update bank and score 
        '''
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        for word in bank:
            self.text.insert(END, word + '\n')
        self.text.config(state=DISABLED)
        self.score_label["text"] = f"score: {points}"

    ################################## board settings #######################################

    def board_frame(self):
        '''
        creates the cells btn obj
        '''
        # creates the board
        for row in range(SIZE):
            for col in range(SIZE):
                cell = Button(self.board,
                              bg="#1a1a1a",
                              width=5,
                              height=2,
                              bd=3,
                              fg="gray88",
                              font=("bistream charter", 22, BOLD))
                cell.grid(row=row, column=col)
                self.buttons[(row, col)] = cell
                cell.bind("<Enter>", self.enter_cell)
                cell.bind("<Leave>", self.leave_cell)

    def enter_cell(self, event):
        event.widget["bg"] = "#d02c41"
        self.hover_sound.play()

    def leave_cell(self, event):
        event.widget["bg"] = "#1a1a1a"

    ################################ game buttons ###################################

    def navigation_frame(self):
        '''
        pack navigation button
        '''
        self.refresh = Button(self.bg_label, text="refresh choice", font=(
            "helvetica", 20), bg="#d02c41", activebackground="MistyRose4", bd=3)
        self.refresh.place(x=770, y=250)
        self.buttons["refresh"] = self.refresh

        self.check = Button(self.bg_label, text="check word!", font=(
            "helvetica", 20), bg="#d02c41", activebackground="MistyRose4", bd=3)
        self.check.place(x=783, y=350)
        self.buttons["check"] = self.check

    def menu_frame(self):
        '''
        pack menu buttons
        '''
        # reset board/time
        self.reset_button = Button(self.bg_label, text="reset", font=(
            "courier", 15), bg="SlateBlue1", activebackground="Blue", bd=3, width=12)
        self.reset_button.place(x=660, y=620)
        self.buttons["reset"] = self.reset_button

        # exit game
        self.exit_butt = Button(self.bg_label, text="exit", font=(
            "courier", 15), bg="firebrick3", activebackground="red", command=lambda: exit(), bd=3, width=12)
        self.exit_butt.place(x=190, y=620)

        # return to home page button
        self.return_butt = Button(self.bg_label, text="return", font=(
            "courier", 15), bg="seagreen3", activebackground="green", bd=3, width=12)
        self.return_butt.place(x=420, y=620)
        self.buttons["return"] = self.return_butt


class EndPage(Frame):

    def __init__(self, parent):
        '''
        end frame init
        '''
        # creates the frame
        super().__init__(parent)
        self["bg"] = "#1a1a1a"

        # label config
        self.end_label = Label(self, text="Times up!", font=(
            "helvetica", 35), bg="#1a1a1a", fg="white", bd=5)
        self.end_label.pack()

        # score label config
        self.score_label = Label(self, font=(
            "fangsong ti", 30), bg="#1a1a1a", fg="white", pady=20)
        self.score_label.pack()

        # play again button config
        self.play_again = Button(self, text="Main menu", font=(
            "helvetica", 20), bg="lightblue", bd=5, activebackground="RoyalBlue1")
        self.play_again.place(x=415, y=250)

        # exit button config
        self.exit_butt = Button(self, text="exit", font=(
            "courier", 20), bg="firebrick3", activebackground="red", padx=10, command=lambda: exit(), bd=5)
        self.exit_butt.pack(pady=35, side=BOTTOM)
