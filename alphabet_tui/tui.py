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


def print_challenge_screen(goal_key: str) -> None:
    """Print challenge screen to terminal.

    Args:
        goal_key: character that needs to be pressed.
    """
    os.system("clear")
    print(LETTERS[goal_key])


def print_success_screen(goal_key: str) -> None:
    """Print success screen to terminal.

    Args:
        goal_key: character that needs to be pressed.
    """
    os.system("clear")
    print(SYMBOLS[goal_key])
    sleep(5)


def on_press(
    key: KeyCode,
    goal_key: str,
) -> bool:
    """Handle keypress.

    Args:
        key: pressed key.
        goal_key: character that needs to be pressed.
    """
    match key:
        case Key.esc:
            sys.exit(0)
        case KeyCode(char=key) if key.upper() == goal_key:
            print_success_screen(goal_key=goal_key)
            return False  # stop keyboard listener
        case _:
            print_challenge_screen(goal_key=goal_key)


def wait_for_keypress(goal_key: str) -> None:
    """Set up keyboard listener handler for keypress.

    Args:
        goal_key: character that needs to be pressed.
    """
    # setup 'on_press' handler with goal_key as partial argument
    on_press_of_goal_key = partial(on_press, goal_key=goal_key)

    # start keyboard listener
    try:
        with Listener(on_press=on_press_of_goal_key) as listener:
            listener.join()
    except ConnectionClosedError:
        # HERE: keyboard listener was closed by user
        os.system("clear")
        sys.exit(0)


if __name__ == "__main__":
    goal_key = ""
    while True:
        # randomly choose (different) goal character
        other_letters = list(set(LETTERS.keys()) - set(goal_key))
        goal_key = random.choice(list(LETTERS.keys()))

        # print goal character
        print_challenge_screen(goal_key=goal_key)

        # wait for user to press goal character
        wait_for_keypress(goal_key=goal_key)
