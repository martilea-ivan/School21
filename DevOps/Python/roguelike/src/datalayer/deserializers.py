from domain.objects.enum import (
    EnemyType,
    FoodType, WeaponType, ScrollType, ElixirType, TreasureType, KeyType,
)
from domain.objects.backpack import Backpack
from domain.objects.player import Player
from domain.objects.enemy import Enemy
from domain.objects.room import Room
from domain.objects.hallway import Hallway
from domain.objects.level import Level
from domain.objects.statistics import Statistics
from domain.objects.items.food import Food
from domain.objects.items.weapon import Weapon
from domain.objects.items.scroll import Scroll
from domain.objects.items.elixir import Elixir
from domain.objects.items.treasure import Treasure
from domain.objects.items.key import Key


def item_from_dict(data):
    kind = data["kind"]
    if kind == "food":
        item = Food(FoodType[data["name"]])
    elif kind == "weapon":
        item = Weapon(WeaponType[data["name"]])
    elif kind == "scroll":
        item = Scroll(ScrollType[data["name"]])
    elif kind == "elixir":
        item = Elixir(ElixirType[data["name"]])
    elif kind == "treasure":
        item = Treasure(TreasureType[data["name"]])
        item.gold = data["gold"]
    elif kind == "key":
        item = Key(KeyType[data["name"]])
    else:
        raise ValueError(f"Unknown item kind: {kind}")

    item.set_position(data["x"], data["y"])
    return item


def backpack_from_dict(data):
    b = Backpack()
    b._items = [item_from_dict(d) for d in data["items"]]
    return b


def player_from_dict(data):
    p = Player(data["name"], data["x"], data["y"])
    p._health = data["health"]
    p._max_health = data["max_health"]
    p._strength = data["strength"]
    p._dexterity = data["dexterity"]
    p._is_alive = data["is_alive"]
    p._is_sleeping = data["is_sleeping"]
    p._weapon = item_from_dict(data["weapon"]) if data["weapon"] else None
    p._backpack = backpack_from_dict(data["backpack"])
    p._temp_bonuses = {k: tuple(v) for k, v in data["temp_bonuses"].items()}
    p._statistics = Statistics.from_dict(data["statistics"])
    p._keys = {KeyType[name] for name in data.get("keys", [])}
    p._angle = data.get("angle", 0.0)
    return p


def enemy_from_dict(data):
    e = Enemy(EnemyType[data["type"]], data["x"], data["y"], dungeon_level=1)
    e._health = data["health"]
    e._is_alive = data["is_alive"]
    e._vrability = data["vrability"]
    e._status_chase = data["status_chase"]
    e._has_attacked = data["has_attacked"]
    e._is_resting = data["is_resting"]
    e._disguise_symbol = data.get("disguise_symbol")
    return e


def room_from_dict(data):
    r = Room(data["id"], data["x"], data["y"], data["width"], data["height"])
    r._start_room = data["start_room"]
    r._exit_room = data["exit_room"]
    r._is_visit = data["is_visit"]
    r._exit_cell = tuple(data["exit_cell"]) if data["exit_cell"] else None
    r._enemies = [enemy_from_dict(d) for d in data["enemies"]]
    r._items = [item_from_dict(d) for d in data["items"]]
    return r


def hallway_from_dict(data, rooms_by_id):
    h = Hallway.__new__(Hallway)
    h._start_room = rooms_by_id[data["start_room_id"]]
    h._end_room = rooms_by_id[data["end_room_id"]]
    h._all_rooms = list(rooms_by_id.values())
    h._tiles = {tuple(t) for t in data["tiles"]}
    h._door_color = KeyType[data["door_color"]] if data.get("door_color") else None
    return h


def level_from_dict(data):
    rooms = [room_from_dict(d) for d in data["rooms"]]
    rooms_by_id = {r.id: r for r in rooms}
    hallways = [hallway_from_dict(d, rooms_by_id) for d in data["hallways"]]
    return Level(
        data["number"],
        rooms,
        hallways,
        rooms_by_id[data["start_room_id"]],
        rooms_by_id[data["exit_room_id"]],
    )
