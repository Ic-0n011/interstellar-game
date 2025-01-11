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
    start_color,
    init_pair,
    color_pair,
    COLOR_BLACK,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_CYAN,
    KEY_LEFT,
    KEY_B3,
    KEY_RIGHT,
    KEY_B1,
    KEY_UP,
    KEY_A2,
    KEY_DOWN,
    KEY_C2,
    napms,
    )
import random

class Game:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.stdscr.nodelay(1)  # Делаем ввод неблокирующим
        self.stdscr.timeout(100)  # Задержка для обновления экрана

        self.field = [[EMPTY for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.ship = Ship(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.generate_field()
        self.base_x, self.base_y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
        self.field[self.base_y][self.base_x] = BASE

    def generate_field(self) -> None:
        # Генерация чёрных дыр и белых дыр
        for _ in range(3):
            x, y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
            self.field[y][x] = BLACK_HOLE
            x, y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
            self.field[y][x] = WHITE_HOLE

        # Генерация обломков материи
        for _ in range(30):
            x, y = random.randint(0, FIELD_WIDTH - 1), random.randint(0, FIELD_HEIGHT - 1)
            self.field[y][x] = DEBRIS

    def draw(self) -> None:
        start_color()
        init_pair(3, COLOR_RED, COLOR_BLACK)
        init_pair(2, COLOR_YELLOW, COLOR_BLACK)
        init_pair(1, COLOR_CYAN, COLOR_BLACK)

        self.stdscr.clear()

        # Рисуем границы
        for y in range(FIELD_HEIGHT + 2):
            for x in range(FIELD_WIDTH + 2):
                if y == 0 or y == FIELD_HEIGHT + 1 or x == 0 or x == FIELD_WIDTH + 1:
                    self.stdscr.addch(y, x, '#', color_pair(1))

        # Рисуем игровое поле
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.ship.x == x and self.ship.y == y:
                    self.stdscr.addch(y + 1, x + 1, self.ship.img, color_pair(2))
                else:
                    self.stdscr.addch(y + 1, x + 1, self.field[y][x], color_pair(3))

        # Отображаем информацию
        base_distance = abs(self.ship.x - self.base_x) + abs(self.ship.y - self.base_y)
        elapsed_hours = int(self.elapsed_time // 60)
        elapsed_minutes = int(self.elapsed_time % 60)

        self.stdscr.addstr(FIELD_HEIGHT + 3, 0, f"|Скорость: {self.ship.speed}", color_pair(2))
        self.stdscr.addstr(FIELD_HEIGHT + 4, 0, f"|Направление: {DIRECTIONS_IMG[self.ship.direction]}", color_pair(2))
        self.stdscr.addstr(FIELD_HEIGHT + 5, 0, f"|Координаты: ({self.ship.x}, {self.ship.y})", color_pair(2))
        self.stdscr.addstr(FIELD_HEIGHT + 6, 0, f"|Расстояние до базы: {base_distance}", color_pair(2))
        self.stdscr.addstr(FIELD_HEIGHT + 7, 0, f"|Топливо: {self.ship.fuel}", color_pair(2))
        self.stdscr.addstr(FIELD_HEIGHT + 8, 0, f"|Время: {elapsed_hours} ч {elapsed_minutes} мин", color_pair(2))

        self.stdscr.refresh()

    def handle_input(self) -> None:
        key = self.stdscr.getch()

        if key == KEY_LEFT or key == KEY_B3:
            self.ship.turn_left()
        elif key == KEY_RIGHT or key == KEY_B1:
            self.ship.turn_right()
        elif key == KEY_UP or key == KEY_A2:
            self.ship.accelerate()
        elif key == KEY_DOWN or key == KEY_C2:
            self.ship.decelerate()

        # Постоянное движение корабля
        dx, dy = DIRECTIONS[self.ship.direction]
        self.ship.move(dx, dy)

    def check_collisions(self) -> str:
        x, y = self.ship.x, self.ship.y

        if x < 0 or x >= FIELD_WIDTH or y < 0 or y >= FIELD_HEIGHT:
            return 'loss'  # Вышел за границы поля

        if self.field[y][x] == DEBRIS:
            return 'loss'  # Столкновение с обломками

        if self.field[y][x] == BLACK_HOLE:
            # Телепортируем игрока в белую дыру
            white_holes = [(wx, wy) for wy in range(FIELD_HEIGHT) for wx in range(FIELD_WIDTH) if self.field[wy][wx] == WHITE_HOLE]
            if white_holes:
                self.ship.x, self.ship.y = random.choice(white_holes)
                # Отбрасываем игрока на 1 клетку в случайную сторону
                self.ship.move(random.choice([-1, 1]), random.choice([-1, 1]))

        if self.field[y][x] == WHITE_HOLE:
            # Отбрасываем игрока на 2 клетки в случайную сторону
            dx, dy = random.choice(DIRECTIONS)
            for _ in range(2):
                new_x, new_y = self.ship.x + dx, self.ship.y + dy
                if 0 <= new_x < FIELD_WIDTH and 0 <= new_y < FIELD_HEIGHT and self.field[new_y][new_x] == EMPTY:
                    self.ship.x, self.ship.y = new_x, new_y
                    break

        # Влияние чёрных и белых дыр на время
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if 0 <= y + dy < FIELD_HEIGHT and 0 <= x + dx < FIELD_WIDTH:
                    if self.field[y + dy][x + dx] == BLACK_HOLE:
                        self.ship.time_factor = 2.0
                    elif self.field[y + dy][x + dx] == WHITE_HOLE:
                        self.ship.time_factor = 0.67

        if self.ship.fuel <= 0:
            return 'loss'

        if self.field[y][x] == BASE:
            return 'win'  # Достиг базы

        return 'continue'

    def play(self) -> str:
        self.elapsed_time = 0

        while True:
            self.draw()
            self.handle_input()

            # Обновление времени
            napms(int(100 / (1500 if self.ship.speed == 2 else 1)))

            self.elapsed_time += self.ship.time_factor * (0.5 if self.ship.speed == 0 else 1)

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
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.img = DIRECTIONS_IMG[0] # Отображение корабля - зависит от направления
        self.direction = 0 # Текущее направление
        self.speed = 0  # Текущая скорость
        self.fuel = 100  # Начальное количество топлива
        self.time_factor = 1.0  # Коэффициент времени (1.0 - нормальное время)

    def move(self, dx, dy) -> None:
        if self.speed:
            self.x += dx
            self.y += dy
            self.fuel -= self.speed * 0.2  # Чем выше скорость, тем больше расход топлива

    def turn_left(self) -> None:
        self.direction = (self.direction - 1) % 8
        self.img = DIRECTIONS_IMG[self.direction]

    def turn_right(self) -> None:
        self.direction = (self.direction + 1) % 8
        self.img = DIRECTIONS_IMG[self.direction]

    def accelerate(self) -> None:
        if self.fuel > 0 and self.speed < 2:  # Ограничение максимальной скорости
            self.speed += 1
            self.update_time_factor()

    def decelerate(self) -> None:
        if self.speed > 0:
            self.speed -= 1
            self.update_time_factor()

    def update_time_factor(self) -> None:
        """Обновляем коэффициент времени и расход топлива в зависимости от скорости."""
        self.time_factor = max(0.5, 1.0 - self.speed * 0.1)
