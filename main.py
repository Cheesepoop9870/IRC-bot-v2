import random as r
import re
import socket
import ssl
import sys
import time
import os
import crom
import base64
import json
import logging as log
import pastebin2
from local_googlesearch_python import search
from youtube_search import YoutubeSearch as ytsearch 

# from pastebin import PastebinAPI
#for infinite rolls
#remove this maybe
infindex = ["pi", "e", "inf", "infinity", "tau", "phi", "euler", "catalan", "glaisher", "sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(7)", "sqrt(11)", "sqrt(13)", "sqrt(17)", "sqrt(19)", "sqrt(23)", "sqrt(29)", "sqrt(31)", "sqrt(37)", "sqrt(41)", "sqrt(43)", "Fall out Boy", "bleventeen", "Gravity Falls", "Adventure Time", "Steven Universe", "Rick and Morty", "The Simpsons", "The Office", "Probabilitor", "*", "/", "+", "-", "=", ">", "<", "!", "?", "@", "#", "$", "%", "^", "&",  "(", ")", "_", "-", "+", "=", "[", "]", "{", "}",  "pyscp", "SCP-033", "SCP-055" "SCP-035", "SCP-049", "SCP-076", "SCP-096", "SCP-173", "SCP-294", "reddit", "youtube", "twitch", "twitter", "facebook", "instagram", "tiktok", "snapchat", "discord", "telegram", "whatsapp", "skype", "zoom", "minecraft", "IRC", "#IRC!", "#facility36", "LetsGameItOut", "SCP-3125", "numpy", "qwerty", "asdfghjkl", "zxcvbnm", "1234567890", "python", "java", "c++", "c#", "javascript", "html", "css", "php", "sql", "ruby", "swift", "kotlin", "go", "rust", "typescript", "dart","english", "spanish", "french", "german", "italian", "portuguese", "dutch", "russian", "chinese", "japanese", "korean", "arabic","fnaf", "minecraft", "fortnite", "apex legends", "call of duty", "battlefield", "overwatch", "rainbow six", "valorant", "csgo", "hydrogen", "helium", "lithium", "beryllium", "boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon", "sodium", "magnesium", "aluminum", "silicon", "phosphorus", "sulfur", "chlorine", "argon", "potassium", "calcium", "scandium", "titanium", "vanadium", "chromium","manganese", "iron", "cobalt", "nickel", "copper", "zinc", "gallium", "germanium", "arsenic", "selenium", "bromine","krypton", "rubidium", "strontium", "yttrium", "zirconium", "niobium", "molybdenum", "technetium", "ruthenium", "rhodium","palladium", "silver", "cadmium", "indium", "tin", "antimony", "tellurium", "iodine", "xenon", "cesium", "barium","lanthanum", "cerium", "praseodymium", "neodymium", "promethium", "samarium", "europium", "gadolinium", "terbium","dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium", "hafnium", "tantalum", "tungsten", "rhenium","osmium", "iridium", "platinum", "gold", "mercury", "thallium", "lead", "bismuth", "polonium", "astatine", "radon","francium","radium", "actinium", "thorium", "protactinium", "uranium", "neptunium", "plutonium", "americium", "curium","berkelium", "californium" "einsteinium", "fermium", "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium", "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium", "roentgenium", "copernicium", "nihonium", "flerovium", "moscovium", "livermorium","tennessine", "oganesson",]
#note: add !pingall message availibility

#logging stuff
log.basicConfig(
    level=log.INFO,  
    format='[%(asctime)s,%(msecs)d] [%(levelname)s]: %(message)s',
    filename='app.log',  # Log to a file named 'app.log'
    filemode='w',         # Append to the file (default is 'a', 'w' for overwrite)
    datefmt='%H:%M:%S',
)

