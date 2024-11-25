import random
import curses
import math


"""
TODO:
     дать направление кораблю для удобства пользователя
     сделать поле больше и выводить только малую его часть
     попробовать сонарное видение
     удобный интерфейс

ВОЗМОЖНО, если будет время и все будет сделано:
                добавить время(для соревновательного режима)
                ??? скорость/инерция корабля   -   добавить топливо(кол-во ходов которые можно сделать)????
"""

# Размеры игрового поля
FIELD_WIDTH = 40
FIELD_HEIGHT = 20

# Объекты поля
EMPTY = ' '
BLACK_HOLE = 'B'
WHITE_HOLE = 'W'
DEBRIS = 'X'
BASE = 'O'
SHIP = 'S'

# Направления движения
DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]  # 8 направлений (45 градусов)

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # Направление 0 = движение вправо

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def turn_left(self):
        self.direction = (self.direction - 1) % 8

    def turn_right(self):
        self.direction = (self.direction + 1) % 8

    def accelerate(self):
        dx, dy = DIRECTIONS[self.direction]
        return dx, dy

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.nodelay(1)  # Делаем ввод неблокирующим
        self.stdscr.timeout(100)  # Задержка для обновления экрана

        self.field = [[EMPTY for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.ship = Ship(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.generate_field()
        self.base_x, self.base_y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
        self.field[self.base_y][self.base_x] = BASE

    def generate_field(self):
        # Генерация чёрных дыр
        for _ in range(5):
            x, y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
            self.field[y][x] = BLACK_HOLE

        # Генерация белых дыр
        for _ in range(5):
            x, y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
            self.field[y][x] = WHITE_HOLE

        # Генерация обломков материи
        for _ in range(10):
            x, y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
            self.field[y][x] = DEBRIS

    def draw(self):
        # Проверяем размеры терминала
        max_y, max_x = self.stdscr.getmaxyx()
        if max_y < FIELD_HEIGHT or max_x < FIELD_WIDTH:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Терминал слишком мал для игры!")
            self.stdscr.refresh()
            return

        self.stdscr.clear()

        # Рисуем игровое поле
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.ship.x == x and self.ship.y == y:
                    self.stdscr.addch(y, x, SHIP)
                else:
                    self.stdscr.addch(y, x, self.field[y][x])

        self.stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()
    
        # Отладка: выводим нормализованный код клавиши TODO: удалить!!!
        self.stdscr.addstr(0, 0, f"Нормализованный код клавиши: {key}")
        self.stdscr.refresh()
        """ FIXME
        что вывело(терминал vscode) = что нажал: KEY-B1(452) = стрелка влево,
          KEY-A2(450) = стрелка вверх, KEY-B3(454) = стрелка вправо

          
        должно быть(при запуске файла без редакторов все работает)  KEY_LEFT(260),  KEY_UP(259),  KEY_RIGHT(261)

        число в key тоже отличается (отображено в скобках)
        """

        if key == curses.KEY_LEFT:
            self.ship.turn_left()
        elif key == curses.KEY_RIGHT:
            self.ship.turn_right()
        elif key == curses.KEY_UP:
            dx, dy = self.ship.accelerate()
            self.ship.move(dx, dy)

    def check_collisions(self):
        # Проверка столкновений с препятствиями
        x, y = self.ship.x, self.ship.y

        if x < 0 or x >= FIELD_WIDTH or y < 0 or y >= FIELD_HEIGHT:
            return 'loss'  # Вышел за границы поля

        if self.field[y][x] == DEBRIS:
            return 'loss'  # Столкновение с обломками

        if self.field[y][x] == BLACK_HOLE:
            # Попадание в чёрную дыру
            self.ship.x, self.ship.y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)

        if self.field[y][x] == WHITE_HOLE:
            # Попадание в белую дыру — отбрасываем в случайном направлении
            self.ship.move(random.randint(-2, 2), random.randint(-2, 2))

        if self.field[y][x] == BASE:
            return 'win'  # Достиг базы

        return 'continue'

    def play(self):
        while True:
            self.draw()
            self.handle_input()

            status = self.check_collisions()

            if status == 'win':
                self.stdscr.addstr(FIELD_HEIGHT // 2, FIELD_WIDTH // 2 - 5, "You Win!")
                self.stdscr.refresh()
                curses.napms(2000)
                break
            elif status == 'loss':
                self.stdscr.addstr(FIELD_HEIGHT // 2, FIELD_WIDTH // 2 - 5, "Game Over!")
                self.stdscr.refresh()
                curses.napms(2000)
                break

def main_menu(stdscr):
    current_row = 0

    menu = ["Начать новую игру", "Что нужно делать", "Об авторе", "Выход"]

    while True:
        stdscr.clear()

        # Рисуем меню
        for idx, row in enumerate(menu):
            x = (FIELD_WIDTH // 2) - (len(row) // 2)
            y = FIELD_HEIGHT // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.addstr(y, x, row, curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
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

def show_instructions(stdscr):
    stdscr.clear()
    instructions = [
        "Цель игры: добраться до базы (O),",
        "избегая чёрных дыр (B) и обломков материи (X).",
        "Белые дыры (W) отбросят вас в случайном направлении.",
        "",
        "Управление:",
        "Стрелка влево/вправо - Поворот корабля.",
        "Стрелка вверх - Ускорение.",
        "",
        "Нажмите любую клавишу, чтобы вернуться в меню."
    ]

    for idx, line in enumerate(instructions):
        stdscr.addstr(FIELD_HEIGHT // 2 - len(instructions) // 2 + idx, 2, line)
    stdscr.refresh()
    stdscr.getch()

def show_author(stdscr):
    stdscr.clear()
    author_info = [
        "Автор игры: Ic-0n.",
        "Версия: 1.0.",
        "Спасибо за игру!",
        "",
        "Нажмите любую клавишу, чтобы вернуться в меню."
    ]

    for idx, line in enumerate(author_info):
        stdscr.addstr(FIELD_HEIGHT // 2 - len(author_info) // 2 + idx, 2, line)
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Цвет для выделенного пункта меню

    while True:
        choice = main_menu(stdscr)
        if choice == "new_game":
            game = Game(stdscr)
            game.play()
        elif choice == "exit":
            break

curses.wrapper(main)


