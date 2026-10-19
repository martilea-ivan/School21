import curses

from domain.objects.enum import EnemyType, KeyType
from presentation.raycasting import has_line_of_sight


ITEM_SYMBOLS = {
    'BANANA': 'b',
    'APPLE': 'a',
    'MEAT': 'm',
    'FISH': 'f',
    'EGG': 'e',
    'DAGGER': '/',
    'SPEAR': '|',
    'MACE': 'T',
    'SCROLL_MAX_HP': '?',
    'SCROLL_ST': '?',
    'SCROLL_DEX': '?',
    'ELIXIR_HP': '%',
    'ELIXIR_ST': '%',
    'ELIXIR_DEX': '%',
    'SILVER_COIN': '$',
    'GOLD_COIN': '$',
    'RUBY': '*',
    'DRAGON_GEM': '&',
    'RED': 'k',
    'BLUE': 'k',
    'GREEN': 'k',
}

ITEM_COLORS = {
    'BANANA': 20,
    'APPLE': 21,
    'MEAT': 21,
    'FISH': 22,
    'EGG': 23,
    'DAGGER': 23,
    'SPEAR': 23,
    'MACE': 23,
    'SCROLL_MAX_HP': 24,
    'SCROLL_ST': 20,
    'SCROLL_DEX': 25,
    'ELIXIR_HP': 21,
    'ELIXIR_ST': 20,
    'ELIXIR_DEX': 25,
    'SILVER_COIN': 23,
    'GOLD_COIN': 20,
    'RUBY': 21,
    'DRAGON_GEM': 24,
    'RED': 21,
    'BLUE': 22,
    'GREEN': 25,
}


