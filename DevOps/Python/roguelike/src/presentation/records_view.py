import curses

from datalayer import save


def _draw_detail(stdscr, r):
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    title = "ДЕТАЛИ РЕКОРДА"
    stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

    lines = [
        f"Имя:         {r['name']}",
        f"Уровень:     {r['level']}",
        f"Золото:      {r['gold']}",
        f"Убийств:     {r.get('enemies_killed', 0)}",
        f"Еда:         {r.get('food_eaten', 0)}",
        f"Эликсир:     {r.get('elixirs_drunk', 0)}",
        f"Свитки:      {r.get('scrolls_read', 0)}",
        f"Ударов:      {r.get('hits_dealt', 0)}",
        f"Промахов:    {r.get('hits_missed', 0)}",
        f"Клеток:      {r.get('cells_moved', 0)}",
        f"Собрано:     {r.get('treasures_collected', 0)}",
        f"Потеряно HP: {r.get('hp_lost', 0)}",
        f"Уровней:     {r.get('levels_passed', 0)}",
        f"Смертей:     {r.get('deaths', 0)}",
    ]

    for i, line in enumerate(lines):
        stdscr.addstr(3 + i, 2, line)

    stdscr.addstr(height - 2, 2, "Нажмите любую клавишу для выхода")
    stdscr.refresh()
    stdscr.get_wch()


def show_records(stdscr):
    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        title = "ТАБЛИЦА РЕКОРДОВ"
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        records = save.get_top_records(10)

        if not records:
            stdscr.addstr(3, 2, "Пока нет рекордов")
        else:
            header = f"{'#':<4}{'Имя':<15}{'Ур':<4}{'Золото':<8}"
            stdscr.addstr(3, 2, header, curses.A_BOLD)
            for i, r in enumerate(records, 1):
                line = f"{i:<4}{r['name']:<15}{r['level']:<4}{r['gold']:<8}"
                stdscr.addstr(3 + i, 2, line)

        stdscr.addstr(height - 2, 2, "1-9 — детали записи | Другая клавиша — выход")
        stdscr.refresh()

        key = stdscr.get_wch()
        if key in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            idx = int(key) - 1
            if 0 <= idx < len(records):
                _draw_detail(stdscr, records[idx])
                continue
        return