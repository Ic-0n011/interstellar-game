from config import (
    EMPTY,
    FIELD_HEIGHT,
    FIELD_WIDTH,
    BASE,
    BLACK_HOLE,
    WHITE_HOLE,
    DEBRIS,
    DIRECTIONS,
    )
from curses import (
    start_color,
    init_pair,
    color_pair,
    COLOR_BLACK,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_CYAN,
    COLOR_WHITE,
    COLOR_GREEN,
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
from texts import ASCII_SHIP_WIN, ASCII_SHIP_LOSE, ASCII_TITLE


class Game:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.stdscr.nodelay(1)
        self.stdscr.timeout(50)
        self.running = True
        self.field = [
            [EMPTY for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)
        ]
        self.empty_cells = [
            (x, y) for y in range(FIELD_HEIGHT) for x in range(FIELD_WIDTH)
        ]
        self.holes = []
        self.ship = Ship(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.generate_field()
        self.base_x, self.base_y = self.place_object(BASE)

    def place_object(self, obj, min_distance=5) -> tuple[int, int]:
        """Размещает объект на игровом поле, избегая близости к черным дырам"""
        while self.empty_cells:
            x, y = random.choice(self.empty_cells)
            if all(
                abs(x - h.x) + abs(y - h.y) >= min_distance for h in self.holes
            ):
                self.field[y][x] = obj
                self.empty_cells.remove((x, y))
                return x, y

    def generate_field(self) -> None:
        """Генерирует черные и белые дыры, а также обломки."""
        for _ in range(6):
            while self.empty_cells:
                x, y = random.choice(self.empty_cells)
                radius = random.choice([2, 3])
                if len(self.holes) % 2 == 0:
                    hole_type = BLACK_HOLE
                else:
                    hole_type = WHITE_HOLE
                new_hole = Hole(x, y, hole_type, radius)
                new_hole.calculate_influence(self.empty_cells)

                if not any(new_hole.intersects(hole) for hole in self.holes):
                    self.holes.append(new_hole)
                    break

        for _ in range(30):
            if self.empty_cells:
                self.place_object(DEBRIS)

    def draw(self) -> None:
        """Отображает игровое поле и интерфейс в терминале."""
        start_color()
        init_pair(1, COLOR_CYAN, COLOR_BLACK)   # Корабль (синий)
        init_pair(2, COLOR_GREEN, COLOR_BLACK)  # База (зелёный)
        init_pair(3, COLOR_RED, COLOR_BLACK)    # Обломки (красный)
        init_pair(4, COLOR_WHITE, COLOR_BLACK)  # Чёрная дыра (белый)
        init_pair(5, COLOR_YELLOW, COLOR_BLACK)  # Белая дыра (жёлтый)

        self.stdscr.clear()
        # Проверяем размеры терминала
        height, width = self.stdscr.getmaxyx()
        if height < (FIELD_HEIGHT + 16) or width < FIELD_WIDTH:
            self.stdscr.addstr(0, 0, "Увеличьте размер окна терминала.")
            self.stdscr.refresh()
            self.stdscr.getch()
            return

        buffer = []

        # Рисуем границы
        for y in range(FIELD_HEIGHT + 2):
            for x in range(FIELD_WIDTH + 2):
                if y == 0 or y == FIELD_HEIGHT + 1:
                    buffer.append((y, x, '─', 1))
                elif x == 0 or x == FIELD_WIDTH + 1:
                    buffer.append((y, x, '│', 1))

        # Рисуем игровое поле
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                ch = self.field[y][x]
                color = 0  # Цвет по умолчанию
                if ch == BASE:
                    color = 2
                elif ch == DEBRIS:
                    color = 3
                elif ch == BLACK_HOLE:
                    color = 4
                elif ch == WHITE_HOLE:
                    color = 5

                buffer.append((y + 1, x + 1, ch, color))

        # Рисуем корабль
        buffer.append((self.ship.y + 1, self.ship.x + 1, self.ship.img, 1))

        # Рисуем зоны влияния дыр
        for hole in self.holes:
            for cell in hole.body:
                buffer.append(
                    (
                        cell[1] + 1,
                        cell[0] + 1,
                        hole.type,
                        4 if hole.type == BLACK_HOLE else 5
                    )
                )
            buffer.append(
                (
                    hole.y + 1,
                    hole.x + 1,
                    f"{hole.radius}",
                    4 if hole.type == BLACK_HOLE else 5
                )
            )

        # Отображаем всё сразу
        for y, x, ch, color in buffer:
            self.stdscr.addch(y, x, ch, color_pair(color))

        # Вычисляем необходимые значения
        to_base = abs(self.ship.x-self.base_x)+abs(self.ship.y-self.base_y)
        elapsed_hours = int(self.elapsed_time // 60)
        elapsed_minutes = int(self.elapsed_time % 60)

        # Информация об игре
        info_lines = [
            (f"│Скорость: {self.ship.speed}", 3, 1),
            (f"│Направление: {self.ship.img}", 4, 2),
            (f"│Координаты: ({self.ship.x}, {self.ship.y})", 5, 3),
            (f"│Расстояние до базы: {to_base}", 6, 4),
            (f"│Топливо: {round(self.ship.fuel, 2)}", 7, 1),
            (f"│Время: {elapsed_hours} ч {elapsed_minutes} мин", 8, 5),
        ]

        # Легенда
        legend_y = FIELD_HEIGHT + 10
        legend_lines = [
            ("│Легенда:", legend_y, 1),
            (f"│{self.ship.img} - Ваш корабль", legend_y + 1, 1),
            ("│O - База", legend_y + 2, 2),
            ("│X - Обломки", legend_y + 3, 3),
            ("│B - Чёрная дыра", legend_y + 4, 4),
            ("│W - Белая дыра", legend_y + 5, 5),
        ]

        # Вывод информации
        for text, offset, color in info_lines:
            self.stdscr.addstr(
                FIELD_HEIGHT + offset,
                0,
                text,
                color_pair(color)
                )

        # Вывод легенды
        for text, offset, color in legend_lines:
            self.stdscr.addstr(offset, 0, text, color_pair(color))
        self.stdscr.refresh()

    def handle_input(self) -> None:
        """Управление игрока с помощью стрелок"""
        key = self.stdscr.getch()

        if key != -1:  # Если клавиша нажата
            self.last_key = key

        if key == 27:  # ESC
            self.running = False
        elif self.last_key == KEY_RIGHT or self.last_key == KEY_B3:
            self.ship.change_direction(-1)
        elif self.last_key == KEY_LEFT or self.last_key == KEY_B1:
            self.ship.change_direction(1)
        elif self.last_key == KEY_UP or self.last_key == KEY_A2:
            self.ship.change_speed(1)
        elif self.last_key == KEY_DOWN or self.last_key == KEY_C2:
            self.ship.change_speed(-1)

        self.last_key = -1  # Очищаем последнюю нажатую кнопку

        # Постоянное движение корабля
        dx, dy = DIRECTIONS[self.ship.img]
        self.ship.move(dx, dy)

    def check_collisions(self) -> str:
        x, y = self.ship.x, self.ship.y

        if (
            x < 0 or x >= FIELD_WIDTH or  # Вышел за границы поля
            y < 0 or y >= FIELD_HEIGHT or
            self.field[y][x] == DEBRIS or  # Столкнулся с обломками
            self.ship.fuel <= 0  # закончилось топливо
        ):
            return 'loss'

        for hole in self.holes:  # проверяем близость к дырам
            hole.affect_ship(self.ship, self.holes)

        if self.field[y][x] == BASE:
            return 'win'  # Достиг базы

        return 'continue'

    def play(self) -> str:
        """Начало игры, игровой цикл"""
        self.show_ASCII_screen(ASCII_TITLE, "Начало игры")
        self.elapsed_time = 0
        self.last_key = -1

        while self.running:
            self.draw()
            self.handle_input()
            # Обновление времени
            napms(int(150 / (2 if self.ship.speed == 2 else 1)))
            self.elapsed_time += 0.3 if self.ship.speed < 2 else 0.15

            status = self.check_collisions()

            if status == 'win':
                self.show_ASCII_screen(ASCII_SHIP_WIN, "Вы победили!")
                return "win"
            elif status == 'loss':
                self.show_ASCII_screen(ASCII_SHIP_LOSE, "Вы проиграли!")
                return "lose"

    def show_ASCII_screen(self, ascii_art: str, message: str) -> None:
        """Показывает экран победы или поражения с ASCII-артом."""
        self.stdscr.clear()
        lines = ascii_art.split("\n")
        start_y = FIELD_HEIGHT // 2 - len(lines) // 2
        start_x = FIELD_WIDTH // 2 - 5

        for i, line in enumerate(lines):
            self.stdscr.addstr(start_y + i, start_x, line)

        self.stdscr.addstr(start_y + len(lines) + 1, start_x, message)
        self.stdscr.refresh()
        napms(2000)


class Hole:
    def __init__(self, x, y, hole_type, radius=4) -> None:
        self.x = x
        self.y = y
        self.type = hole_type  # Тип дыры: чёрная или белая
        self.radius = radius  # радиус дыры
        self.body = []  # Части тела дыры
        self.influence_area = []
        self.timer = 0
        self.construct_body()

    def construct_body(self) -> None:
        """Формирует тело дыры в виде клеток."""
        offsets = [(-1 + dx, -1 + dy) for dx in range(3) for dy in range(3)]
        if self.radius != 3:
            offsets = [(dx, dy) for dx, dy in offsets if dx == 0 or dy == 0]
        for dx, dy in offsets:
            self.body.append((self.x + dx, self.y + dy))

    def calculate_influence(self, empty_cells) -> None:
        """Сохраняет клетки в зоне влияния и удаляет их из доступных."""
        for dy in range(-self.radius, self.radius + 1):
            for dx in range(-self.radius, self.radius + 1):
                nx, ny = self.x + dx, self.y + dy
                if (nx, ny) in empty_cells:
                    empty_cells.remove((nx, ny))
                    self.influence_area.append((nx, ny))

    def intersects(self, other) -> bool:
        """Проверяет, пересекается ли зона влияния с другой дырой."""
        for cell in self.influence_area:
            if cell in other.influence_area:
                return True
        return False

    def affect_ship(self, ship, holes) -> None:
        """Влияет на положение корабля в зависимости от типа дыры."""
        ship_position = (ship.x, ship.y)

        # Проверяем, находится ли корабль в зоне тела дыры
        if ship_position in self.body:
            if self.type == BLACK_HOLE:
                # Телепорт в случайную белую дыру
                white_holes = [hole for hole in holes
                               if hole.type == WHITE_HOLE]
                if white_holes:
                    target = random.choice(white_holes)
                    ship.x, ship.y = target.x, target.y

                    # продолжает движение в случайном направлении
                    available_directions = [
                        (dx, dy) for dx, dy in DIRECTIONS.values()
                        if 0 <= ship.x + dx < FIELD_WIDTH and
                        0 <= ship.y + dy < FIELD_HEIGHT
                    ]
                    if available_directions:
                        dx, dy = random.choice(available_directions)
                        ship.x += dx
                        ship.y += dy

            elif self.type == WHITE_HOLE:
                # Отталкивание в свободную клетку
                dx = ship.x - self.x
                dy = ship.y - self.y
                magnitude = max(1, abs(dx) + abs(dy))
                dx = dx // magnitude
                dy = dy // magnitude

                # Отталкиваем корабль сильнее, если он движется быстрее
                push_distance = max(1, ship.speed * 2)
                new_x = ship.x + dx * push_distance
                new_y = ship.y + dy * push_distance

                # Проверяем границы поля
                if 0 <= new_x < FIELD_WIDTH:
                    ship.x = new_x
                if 0 <= new_y < FIELD_HEIGHT:
                    ship.y = new_y

        # Проверяем, если корабль в зоне влияния, но не внутри тела
        elif ship_position in self.influence_area:
            if self.type == BLACK_HOLE:
                # Притягивание: уменьшает расстояние к центру дыры
                dx = -1 if ship.x > self.x else (1 if ship.x < self.x else 0)
                dy = -1 if ship.y > self.y else (1 if ship.y < self.y else 0)
                ship.x += dx * ship.speed  # Учитываем скорость
                ship.y += dy * ship.speed


class Ship:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.img = "↓"  # Отображение корабля - зависит от направления
        self.direction = 0  # Текущее направление
        self.speed = 0  # Текущая скорость
        self.fuel = 100  # Начальное количество топлива

    def move(self, dx, dy) -> None:
        if self.speed:
            self.x += dx
            self.y += dy
            # Чем выше скорость, тем больше расход топлив
            self.fuel -= self.speed * 0.4

    def change_direction(self, step) -> None:
        """Меняет направление корабля"""
        # Получаем список направлений
        directions_list = list(DIRECTIONS.keys())
        current_index = directions_list.index(self.img)
        new_index = (current_index + step) % len(directions_list)
        self.img = directions_list[new_index]  # Обновляем изображение корабля

    def change_speed(self, delta) -> None:
        """Изменяет скорость корабля"""
        self.speed = max(0, min(2, self.speed + delta))
