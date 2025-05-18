import socket
import ssl
import time
import random as r
import sys
from local_googlesearch_python import search
# import googlesearch
# https://pypi.org/project/googlesearch-python/
# from local_pyscp import *


#note: add !pingall message availibility

server = 'irc.scpwiki.com'
channel = '#cheesepoop9870'
# channel_debug = ""
nick = 'Mando-Bot'
realname = 'v1.2.5-alpha'  # This will be displayed in WHOIS
port = 6697

def str_remove(string):
    new_string = ""
    for char in string:
        new_string = new_string.replace(char, "")
    return new_string


# List of admin usernames who can use privileged commands
ADMIN_USERS = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", "The_Fox_Empress",} # Add admin usernames here

def handle_command(command, args, handle, sender, channel_debug):
    output = []
    output_str = ""
    #Handle IRC commands starting with !
    if command == "hello":
        handle.write(f'PRIVMSG {channel_debug} :Hello, {sender}!\r\n')
        handle.flush()
    elif command == "quit":
        if sender in ADMIN_USERS:
            handle.write('QUIT :\r\n')
            handle.flush()
            sys.exit(0)
        else:
            handle.write(f'PRIVMSG {channel_debug} :Sorry, you are not authorized to use this command.\r\n')
            handle.flush()
    elif command == "clear":
        handle.write(f'PRIVMSG {channel_debug} :Message history cleared!\r\n')
        handle.flush()
    elif command == "!help":
        handle.write(f'PRIVMSG {channel_debug} :List of Commands: https://scp-sandbox-3.wikidot.com/mandobot-commands\r\n')
        handle.flush()
    elif command == "setup":
        if sender in ADMIN_USERS:
            handle.write(f'PRIVMSG {channel_debug} :Setting up the bot...\r\n')
            
            handle.write(f"PRIVMSG {channel_debug} :Bot setup complete!\r\n")
            time.sleep(3)
            handle.flush()
        else:
            handle.write(f'PRIVMSG {channel_debug} :Sorry, you are not authorized to use this command.\r\n')
            handle.flush()
    elif command == "!roll":
        if len(args) == 1:
            dice_args = args[0].split("d")
            if len(dice_args) == 2:
                try:
                    num_dice = int(dice_args[0])
                    dice_size = int(dice_args[1])
                    for x in range(num_dice):
                        output.append(r.randint(1, dice_size))
                    handle.write(f'PRIVMSG {channel_debug} :{sender} rolled {num_dice}d{dice_size}: {str(output).strip("[]")} Total: {sum(output)}\r\n')
                    handle.flush()
                except ValueError:
                    handle.write(f'PRIVMSG {channel_debug} :Invalid dice format. Use: !roll NdM (example: !roll 1d20)\r\n')
                    handle.flush()
            else:
                handle.write(f'PRIVMSG {channel_debug} :Invalid dice format. Use: !!roll NdM (example: !!roll 1d20)\r\n')
                handle.flush()
        else:
            handle.write(f'PRIVMSG {channel_debug} :Invalid dice format. Use: !!roll NdM (example: !!roll 1d20)\r\n')
            handle.flush()
    elif command == "ch":
        output = ' '.join(args).split(',')
        handle.write(f'PRIVMSG {channel_debug} :{output[r.randint(0, len(output)-1)]}\r\n')
        handle.flush()
    elif command == "everyone":
        handle.write(f'NAMES {channel_debug}\r\n')
        handle.flush()
    elif command == "join":
        handle.write(f'JOIN {args[0]}\r\n')
        handle.flush()
    elif command == "leave":
        if sender in ADMIN_USERS:
            handle.write(f'LEAVE {args[0]}\r\n')
            handle.flush()
    elif command == "google":
        output = googlesearch.search("args", num_results=1)
        handle.write(f'PRIVMSG {channel_debug} :{output}\r\n')
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
                handle.write(f'MODE {nick} :+B\r\n')
                handle.flush()
                joined = True
            continue

        # Check for PRIVMSG (chat messages)
        if "PRIVMSG" in line and ':!' in line or "PRIVMSG" in line and ':@' in line:
            # Extract the sender's nickname
            sender = line.split('!')[0][1:]
            # Extract the channel
            channel_temp = line.split('PRIVMSG')[1].split(':')[0].strip()
            # Extract the command part
            
            msg_parts = line.split(':!')
            if len(msg_parts) > 1:
                # Split command and arguments
                cmd_parts = msg_parts[1].split()
                command = cmd_parts[0].lower()
                args = cmd_parts[1:] if len(cmd_parts) > 1 else []

                # Handle the command
                if handle_command(command, args, handle, sender, channel_temp):
                    break

except Exception as e:
    print(f"Error: {e}")
    # break
finally:
    try:
        ircsock.close()
    except:
        pass
