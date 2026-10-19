import random

from domain.objects.room import Room
from domain.objects.hallway import Hallway
from domain.objects.level import Level
from domain.objects.enemy import Enemy
from domain.objects.enum import (
    GenerationConfig, EnemyType, ItemType, KeyType,
    FoodType, WeaponType, ScrollType, ElixirType,
)
from domain.objects.items.food import Food
from domain.objects.items.weapon import Weapon
from domain.objects.items.scroll import Scroll
from domain.objects.items.elixir import Elixir
from domain.objects.items.key import Key
from domain.logic.difficulty import DifficultyManager


class LevelGenerator:

    def __init__(self):
        self._cfg = GenerationConfig

    def generate(self, level_number, player=None):
        for _ in range(10):
            level = self._try_generate(level_number, player)
            if level is not None:
                return level
        raise RuntimeError("Не удалось сгенерировать уровень за 10 попыток")

    def _try_generate(self, level_number, player=None):
        rooms = self._generate_rooms()
        if rooms is None:
            return None

        start_room = rooms[0]
        exit_room = rooms[8]
        start_room.start_room = True
        exit_room.exit_room = True
        exit_room.exit_cell = exit_room.get_center()

        hallways = self._connect_rooms(rooms)
        if hallways is None:
            return None

        if level_number >= 2:
            if not self._assign_doors_and_keys(rooms, hallways, start_room, exit_room):
                return None

        self._populate_rooms(rooms, start_room, level_number, player)

        return Level(level_number, rooms, hallways, start_room, exit_room)

    def _generate_rooms(self):
        cfg = self._cfg
        section_w = cfg.MAP_WIDTH.value // 3
        section_h = cfg.MAP_HEIGHT.value // 3
        padding = cfg.PADDING.value
        min_size = cfg.MIN_ROOM_SIZE.value
        max_size = cfg.MAX_ROOM_SIZE.value

        max_w = section_w - 2 * padding
        max_h = section_h - 2 * padding

        rooms = []
        for i in range(cfg.ROOM_COUNT.value):
            col = i % 3
            row = i // 3
            sec_x = col * section_w
            sec_y = row * section_h

            width = random.randint(min_size, min(max_size, max_w))
            height = random.randint(min_size, min(max_size, max_h))

            x = random.randint(sec_x + padding, sec_x + section_w - padding - width)
            y = random.randint(sec_y + padding, sec_y + section_h - padding - height)

            rooms.append(Room(i, x, y, width, height))

        return rooms

    def _connect_rooms(self, rooms):
        n = len(rooms)
        parent = list(range(n))

        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            parent[ra] = rb
            return True

        hallways = []

        for _ in range(500):
            if len({find(i) for i in range(n)}) == 1:
                break

            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            if i == j or find(i) == find(j):
                continue

            h = Hallway(rooms[i], rooms[j], rooms)
            if not h.tiles:
                continue

            hallways.append(h)
            union(i, j)
        else:
            return None

        return hallways

    def _populate_rooms(self, rooms, start_room, level_number, player=None):
        cfg = self._cfg

        enemy_chance = min(
            cfg.BASE_ENEMY_CHANCE.value
            + cfg.ENEMY_CHANCE_INCREMENT.value * level_number,
            cfg.MAX_ENEMY_CHANCE.value,
        )
        item_chance = max(
            cfg.MIN_ITEM_CHANCE.value,
            cfg.BASE_ITEM_CHANCE.value
            - cfg.ITEM_CHANCE_DECREMENT.value * level_number,
        )

        if player is not None:
            enemy_mod, item_mod = DifficultyManager.get_modifiers(player)
            enemy_chance = min(cfg.MAX_ENEMY_CHANCE.value, enemy_chance * enemy_mod)
            item_chance = max(cfg.MIN_ITEM_CHANCE.value, item_chance * item_mod)

        for room in rooms:
            if room is start_room:
                continue
            self._populate_enemies(room, enemy_chance, cfg, level_number)
            self._populate_items(room, item_chance, cfg, level_number)

    def _populate_enemies(self, room, enemy_chance, cfg, level_number):
        max_enemies = min(
            cfg.MAX_ENEMIES_PER_ROOM_BASE.value
            + int(cfg.MAX_ENEMIES_PER_ROOM_INCREMENT.value * level_number),
            cfg.MAX_ENEMIES_PER_ROOM_ABSOLUTE.value,
        )

        for _ in range(max_enemies):
            if random.random() > enemy_chance:
                continue
            cell = room.get_random_free_cell()
            if cell is None:
                break

            # 15% шанс мимика
            if random.random() < 0.15:
                enemy_type = EnemyType.MIMIC
            else:
                enemy_type = random.choice([e for e in EnemyType if e != EnemyType.MIMIC])

            enemy = Enemy(enemy_type, cell[0], cell[1], level_number)
            room.enemies.append(enemy)

    def _populate_items(self, room, item_chance, cfg, level_number):
        max_items = min(
            cfg.MAX_ITEMS_PER_ROOM_BASE.value
            + int(cfg.MAX_ITEMS_PER_ROOM_INCREMENT.value * level_number),
            cfg.MAX_ITEMS_PER_ROOM_ABSOLUTE.value,
        )

        for _ in range(max_items):
            if random.random() > item_chance:
                continue
            cell = room.get_random_free_cell()
            if cell is None:
                break
            item = self._random_item()
            item.set_position(cell[0], cell[1])
            room.items.append(item)

    def _random_item(self):
        kind = random.choice(list(ItemType))
        if kind == ItemType.FOOD:
            return Food(random.choice(list(FoodType)))
        if kind == ItemType.WEAPON:
            return Weapon(random.choice(list(WeaponType)))
        if kind == ItemType.SCROLL:
            return Scroll(random.choice(list(ScrollType)))
        return Elixir(random.choice(list(ElixirType)))

    @staticmethod
    def _bfs_reachable(rooms, hallways, start_room, opened_colors=None):
        """
        BFS от start_room. Возвращает set id доступных комнат.
        opened_colors — set цветов дверей, которые можно открыть.
        """
        if opened_colors is None:
            opened_colors = set()

        visited = {start_room.id}
        queue = [start_room]

        while queue:
            room = queue.pop(0)

            for h in hallways:
                if h.start_room.id != room.id and h.end_room.id != room.id:
                    continue

                if h.door_color is not None and h.door_color not in opened_colors:
                    continue

                neighbor = h.end_room if h.start_room.id == room.id else h.start_room
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor)

        return visited

    @staticmethod
    def _all_rooms_reachable(rooms, hallways, start_room, opened_colors=None):
        """True, если ВСЕ комнаты достижимы."""
        reachable = LevelGenerator._bfs_reachable(rooms, hallways, start_room, opened_colors)
        return len(reachable) == len(rooms)

    def _assign_doors_and_keys(self, rooms, hallways, start_room, exit_room):
        """
        Назначает 2 двери (2 цвета) и размещает ключи.
        Возвращает True, если удалось, False — если нужна перегенерация.
        """
        colors = random.sample([KeyType.RED, KeyType.BLUE, KeyType.GREEN], 2)

        placed_keys = []
        key_rooms = []
        assigned_hallways = []

        for color in colors:
            candidates = [h for h in hallways if h.door_color is None]
            random.shuffle(candidates)

            placed = False
            for h in candidates:
                h._door_color = color

                key_room = self._pick_key_room(rooms, hallways, start_room,
                                                placed_keys, color, exit_room)
                if key_room is not None:
                    placed_keys.append(color)
                    key_rooms.append(key_room)
                    assigned_hallways.append(h)
                    placed = True
                    break
                else:
                    h._door_color = None

            if not placed:
                for h in assigned_hallways:
                    h._door_color = None
                return False

        for color, room in zip(placed_keys, key_rooms):
            cell = room.get_random_free_cell()
            if cell is None:
                for h in assigned_hallways:
                    h._door_color = None
                return False
            key = Key(color)
            key.set_position(cell[0], cell[1])
            room.items.append(key)

        opened = set(placed_keys)
        if not self._all_rooms_reachable(rooms, hallways, start_room, opened):
            for h in assigned_hallways:
                h._door_color = None
            return False

        return True

    def _pick_key_room(self, rooms, hallways, start_room, placed_keys, new_color, exit_room):
        """
        Выбирает комнату для ключа цвета new_color.
        Возвращает Room или None.
        """
        # Доступные комнаты без нового ключа
        reachable = self._bfs_reachable(rooms, hallways, start_room, set(placed_keys))

        # Исключаем стартовую и выходную
        candidates = [r for r in rooms
                      if r.id in reachable and r is not start_room and r is not exit_room]

        if not candidates:
            return None

        return random.choice(candidates)