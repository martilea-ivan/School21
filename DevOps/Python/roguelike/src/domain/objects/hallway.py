import random


class Hallway:

    def __init__(self, start_room, end_room, all_rooms, door_color=None):
        self._start_room = start_room
        self._end_room = end_room
        self._all_rooms = all_rooms
        self._door_color = door_color
        self._tiles = self._build_tiles()

    @property
    def start_room(self):
        return self._start_room

    @property
    def end_room(self):
        return self._end_room

    @property
    def tiles(self):
        return self._tiles

    @property
    def door_color(self):
        return self._door_color

    @door_color.setter
    def door_color(self, value):
        self._door_color = value

    @property
    def door_cell(self):
        if self._door_color is None:
            return None
        for (x, y) in self._tiles:
            if (self._start_room.x <= x < self._start_room.x + self._start_room.width and
                    self._start_room.y <= y < self._start_room.y + self._start_room.height):
                continue
            # Проверим, что это ПЕРВАЯ клетка по пути (соседняя с комнатой)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (self._start_room.x <= nx < self._start_room.x + self._start_room.width and
                        self._start_room.y <= ny < self._start_room.y + self._start_room.height):
                    return (x, y)
        return None

    def _build_tiles(self) -> set:
        cx1, cy1 = self._start_room.get_center()
        cx2, cy2 = self._end_room.get_center()

        for order in random.sample(['hv', 'vh'], 2):
            tiles = self._build_l(cx1, cy1, cx2, cy2, order)
            if not self._intersects_room(tiles):
                return tiles

        return set()

    @staticmethod
    def _build_l(cx1: int, cy1: int, cx2: int, cy2: int, order: str) -> set:
        tiles = set()

        if order == 'hv':
            Hallway._add_horizontal(tiles, cx1, cx2, cy1)
            Hallway._add_vertical(tiles, cy1, cy2, cx2)
        else:
            Hallway._add_vertical(tiles, cy1, cy2, cx1)
            Hallway._add_horizontal(tiles, cx1, cx2, cy2)

        return tiles

    @staticmethod
    def _add_horizontal(tiles: set, x1: int, x2: int, y: int):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y))

    @staticmethod
    def _add_vertical(tiles: set, y1: int, y2: int, x: int):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x, y))

    def _intersects_room(self, tiles: set) -> bool:
        for room in self._all_rooms:
            if room is self._start_room or room is self._end_room:
                continue
            for (x, y) in tiles:
                if (room.x <= x < room.x + room.width and
                        room.y <= y < room.y + room.height):
                    return True
        return False

    def get_tiles(self) -> set:
        return self._tiles

    def to_dict(self):
        return {
            "start_room_id": self._start_room.id,
            "end_room_id": self._end_room.id,
            "tiles": [[x, y] for (x, y) in self._tiles],
            "door_color": self._door_color.name if self._door_color else None,
        }