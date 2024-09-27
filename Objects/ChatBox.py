import curses

def drawChatBox(screen, messages: list[dict], selected_channel: str):
    if not selected_channel in messages:
        return

    for i in range(len(messages[selected_channel])):
        offset = i*3
        message = messages[selected_channel][-i-1]

        if offset >= curses.LINES - 5:
            return
        
        screen.addstr(curses.LINES-2 - offset - 2, 0, message["username"])
        screen.addstr(curses.LINES-2 - offset - 1, 0, message["message"])