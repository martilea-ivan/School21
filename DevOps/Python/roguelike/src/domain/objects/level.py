from domain.objects.room import Room
from domain.objects.hallway import Hallway


class Level:

    def __init__(self, number: int, rooms: list[Room], hallways: list[Hallway],
                 start_room: Room, exit_room: Room):
        self._number = number
        self._rooms = rooms
        self._hallways = hallways
        self._start_room = start_room
        self._exit_room = exit_room

    @property
    def number(self) -> int:
        return self._number

    @property
    def rooms(self) -> list[Room]:
        return self._rooms

    @property
    def hallways(self) -> list[Hallway]:
        return self._hallways

    @property
    def start_room(self) -> Room:
        return self._start_room

    @property
    def exit_room(self) -> Room:
        return self._exit_room

    def is_walkable(self, x: int, y: int) -> bool:
        for room in self._rooms:
            if (room.x + 1 <= x < room.x + room.width - 1 and
                    room.y + 1 <= y < room.y + room.height - 1):
                return True
        for hallway in self._hallways:
            if (x, y) in hallway.tiles:
                return True
        return False

    def get_room_at(self, x: int, y: int) -> Room | None:
        for room in self._rooms:
            if (room.x <= x < room.x + room.width and
                    room.y <= y < room.y + room.height):
                return room
        return None

    def to_dict(self):
        return {
            "number": self._number,
            "start_room_id": self._start_room.id,
            "exit_room_id": self._exit_room.id,
            "rooms": [room.to_dict() for room in self._rooms],
            "hallways": [h.to_dict() for h in self._hallways],
        }