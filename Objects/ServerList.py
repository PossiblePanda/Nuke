import curses, Objects.LineBreak, Objects.BindList
import curses.ascii

def drawServerList(screen, servers: list[dict]):
    width = curses.COLS - Objects.BindList.width
    for i in range(len(servers)):
        server = servers[i]
        offset = i*3

        screen.addstr(offset + 2, 0, f"{server['ip']}:{server['port']} - {i+1}")
        screen.addstr(offset + 3, 0, f"Username: {server["username"]}")
        screen.addstr(offset + 4, 0, f"{"═"*(width)}")

        if Objects.BindList.furthest_offset > offset + 4:
            screen.addstr(offset+4, width, "╬")
