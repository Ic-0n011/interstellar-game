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
# pip install windows-curses


def main_menu(stdscr) -> str:
    current_row = 0
    menu = ["Начать новую игру", "Что нужно делать", "Об авторе", "Выход"]

    while True:
        stdscr.clear()

        # Получаем размеры текущего окна
        height, width = stdscr.getmaxyx()

        # Проверяем, достаточно ли места для отображения
        if height < FIELD_HEIGHT or width < FIELD_WIDTH:
            stdscr.addstr(0, 0, "Увеличьте размер окна терминала.")
            stdscr.refresh()
            stdscr.getch()
            continue

        # Рисуем меню
        for idx, row in enumerate(menu):
            x = (width // 2) - (len(row) // 2)
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.addstr(y, x, row, color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()
        key = stdscr.getch()

        if (key == KEY_UP or key == KEY_A2) and current_row > 0:
            current_row -= 1
        elif (key == KEY_DOWN or key == KEY_C2) and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord('\n'):  # Enter
            if current_row == 0:  # Начать новую игру
                return "new_game"
            elif current_row == 1:  # Что нужно делать
                show_instructions(stdscr)
            elif current_row == 2:  # Об авторе
                show_author(stdscr)
            elif current_row == 3:  # Выход
                return "exit"

def show_instructions(stdscr) -> None:
    stdscr.clear()
    instructions = [
        "Цель игры: добраться до базы (O),",
        "за кратчайшее время, следите за показателем топлива!",
        "избегая чёрных дыр (B) и обломков материи (X).",
        "Белые дыры (W) отбросят вас в случайном направлении.",
        "",
        "",
        "Управление:",
        "Стрелка влево/вправо - Поворот корабля.",
        "Стрелка вверх - Ускорение, стрелка вниз - тормоз",
        "",
        "",
        "Нажмите любую клавишу, чтобы вернуться в меню."
    ]

    for idx, line in enumerate(instructions):
        stdscr.addstr(FIELD_HEIGHT // 2 - len(instructions) // 2 + idx, 2, line)
    stdscr.refresh()
    stdscr.getch()

def show_author(stdscr) -> None:
    stdscr.clear()
    author_info = [
        "Автор игры: Ic-0n.",
        "Версия: 1.0.",
        "",
        "Нажмите любую клавишу, чтобы вернуться в меню."
    ]

    for idx, line in enumerate(author_info):
        stdscr.addstr(FIELD_HEIGHT // 2 - len(author_info) // 2 + idx, 2, line)
    stdscr.refresh()
    stdscr.getch()

def main(stdscr) -> None:
    start_color()
    init_pair(1, COLOR_RED, COLOR_MAGENTA)

    while True:
        choice = main_menu(stdscr)
        if choice == "new_game":
            game = Game(stdscr)
            game.play()
        elif choice == "exit":
            break

wrapper(main)