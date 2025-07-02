import random as r
import re
import socket
import ssl
import sys
import time
from local_googlesearch_python import search
# from crom import wikisearch, ausearch, latest, refresh_cache, cache_set
import os
import crom

#for infinite rolls
infindex = ["pi", "e", "inf", "infinity", "tau", "phi", "euler", "catalan", "glaisher", "sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(7)", "sqrt(11)", "sqrt(13)", "sqrt(17)", "sqrt(19)", "sqrt(23)", "sqrt(29)", "sqrt(31)", "sqrt(37)", "sqrt(41)", "sqrt(43)", "Fall out Boy", "bleventeen", "Gravity Falls", "Adventure Time", "Steven Universe", "Rick and Morty", "The Simpsons", "The Office", "Probabilitor", "*", "/", "+", "-", "=", ">", "<", "!", "?", "@", "#", "$", "%", "^", "&",  "(", ")", "_", "-", "+", "=", "[", "]", "{", "}",  "pyscp", "SCP-033", "SCP-055" "SCP-035", "SCP-049", "SCP-076", "SCP-096", "SCP-173", "SCP-294", "reddit", "youtube", "twitch", "twitter", "facebook", "instagram", "tiktok", "snapchat", "discord", "telegram", "whatsapp", "skype", "zoom", "minecraft", "IRC", "#IRC!", "#facility36", "LetsGameItOut", "SCP-3125", "numpy", "qwerty", "asdfghjkl", "zxcvbnm", "1234567890", "python", "java", "c++", "c#", "javascript", "html", "css", "php", "sql", "ruby", "swift", "kotlin", "go", "rust", "typescript", "dart","english", "spanish", "french", "german", "italian", "portuguese", "dutch", "russian", "chinese", "japanese", "korean", "arabic","fnaf", "minecraft", "fortnite", "apex legends", "call of duty", "battlefield", "overwatch", "rainbow six", "valorant", "csgo", "hydrogen", "helium", "lithium", "beryllium", "boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon", "sodium", "magnesium", "aluminum", "silicon", "phosphorus", "sulfur", "chlorine", "argon", "potassium", "calcium", "scandium", "titanium", "vanadium", "chromium","manganese", "iron", "cobalt", "nickel", "copper", "zinc", "gallium", "germanium", "arsenic", "selenium", "bromine","krypton", "rubidium", "strontium", "yttrium", "zirconium", "niobium", "molybdenum", "technetium", "ruthenium", "rhodium","palladium", "silver", "cadmium", "indium", "tin", "antimony", "tellurium", "iodine", "xenon", "cesium", "barium","lanthanum", "cerium", "praseodymium", "neodymium", "promethium", "samarium", "europium", "gadolinium", "terbium","dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium", "hafnium", "tantalum", "tungsten", "rhenium","osmium", "iridium", "platinum", "gold", "mercury", "thallium", "lead", "bismuth", "polonium", "astatine", "radon","francium","radium", "actinium", "thorium", "protactinium", "uranium", "neptunium", "plutonium", "americium", "curium","berkelium", "californium" "einsteinium", "fermium", "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium", "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium", "roentgenium", "copernicium", "nihonium", "flerovium", "moscovium", "livermorium","tennessine", "oganesson",]
#note: add !pingall message availibility

server = 'irc.scpwiki.com'
channel = '#cheesepoop9870'
# channel_debug = ""
nick = 'Mando-Bot'
realname = 'v1.2.8-alpha'  # This will be displayed in WHOIS
port = 6697
channel_list = ["#cheesepoop9870",] #facility36",]


# List of admin usernames who can use privileged commands
ADMIN_USERS = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", "The_Fox_Empress", "BineappleOnPizza", "PineappleOnSleepza", "my.poop.is.cheese", "illegal.food.combo",} # Add admin usernames/hosts here

debug_flag = 0 # 0 = off, 1 = on | SHOULD BE 0 WHEN NOT IN DEBUG MODE
latest_range = 3 # 3 = 3 results, 5 = 5 results, etc. | MAX 5


