import socket
import ssl
import time
import random as r
import sys
import re
import requests
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
realname = 'v1.2.7'  # This will be displayed in WHOIS
port = 6697
channel_list = ["#cheesepoop9870",] #facility36",]

#crom api

def wikisearch(query):
    url = "https://api.crom.avn.sh"
    body = """
    query Search($query: String!, $noAttributions: Boolean!) {
      searchPages(query: $query, filter: { anyBaseUrl: "http://scp-wiki.wikidot.com" }) {
        url
        wikidotInfo {
          title
          rating
        }
        attributions @skip(if: $noAttributions) {
          type
          user {
            name
          }
        }
      }
    }
    """
    variables2 = {
      'query': f'{query}',  # term
      'noAttributions': False
    }
    response = requests.post(url=url, json={"query": body, "variables": variables2})
    if response.status_code == 200:
      return response.content
    else: 
      return f"Error {response.status_code}"



# List of admin usernames who can use privileged commands
ADMIN_USERS = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", "The_Fox_Empress", "BineappleOnPizza"} # Add admin usernames here

debug_flag = 0 # 0 = off, 1 = on | SHOULD BE 0 WHEN NOT IN DEBUG MODE

def handle_command(command, args, handle, sender, channel_debug):
    
    #debug command
    def debug(var, args):
      if debug_flag == 1:
           handle.write(f'PRIVMSG {channel_debug} :{var} {args}\r\n')
           handle.flush()

    #variables
    output = []
    output2 = []
    output_str = ""
    
    #dice stuff bc im lazy
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
            handle.write(f'QUIT :Quit command used by {sender} in channel {channel_debug}\r\n')
            handle.flush()
            sys.exit(0)
        else:
            handle.write(f'PRIVMSG {channel_debug} :Sorry, you are not authorized to use this command.\r\n')
            handle.flush()
            
    elif command == "clear":
        handle.write(f'PRIVMSG {channel_debug} :Message history cleared!\r\n')
        handle.flush()
        
    elif command == "commands":
        handle.write(f'PRIVMSG {channel_debug} :List of Commands: https://scp-sandbox-3.wikidot.com/mandobot-commands\r\n')
        handle.flush()
        
    elif command == "setup":
        if sender in ADMIN_USERS:
            handle.write(f'PRIVMSG {channel_debug} :Setting up the bot...\r\n')
            handle.write(f"PRIVMSG {channel_debug} :Bot setup complete!\r\n")
            #time.sleep(3)
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
            handle.flush()
            
    elif command == "join": #add multiple channel support
        handle.write(f'JOIN {args[0]}\r\n')
        channel_list.append(args[0])
        if "#" not in args[0]:
            handle.write(f'PRIVMSG {channel_debug} :{sender}: Invalid format. Use !join #channel\r\n')
            handle.flush()
        else:
          handle.write(f'PRIVMSG {channel_debug} :Joined {args[0]}\r\n')
        handle.flush()
        
    elif command == "leave": #add multiple channel support
        if sender in ADMIN_USERS:
            handle.write(f'PART {args[0]}\r\n')
            channel_list.remove(args[0])
            handle.flush()
            
    elif command == "google" or command == "g":
        #note: ADD SPACE BETWEEN URL AND TITLE
        debug(-1, list(search(args, num_results=2)))
        debug(-1.5, bool(list(search(args, num_results=1))[0]))
        debug(0, bool(list(search(args, num_results=1))[0]))
        if not bool(list(search(args, num_results=1))[0]) or "/search?" in str(list(search(args, num_results=1))[0]): # false, 1st result contains no results/404
            output = list(search(args, num_results=2, advanced=True))
            debug(1, output)
            output = str(output[1]).split("(", 1)
            debug(2, output)
            output.pop(0) # Remove the first element
            debug(3, output)
            output2 = str(output[0]).split("=")
            debug(4, output2)
            output2.pop(0) # Remove the first element
            debug(5, output2)
            output = output2
            debug(6, output)
            output_str = "".join(output)
            debug(7, output_str)
            output2 = output_str.split("title")
            debug(8, output2)
            output_str = " | ".join(output)
            debug(9, output_str)
            output_str = output_str[0:len(output_str)-2]
            #404 check
            if ", title | , description |" in output_str or "/search?" in output_str:
              handle.write(f'PRIVMSG {channel_debug} :{sender}: No results found!\r\n')
              handle.flush()
            else:
              handle.write(f'PRIVMSG {channel_debug} :{sender}: {output_str}\r\n')
              handle.flush()
        elif bool(list(search(args, num_results=1))[0]): # true
            try:
                output = list(search(args, num_results=1, advanced=True))
                debug(1, output)
                output = str(output[0]).split("(", 1)
                debug(2, output)
                output.pop(0) # Remove the first element
                debug(3, output)
                output = re.split(r"url=|title=|description=" ,str(output[0]))
                debug(4, output)
                output.pop(0) # Remove the first element
                debug(5, output)
                output2 = output[0].split(",")
                debug(6, output2)
                output2.pop(1) # Remove the second element
                debug(7, output2)
                output.pop(0) #Replace the first element
                debug(8, output)
                output.insert(0, output2[0]) #^
                debug(9, output)
                output_str = " | ".join(output)
                debug(10, output_str)
                output = output_str.split(",")
                #do same thing as above
                if ", title | , description |" in output_str or "/search?" in output_str:
                  handle.write(f'PRIVMSG {channel_debug} :{sender}: Error!\r\n')
                  handle.flush()
                else:
                  handle.write(f"PRIVMSG {channel_debug} :{sender}: {output_str[0:len(output_str)-2]}\r\n")
                  handle.flush()
            except Exception as e:
                handle.write(f'PRIVMSG {channel_debug} :Error! if this happenes, tell cheese. Error string: {e}\r\n')
                handle.flush()
        else:
            handle.write(f'PRIVMSG {channel_debug} :Error! if this happens, tell cheese. Error string 424\r\n')
            
    elif command == "!flags":
        if " ".join(args) == "debug":
            if sender in ADMIN_USERS:
                global debug_flag
                debug_flag = debug_flag + 1
                if debug_flag > 1:
                    debug_flag = 0
                handle.write(f'PRIVMSG {channel_debug} :Debug mode = {debug_flag}\r\n')
                handle.flush()
                debug("", "r")
            else:
                handle.write(f'PRIVMSG {channel_debug} :Sorry, you are not authorized to use this command.\r\n')
                handle.flush()
                
    elif command == "ch" or command == "choose":
        output_str = " ".join(args)
        output = output_str.split(",")
        handle.write(f'PRIVMSG {channel_debug} :{sender}: {output[r.randint(0, len(output)-1)]}\r\n')
        handle.flush()    
        
    elif command == "search" or command == "s":
        output = wikisearch(" ".join(args))
        debug(0, output)
        handle.write(f'PRIVMSG {channel_debug} :{sender}: {output}\r\n')

    elif command == "raw":
        if sender in ADMIN_USERS:
            handle.write(f'{args}\r\n')
            handle.flush()

##################################################################################
##################################################################################

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
                handle.write('PRIVMSG NickServ :identify PASSWORD\r\n') #remember to hide password
                time.sleep(2)
                for x in range(0, len(channel_list)):
                    handle.write(f'JOIN {channel_list[x]}\r\n')
                handle.write(f'MODE {nick} :+B\r\n')
                handle.flush()
                joined = True
            continue

        # Check for PRIVMSG (chat messages)
        if "PRIVMSG" in line and ':!' in line:
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
            history_check = line.split(":!!clear")
            history_channel = line #may break
            if len(history_check) > 1 and "#cheesepoop9870" in history_channel:
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
