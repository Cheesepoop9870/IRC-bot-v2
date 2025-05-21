import socket
import ssl
import time
import random as r
import sys
from local_googlesearch_python import search
# import googlesearch
# https://pypi.org/project/googlesearch-python/
# from pyscp import core, snapshot, wikidot
# from utils_local import utils

#for infinite rolls
infindex = ["pi", "e", "inf", "infinity", "tau", "phi", "euler", "catalan", "glaisher", "sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(7)", "sqrt(11)", "sqrt(13)", "sqrt(17)", "sqrt(19)", "sqrt(23)", "sqrt(29)", "sqrt(31)", "sqrt(37)", "sqrt(41)", "sqrt(43)", "Fall out Boy", "bleventeen", "Gravity Falls", "Adventure Time", "Steven Universe", "Rick and Morty", "The Simpsons", "The Office", "Probabilitor", "*", "/", "+", "-", "=", ">", "<", "!", "?", "@", "#", "$", "%", "^", "&",  "(", ")", "_", "-", "+", "=", "[", "]", "{", "}",  "pyscp", "SCP-033", "SCP-055" "SCP-035", "SCP-049", "SCP-076", "SCP-096", "SCP-173", "SCP-294", "reddit", "youtube", "twitch", "twitter", "facebook", "instagram", "tiktok", "snapchat", "discord", "telegram", "whatsapp", "skype", "zoom", "minecraft", "IRC", "#IRC!", "#facility36", "LetsGameItOut", "SCP-3125", "numpy", "qwerty", "asdfghjkl", "zxcvbnm", "1234567890", "python", "java", "c++", "c#", "javascript", "html", "css", "php", "sql", "ruby", "swift", "kotlin", "go", "rust", "typescript", "dart","english", "spanish", "french", "german", "italian", "portuguese", "dutch", "russian", "chinese", "japanese", "korean", "arabic","fnaf", "minecraft", "fortnite", "apex legends", "call of duty", "battlefield", "overwatch", "rainbow six", "valorant", "csgo", "hydrogen", "helium", "lithium", "beryllium", "boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon", "sodium", "magnesium", "aluminum", "silicon", "phosphorus", "sulfur", "chlorine", "argon", "potassium", "calcium", "scandium", "titanium", "vanadium", "chromium","manganese", "iron", "cobalt", "nickel", "copper", "zinc", "gallium", "germanium", "arsenic", "selenium", "bromine","krypton", "rubidium", "strontium", "yttrium", "zirconium", "niobium", "molybdenum", "technetium", "ruthenium", "rhodium","palladium", "silver", "cadmium", "indium", "tin", "antimony", "tellurium", "iodine", "xenon", "cesium", "barium","lanthanum", "cerium", "praseodymium", "neodymium", "promethium", "samarium", "europium", "gadolinium", "terbium","dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium", "hafnium", "tantalum", "tungsten", "rhenium","osmium", "iridium", "platinum", "gold", "mercury", "thallium", "lead", "bismuth", "polonium", "astatine", "radon","francium","radium", "actinium", "thorium", "protactinium", "uranium", "neptunium", "plutonium", "americium", "curium","berkelium", "californium" "einsteinium", "fermium", "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium", "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium", "roentgenium", "copernicium", "nihonium", "flerovium", "moscovium", "livermorium","tennessine", "oganesson",]
#note: add !pingall message availibility

server = 'irc.scpwiki.com'
channel = '#cheesepoop9870'
# channel_debug = ""
nick = 'Mando-Bot'
realname = 'v1.2.5-alpha'  # This will be displayed in WHOIS
port = 6697
channel_list = ["#cheesepoop9870",] #facility36",]


def str_remove(string):
    new_string = ""
    for char in string:
        new_string = new_string.replace(char, "")
    return new_string


# List of admin usernames who can use privileged commands
ADMIN_USERS = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", "The_Fox_Empress",} # Add admin usernames here

