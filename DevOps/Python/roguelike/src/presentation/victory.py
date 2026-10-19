import curses


def show_victory(stdscr, player, level):
    curses.flushinp()
    stdscr.erase()

    height, width = stdscr.getmaxyx()

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(30, curses.COLOR_YELLOW, -1)
    curses.init_pair(31, curses.COLOR_CYAN, -1)
    curses.init_pair(32, curses.COLOR_GREEN, -1)

    box_w = 50
    box_h = 13
    start_y = (height - box_h) // 2
    start_x = (width - box_w) // 2

    top = "╔" + "═" * (box_w - 2) + "╗"
    bottom = "╚" + "═" * (box_w - 2) + "╝"

    stdscr.addstr(start_y, start_x, top, curses.color_pair(30) | curses.A_BOLD)

    for i in range(1, box_h - 1):
        stdscr.addstr(start_y + i, start_x, "║", curses.color_pair(30))
        stdscr.addstr(start_y + i, start_x + box_w - 1, "║", curses.color_pair(30))

    stdscr.addstr(start_y + box_h - 1, start_x, bottom,
                  curses.color_pair(30) | curses.A_BOLD)

    stars = "П О З Д Р А В Л Я Е М"
    stdscr.addstr(start_y + 2, start_x + (box_w - len(stars)) // 2,
                  stars, curses.color_pair(30) | curses.A_BOLD)

    title = "П О Б Е Д А"
    stdscr.addstr(start_y + 4, start_x + (box_w - len(title)) // 2,
                  title, curses.color_pair(30) | curses.A_BOLD)

    sub = "Вы прошли все 21 уровень!"
    stdscr.addstr(start_y + 6, start_x + (box_w - len(sub)) // 2,
                  sub, curses.color_pair(30))

    stats = [
        f"Имя:     {player.name}",
        f"Уровень: {level.number}",
        f"Золото:  {player.gold}",
    ]
    for i, line in enumerate(stats):
        stdscr.addstr(start_y + 8 + i, start_x + (box_w - len(line)) // 2,
                      line, curses.color_pair(30))

    hint = "Нажмите любую клавишу..."
    stdscr.addstr(start_y + box_h + 3, start_x + (box_w - len(hint)) // 2,
                  hint, curses.color_pair(32))

    stdscr.refresh()

    while True:
        k = stdscr.get_wch()
        if k:
            break