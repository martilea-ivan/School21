import curses
import math

from presentation.map_renderer import ITEM_SYMBOLS, ITEM_COLORS


class Renderer3D:

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._height, self._width = stdscr.getmaxyx()
        self._fov = math.pi / 3        # 60 градусов
        self._max_depth = 20           # дальность
        self._view_width = self._width - 40  # 40 символов под мини-карту

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

        self._draw_3d(player, level)
        self._draw_sprites(player, level, view_w, view_h)
        self._draw_minimap(player, level)
        self._draw_status(player, level)
        self._draw_message(message)
        self._draw_controls()

        self._stdscr.refresh()

    def _draw_3d(self, player, level):
        """Основной 3D-вид от первого лица."""
        view_h = self._height - 4
        view_w = self._width

        angle = player.angle   # ← направление взгляда (0..2π)

        for col in range(view_w):
            # Угол луча
            ray_angle = angle - self._fov / 2 + (col / view_w) * self._fov

            dist, wall_type = self._cast_ray(player, level, ray_angle)

            # Высота стены на экране обратно пропорциональна расстоянию
            if dist > 0:
                line_height = min(int(view_h / dist * 2), view_h)
            else:
                line_height = view_h

            # Символ стены по расстоянию
            if dist < 3:
                ch = '#'
                attr = curses.A_BOLD
            elif dist < 6:
                ch = '='
                attr = curses.A_NORMAL
            elif dist < 12:
                ch = '-'
                attr = curses.A_DIM
            else:
                ch = '.'
                attr = curses.A_DIM

            # Рисуем вертикальную линию
            top = (view_h - line_height) // 2
            bottom = top + line_height
            for row in range(top, bottom):
                if 0 <= row < view_h and 0 <= col < view_w:
                    try:
                        self._stdscr.addch(row, col, ch, attr)
                    except curses.error:
                        pass

    def _cast_ray(self, player, level, angle):

        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        step = 0.1

        x, y = player.x + 0.5, player.y + 0.5

        for dist in [i * step for i in range(1, int(self._max_depth / step))]:
            tx = int(x + cos_a * dist)
            ty = int(y + sin_a * dist)

            if not level.is_walkable(tx, ty):
                return dist, 'wall'

        return self._max_depth, 'floor'

    def _get_cell_char(self, level, x, y, player):
        # Выход?
        for room in level.rooms:
            if room.exit_cell is not None and room.is_visit:
                if room.exit_cell[0] == x and room.exit_cell[1] == y:
                    return '0'

        # Враг?
        for room in level.rooms:
            for enemy in room.enemies:
                if enemy.is_alive and enemy.x == x and enemy.y == y:
                    return enemy.symbol

        # Предмет?
        for room in level.rooms:
            for item in room.items:
                sym = ITEM_SYMBOLS.get(item.name, '?')
                if item.x == x and item.y == y:
                    return sym

        # Дверь?
        for hallway in level.hallways:
            if hallway.door_color is None:
                continue
            door_cell = hallway.door_cell
            if door_cell is not None and door_cell[0] == x and door_cell[1] == y:
                return '+'

        # Комната?
        room = level.get_room_at(x, y)
        if room is not None:
            if not room.is_visit:
                return ' '
            if (x == room.x or x == room.x + room.width - 1 or
                    y == room.y or y == room.y + room.height - 1):
                return '#'
            return '.'

        # Коридор?
        for hallway in level.hallways:
            if (x, y) in hallway.tiles:
                if (player.x, player.y) in hallway.tiles:
                    return '.'
                if hallway.start_room.is_visit or hallway.end_room.is_visit:
                    return '.'
                return ' '

        return ' '

    def _draw_sprites(self, player, level, view_w, view_h):
        """Рисует врагов и предметы как спрайты в 3D."""
        sprites = []

        for room in level.rooms:
            for enemy in room.enemies:
                if enemy.is_alive:
                    sprites.append((enemy.x, enemy.y, enemy.symbol, 'enemy'))

            for item in room.items:
                sym = '*'
                sprites.append((item.x, item.y, sym, 'item'))

            if room.exit_cell is not None and room.is_visit:
                sprites.append((room.exit_cell[0], room.exit_cell[1], '0', 'exit'))

        # Сортируем спрайты по расстоянию — дальние рисуем первыми
        sprites.sort(key=lambda s: -((s[0] - player.x) ** 2 + (s[1] - player.y) ** 2))

        for (sx, sy, sym, kind) in sprites:
            dx = sx - player.x
            dy = sy - player.y

            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 0.5 or dist > self._max_depth:
                continue

            # Угол до спрайта
            angle_to = math.atan2(dy, dx)

            # Разница между углом игрока и углом до спрайта
            diff = angle_to - player.angle
            while diff > math.pi:
                diff -= 2 * math.pi
            while diff < -math.pi:
                diff += 2 * math.pi

            # Если спрайт вне поля зрения — пропускаем
            if abs(diff) > self._fov / 2:
                continue

            # Экранная координата по X
            screen_x = int((diff + self._fov / 2) / self._fov * view_w)
            if not (0 <= screen_x < view_w):
                continue

            # Высота спрайта обратно пропорциональна расстоянию
            sprite_h = min(int(view_h / dist), view_h - 1)
            top = (view_h - sprite_h) // 2

            # Рисуем вертикальную линию спрайта
            for i in range(sprite_h):
                row = top + i
                if 0 <= row < view_h:
                    try:
                        self._stdscr.addch(row, screen_x, sym, curses.A_BOLD)
                    except curses.error:
                        pass

    def _get_cell_with_color(self, level, x, y, player):
        # Выход?
        for room in level.rooms:
            if room.exit_cell is not None and room.is_visit:
                if room.exit_cell[0] == x and room.exit_cell[1] == y:
                    return ('0', curses.color_pair(9) | curses.A_BOLD)

        # Враг?
        for room in level.rooms:
            for enemy in room.enemies:
                if enemy.is_alive and enemy.x == x and enemy.y == y:
                    pair = self._enemy_pair(enemy.enemy_type)
                    return (enemy.symbol, curses.color_pair(pair))

        # Предмет?
        for room in level.rooms:
            for item in room.items:
                if item.x == x and item.y == y:
                    sym = ITEM_SYMBOLS.get(item.name, '?')
                    pair = ITEM_COLORS.get(item.name, 8)
                    return (sym, curses.color_pair(pair))

        # Дверь?
        for hallway in level.hallways:
            if hallway.door_color is None:
                continue
            door_cell = hallway.door_cell
            if door_cell is not None and door_cell[0] == x and door_cell[1] == y:
                pair = self._door_color_pair(hallway.door_color)
                return ('+', curses.color_pair(pair) | curses.A_BOLD)

        # Комната
        room = level.get_room_at(x, y)
        if room is not None:
            if not room.is_visit:
                return (' ', 0)
            if (x == room.x or x == room.x + room.width - 1 or
                    y == room.y or y == room.y + room.height - 1):
                return ('#', curses.color_pair(1))
            return ('.', 0)

        # Коридор
        for hallway in level.hallways:
            if (x, y) in hallway.tiles:
                if (player.x, player.y) in hallway.tiles:
                    return ('.', 0)
                if hallway.start_room.is_visit or hallway.end_room.is_visit:
                    return ('.', 0)
                return (' ', 0)

        return (' ', 0)

    def _enemy_pair(self, enemy_type):
        from domain.objects.enum import EnemyType
        mapping = {
            EnemyType.ZOMBI: 2,
            EnemyType.VAMPIRE: 3,
            EnemyType.PHANTOM: 4,
            EnemyType.ORGE: 5,
            EnemyType.SNACE_MAGE: 6,
            EnemyType.MIMIC: 4,
        }
        return mapping.get(enemy_type, 1)

    def _door_color_pair(self, door_color):
        from domain.objects.enum import KeyType
        mapping = {
            KeyType.RED: 21,
            KeyType.BLUE: 22,
            KeyType.GREEN: 25,
        }
        return mapping.get(door_color, 1)

    def _draw_minimap(self, player, level):
        """Мини-карта в углу экрана."""
        map_w = 30
        map_h = 15
        start_x = self._width - map_w - 1
        start_y = 0

        for dy in range(map_h):
            for dx in range(map_w):
                mx = player.x - map_w // 2 + dx
                my = player.y - map_h // 2 + dy

                sx = start_x + dx
                sy = start_y + dy

                if not (0 <= sx < self._width and 0 <= sy < self._height - 4):
                    continue

                ch, attr = self._get_cell_with_color(level, mx, my, player)

                try:
                    self._stdscr.addch(sy, sx, ch, attr)
                except curses.error:
                    pass

        px = start_x + map_w // 2
        py = start_y + map_h // 2
        try:
            self._stdscr.addch(py, px, '@', curses.color_pair(7) | curses.A_BOLD)
        except curses.error:
            pass

    def _draw_status(self, player, level):
        line = self._height - 3
        weapon = player.weapon.name if player.weapon else "нет"
        keys = " ".join(k.name[0] for k in player.keys) if player.keys else "нет"
        status = (f" [3D] Уровень: {level.number} | HP: {player.health}/{player.max_health}"
                  f" | ST: {player.strength} | DEX: {player.dexterity}"
                  f" | Золото: {player.gold} | Оружие: {weapon} | Ключи: {keys} ")
        try:
            self._stdscr.addstr(line, 0, status[:self._width - 1], curses.color_pair(9))
        except curses.error:
            pass

    def _draw_message(self, message):
        line = self._height - 2
        try:
            self._stdscr.addstr(line, 0, message[:self._width - 1])
        except curses.error:
            pass

    def _draw_controls(self):
        line = self._height - 1
        controls = " [3D] W-вперёд | S-назад | A-влево | D-вправо | V-переключить вид | Q-выход "
        try:
            self._stdscr.addstr(line, 0, controls[:self._width - 1])
        except curses.error:
            pass