def handle_command(command, args, handle, sender, channel_debug):
    output = []
    output2 = []
    output_str = ""
    #dice stuff
    commandargs = ""
    commandargs2 = []
    commandargsoutput = []
    commandargs3 = []
    cflag_plus_roll = 0
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
        try:
            commandargs = "".join(args)
            if "+" in commandargs:
                commandargs3 = commandargs.split("+")
                commandargs2 = commandargs3[0].split("d")
                cflag_plus_roll = 1
            else: #no + in there
                commandargs2 = commandargs.split("d")        
            #inf/0 check
            if commandargs2[0] in ["inf", "0", "Inf", "infinity",] or commandargs2[1] in ["inf", "0", "Inf", "infinity",]:
              if commandargs2[0] == "0" or commandargs2[1] == "0":
                handle.write(f"PRIVMSG {channel_debug} :{sender} rolled {commandargs2[0]}d{commandargs2[1]} and got \r\n")
                handle.flush()
              elif commandargs2[0] == "inf" or commandargs2[1] == "inf":
                rng = r.randint(1, 2)
                if rng == 1:
                  handle.write(f"PRIVMSG {channel_debug} : {sender} rolled {commandargs2[0]}d{commandargs2[1]} and got {r.randint(-1000000000000000000000000000000000000000000000000000000, 1000000000000000000000000000000000000000000000000000000)}\r\n")
                  handle.flush()
                else: #rng == 2
                    handle.write(f"PRIVMSG {channel_debug} :{sender} rolled {commandargs2[0]}d{commandargs2[1]} and got {infindex[r.randint(0, len(infindex)-1)]} \r\n")
                    handle.flush()
                rng = 0
                commandargs = ""
                commandargs2 = []
            else: #normal roll
              for i in range(int(commandargs2[0])):
                commandargsoutput.append(r.randint(1, int(commandargs2[1])))
              commandargs2.append((str(commandargsoutput)).strip("[]"))
          #add some 1d6 +1 funtionality
            if cflag_plus_roll == 0:
              handle.write(f"PRIVMSG {channel_debug} :{sender} rolled {commandargs2[0]}d{commandargs2[1]}: {commandargs2[len(commandargs2)-1]} Total: {sum(commandargsoutput)}\r\n")
              handle.flush()
            else:
              handle.write(f"PRIVMSG {channel_debug} :{sender} rolled {commandargs2[0]}d{commandargs2[1]}(+{commandargs3[1]}): {commandargs2[len(commandargs2)-1]} Total: {sum(commandargsoutput)}(+{commandargs3[1]}) = {sum(commandargsoutput, int(commandargs3[1]))}\r\n")
              handle.flush()
            commandargs = ""
            commandargs2 = []
            commandargsoutput = []
            commandargs3 = []
            cflag_plus_roll = 0
        except IndexError:
            handle.write(f'PRIVMSG {channel_debug} :Invalid dice format. use 1d10 or similar\r\n')
            handle.flush()
    elif command == "everyone":
        handle.write(f'NAMES {channel_debug}\r\n')
        handle.flush()
        # Get next line which contains names
        response = handle.readline().strip()
        if "353" in response:  # 353 is the IRC code for names list
            names = response.split(':')[-1].strip()  # Get names portion
            handle.write(f'PRIVMSG {channel_debug} :Users in channel: {names}\r\n')
            handle.flush()
        else:
            handle.write(f"PRIVMSG {channel_debug} :Error! if this happenes, tell cheese. Error string: 425/404\r\n")
    elif command == "join":
        handle.write(f'JOIN {args[0]}\r\n')
        channel_list.append(args[0])
        handle.flush()
    elif command == "leave":
        if sender in ADMIN_USERS:
            handle.write(f'PART {args[0]}\r\n')
            channel_list.remove(args[0])
            handle.flush()
    elif command == "google" or command == "g":
        # handle.write(f'PRIVMSG {channel_debug} :{bool(list(search(args, num_results=1))[0])}\r\n')
        if not bool(list(search(args, num_results=1))[0]): # false
            output = list(search(args, num_results=2, advanced=True))
            output = str(output[1]).split("(", 1)
            output.pop(0) # Remove the first element
            output2 = str(output[0]).split("=")
            output2.pop(0) # Remove the first element
            output = output2
            output_str = "".join(output)
            output2 = output_str.split("title")
            output_str = "".join(output)
            output = output_str.split(")")
            handle.write(f'PRIVMSG {channel_debug} :{sender}: {output[0]}\r\n')
            handle.flush()
        elif bool(list(search(args, num_results=1))[0]): # true
            try:
                output = list(search(args, num_results=1, advanced=True))
                output = str(output[0]).split("(", 1)
                output.pop(0) # Remove the first element
                output = str(output[0]).split("=")
                output.pop(0) # Remove the first element
                output2 = output[0].split(",")
                output2.pop(1) # Remove the second element
                output.pop(0) #Replace the first element
                output.insert(0, output2[0]) #^
                output_str = "".join(output)
                output = output_str.split(",")
                #do same thing as above
                handle.write(f"PRIVMSG {channel_debug} :{sender}: {output_str[0:len(output_str)-2]}\r\n")
                handle.flush()
            except IndexError:
                handle.write(f'PRIVMSG {channel_debug} :Error! if this happenes, tell cheese. Error string: 417\r\n')
                handle.flush()
        else:
            handle.write(f'PRIVMSG {channel_debug} :Error! if this happens, tell cheese. Error string 424\r\n')
    elif command == "flags":
        handle.write(f'PRIVMSG {channel_debug} :does nothing rn\r\n')
        handle.flush()
    elif command == "ch":
        output_str = "".join(args)
        output = output_str.split(",")
        handle.write(f'PRIVMSG {channel_debug} :{sender}: {output[r.randint(0, len(output)-1)]}\r\n')
        handle.flush()
        
    # elif 

try:
    # Create socket and wrap with SSL
    context = ssl.create_default_context()
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock = context.wrap_socket(ircsock, server_hostname=server)
    ircsock.connect((server, port))
    handle = ircsock.makefile(mode='rw', buffering=1, encoding='utf-8', newline='\r\n')

    print('NICK', nick, file=handle)
    print('USER', nick, nick, nick, ':'+realname, file=handle)


    joined = False
    history_bypass = 0
    while True:
        line = handle.readline().strip()
        print(line)


        # Check for PING and respond with PONG
        if "PING" in line:
            pong = "PONG :" + line.split(':')[1]
            handle.write(pong + '\r\n')
            handle.flush()

            # Join channel after first PING (server ready)
            if not joined:
                for x in range(0, len(channel_list)):
                    handle.write(f'JOIN {channel_list[x]}\r\n')
                handle.write(f'MODE {nick} :+B\r\n')
                handle.flush()
                joined = True
            continue

        # Check for PRIVMSG (chat messages)
        if "PRIVMSG" in line and ':!' in line or "MSG" in line and ":!" in line:
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
                if history_bypass == 1:
                    if handle_command(command, args, handle, sender, channel_temp):
                        break
            history_check = line.split(":!clear")
            if len(history_check) > 1:
                history_bypass = 1
                handle.write(f'PRIVMSG {channel_temp} :History cleared!\r\n')
except Exception as e:
    print(f"Error: {e}")
    # break
finally:
    try:
        context = ssl.create_default_context()
        ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ircsock = context.wrap_socket(ircsock)
        handle = ircsock.makefile(mode='rw', buffering=1, encoding='utf-8', newline='\r\n')
        handle.write('QUIT :\r\n')
        handle.flush()
        sys.exit(1)
    except:
        pass