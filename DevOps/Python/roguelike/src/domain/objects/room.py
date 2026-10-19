import random


class Room:

    def __init__(self, room_id, x, y, width, height):
        self._id = room_id
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._enemies = []
        self._items = []
        self._start_room = False
        self._exit_room = False
        self._is_visit = False
        self._exit_cell = None
        self._seen_cells = set()


    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def enemies(self):
        return self._enemies

    @property
    def items(self):
        return self._items

    @property
    def start_room(self):
        return self._start_room

    @property
    def exit_room(self):
        return self._exit_room

    @property
    def is_visit(self):
        return self._is_visit

    @start_room.setter
    def start_room(self, value):
        self._start_room = value

    @exit_room.setter
    def exit_room(self, value):
        self._exit_room = value

    @is_visit.setter
    def is_visit(self, value):
        self._is_visit = value

    def get_center(self):
        cx = self._x + self._width // 2
        cy = self._y + self._height // 2
        return cx, cy

    def mark_visited(self):
        self._is_visit = True

    @property
    def seen_cells(self):
        return self._seen_cells

    def mark_seen(self, x, y):
        self._seen_cells.add((x, y))
    @property
    def exit_cell(self):
        return self._exit_cell

    @exit_cell.setter
    def exit_cell(self, value):
        self._exit_cell = value

    def get_random_free_cell(self):
        for _ in range(100):
            x = random.randint(self._x + 1, self._x + self._width - 2)
            y = random.randint(self._y + 1, self._y + self._height - 2)

            if any(e.x == x and e.y == y for e in self._enemies):
                continue
            if any(i.x == x and i.y == y for i in self._items):
                continue
            return x, y
        return None

    def to_dict(self):
        return {
            "id": self._id,
            "x": self._x,
            "y": self._y,
            "width": self._width,
            "height": self._height,
            "start_room": self._start_room,
            "exit_room": self._exit_room,
            "is_visit": self._is_visit,
            "exit_cell": list(self._exit_cell) if self._exit_cell else None,
            "enemies": [e.to_dict() for e in self._enemies],
            "items": [i.to_dict() for i in self._items],
        }