import curses, Objects.LineBreak
import curses.ascii

width = 17

def drawChannelList(screen, channels: list[str], selected_channel: str, channel_scroll: int):
    Objects.LineBreak.drawLineBreak(screen, 1, curses.COLS - width, curses.LINES - 2, "║", "vertical")
    screen.addstr(1, curses.COLS - width, "╦")
    screen.addstr(curses.LINES - 2, curses.COLS - width, "╩")

    screen.addstr(2, curses.COLS - width + 1, " Channels")
    screen.addstr(3, curses.COLS - width, f"╠{"═"*(width-1)}")

    for i in range(channel_scroll, len(channels)):
        channel = channels[i]
        offset = (i-channel_scroll)*3
        key = channels.index(channel) + 1

        if offset >= curses.LINES - 5:
            return

        lineChar = "╩" if offset + 7 >= curses.LINES - 1 else "╠"
        try:
            if channel == selected_channel:
                screen.addstr(offset + 4, curses.COLS - width + 1, f" #{channel}", curses.A_STANDOUT)
            else:
                screen.addstr(offset + 4, curses.COLS - width + 1, f" #{channel}")
            
            if offset + 7 >= curses.LINES - 1:
                return
            screen.addstr(offset + 5, curses.COLS - width + 1, f" alt + {key}")
            screen.addstr(offset + 6, curses.COLS - width, f"{lineChar}{"═"*(width-1)}")
        except curses.error:
            return
