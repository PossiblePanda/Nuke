import curses, curses.textpad, keyboard, json, subprocess, sys

from Objects import LineBreak, BindList, ServerList

options = {}

def draw(screen):
    screen.clear()

    # Top Bar
    screen.addstr(0, 0, "Select a server")
    LineBreak.drawLineBreak(screen, 1, 0, curses.COLS, "═", "horizontal")

    # Bind List
    BindList.drawBindList(screen, [
        {
            "bind": "1-9",
            "action": "Select server"
        },
        {
            "bind": "CTRL + N",
            "action": "New server"
        }
    ])

    ServerList.drawServerList(screen, options["servers"])

    screen.refresh()


def main(screen):
    print("G")
    global options
    curses.curs_set(0)

    with open("options.json", "r") as json_data:
        options = json.load(json_data)
        json_data.close()

    draw(screen)

    def select_server(server):
        url = f"ws://{server['ip']}:{server['port']}"
        subprocess.call(f'python3 main.py {url}', creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.quit()

    for i in range(len(options["servers"])):
        server = options["servers"][i]
        keyboard.add_hotkey(f"{i+1}", select_server, args=[server])

    while True:
        pass

curses.wrapper(main)