class MapRenderer:

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._height, self._width = stdscr.getmaxyx()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self._init_colors()

    def _init_colors(self):
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(4, curses.COLOR_WHITE, -1)
        curses.init_pair(5, curses.COLOR_YELLOW, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        curses.init_pair(7, curses.COLOR_YELLOW, -1)
        curses.init_pair(8, curses.COLOR_MAGENTA, -1)
        curses.init_pair(9, curses.COLOR_CYAN, -1)

        curses.init_pair(20, curses.COLOR_YELLOW, -1)
        curses.init_pair(21, curses.COLOR_RED, -1)
        curses.init_pair(22, curses.COLOR_CYAN, -1)
        curses.init_pair(23, curses.COLOR_WHITE, -1)
        curses.init_pair(24, curses.COLOR_MAGENTA, -1)
        curses.init_pair(25, curses.COLOR_GREEN, -1)

    def render(self, player, level, message=""):
        self._stdscr.erase()

        view_h = self._height - 4
        view_w = self._width

        cam_x = player.x - view_w // 2
        cam_y = player.y - view_h // 2

        self._draw_world(level, player, cam_x, cam_y, view_w, view_h)
        self._draw_status(player, level)
        self._draw_message(message)
        self._draw_controls()

        self._update_seen(level, player)

        self._stdscr.refresh()

    def _draw_world(self, level, player, cam_x, cam_y, view_w, view_h):
        for room in level.rooms:
            self._draw_room(room, level, player, cam_x, cam_y, view_w, view_h)

        for hallway in level.hallways:
            self._draw_hallway(hallway, cam_x, cam_y, view_w, view_h)
            self._draw_door(hallway, level, cam_x, cam_y, view_w, view_h)

        for room in level.rooms:
            for item in room.items:
                self._draw_item(item, level, player, cam_x, cam_y, view_w, view_h)
            for enemy in room.enemies:
                if enemy.is_alive:
                    self._draw_enemy(enemy, level, player, cam_x, cam_y, view_w, view_h)

        for room in level.rooms:
            if room.exit_cell is not None and room.is_visit:
                self._put(room.exit_cell[0], room.exit_cell[1],
                          cam_x, cam_y, view_w, view_h, '0',
                          curses.color_pair(9) | curses.A_BOLD)

        px = player.x - cam_x
        py = player.y - cam_y
        if 0 <= px < view_w and 0 <= py < view_h:
            self._safe_addch(py, px, '@',
                             curses.color_pair(7) | curses.A_BOLD)

    def _update_seen(self, level, player):
        for room in level.rooms:
            if not room.is_visit:
                continue
            for y in range(room.y, room.y + room.height):
                for x in range(room.x, room.x + room.width):
                    if self._is_visible_cell(level, player, x, y):
                        room.mark_seen(x, y)

    def _draw_room(self, room, level, player, cam_x, cam_y, view_w, view_h):
        if not room.is_visit:
            return

        is_current = self._is_current_room(player, room)
        in_adjacent_hallway = self._is_player_in_adjacent_hallway(level, player, room)

        # Если игрок рядом — комната видна ЦЕЛИКОМ
        fully_visible = is_current or in_adjacent_hallway

        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                is_wall = self._is_wall(room, x, y)

                if fully_visible:
                    if is_wall:
                        self._put(x, y, cam_x, cam_y, view_w, view_h, '#',
                                  curses.color_pair(1))
                    else:
                        self._put(x, y, cam_x, cam_y, view_w, view_h, '.')
                else:
                    if is_wall:
                        self._put(x, y, cam_x, cam_y, view_w, view_h, '#',
                                  curses.color_pair(1))

    def _is_wall(self, room, x, y):
        return (x == room.x or x == room.x + room.width - 1 or
                y == room.y or y == room.y + room.height - 1)

    def _draw_hallway(self, hallway, cam_x, cam_y, view_w, view_h):
        if not hallway.start_room.is_visit and not hallway.end_room.is_visit:
            return

        for (x, y) in hallway.tiles:
            if self._in_room(hallway, x, y):
                continue
            self._put(x, y, cam_x, cam_y, view_w, view_h, '.')

    def _in_room(self, hallway, x, y):
        for room in (hallway.start_room, hallway.end_room):
            if (room.x <= x < room.x + room.width and
                    room.y <= y < room.y + room.height):
                return True
        return False

    def _is_current_room(self, player, room):
        return (room.x <= player.x < room.x + room.width and
                room.y <= player.y < room.y + room.height)

    def _draw_door(self, hallway, level, cam_x, cam_y, view_w, view_h):
        if hallway.door_color is None:
            return

        door_cell = hallway.door_cell
        if door_cell is None:
            return

        x, y = door_cell
        color = self._door_color_pair(hallway.door_color)
        self._put(x, y, cam_x, cam_y, view_w, view_h, '+',
                  curses.color_pair(color) | curses.A_BOLD)

    def _door_color_pair(self, door_color):
        mapping = {
            KeyType.RED: 21,
            KeyType.BLUE: 22,
            KeyType.GREEN: 25,
        }
        return mapping.get(door_color, 1)

    def _is_in_corridor(self, level, x, y):
        for hallway in level.hallways:
            if (x, y) in hallway.tiles and not self._in_room(hallway, x, y):
                return True
        return False

    def _is_player_in_adjacent_hallway(self, level, player, room):
        """Игрок в коридоре, соединяющем эту комнату?"""
        for hallway in level.hallways:
            if hallway.start_room.id == room.id or hallway.end_room.id == room.id:
                if (player.x, player.y) in hallway.tiles:
                    if not self._in_room(hallway, player.x, player.y):
                        return True
        return False

    def _is_visible_cell(self, level, player, x, y):
        """
        True, если клетка (x, y) видна игроку.
        Использует Ray Casting от игрока до клетки.
        """
        room = level.get_room_at(x, y)

        if room is not None and not room.is_visit:
            return False

        # Игрок в той же комнате — видно всё
        if room is not None and self._is_current_room(player, room):
            return True

        # Игрок в коридоре рядом с комнатой — Ray Casting
        if room is not None and self._is_player_in_adjacent_hallway(level, player, room):
            return has_line_of_sight(level, player.x, player.y, x, y)

        # Игрок в том же коридоре — Ray Casting
        for hallway in level.hallways:
            if (x, y) in hallway.tiles:
                if (player.x, player.y) in hallway.tiles:
                    return has_line_of_sight(level, player.x, player.y, x, y)

        return False

    def _draw_item(self, item, level, player, cam_x, cam_y, view_w, view_h):
        if not self._is_visible_cell(level, player, item.x, item.y):
            return
        sym = ITEM_SYMBOLS.get(item.name, '?')
        pair = ITEM_COLORS.get(item.name, 8)
        self._put(item.x, item.y, cam_x, cam_y, view_w, view_h,
                  sym, curses.color_pair(pair))

    def _is_player_close(self, player, enemy):
        """Игрок рядом с врагом (в радиусе 2 клеток)?"""
        return abs(player.x - enemy.x) + abs(player.y - enemy.y) <= 2

    def _draw_enemy(self, enemy, level, player, cam_x, cam_y, view_w, view_h):
        if not enemy.is_alive:
            return
        if not self._is_visible_cell(level, player, enemy.x, enemy.y):
            return

        if enemy.enemy_type == EnemyType.MIMIC:
            close = self._is_player_close(player, enemy)
            if close:
                # Проявился — рисуем как врага
                pair = self._enemy_pair(enemy.enemy_type)
                self._put(enemy.x, enemy.y, cam_x, cam_y, view_w, view_h,
                          enemy.symbol, curses.color_pair(pair))
            else:
                # Прикидывается предметом
                sym = enemy.disguise_symbol or '?'
                self._put(enemy.x, enemy.y, cam_x, cam_y, view_w, view_h,
                          sym, curses.color_pair(8))
            return

        pair = self._enemy_pair(enemy.enemy_type)
        self._put(enemy.x, enemy.y, cam_x, cam_y, view_w, view_h,
                  enemy.symbol, curses.color_pair(pair))

    def _enemy_pair(self, enemy_type):
        mapping = {
            EnemyType.ZOMBI: 2,
            EnemyType.VAMPIRE: 3,
            EnemyType.PHANTOM: 4,
            EnemyType.ORGE: 5,
            EnemyType.SNACE_MAGE: 6,
            EnemyType.MIMIC: 4,
        }
        return mapping.get(enemy_type, 1)

    def _put(self, x, y, cam_x, cam_y, view_w, view_h, ch, attr=0):
        sx = x - cam_x
        sy = y - cam_y
        if 0 <= sx < view_w and 0 <= sy < view_h:
            self._safe_addch(sy, sx, ch, attr)

    def _draw_status(self, player, level):
        line = self._height - 3
        weapon = player.weapon.name if player.weapon else "нет"
        keys = " ".join(k.name[0] for k in player.keys) if player.keys else "нет"
        status = (f" Уровень: {level.number} | HP: {player.health}/{player.max_health}"
                  f" | ST: {player.strength} | DEX: {player.dexterity}"
                  f" | Золото: {player.gold} | Оружие: {weapon} | Ключи: {keys} ")
        self._safe_addstr(line, 0, status[:self._width - 1], curses.color_pair(9))

    def _draw_message(self, message):
        line = self._height - 2
        self._safe_addstr(line, 0, message[:self._width - 1])

    def _draw_controls(self):
        line = self._height - 1
        controls = " WASD-движение | H-оружие | J-еда | K-эликсир | E-свиток | Q-выход "
        self._safe_addstr(line, 0, controls[:self._width - 1])

    def _safe_addch(self, y, x, ch, attr=0):
        try:
            self._stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass

    def _safe_addstr(self, y, x, text, attr=0):
        try:
            self._stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass