def bresenham_line(x0, y0, x1, y1):
    """Алгоритм Брезенхэма. Возвращает список клеток (x, y)
    от (x0, y0) до (x1, y1), не включая начальную."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0
    while True:
        if (x, y) != (x0, y0):
            points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return points


def has_line_of_sight(level, x0, y0, x1, y1):
    """
    True, если из (x0, y0) видна клетка (x1, y1).
    Идём по линии Брезенхэма. Если на пути стена — False.
    Конечная клетка может быть стеной — её видно.
    """
    line = bresenham_line(x0, y0, x1, y1)

    for (x, y) in line[:-1]:   # не проверяем конечную клетку
        if not _is_transparent(level, x, y):
            return False

    return True


def _is_transparent(level, x, y):
    """True, если клетка прозрачна (пол комнаты или коридор)."""
    if level.get_room_at(x, y) is not None:
        return level.is_walkable(x, y)
    for hallway in level.hallways:
        if (x, y) in hallway.tiles:
            return True
    return False
