
import socket
import ssl
import time
import random

server = 'irc.scpwiki.com'
channel = '#cheesepoop9870'
nick = 'Mando-Bot'
realname = 'v1'  # This will be displayed in WHOIS
port = 6697


# List of admin usernames who can use privileged commands
ADMIN_USERS = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_"} # Add admin usernames here

def handle_command(command, args, handle, sender):
    output = []
    #Handle IRC commands starting with !
    if command == "hello":
        handle.write(f'PRIVMSG {channel} :Hello!\r\n')
        handle.flush()
    elif command == "quit":
        if sender in ADMIN_USERS:
            handle.write('QUIT :\r\n')
            handle.flush()
        else:
            handle.write(f'PRIVMSG {channel} :Sorry, you are not authorized to use this command.\r\n')
            handle.flush()
    elif command == "clear":
        handle.write(f'PRIVMSG {channel} :Message history cleared!\r\n')
        handle.flush()
    elif command == "!help":
        handle.write(f'PRIVMSG {channel} :Available commands: !hello, !quit, !clear, !help\r\n')
        handle.flush()
    elif command == "setup":
        if sender in ADMIN_USERS:
            handle.write(f'PRIVMSG {channel} :Setting up the bot...\r\n')
            handle.write(f'MODE {nick} :+B\r\n')
            time.sleep(1)
            handle.write(f"PRIVMSG {channel} :Bot setup complete!\r\n")
            handle.flush()
        else:
            handle.write(f'PRIVMSG {channel} :Sorry, you are not authorized to use this command.\r\n')
            handle.flush()
    elif command == "!roll":
        args = args.split("d")
        for x in range(0, int(args[0])):
            output.append(random.randint(1, int(args[1])))
        handle.write(f'PRIVMSG {channel} :{sender} rolled {args[0]}d{args[1]}:{str(output).strip("[]")} Total: {sum(output)}\r\n')
        handle.flush()
try:
    # Create socket and wrap with SSL
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock = ssl.wrap_socket(ircsock)
    ircsock.connect((server, port))

    handle = ircsock.makefile(mode='rw', buffering=1, encoding='utf-8', newline='\r\n')

    print('NICK', nick, file=handle)
    print('USER', nick, nick, nick, ':'+realname, file=handle)
    
    
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
            # Extract the sender's nickname
            sender = line.split('!')[0][1:]
            # Extract the command part
            msg_parts = line.split(':!')
            if len(msg_parts) > 1:
                # Split command and arguments
                cmd_parts = msg_parts[1].split()
                command = cmd_parts[0].lower()
                args = cmd_parts[1:] if len(cmd_parts) > 1 else []

                # Handle the command
                if handle_command(command, args, handle, sender):
                    break

except Exception as e:
    print(f"Error: {e}")
    # break
finally:
    try:
        ircsock.close()
    except:
        pass
