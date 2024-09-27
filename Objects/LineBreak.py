import curses

def drawLineBreak(screen, y, x, length, character: str = "═", direction = "horizontal"):
    if direction == "horizontal":
        for i in range(length):
            screen.addch(y, x + i, character)
    elif direction == "vertical":
        for i in range(length):
            screen.addch(y + i, x, character)
    else:
        raise ValueError("Invalid direction")
