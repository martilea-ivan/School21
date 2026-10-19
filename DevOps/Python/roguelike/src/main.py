import curses
import math

from domain.logic.level_generator import LevelGenerator
from domain.logic.logic_game import GameEngine
from domain.logic import logic_environment as env
from domain.objects.player import Player
from domain.objects.level import Level
from domain.objects.enum import ItemType
from datalayer import save
from presentation.map_renderer import MapRenderer
from presentation.renderer_3d import Renderer3D
from presentation.menu import show_main_menu
from presentation.records_view import show_records
from presentation.name_input import ask_name
from presentation.victory import show_victory


def main(stdscr):
    stdscr.keypad(True)
    curses.curs_set(0)

    while True:
        choice = show_main_menu(stdscr, save.has_save())

        if choice == "exit":
            break
        elif choice == "new":
            name = ask_name(stdscr)
            run_game(stdscr, name=name, load=False)
        elif choice == "load":
            run_game(stdscr, name=None, load=True)
        elif choice == "records":
            show_records(stdscr)


def run_game(stdscr, name=None, load=False):
    gen = LevelGenerator()
    engine = GameEngine()
    renderer = MapRenderer(stdscr)
    renderer_3d = Renderer3D(stdscr)
    use_3d = False

    if load:
        data = save.load_game()
        if data is None:
            return
        player, level = data
    else:
        level = gen.generate(21)
        level.start_room.mark_visited()
        cx, cy = level.start_room.get_center()
        player = Player(name, cx, cy)

    message = "Добро пожаловать!"

    while True:
        if use_3d:
            renderer_3d.render(player, level, message)
        else:
            renderer.render(player, level, message)

        key = stdscr.get_wch()
        message = ""
        direction = None

        # Переключение режима
        if key in ('v', 'V', 'м', 'М'):
            use_3d = not use_3d
            continue

        # 3D-управление
        if use_3d:
            if key in ('w', 'W', 'ц', 'Ц'):
                dx = int(round(math.cos(player.angle)))
                dy = int(round(math.sin(player.angle)))
                direction = (dx, dy)
            elif key in ('s', 'S', 'ы', 'Ы'):
                dx = -int(round(math.cos(player.angle)))
                dy = -int(round(math.sin(player.angle)))
                direction = (dx, dy)
            elif key in ('a', 'A', 'ф', 'Ф'):
                player.angle -= 0.2
                continue
            elif key in ('d', 'D', 'в', 'В'):
                player.angle += 0.2
                continue
            elif key in ('q', 'Q', 'й', 'Й'):
                save.save_game(player, level)
                return
            else:
                continue
        else:
            # 2D-управление
            if key in ('w', 'W', 'ц', 'Ц', curses.KEY_UP):
                direction = (0, -1)
            elif key in ('s', 'S', 'ы', 'Ы', curses.KEY_DOWN):
                direction = (0, 1)
            elif key in ('a', 'A', 'ф', 'Ф', curses.KEY_LEFT):
                direction = (-1, 0)
            elif key in ('d', 'D', 'в', 'В', curses.KEY_RIGHT):
                direction = (1, 0)
            elif key in ('q', 'Q', 'й', 'Й'):
                save.save_game(player, level)
                message = "Игра сохранена. Выход..."
                renderer.render(player, level, message)
                stdscr.getch()
                return
            elif key in ('h', 'H', 'р', 'Р'):
                message = _pick_and_use(stdscr, renderer, player, level, ItemType.WEAPON)
                continue
            elif key in ('j', 'J', 'о', 'О'):
                message = _pick_and_use(stdscr, renderer, player, level, ItemType.FOOD)
                continue
            elif key in ('k', 'K', 'л', 'Л'):
                message = _pick_and_use(stdscr, renderer, player, level, ItemType.ELIXIR)
                continue
            elif key in ('e', 'E', 'у', 'У'):
                message = _pick_and_use(stdscr, renderer, player, level, ItemType.SCROLL)
                continue
            else:
                continue

        engine.process_turn(player, level, direction)

        if not player.is_alive:
            player.statistics.add_death()
            save.add_record(player.name, level.number, player.gold, player.statistics)
            renderer.render(player, level, "Вы погибли! Нажмите любую клавишу...")
            stdscr.getch()
            return

        if engine.check_exit(player, level):
            if level.number >= 21:
                save.add_record(player.name, level.number, player.gold, player.statistics)
                show_victory(stdscr, player, level)
                return
            level = gen.generate(level.number + 1, player=player)
            level.start_room.mark_visited()
            cx, cy = level.start_room.get_center()
            player.x = cx
            player.y = cy
            player.clear_keys()
            player.statistics.add_level_passed()
            message = f"Уровень {level.number}!"
            continue


