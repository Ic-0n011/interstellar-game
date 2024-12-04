from config import (
    EMPTY,
    FIELD_HEIGHT,
    FIELD_WIDTH,
    BASE,
    BLACK_HOLE,
    WHITE_HOLE,
    DEBRIS,
    DIRECTIONS,
    DIRECTIONS_IMG,
    )
from curses import (
    KEY_LEFT,
    KEY_B3,
    KEY_RIGHT,
    KEY_B1,
    KEY_UP,
    KEY_A2,
    napms,
    )
import random

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
                    self.stdscr.addch(y, x, self.ship.img)
                else:
                    self.stdscr.addch(y, x, self.field[y][x])

        self.stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()

        if key == KEY_LEFT or key == KEY_B3:
            self.ship.turn_left()
        elif key == KEY_RIGHT or key == KEY_B1:
            self.ship.turn_right()
        elif key == KEY_UP or key == KEY_A2:
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
                napms(2000)
                break
            elif status == 'loss':
                self.stdscr.addstr(FIELD_HEIGHT // 2, FIELD_WIDTH // 2 - 5, "Game Over!")
                self.stdscr.refresh()
                napms(2000)
                break


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = DIRECTIONS_IMG[0]
        self.direction = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def turn_left(self):
        self.direction = (self.direction - 1) % 8

    def turn_right(self):
        self.direction = (self.direction + 1) % 8

    def accelerate(self):
        dx, dy = DIRECTIONS[self.direction]
        self.img = DIRECTIONS_IMG[self.direction]
        return dx, dy
