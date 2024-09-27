import curses, Objects.LineBreak
import curses.ascii

width = 17
furthest_offset = 0

def drawBindList(screen, binds: list[dict]):
    global furthest_offset
    Objects.LineBreak.drawLineBreak(screen, 1, curses.COLS - width, curses.LINES - 2, "║", "vertical")
    screen.addstr(1, curses.COLS - width, "╦")

    for i in range(len(binds)):
        bind = binds[i]
        offset = i*3

        furthest_offset = len(binds) * 3

        screen.addstr(offset + 2, curses.COLS - width + 1, f" {bind['bind']}")
        screen.addstr(offset + 3, curses.COLS - width + 1, f" {bind['action']}")
        screen.addstr(offset + 4, curses.COLS - width, f"╠{"═"*(width-1)}")
