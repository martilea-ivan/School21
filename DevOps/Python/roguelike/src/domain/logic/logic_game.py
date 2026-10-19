import random

from domain.objects.enum import EnemyType, TreasureType, KeyType
from domain.objects.items.treasure import Treasure
from domain.logic import logic_environment as env


class GameEngine:

    def __init__(self):
        pass

    # ==================== ГЛАВНЫЙ ХОД ====================

    def process_turn(self, player, level, direction):
        if player.is_sleeping:
            player.is_sleeping = False
        else:
            self._player_action(player, level, direction)

        self._move_all_enemies(player, level)
        player.tick_temp_bonuses()

        if player.health <= 0 and player.is_alive:
            player._health = 1

    def _can_pass_door(self, player, level, nx, ny):
        for hallway in level.hallways:
            if hallway.door_color is None:
                continue

            door_cell = hallway.door_cell
            if door_cell is None:
                continue

            if (nx, ny) == door_cell:
                return player.has_key(hallway.door_color)

            if (player.x, player.y) == door_cell:
                return player.has_key(hallway.door_color)

        return True

    def _player_action(self, player, level, direction):
        nx, ny = player.x + direction[0], player.y + direction[1]

        if not self._can_pass_door(player, level, nx, ny):
            return

        enemy = self._enemy_at(level, nx, ny)
        if enemy is not None:
            self._resolve_combat(player, enemy, level)
            return

        if level.is_walkable(nx, ny):
            player.x = nx
            player.y = ny
            player.statistics.add_cell_moved()
            room = level.get_room_at(nx, ny)
            if room is not None:
                room.mark_visited()
            self._try_pickup(player, level, nx, ny)

    # ==================== ПОИСК ====================

    def _enemy_at(self, level, x, y):
        for room in level.rooms:
            for enemy in room.enemies:
                if enemy.x == x and enemy.y == y and enemy.is_alive:
                    return enemy
        return None

    def _try_pickup(self, player, level, x, y):
        room = level.get_room_at(x, y)
        if room is None:
            return
        for item in room.items:
            if item.x == x and item.y == y:
                env.pickup(player, item, room)
                return

    # ==================== БОЙ ====================

    def _resolve_combat(self, player, enemy, level):
        self._player_attacks(player, enemy, level)
        if not enemy.is_alive:
            return
        self._enemy_attacks(enemy, player)

    def _player_attacks(self, player, enemy, level):
        if enemy.enemy_type == EnemyType.VAMPIRE and not enemy.has_attacked:
            enemy.has_attacked = True
            return

        if not self._hit_check(player, enemy):
            player.statistics.add_hit_missed()
            return

        player.statistics.add_hit_dealt()
        damage = self._calculate_damage(player, enemy)
        self._apply_damage(enemy, damage)

        if not enemy.is_alive:
            self._on_enemy_death(enemy, level, player)

    def _enemy_attacks(self, enemy, player):
        if enemy.enemy_type == EnemyType.ORGE:
            if enemy.is_resting:
                enemy.is_resting = False
                return
            self._apply_damage(player, self._calculate_damage(enemy, player))
            enemy.is_resting = True
            return

        if not self._hit_check(enemy, player):
            return

        damage = self._calculate_damage(enemy, player)
        self._apply_damage(player, damage)

        if enemy.enemy_type == EnemyType.VAMPIRE:
            player.reduce_max_health(2)

        if enemy.enemy_type == EnemyType.SNACE_MAGE:
            if random.random() < 0.30:
                player.is_sleeping = True

    def _hit_check(self, attacker, target):
        atk_dex = attacker.get_effective_dexterity()
        tgt_dex = target.dexterity
        chance = atk_dex / (atk_dex + tgt_dex)
        return random.random() < chance

    def _calculate_damage(self, attacker, target):
        base = attacker.get_effective_strength()
        weapon = getattr(attacker, 'weapon', None)
        if weapon is not None:
            base += weapon.damage
        return base

    def _apply_damage(self, target, damage):
        old_health = target.health
        target.take_damage(damage)
        actual_lost = old_health - target.health

        if hasattr(target, 'statistics'):
            target.statistics.add_hp_lost(actual_lost)

    # ==================== СМЕРТЬ ВРАГА ====================

    def _on_enemy_death(self, enemy, level, player):
        room = level.get_room_at(enemy.x, enemy.y)
        if room is None:
            return

        if enemy not in room.enemies:
            return

        room.enemies.remove(enemy)
        reward = self._enemy_reward(enemy)
        treasure = Treasure(reward)
        treasure.set_position(enemy.x, enemy.y)
        room.items.append(treasure)

        player.statistics.add_enemy_killed()
        player.statistics.add_treasure_collected(reward.value)

    def _enemy_reward(self, enemy):
        power = enemy.strength + enemy.dexterity + enemy.health // 2
        if power >= 25:
            return TreasureType.DRAGON_GEM
        if power >= 18:
            return TreasureType.RUBY
        if power >= 12:
            return TreasureType.GOLD_COIN
        return TreasureType.SILVER_COIN

    # ==================== ДВИЖЕНИЕ ВРАГОВ ====================

    def _move_all_enemies(self, player, level):
        for room in level.rooms:
            for enemy in list(room.enemies):
                if not enemy.is_alive:
                    continue
                self._move_enemy(enemy, player, room, level)

    def _move_enemy(self, enemy, player, room, level):
        dist = abs(enemy.x - player.x) + abs(enemy.y - player.y)
        if dist <= enemy.vrability:
            enemy.status_chase = True

        if enemy.status_chase:
            self._chase_player(enemy, player, level)
        else:
            self._move_by_pattern(enemy, room, level)

    # ==================== ПАТТЕРНЫ ПО ТИПУ ====================

    def _move_by_pattern(self, enemy, room, level):
        if enemy.enemy_type == EnemyType.ZOMBI:
            self._pattern_zombi(enemy, room)
        elif enemy.enemy_type == EnemyType.VAMPIRE:
            self._pattern_vampire(enemy, room, level)
        elif enemy.enemy_type == EnemyType.PHANTOM:
            self._pattern_phantom(enemy, room)
        elif enemy.enemy_type == EnemyType.ORGE:
            self._pattern_orge(enemy, room, level)
        elif enemy.enemy_type == EnemyType.SNACE_MAGE:
            self._pattern_snake(enemy, room, level)

    def _pattern_zombi(self, enemy, room):
        self._random_step(enemy, room, steps=1)

    def _pattern_vampire(self, enemy, room, level):
        self._random_step(enemy, room, steps=1)

    def _pattern_phantom(self, enemy, room):
        cell = room.get_random_free_cell()
        if cell is None:
            return
        enemy.x = cell[0]
        enemy.y = cell[1]

    def _pattern_orge(self, enemy, room, level):
        for _ in range(2):
            self._random_step(enemy, room, steps=1)

    def _pattern_snake(self, enemy, room, level):
        if not hasattr(enemy, '_snake_dir'):
            enemy._snake_dir = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        dx, dy = enemy._snake_dir
        nx, ny = enemy.x + dx, enemy.y + dy

        if not self._in_room(room, nx, ny):
            enemy._snake_dir = (-dx, -dy)
            nx, ny = enemy.x - dx, enemy.y - dy

        if self._in_room(room, nx, ny):
            enemy.x = nx
            enemy.y = ny

    def _random_step(self, enemy, room, steps=1):
        for _ in range(steps):
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = enemy.x + dx, enemy.y + dy
                if self._in_room(room, nx, ny):
                    enemy.x = nx
                    enemy.y = ny
                    break

    def _in_room(self, room, x, y):
        return (room.x + 1 <= x < room.x + room.width - 1 and
                room.y + 1 <= y < room.y + room.height - 1)

    # ==================== ПРЕСЛЕДОВАНИЕ ====================

    def _chase_player(self, enemy, player, level):
        if enemy.enemy_type == EnemyType.PHANTOM:
            self._chase_phantom(enemy, player, level)
            return

        if enemy.enemy_type == EnemyType.SNACE_MAGE:
            self._chase_snake(enemy, player, level)
            return

        dx = 0
        dy = 0
        if player.x > enemy.x:
            dx = 1
        elif player.x < enemy.x:
            dx = -1
        if player.y > enemy.y:
            dy = 1
        elif player.y < enemy.y:
            dy = -1

        for step in [(dx, dy), (dx, 0), (0, dy)]:
            if step == (0, 0):
                continue
            nx, ny = enemy.x + step[0], enemy.y + step[1]
            if (player.x, player.y) == (nx, ny):
                self._enemy_attacks(enemy, player)
                return
            if self._enemy_at(level, nx, ny) is not None:
                continue
            if level.is_walkable(nx, ny):
                enemy.x = nx
                enemy.y = ny
                return

    def _chase_phantom(self, enemy, player, level):
        room = level.get_room_at(player.x, player.y)
        if room is None:
            return
        if enemy.x != player.x or enemy.y != player.y:
            dx = 1 if player.x > enemy.x else (-1 if player.x < enemy.x else 0)
            dy = 1 if player.y > enemy.y else (-1 if player.y < enemy.y else 0)
            nx, ny = enemy.x + dx, enemy.y + dy
            if (player.x, player.y) == (nx, ny):
                self._enemy_attacks(enemy, player)
                return
            if self._in_room(room, nx, ny):
                enemy.x = nx
                enemy.y = ny

    def _chase_snake(self, enemy, player, level):
        dx = 1 if player.x > enemy.x else (-1 if player.x < enemy.x else 0)
        dy = 1 if player.y > enemy.y else (-1 if player.y < enemy.y else 0)
        nx, ny = enemy.x + dx, enemy.y + dy
        if (player.x, player.y) == (nx, ny):
            self._enemy_attacks(enemy, player)
            return
        if level.is_walkable(nx, ny):
            enemy.x = nx
            enemy.y = ny

    def check_exit(self, player, level):
        exit_room = level.exit_room
        if exit_room.exit_cell is None:
            return False
        return (player.x, player.y) == exit_room.exit_cell