import curses


MENU_ITEMS = [
    ("new", "Начать игру"),
    ("load", "Загрузить игру"),
    ("records", "Таблица рекордов"),
    ("exit", "Выход"),
]


def show_main_menu(stdscr, has_save):
    cursor = 0

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        title = "ROGUE"
        stdscr.addstr(height // 2 - 5, (width - len(title)) // 2, title,
                      curses.A_BOLD)

        for i, (key, label) in enumerate(MENU_ITEMS):
            if key == "load" and not has_save:
                continue
            marker = "> " if i == cursor else "  "
            line = marker + label
            y = height // 2 - 2 + i
            x = (width - len(line)) // 2
            stdscr.addstr(y, x, line)

        stdscr.refresh()

        key = stdscr.get_wch()

        if key in ('w', 'W', 'ц', 'Ц', curses.KEY_UP):
            cursor = (cursor - 1) % len(MENU_ITEMS)
            if MENU_ITEMS[cursor][0] == "load" and not has_save:
                cursor = (cursor - 1) % len(MENU_ITEMS)
        elif key in ('s', 'S', 'ы', 'Ы', curses.KEY_DOWN):
            cursor = (cursor + 1) % len(MENU_ITEMS)
            if MENU_ITEMS[cursor][0] == "load" and not has_save:
                cursor = (cursor + 1) % len(MENU_ITEMS)
        elif key in ('d', 'D', 'в', 'В', 10, 13, '\n', curses.KEY_RIGHT):
            return MENU_ITEMS[cursor][0]
        elif key in ('q', 'Q', 'й', 'Й', 27):
            return "exit"