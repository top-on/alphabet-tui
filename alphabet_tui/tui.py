"""TUI for alphabet game."""

import os
import random
import sys
from functools import partial
from time import sleep

from pynput.keyboard import Listener
from pynput.keyboard._xorg import Key, KeyCode
from Xlib.error import ConnectionClosedError

from alphabet_tui.ascii import LETTERS, SYMBOLS


def print_challenge_screen(goal_key: str):
    """Print challenge screen to terminal."""
    os.system("clear")
    print(LETTERS[goal_key])


def print_success_screen(goal_key: str):
    """Print success screen to terminal."""
    os.system("clear")
    print(SYMBOLS[goal_key])
    sleep(10)


def on_press(key: KeyCode, goal_key: str):
    """Handle keypress."""
    if key == KeyCode.from_char(goal_key.lower()):
        print_success_screen(goal_key=goal_key)
        return False
    elif key == Key.esc:
        sys.exit(0)
    else:
        print_challenge_screen(goal_key=goal_key)


def wait_for_keypress(goal_key: str):
    """Set up keyboard listener handler for keypress."""
    on_press_of_goal_key = partial(on_press, goal_key=goal_key)

    try:
        with Listener(on_press=on_press_of_goal_key) as listener:
            listener.join()
    except ConnectionClosedError:
        os.system("clear")
        sys.exit(0)


if __name__ == "__main__":
    goal_key = ""
    while True:
        # randomly choose (different) goal character
        other_letters = list(set(LETTERS.keys()) - set(goal_key))
        goal_key = random.choice(other_letters)

        # print goal character
        print_challenge_screen(goal_key=goal_key)

        # wait for user to press goal character
        wait_for_keypress(goal_key=goal_key)
        wait_for_keypress(goal_key=goal_key)
