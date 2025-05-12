
import socket
import ssl

server = 'irc.scpwiki.com'
channel = '#cheesepoop9870'
nick = 'CheeseBot-v1'
port = 6697

def handle_command(command, args, handle):
    #Handle IRC commands starting with !
    if command == "hello":
        handle.write(f'PRIVMSG {channel} :Hello!\r\n')
        handle.flush()
    elif command == "quit":
        handle.write('QUIT :\r\n')
        handle.flush()
        break
try:
    # Create socket and wrap with SSL
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock = ssl.wrap_socket(ircsock)
    ircsock.connect((server, port))

    handle = ircsock.makefile(mode='rw', buffering=1, encoding='utf-8', newline='\r\n')

    print('NICK', nick, file=handle)
    print('USER', nick, nick, nick, ':'+nick, file=handle)

    joined = False
    while True:
        line = handle.readline().strip()
        print(line)

        if "PING" in line:
            pong = "PONG :" + line.split(':')[1]
            handle.write(pong + '\r\n')
            handle.flush()
            
            # Join channel after first PING (server ready)
            if not joined:
                handle.write(f'JOIN {channel}\r\n')
                handle.flush()
                joined = True
            continue

        # Check for PRIVMSG (chat messages)
        if "PRIVMSG" in line and ':!' in line:
            # Extract the command part
            msg_parts = line.split(':!')
            if len(msg_parts) > 1:
                # Split command and arguments
                cmd_parts = msg_parts[1].split()
                command = cmd_parts[0].lower()
                args = cmd_parts[1:] if len(cmd_parts) > 1 else []

                # Handle the command
                handle_command(command, args, handle)

except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        ircsock.close()
    except:
        pass