def _pick_and_use(stdscr, renderer, player, level, item_type):
    items = player.backpack.get_items_by_type(item_type)

    if item_type == ItemType.WEAPON and not items and player.weapon is None:
        return "В рюкзаке нет оружия"

    if item_type != ItemType.WEAPON and not items:
        return "В рюкзаке нет таких предметов"

    idx = _select_item(stdscr, renderer, player, level, items, item_type)

    if idx is None:
        return "Отменено"

    if idx == -1:
        old = player.weapon
        if old is None:
            return "Оружие и так не в руках"
        env._drop_to_neighbor(player, old, level)
        player._weapon = None
        return f"Оружие снято: {old.name}"

    item = items[idx]

    if item_type == ItemType.WEAPON:
        env.use_weapon(player, item, level)
        return f"Взято в руки: {item.name}"
    if item_type == ItemType.FOOD:
        env.use_food(player, item)
        return f"Съедено: {item.name}"
    if item_type == ItemType.ELIXIR:
        env.use_elixir(player, item)
        return f"Выпито: {item.name}"
    if item_type == ItemType.SCROLL:
        env.use_scroll(player, item)
        return f"Прочитано: {item.name}"

    return ""


def _select_item(stdscr, renderer, player, level, items, item_type):
    allow_unequip = (item_type == ItemType.WEAPON)

    while True:
        hint = f"Выберите {item_type.value} (1-{min(len(items), 9)})"
        if allow_unequip:
            hint += " | 0 — снять оружие"
        hint += " | Q — отмена"
        renderer.render(player, level, hint)
        _draw_menu(stdscr, items, allow_unequip)
        stdscr.refresh()

        key = stdscr.get_wch()

        if key in ('q', 'Q', 'й', 'Й', 27):
            return None

        if allow_unequip and key == '0':
            return -1   # специальный код: снять оружие

        if key in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            idx = int(key) - 1
            if 0 <= idx < len(items):
                return idx


def _draw_menu(stdscr, items, allow_unequip=False):
    height, width = stdscr.getmaxyx()
    rows = len(items)
    box_h = rows + (3 if allow_unequip else 2)
    box_w = 44
    start_y = (height - box_h) // 2
    start_x = (width - box_w) // 2

    for i in range(box_h):
        stdscr.addstr(start_y + i, start_x, " " * box_w)

    stdscr.addstr(start_y, start_x, "+" + "-" * (box_w - 2) + "+")

    for i, item in enumerate(items):
        num = i + 1
        line = f" {num}. {item.name}"
        stdscr.addstr(start_y + 1 + i, start_x,
                      "|" + line.ljust(box_w - 2) + "|")

    if allow_unequip:
        line = " 0. Снять оружие"
        stdscr.addstr(start_y + 1 + rows, start_x,
                      "|" + line.ljust(box_w - 2) + "|")

    stdscr.addstr(start_y + box_h - 1, start_x,
                  "+" + "-" * (box_w - 2) + "+")


if __name__ == "__main__":
    curses.wrapper(main)