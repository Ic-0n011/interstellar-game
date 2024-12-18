# Размеры игрового поля
FIELD_WIDTH = 40
FIELD_HEIGHT = 20

# Объекты поля
EMPTY = ' '
BLACK_HOLE = 'B'
WHITE_HOLE = 'W'
DEBRIS = 'X'
BASE = 'O'


# Направления движения
DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]  # 8 направлений (45 градусов)
DIRECTIONS_IMG = ['↓', '↘', '→', '↗', '↑', '↖', '←', '↙']