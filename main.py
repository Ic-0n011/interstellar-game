from config import FIELD_HEIGHT, FIELD_WIDTH
from curses import (
    wrapper,
    color_pair,
    start_color,
    init_pair,
    KEY_UP,
    KEY_A2,
    KEY_DOWN,
    KEY_C2,
    COLOR_RED,
    COLOR_MAGENTA,
    )
from game import Game
from texts import MAIN_MENU, INSTRUCTIONS, AUTHOR_INFO


def main_menu(stdscr) -> str:
    current_row = 0
    while True:
        start_color()
        init_pair(6, COLOR_RED, COLOR_MAGENTA)
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if height < (FIELD_HEIGHT + 16) or width < FIELD_WIDTH:
            stdscr.addstr(0, 0, "Увеличьте размер окна терминала.")
            stdscr.refresh()
            stdscr.getch()
            continue

        for idx, row in enumerate(MAIN_MENU):
            x = (width // 2) - (len(row) // 2)
            y = height // 2 - len(MAIN_MENU) // 2 + idx
            if idx == current_row:
                stdscr.addstr(y, x, row, color_pair(6))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27:  # ESC
            break
        elif (key == KEY_UP or key == KEY_A2) and current_row > 0:
            current_row -= 1
        elif (
            (key == KEY_DOWN or key == KEY_C2) and
            current_row < len(MAIN_MENU) - 1
        ):
            current_row += 1
        elif key == ord('\n'):  # Enter
            if current_row == 0:
                game = Game(stdscr)
                game.play()
            elif current_row == 1:
                show_text_screen(stdscr, INSTRUCTIONS)
            elif current_row == 2:
                show_text_screen(stdscr, AUTHOR_INFO)
            elif current_row == 3:
                break


def show_text_screen(stdscr, text_list) -> None:
    stdscr.clear()
    for idx, line in enumerate(text_list):
        stdscr.addstr(FIELD_HEIGHT // 2 - len(text_list) // 2 + idx, 2, line)
    stdscr.refresh()
    stdscr.getch()


wrapper(main_menu)
