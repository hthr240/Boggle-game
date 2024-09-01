import random
from pathlib import Path

cwd = Path.cwd()
sound_path = cwd / "sounds"

# words path
WORDS = cwd / "boggle_dict.txt"

# image BG
MENU_BG = cwd / "menu_bg.png"

# backgrounds
GAME_MUSIC = sound_path / "bg_music.mp3"
MENU_MUSIC = sound_path / "menu_music.mp3"

# btn sounds
HOVER_SOUND_PATH = sound_path / "blip.wav"
CLICK_SOUND = sound_path / "click.wav"

# checks sounds
CHEK1 = sound_path / "check1.mp3"
CHECK2 = sound_path / "check2.mp3"
CHECK3 = sound_path / "check3.mp3"
CHECK4 = sound_path / "check4.mp3"
WRONG = sound_path / "wrong.mp3"

CHECK_SOUNDS = [CHEK1, CHECK2, CHECK3, CHECK4]


def get_check_sound(check_sounds: list):
    '''
    this func return random sound for check
    '''
    random.shuffle(check_sounds)
    return check_sounds[0]


def create_words_dictionary():
    '''
    creates the words dict
    key=word : value=len(word)
    '''
    word_dictionary = {}
    with open(WORDS) as file:
        lines = [line.rstrip() for line in file]
        for word in lines:
            word_dictionary[word] = len(word)
    return word_dictionary