def handle_command(command, args, handle, sender, channel_debug, full_host=None):

    #debug command
    def debug(var, args):
      if debug_flag == 1:
           handle.write(f'PRIVMSG {channel_debug} :{var} {args}\r\n')
           handle.flush()

    #message splitting function
    def send_message(channel, message):
        if len(message) <= 433:
            print(f'PRIVMSG {channel} :{message}')
            handle.write(f'PRIVMSG {channel} :{message}\r\n')
            handle.flush()
        else:
            # Split message into chunks of 433 characters or less
            chunks = []
            while len(message) > 433:
                # Find a good place to split (prefer space)
                split_pos = 433
                if ' ' in message[:433]:
                    split_pos = message[:433].rfind(' ')
                chunks.append(message[:split_pos])
                message = message[split_pos:].lstrip()
            if message:  # Add remaining part
                chunks.append(message)

            # Send each chunk
            for chunk in chunks:
                print(f'PRIVMSG {channel} :{chunk}')
                handle.write(f'PRIVMSG {channel} :{chunk}\r\n')
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
        send_message(channel_debug, f'Hello, {sender}!')

    elif command == "quit" or command == "!quit":
        # Extract just the host part (after @) if full_host exists
        host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
        if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
            handle.write(f'QUIT :Quit command used by {sender} in channel {channel_debug}\r\n')
            handle.flush()
            sys.exit(0)
        else:
            send_message(channel_debug, 'Sorry, you are not authorized to use this command.')

    elif command == "clear":
        send_message(channel_debug, 'Message history cleared!')

    elif command == "commands":
        send_message(channel_debug, 'List of Commands: https://scp-sandbox-3.wikidot.com/mandobot-commands')

    elif command == "setup":
        # Extract just the host part (after @) if full_host exists
        host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
        if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
            send_message(channel_debug, 'Setting up the bot...')
            send_message(channel_debug, 'Bot setup complete!')
            #time.sleep(3)
        else:
            send_message(channel_debug, 'Sorry, you are not authorized to use this command.')

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
                send_message(channel_debug, f"{sender} rolled {commandargs2[0]}d{commandargs2[1]} and got ")
              elif commandargs2[0] == "inf" or commandargs2[1] == "inf":
                rng = r.randint(1, 2)
                if rng == 1:
                  send_message(channel_debug, f" {sender} rolled {commandargs2[0]}d{commandargs2[1]} and got {r.randint(-1000000000000000000000000000000000000000000000000000000, 1000000000000000000000000000000000000000000000000000000)}")
                else: #rng == 2
                    send_message(channel_debug, f"{sender} rolled {commandargs2[0]}d{commandargs2[1]} and got {infindex[r.randint(0, len(infindex)-1)]} ")
                rng = 0
                commandargs = ""
                commandargs2 = []
            else: #normal roll
              for i in range(int(commandargs2[0])):
                commandargsoutput.append(r.randint(1, int(commandargs2[1])))
              commandargs2.append((str(commandargsoutput)).strip("[]"))
          #add some 1d6 +1 funtionality
            if cflag_plus_roll == 0:
              send_message(channel_debug, f"{sender} rolled {commandargs2[0]}d{commandargs2[1]}: {commandargs2[len(commandargs2)-1]} Total: {sum(commandargsoutput)}")
            else:
              send_message(channel_debug, f"{sender} rolled {commandargs2[0]}d{commandargs2[1]}(+{commandargs3[1]}): {commandargs2[len(commandargs2)-1]} Total: {sum(commandargsoutput)}(+{commandargs3[1]}) = {sum(commandargsoutput, int(commandargs3[1]))}")
            commandargs = ""
            commandargs2 = []
            commandargsoutput = []
            commandargs3 = []
            cflag_plus_roll = 0
        except IndexError:
            send_message(channel_debug, 'Invalid dice format. use 1d10 or similar')

    elif command == "everyone":
        handle.write(f'NAMES {channel_debug}\r\n')
        handle.flush()
        # Get next line which contains names
        response = handle.readline().strip()
        if "353" in response:  # 353 is the IRC code for names list
            names = response.split(':')[-1].strip()  # Get names portion
            send_message(channel_debug, f'Users in channel: {names}')
        else:
            send_message(channel_debug, 'Error! if this happenes, tell cheese. Error string: 425/404')

    elif command == "join": #add multiple channel support
        handle.write(f'JOIN {args[0]}\r\n')
        channel_list.append(args[0])
        if "#" not in args[0]:
            send_message(channel_debug, f'{sender}: Invalid format. Use !join #channel')
        else:
          send_message(channel_debug, f'Joined {args[0]}')
        handle.flush()

    elif command == "leave": #add multiple channel support
        # Extract just the host part (after @) if full_host exists
        host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
        if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
            if len(args[0])> 0:
                handle.write(f'PART {args[0]}\r\n')
                channel_list.remove(args[0])
                handle.flush()
            else:
                handle.write(f"PART {channel_debug}\r\n")
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
              send_message(channel_debug, f'{sender}: No results found!')
            else:
              send_message(channel_debug, f'{sender}: {output_str}')
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
                  send_message(channel_debug, f'{sender}: Error!')
                else:
                  send_message(channel_debug, f"{sender}: {output_str[0:len(output_str)-2]}")
            except Exception as e:
                send_message(channel_debug, f'Error! if this happenes, tell cheese. Error string: {e}')
        else:
            send_message(channel_debug, 'Error! if this happens, tell cheese. Error string 424')

    elif command == "!flags":
        if args[0] == "set":
            if args[1] == "debug":
                # Extract just the host part (after @) if full_host exists
                host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
                if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
                    global debug_flag
                    debug_flag = debug_flag + 1
                    if debug_flag > 1:
                        debug_flag = 0
                    send_message(channel_debug, f'Debug mode = {debug_flag}')
                    debug("", "check")
                else:
                    send_message(channel_debug, 'Sorry, you are not authorized to use this command.')

            elif args[1] == "latest_range":
                # Extract just the host part (after @) if full_host exists
                host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
                if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
                    global latest_range
                    latest_range = args[2]
                    try:
                        if int(latest_range) > 5:
                            send_message(channel_debug, 'Error! latest_range cannot be greater than 5')
                        send_message(channel_debug, f'Latest search range = {latest_range}')
                    except ValueError:
                        send_message(channel_debug, 'Error! latest_range must be an integer')
                else:
                    send_message(channel_debug, 'Sorry, you are not authorized to use this command.')

    elif command == "ch" or command == "choose":
        output_str = " ".join(args)
        output = output_str.split(",")
        send_message(channel_debug, f'{sender}: {output[r.randint(0, len(output)-1)]}')    

    elif command == "search" or command == "s":
        try:
            output = crom.wikisearch(" ".join(args))
            output2 = ""
            output3 = []
            debug(0, output)
            #note: errors are intentional, they wont cause a problem
            if output["title2"] == []: #no alt title
                output["title2"] = ""
                output["title"] = f"{output['title']},"
            else:
                output["title"] = f"{output['title']}:"
                output_str = dict(output["title2"][0])["title"]
                output_str = f"{output_str},"
            for x in range(0, len(output["authors"])):
                output3.append(dict(output["authors"][x])["user"]["name"])
            send_message(channel_debug, f"{sender}: {output['title']} {output_str} ({output['rating']}, written on {output['createdAt']} by {', '.join(output3)} with {output['comments']} comments) - {output['url']}")
        except IndexError:
            send_message(channel_debug, f'{sender}: No results found!')
            return
        except Exception as e:
            send_message(channel_debug, f'{sender}: Error! String: {e}')

    elif command == "raw":
        # Extract just the host part (after @) if full_host exists
        host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
        if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
            args = " ".join(args)
            handle.write(f'{args}\r\n')
            handle.flush()
        else:
            send_message(channel_debug, 'Sorry, you are not authorized to use this command.')

    elif command == "reboot":
        # Extract just the host part (after @) if full_host exists
        host_only = full_host.split('@')[1] if full_host and '@' in full_host else None
        if sender in ADMIN_USERS or (host_only and host_only in ADMIN_USERS):
            handle.write("QUIT :Rebooting\r\n")
            handle.flush()
            os.system("python3 main.py")
            sys.exit(0)
        else:
            send_message(channel_debug, "Sorry, you are not authorized to use this command.")

    elif command == "author" or command == "au":
        try:
            output = crom.ausearch(" ".join(args)) 
            #name, rank, mean rating, total rating, page count, scp count, tale count, goi count, artwork count, author page url, author page title, last page url, last page title, last page rating
            #note: errors are intentional, they wont cause a problem
            if output["authorPageUrl"] != "":
                send_message(channel_debug, f"{sender}: {output['name']} ({output['authorPageTitle']} - {output['authorPageUrl']}) has {output['pageCount']} pages ({output['pageCountScp']} SCPs, {output['pageCountTale']} Tales, {output['pageCountGoiFormat']} GOI formats, {output['pageCountArtwork']} Artworks, and {output['pageCountOther']} others) with a total rating of {output['totalRating']} and an average rating of {output['meanRating']}. Their latest page is {output['lastPageTitle']} with a rating of {output['lastPageRating']} - {output['lastPageUrl']}")
            else:
                send_message(channel_debug, f"{sender}: {output['name']} has {output['pageCount']} pages ({output['pageCountScp']} SCPs, {output['pageCountTale']} Tales, {output['pageCountGoiFormat']} GOI formats, {output['pageCountArtwork']} Artworks, and {output['pageCountOther']} others) with a total rating of {output['totalRating']} and an average rating of {output['meanRating']}. Their latest page is {output['lastPageTitle']} with a rating of {output['lastPageRating']} - {output['lastPageUrl']}")
        except IndexError:
            send_message(channel_debug, f'{sender}: No results found!')
            return
        except Exception as e:
            send_message(channel_debug, f'{sender}: Error! String: {e}')
    elif command == "latest" or command == "l":
            for x in range(0, int(latest_range)):
                try:
                    output = crom.latest()[x]
                    output2 = ""
                    output3 = []
                    debug(0, output)
                    if output["title2"] == []: #no alt title
                        output["title2"] = ""
                        output["title"] = f"{output['title']},"
                    else:
                        output["title"] = f"{output['title']}:"
                        output_str = dict(output["title2"][0])["title"]
                        output_str = f"{output_str},"
                    for x in range(0, len(output["authors"])):
                        output3.append(dict(output["authors"][x])["user"]["name"])
                    send_message(channel_debug, f"{sender}: {output['title']} {output_str} ({output['rating']}, written on {output['createdAt']} by {', '.join(output3)} with {output['comments']} comments) - {output['url']}")
                except IndexError:
                    send_message(channel_debug, f'{sender}: No results found!')
                    return
                except Exception as e:
                    send_message(channel_debug, f'{sender}: Error! String: {e}')

    elif command == "refresh":
        send_message(channel_debug, f'{sender}: Manually refreshing cache...')
        crom.refresh_cache()
        send_message(channel_debug, f'{sender}: Cache refreshed!')
        #add db.py commands here too
    elif command == "irc":
        send_message(channel_debug, f'{sender}: https://www.rfc-editor.org/rfc/rfc1459.html')
##################################################################################
##################################################################################

if __name__ == "__main__":
    try:
        # Create socket and wrap with SSL
        #barebones IRC bot
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
                # Extract the full host (nick!user@host)
                full_host = line.split(' PRIVMSG')[0][1:]
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
                        if handle_command(command, args, handle, sender, channel_temp, full_host):
                            break
                history_check = line.split(":!!clear")
                history_channel = line #may break
                if len(history_check) > 1 and "#cheesepoop9870" in history_channel:
                    history_bypass = 1
                    handle.write('PRIVMSG #cheesepoop9870 :History cleared!\r\n')
                    handle.flush()
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
        except Exception:
            pass
# HIDE PASSWORD
