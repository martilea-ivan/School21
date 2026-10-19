from domain.objects.enum import ItemType


def pickup(player, item, room):
    if item.type == ItemType.KEY:
        item.use(player)
        room.items.remove(item)
        return True

    if player.backpack.add_item(item):
        room.items.remove(item)
        return True
    return False


def use_food(player, item):
    item.use(player)
    player.backpack.remove_item(item)
    player.statistics.add_food_eaten()


def use_elixir(player, item):
    item.use(player)
    player.backpack.remove_item(item)
    player.statistics.add_elixir_drunk()


def use_scroll(player, item):
    item.use(player)
    player.backpack.remove_item(item)
    player.statistics.add_scroll_read()


def use_weapon(player, item, level):
    old = player.weapon
    if old is not None:
        _drop_to_neighbor(player, old, level)
    item.use(player)
    player.backpack.remove_item(item)


def drop_item(player, item, level):
    if _drop_to_neighbor(player, item, level):
        player.backpack.remove_item(item)
        return True
    return False


def _drop_to_neighbor(player, item, level):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = player.x + dx, player.y + dy
        if not level.is_walkable(nx, ny):
            continue
        room = level.get_room_at(nx, ny)
        if room is None:
            continue
        if any(i.x == nx and i.y == ny for i in room.items):
            continue
        item.set_position(nx, ny)
        room.items.append(item)
        return True
    return False