log.debug("started")
server = 'irc.scpwiki.com'
channel = '#cheesepoop9870, #Facility36'
# channel_debug = ""
nick = 'Mando-Bot'
realname = 'v1.2.8-alpha'  # This will be displayed in WHOIS
port = 6697
channel_list = ["#cheesepoop9870", "#facility36", "#neutralzone", "#site22", "#Magnishideout"]
# channel_list = db.get_channels()
reg_channel_list = []
# List of admin usernames who can use privileged commands
ADMIN_USERS = {'cheesepoop9870', "PineappleOnPizza", "cheesepoop9870_", "Kiro", "The_Fox_Empress", "Felds", "PineappleOnSleepza", "my.poop.is.cheese", "illegal.food.combo", " stalking.your.sandbox", "site19.isnt.real.cant.hurt.you", "the.queen.of.foxes", "Magnileak", } # Add admin usernames/hosts here
ADMIN_USER_REGEX = {r"(\w+!)?(uid692117|theword987)@(stalking\.your\.sandbox|my\.poop\.is\.cheese|illegal\.food\.combo)$", r"(\w*!)?(uid536230)@(the\.queen\.of\.foxes)$", r"(\w+!)?(Felds)@(the\.amyrlin\.seat|site19\.isnt\.real\.cant\.hurt\.you)$", r"(\w+!)?(uid714194|Magnileak)@(SCP-f5eupe\.tinside\.irccloud\.com|SCP-kin\.6dp\.29\.161\.IP|SCP-phc\.lrc\.149\.118\.IP|SCP-go5\.s65\.149\.118\.IP)$"}
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
        # Replace 'ops' with '0ps' in the message
        message = message.replace('ops', '0ps')
        
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
                
    def checkperms(full_host2):
        for regex in ADMIN_USER_REGEX:
            if re.search(regex, full_host2):
                return True
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
        
        if checkperms(full_host):
            handle.write(f'QUIT :Quit command used by {sender} in channel {channel_debug}\r\n')
            handle.flush()
            log.info(f'Quit command used by {sender} in channel {channel_debug}')
            sys.exit(0)
        else:
            send_message(channel_debug, 'Sorry, you are not authorized to use this command. Action logged.')
            log.warning(f'{sender} tried to use the quit command in channel {channel_debug}')
    elif command == "clear":
        send_message(channel_debug, 'Message history cleared!')
        log.debug(f"clear command used by {sender} in channel")

    elif command == "commands":
        send_message(channel_debug, 'List of Commands: https://scp-sandbox-3.wikidot.com/mandobot-commands')

    elif command == "setup":
        
        if checkperms(full_host):
            send_message(channel_debug, 'Setting up the bot...')
            send_message(channel_debug, 'Bot setup complete!')
            #time.sleep(3)
            log.debug(f"setup command used by {sender} in channel {channel_debug}")
        else:
            send_message(channel_debug, 'Sorry, you are not authorized to use this command. Action logged.')
            log.warning(f'{sender} tried to use the setup command in channel {channel_debug}')
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
                  return
                else: #rng == 2
                    send_message(channel_debug, f"{sender} rolled {commandargs2[0]}d{commandargs2[1]} and got {infindex[r.randint(0, len(infindex)-1)]} ")
                rng = 0
                commandargs = ""
                commandargs2 = []
                return
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
            log.warning(f'{sender} tried to use the roll command in channel {channel_debug} but got an index error')
        except Exception as e:
            send_message(channel_debug, f'Error: {e}')
            log.exception(f"Error: {e}")
    elif command == "everyone":
        handle.write(f'NAMES {channel_debug}\r\n')
        handle.flush()
        # Get next line which contains names
        response = handle.readline().strip()
        if "353" in response:  # 353 is the IRC code for names list
            names = response.split(':')[-1].strip()  # Get names portion
            send_message(channel_debug, f'Users in channel: {names}')
        else:
            send_message(channel_debug, 'Error! if this happenes, tell cheese. Error string: Could not retrieve names')   
            log.error("Error! names command failed")

    elif command == "join": #add multiple channel support
        handle.write(f'JOIN {args[0]}\r\n')
        channel_list.append(args[0])
        if "#" not in args[0]:
            send_message(channel_debug, f'{sender}: Invalid format. Use !join #channel')
        elif "#site19" in args[0] or "#site17" in args[0]:
            send_message(channel_debug, f'{sender}: Sorry, Mando-Bot is not authorized to join that channel. Action logged.')
            log.warning(f'{sender} tried to join {args[0]} in channel {channel_debug} but got an error')
        else:
          send_message(channel_debug, f'Joined {args[0]}')
          log.info(f"Joined {args[0]}")
        handle.flush()

    elif command == "leave": #add multiple channel support
        
        if checkperms(full_host):
            if len(args[0])> 0:
                handle.write(f'PART {args[0]}\r\n')
                channel_list.remove(args[0])
                handle.flush()
                log.info(f"Left {args[0]}")
            else:
                handle.write(f"PART {channel_debug}\r\n")
                handle.flush()
        else: 
            send_message(channel_debug, 'Sorry, you are not authorized to use this command.     Action logged.')
            log.warning(f'{sender} tried to use the leave command in channel {channel_debug}')
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
            output2 = str(output[0]).split("title=")
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
              log.warning(f'{sender} tried to use the google command in channel {channel_debug} but got no results')
            else:
              send_message(channel_debug, f'{sender}: {output_str}')
        elif bool(list(search(args, num_results=1))[0]): # true, first result contains a 404 or error
            log.warning(f'{sender} tried to use the google command in channel {channel_debug} but got a 404 or error on first result')
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
                log.exception(f"Error: {e}")
        else:
            send_message(channel_debug, 'Error! if this happens, tell cheese. Error string 424')
            log.error("Error! google command failed")
    elif command == "!flags":
        if args[0] == "set":
            if args[1] == "debug":
                
                if checkperms(full_host):
                    global debug_flag
                    debug_flag = debug_flag + 1
                    if debug_flag > 1:
                        debug_flag = 0
                    send_message(channel_debug, f'Debug mode = {debug_flag}')
                    debug("", "check")
                    log.info(f'Debug mode set to {debug_flag} by {sender} in channel {channel_debug}')
                else:
                    send_message(channel_debug, 'Sorry, you are not authorized to use this command. Action logged.')    
                    log.warning(f'{sender} tried to use the debug command in channel {channel_debug}')
            elif args[1] == "latest_range":
                
                if checkperms(full_host):
                    global latest_range
                    latest_range = args[2]
                    
                    try:
                        if int(latest_range) > 5:
                            send_message(channel_debug, 'Error! latest_range cannot be greater than 5')
                            log.warning(f'{sender} tried to set latest_range to {latest_range} in channel {channel_debug}')
                            latest_range = 3
                        send_message(channel_debug, f'Latest search range = {latest_range}')
                    except ValueError:
                        send_message(channel_debug, 'Error! latest_range must be an integer')
                        log.warning(f'{sender} tried to set latest_range to {latest_range} in channel {channel_debug}')
                else:
                    send_message(channel_debug, 'Sorry, you are not authorized to use this command. Action logged.')
                    log.warning(f'{sender} tried to use the latest_range command in channel {channel_debug}')
            elif args[1] == "cache":
                
                if checkperms(full_host):
                    try:
                        crom.cache_set(int(args[2]))
                        send_message(channel_debug, f'Cache duration = {args[2]}')
                        log.info(f'Cache duration set to {args[2]} by {sender} in channel {channel_debug}')
                    except ValueError:
                        send_message(channel_debug, 'Error! cache duration must be an integer')
                        log.warning(f'{sender} tried to set cache duration to {args[2]} in channel {channel_debug}')
                    except Exception as e:
                        send_message(channel_debug, f'Error! if this happenes, tell cheese. Error string: {e}')
                        log.exception(f"Error: {e}")
                else:
                    send_message(channel_debug, 'Sorry, you are not authorized to use this command. Action logged.')
                    log.warning(f'{sender} tried to use the cache command in channel {channel_debug}')
        elif args[0] == "get":
            if args[1] == "debug":
                send_message(channel_debug, f'Debug mode = {debug_flag}')
    elif command == "ch" or command == "choose":
        output_str = " ".join(args)
        output = output_str.split(",")
        send_message(channel_debug, f'{sender}: {output[r.randint(0, len(output)-1)]}')    

    elif command == "search" or command == "s":
        try:
            output = crom.wikisearch(" ".join(args))
            output2 = ""
            output3 = []
            output4 = []
            output4.append(output["rating"].split("(")[0])
            output4.append(output["rating"].split("(")[1][0:len(output["rating"].split("(")[1])-1])
            output4.append(output4[1].split("/")[0].strip("+"))
            output4.append(output4[1].split("/")[1].strip("-"))
            output4.append(int(output4[2]) + int(output4[3]))
            output4.append(int(output4[2])/int(output4[4]))
            output4.append("")
            output4[5] = f"{output4[5]:.2%}"
            output4.pop(6)
            debug(0, output)
            debug(1, output4)
            debug(2, output4[5])
            
            #note: errors wont cause a poblem
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
            log.warning(f'{sender} tried to use the search command in channel {channel_debug} but got no results')
            return
        except Exception as e:
            send_message(channel_debug, f'{sender}: Error! String: {e}')
            log.exception(f"Error: {e}")

    elif command == "raw":
        
        if checkperms(full_host):
            args = " ".join(args)
            handle.write(f'{args}\r\n')
            handle.flush()
            log.info(f'Raw command used by {sender} in channel {channel_debug}. {args}')
        else:
            send_message(channel_debug, 'Sorry, you are not authorized to use this command. Action logged.')
            log.warning(f'{sender} tried to use the raw command in channel {channel_debug}')
    elif command == "reboot" or command == "!reboot":
        
        if checkperms(full_host):
            handle.write("QUIT :Rebooting\r\n")
            handle.flush()
            log.info(f'Reboot command used by {sender} in channel {channel_debug}')
            os.system("python3 main.py")
            log.info("Rebooted")
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit(0)
        else:
            send_message(channel_debug, "Sorry, you are not authorized to use this command. Action logged.")
            log.warning(f'{sender} tried to use the reboot command in channel {channel_debug}')
    elif command == "author" or command == "au":
        try:
            if len(args) == 0:
                if sender == "cheesepoop9870": #overrides for some users
                    output = crom.ausearch("theword9870")
                elif sender == "PineappleOnPizza":
                    output = crom.ausearch("theword9870")
                elif sender == "cheesepoop9870_":
                    output = crom.ausearch("theword9870")
                elif sender == "SoundChaser":
                    output = crom.ausearch("Sound Chaser")
                elif sender == "JuneBug":
                    output = crom.ausearch("bunnyomega")
                elif sender == "MsBadBitch":
                    output = crom.ausearch("DrEverett")
                elif sender == "Felds":
                    output = crom.ausearch("djkaktus")
                else:
                    output = crom.ausearch(sender)
            else:
                output = crom.ausearch(" ".join(args)) 
            #name, rank, mean rating, total rating, page count, scp count, tale count, goi count, artwork count, author page url, author page title, last page url, last page title, last page rating
            #note: errors wont cause a problem
            if output["authorPageUrl"] != "":
                send_message(channel_debug, f"{sender}: {output['name']} ({output['authorPageTitle']} - {output['authorPageUrl']}) has {output['pageCount']} pages ({output['pageCountScp']} SCPs, {output['pageCountTale']} Tales, {output['pageCountGoiFormat']} GOI formats, {output['pageCountArtwork']} Artworks, and {output['pageCountOther']} others) with a total rating of {output['totalRating']} and an average rating of {output['meanRating']}. Their latest page is {output['lastPageTitle']} with a rating of {output['lastPageRating']} - {output['lastPageUrl']}")
            else:
                send_message(channel_debug, f"{sender}: {output['name']} has {output['pageCount']} pages ({output['pageCountScp']} SCPs, {output['pageCountTale']} Tales, {output['pageCountGoiFormat']} GOI formats, {output['pageCountArtwork']} Artworks, and {output['pageCountOther']} others) with a total rating of {output['totalRating']} and an average rating of {output['meanRating']}. Their latest page is {output['lastPageTitle']} with a rating of {output['lastPageRating']} - {output['lastPageUrl']}")
        except IndexError:
            send_message(channel_debug, f'{sender}: No results found!')
            log.warning(f'{sender} tried to use the author command in channel {channel_debug} but got no results')
            return
        except Exception as e:
            send_message(channel_debug, f'{sender}: Error! String: {e}')
            log.exception(f"Error: {e}")
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
                    log.warning(f'{sender} tried to use the latest command in channel {channel_debug} but got no results')
                    return
                except Exception as e:
                    send_message(channel_debug, f'{sender}: Error! String: {e}')
                    log.exception(f"Error: {e}")

    elif command == "refresh":
        send_message(channel_debug, f'{sender}: Manually refreshing cache...')
        crom.refresh_cache()
        send_message(channel_debug, f'{sender}: Cache refreshed!')
        log.info(f'Cache refreshed by {sender} in channel {channel_debug}')
        #add db.py commands here too
    elif command == "irc":
        send_message(channel_debug, f'{sender}: https://www.rfc-editor.org/rfc/rfc1459.html')

    elif command == "youtube" or command == "yt" or command == "y":
        results = ytsearch(' '.join(args), 1).to_json()
        debug(0, json.loads(results)["videos"][0])
        debug(1, type(json.loads(results)))
        output.append(f"http://youtube.com/watch?v={json.loads(results)['videos'][0]['id']}") #0
        output.append(json.loads(results)['videos'][0]['title']) #1
        output.append(json.loads(results)['videos'][0]['channel']) #2
        output.append(json.loads(results)['videos'][0]['duration']) #3
        output.append(json.loads(results)['videos'][0]['views']) #4
        output.append(json.loads(results)['videos'][0]['publish_time']) #5
        send_message(channel_debug, f"{sender}: {output[1]} by {output[2]} {output[5]} - length {output[3]} - {output[4]} - {output[0]}")

    elif command == "brauthor" or command == "brau":
        try:
            output = crom.br_ausearch(" ".join(args)) 
            #note: errors wont cause a problem
            if output["authorPageUrl"] != "":
                send_message(channel_debug, f"{sender}: {output['name']} ({output['authorPageTitle']} - {output['authorPageUrl']}) has {output['pageCount']} pages ({output['pageCountLevel']} Levels, {output['pageCountEntity']} Entities, {output['pageCountObject']} Objects, and {output['pageCountOther']} others) with a total rating of {output['totalRating']} and an average rating of {output['meanRating']}. Their latest page is {output['lastPageTitle']} with a rating of {output['lastPageRating']} - {output['lastPageUrl']}")
            else:
                send_message(channel_debug, f"{sender}: {output['name']} has {output['pageCount']} pages ({output['pageCountLevel']} Levels, {output['pageCountEntity']} Entities, {output['pageCountObject']} Objects, and {output['pageCountOther']} others) with a total rating of {output['totalRating']} and an average rating of {output['meanRating']}. Their latest page is {output['lastPageTitle']} with a rating of {output['lastPageRating']} - {output['lastPageUrl']}")
        except IndexError:
            send_message(channel_debug, f'{sender}: No results found!')
            log.warning(f'{sender} tried to use the brauthor command in channel {channel_debug} but got no results')
            return
        except Exception as e:
            send_message(channel_debug, f'{sender}: Error! String: {e}')
            log.exception(f"Error: {e}")

    elif command == "brsearch" or command == "brs":
        try:
            output = crom.br_wikisearch(" ".join(args))
            output2 = ""
            output3 = []
            debug(0, output)
            #note: errors wont cause a poblem
            if output["title2"] == []: #no alt title
                output["title2"] = ""
                output["title"] = f"{output['title']},"
            else:
                output["title"] = f"{output['title']}:"
                output_str = dict(output["title2"][0])["title"]
                output_str = f"{output_str},"
            for x in range(0, len(output["authors"])):
                output3.append(dict(output["authors"][x])["user"]["name"])
            send_message(channel_debug, f"{sender}: {output['title']} ({output['rating']}, written on {output['createdAt']} by {', '.join(output3)} with {output['comments']} comments) - {output['url']}")
        except IndexError:
            send_message(channel_debug, f'{sender}: No results found!')
            log.warning(f'{sender} tried to use the brsearch command in channel {channel_debug} but got no results')
            return
        except Exception as e:
            send_message(channel_debug, f'{sender}: Error! String: {e}')
            log.exception(f"Error: {e}")
    elif command == "ping":
        send_message(channel_debug, f'{sender}: Pong!')
        # log.warning(f'{sender} used the ping command in channel {channel_debug}')
    elif command == "ping2":
        handle.write(f'PING {server} irc.scpwiki.com :ping\r\n')
        handle.flush()
        send_message(channel_debug, "e")
        log.warning(f'{sender} used the ping2 command in channel {channel_debug}')
        log.debug('^ that shouldnt happen')
    elif command == "diagnose":
        log.warning(f'{sender} used the diagnose command in channel {channel_debug}')
        # pinging the server
        handle.write(f'PING {server} irc.scpwiki.com :ping\r\n')
        handle.flush()
        if "PONG" in handle.readline().strip():
            send_message(channel_debug, f'{sender}: confirmed connection with IRC server')
        else:
            send_message(channel_debug, f'{sender}: connection with IRC server failed') 
            log.error(f'{sender} failed to connect to IRC server')
        # check crom
        # ignore the error
        if crom.wikisearch("SCP-049")["title"] == "SCP-049":
            send_message(channel_debug, f'{sender}: confirmed connection with Crom API')
        else:
            send_message(channel_debug, f'{sender}: connection with Crom API failed')
            log.error(f'{sender} failed to connect to Crom API')
        #check wikidot
        output = crom.check_wikidot()
        if output == 200:
            send_message(channel_debug, f'{sender}: confirmed connection with Wikidot ({output})')
        else:
            send_message(channel_debug, f'{sender}: connection with Wikidot failed. Error code: {output}')
            log.error(f'{sender} failed to connect to Wikidot. Error code: {output}')
        output = ""
    elif command == "logs":
        with open("app.log", "r") as file:
            log.info("Reading logs")
            content = file.read()
            # lines = content.split('\n')
            # for line in lines:
            #     if line.strip():  # Only print non-empty lines
            #         print(line.strip())
                    
        # Upload to pastebin
        log.info("Uploading logs to pastebin")
        log.info("Generating user key")
        user_key = pastebin2.generate_user_key(pastebin2.api_dev_key, pastebin2.username, pastebin2.password)
        log.info(f"User key generated: {user_key}")
        result = pastebin2.upload_paste(pastebin2.api_dev_key, user_key, content.strip(), "test", "text", 0, "10M")
        log.info("Uploaded logs to pastebin")
        log.info(f"Upload result: {result}")
        send_message(channel_debug, f'{sender}: Logs: {result}')

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
        log.info("Connected to IRC server")
        handle = ircsock.makefile(mode='rw', buffering=1, encoding='utf-8', newline='\r\n')
        print('NICK', nick, file=handle)
        print('USER', nick, nick, nick, ':'+realname, file=handle)
        log.info("Sent NICK and USER commands")
        
        
        joined = False
        history_bypass = 0
        while True:
            line = handle.readline().strip()
            print(line)
            
            #sasl auth
            #DONT TOUCH THIS
            if "Found" in line: 
                sasl = "Mando-Bot Mando-Bot PASSWORD?" #remember to hide password
                sasl = sasl.encode("utf-8")
                sasl = base64.b64encode(sasl)
                print('CAP REQ :sasl', file=handle)
                print('CAP REQ :sasl')
                print('AUTHENTICATE PLAIN', file=handle)
                print('AUTHENTICATE PLAIN')
                time.sleep(3) #this is needed for some reason
                print('AUTHENTICATE', sasl, file=handle)
                print('AUTHENTICATE', sasl)
                print('CAP END', file=handle)
                print('CAP END')
                log.info("Sent SASL auth")
            # Check for PING and respond with PONG
            if "PING" in line:
                pong = "PONG :" + line.split(':')[1]
                handle.write(pong + '\r\n')
                handle.flush()
                log.info("Sent PONG")
                # Send identification after first PING (server ready)
                if not joined:
                    handle.write('PRIVMSG NickServ :identify PASSWORD\r\n') #remember to hide password
                    log.info("Sent IDENTIFY")
                continue
            
            # Check for successful identification before joining channels
            if "You are now logged in as Mando-Bot" in line and not joined:
                time.sleep(1)  # Small delay after identification
                for x in channel_list:
                    handle.write(f'JOIN {x}\r\n')
                    handle.flush()
                    log.info(f"Joined {x}")
                handle.write(f'MODE {nick} :+B\r\n')
                handle.flush()
                joined = True
                log.info("Joined channel(s) after identification")
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
                        if channel_temp == "Mando-Bot":
                            channel_temp = sender
                        log.info(f"command sent: {command} {args} ({sender} -> {channel_temp})")
                        handle_command(command, args, handle, sender, channel_temp, full_host)
                        
                            # break
                history_check = line.split(":!!clear")
                history_channel = line #may break
                if len(history_check) > 1 and "#cheesepoop9870" in history_channel:
                    history_bypass = 1
                    handle.write('PRIVMSG #cheesepoop9870 :History cleared!\r\n')
                    handle.flush()
                    log.info("manual history clear")
    except Exception as e:
        print(f"Error: {e}")
        log.critical(f"Error: {e}")
        # break
    finally:
        try:
            sys.exit(1)
        except Exception as e:
            log.critical(f"Error: sys.exit(1) failed: {e}")
            pass
# HIDE PASSWORD
