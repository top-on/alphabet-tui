"""TUI for alphabet game."""

import enum
import os
import random
import sys
from time import sleep

from pynput.keyboard import Events
from pynput.keyboard._xorg import Key, KeyCode

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
    sleep(2)


def wait_for_pressed_key() -> KeyCode:
    """Get pressed key.

    Returns:
        pressed key.
    """
    with Events() as events:
        for event in events:
            return event.key


def choose_new_goal_key(options: set[str], blocklist: set[str] = set()) -> str:
    """Choose new goal key.

    Args:
        options: list of characters that can be chosen.
        blocklist: list of characters that should not be chosen. Defaults to empty set.

    Returns:
        new goal key.
    """
    return random.choice(list(options - blocklist))


STATES = {"challenge", "success", "exit"}


class State(enum.Enum):
    """Game state enum."""

    CHALLENGE = enum.auto()
    SUCCESS = enum.auto()
    EXIT = enum.auto()


if __name__ == "__main__":
    # initialize
    goal_key = choose_new_goal_key(options=set(LETTERS.keys()))
    state = State.CHALLENGE

    while True:
        # do action, according to current state
        match state:
            case State.CHALLENGE:
                print_challenge_screen(goal_key=goal_key)

                # state transition, according to user input
                key = wait_for_pressed_key()
                match key:
                    case Key.esc:
                        state = State.EXIT
                    case KeyCode(char=key) if key.upper() == goal_key:
                        state = State.SUCCESS
                    case _:
                        continue

            case State.SUCCESS:
                print_success_screen(goal_key=goal_key)
                goal_key = choose_new_goal_key(
                    options=set(LETTERS.keys()),
                    blocklist={goal_key},
                )
                state = State.CHALLENGE

            case State.EXIT:
                sys.exit(0)
