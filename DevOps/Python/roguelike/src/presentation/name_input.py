import curses


def ask_name(stdscr):
    curses.curs_set(1)
    stdscr.erase()

    height, width = stdscr.getmaxyx()
    prompt = "Введите имя: "
    y = height // 2
    x = (width - len(prompt) - 20) // 2

    stdscr.addstr(y, x, prompt)
    stdscr.refresh()

    curses.echo()
    try:
        name = stdscr.getstr(y, x + len(prompt), 20).decode("utf-8").strip()
    except Exception:
        name = ""
    curses.noecho()
    curses.curs_set(0)

    if not name:
        name = "Игрок"
    return name