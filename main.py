import threading, curses, curses.textpad, websocket, json, keyboard, sys

from Objects import LineBreak, ChatBox, ChannelList

textbox = None
ws = None
ws_url: str

channel_scroll = 0
current_channel = "general"

online_count = 0
server_config = {
    "server_name": "Server Name",
    "server_description": "Server Description",
    "channels": []
}

messages = {}

def connect_server(url: str):
    print(url)
    global ws
    ws = websocket.create_connection(url)

def draw(screen):
    global textbox
    screen.clear()

    # Top Bar
    screen.addstr(0, 0, f"{server_config["server_name"]} | {online_count} Online | {server_config["server_description"]}")
    LineBreak.drawLineBreak(screen, 1, 0, curses.COLS)

    # Message Box
    LineBreak.drawLineBreak(screen, curses.LINES - 2, 0, curses.COLS)

    # Chat Box
    ChatBox.drawChatBox(screen, messages, current_channel)
    input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
    input_win.refresh()
    textbox = curses.textpad.Textbox(input_win)

    # Channel List
    print(server_config)
    ChannelList.drawChannelList(screen, server_config["channels"], current_channel, channel_scroll)

    screen.refresh()


def main(screen):
    global textbox
    curses.curs_set(0)

    draw(screen)
    connect_server(sys.argv[1])

    def server_loop():
        global server_config
        global current_channel
        global messages

        # Recieve packets from the server
        while True:
            data = ws.recv()
            data: dict = json.loads(data)

            if not "type" in data:
                return

            match data["type"]:
                case "message":
                    if not data["channel"] in messages:
                        messages[data["channel"]] = []
                    messages[data["channel"]].append({
                        "username": "Possible Panda",
                        "message": data["message"],
                        "channel": data["channel"]
                    })
                    draw(screen)
                    screen.refresh()
                
                case "connection_established":
                    global online_count

                    online_count = data["online"]
                    server_config = data["config"]
                    current_channel = server_config["channels"][0]

                    def change_channel(channel):
                        global current_channel
                        current_channel = channel

                        draw(screen)
                        screen.refresh()

                    for channel in server_config["channels"]:
                        if channel in messages: 
                            messages[channel] = []
                    
                        keyboard.add_hotkey(f"alt+{server_config["channels"].index(channel) + 1}", change_channel, args=[channel])

                    def change_scroll_amount(amount):
                        global channel_scroll
                        if channel_scroll + amount <0:
                            return
                        
                        if channel_scroll + amount > len(server_config["channels"]) - 1:
                            return

                        channel_scroll += amount
                        print(channel_scroll)
                        
                        draw(screen)

                    keyboard.add_hotkey(f"alt+up", change_scroll_amount, args=[1])
                    keyboard.add_hotkey(f"alt+down", change_scroll_amount, args=[-1])

                    draw(screen)
                    screen.refresh()
                
                case "user_joined":
                    online_count += 1
                    draw(screen)
                    screen.refresh()
                
                case "user_left":
                    online_count -= 1
                    draw(screen)
                    screen.refresh()

    threading.Thread(target=server_loop).start()

    while True:
        text = textbox.edit()

        if text == "":
            continue

        if text[0].isdigit():
            text = text[1:] # Prevents weird bug where the first character is a digit

        input_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        input_win.clear()
        input_win.refresh()

        # Reinitialize the textbox for new input
        textbox = curses.textpad.Textbox(input_win)

        if text != "":
            data = json.dumps({
                    "type": "message", 
                    "message": text,
                    "channel": current_channel
                })
            ws.send(str(data))

def close():
    ws.close()
    sys.exit(1)

curses.wrapper(main)
