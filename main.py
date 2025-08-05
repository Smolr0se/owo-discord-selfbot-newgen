
#!/usr/bin/python

from os import execl, name, system
from sys import executable, argv
from signal import signal, SIGINT
from time import sleep, strftime, localtime, time
from datetime import timedelta
import atexit
import random
from re import findall
import json
from webbrowser import open as open_browser
import logging
from requests import get
from menu import UI
from color import color
from data import data
from gems import gems
from exception import exception
try:
    from requests import get
    from inputimeout import inputimeout, TimeoutOccurred
    import discum
    from discum.utils.slash import SlashCommander
    from discord_webhook import DiscordWebhook
except:
    from requests import get
    from inputimeout import inputimeout, TimeoutOccurred
    import discum
    from discum.utils.slash import SlashCommander
    from discord_webhook import DiscordWebhook

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

wbm = [10, 30]  
ui = UI()
client = data()

# Check for valid channel before proceeding
if not hasattr(client, 'channel') or not client.channel:
    logger.error("Channel ID is missing in settings.json")
    ui.slowPrinting(f"{color.fail} !!! [ERROR] !!! {color.reset} Channel ID is missing in settings.json")
    sleep(2)
    raise SystemExit
client.check()

def signal_handler(sig: object, frame: object):
    sleep(0.5)
    logger.info("Detected Ctrl + C, Stopping...")
    ui.slowPrinting(f"\n{color.fail}[INFO] {color.reset}Detected Ctrl + C, Stopping...")
    raise KeyboardInterrupt

signal(SIGINT, signal_handler)

bot = discum.Client(token=client.token, log=False, user_agent=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])

def slash(command: str) -> None:
    try:
        slashCmds = bot.getSlashCommands(client.OwOID).json()
        s = SlashCommander(slashCmds, application_id=client.OwOID)
        data = s.get([command])
        response = bot.triggerSlashCommand(client.OwOID, channelID=client.channel, data=data, guildID=client.guildID)
        if response and response.status_code == 429:
            logger.warning(f"Rate limit detected in slash command: {command}, pausing for 120s")
            ui.slowPrinting(f"{at()}{color.fail}[ERROR] Rate-limited detected in slash command, pausing for 120s...{color.reset}")
            sleep(120)
    except Exception as e:
        logger.error(f"Error in slash command '{command}': {str(e)}")
        sleep(60)

Gems = gems(bot)

while True:
    system('cls' if name == 'nt' else 'clear')
    ui.logo()
    ui.start()
    try:
        ui.slowPrinting("Automatically Pick Option [1] In 10 Seconds.")
        choice = inputimeout(prompt=f'{color.okgreen}Enter Your Choice: {color.reset}', timeout=10)
    except TimeoutOccurred:
        choice = "1"
    if choice == "1":
        break
    elif choice == "2":
        from newdata import main
        main()
    elif choice == "3":
        ui.info()
        continue
    elif choice == "4":
        logger.info("Closing bot")
        ui.slowPrinting(f"{color.fail}Closing...{color.reset}")
        sleep(1)
        raise SystemExit
    else:
        logger.error("Invalid input in menu")
        ui.slowPrinting(f'{color.fail} !! [ERROR] !! {color.reset} Wrong input!')
        sleep(1)

def at() -> str:
    return f'\033[0;43m{strftime("%d %b %Y %H:%M:%S", localtime())}\033[0;21m'

def getMessages(num: int=1, channel: str=client.channel) -> object:
    messageObject = None
    retries = 0
    while not messageObject and retries <= 10:
        try:
            messageObject = bot.getMessages(channel, num=num)
            messageObject = messageObject.json()
            if not isinstance(messageObject, list):
                messageObject = None
            else:
                break
            retries += 1
            sleep(5)
        except Exception as e:
            logger.error(f"Error in getMessages: {str(e)}")
            retries += 1
            sleep(5)
    if not messageObject:
        logger.error("Failed to retrieve messages after 10 retries")
    return messageObject

@bot.gateway.command
def on_ready(resp: object) -> None:
    if resp.event.ready_supplemental:
        try:
            client.guildID = bot.getChannel(client.channel).json()['guild_id']
            for i in range(len(bot.gateway.session.DMIDs)):
                if client.OwOID in bot.gateway.session.DMs[bot.gateway.session.DMIDs[i]]['recipients']:
                    client.dmsID = bot.gateway.session.DMIDs[i]
            user = bot.gateway.session.user
            logger.info(f"Logged in as {user['username']}#{user['discriminator']}")
            ui.slowPrinting(f"Logged in as {user['username']}#{user['discriminator']}")
            ui.slowPrinting('══════════════════════════════════════')
            ui.slowPrinting(f"{color.purple}Settings: ")
            ui.slowPrinting(f"Channel: {client.channel}")
            ui.slowPrinting(f"Gems Mode: {client.gm}")
            ui.slowPrinting(f"Sleep Mode: {client.sm}")
            ui.slowPrinting(f"Pray Mode: {client.pm}")
            ui.slowPrinting(f"EXP Mode: {client.em['text']}")
            ui.slowPrinting(f"+)Send \"OwO\": {client.em['owo']}")
            ui.slowPrinting(f"Selfbot Commands Prefix: '{client.sbcommands['prefix']}'")
            ui.slowPrinting(f"Selfbot Commands Allowedid: {client.sbcommands['allowedid']}")
            ui.slowPrinting(f"Webhook: {'YES' if client.webhook['link'] else 'NO'}")
            ui.slowPrinting(f"Webhook Ping: {client.webhook['ping']}")
            ui.slowPrinting(f"Daily Mode: {client.daily}")
            ui.slowPrinting(f"{'Stop After (Seconds)' if client.stop and client.stop.isdigit() else 'Stop Mode'}: {client.stop}")
            ui.slowPrinting(f"Sell Mode: {client.sell['enable']}")
            ui.slowPrinting(f"Solve Captcha Mode: No Longer Support")
            ui.slowPrinting('══════════════════════════════════════')
            if client.stop and client.stop.isdigit() and int(client.stop) < 1800:
                logger.warning(f"Stop time set to {client.stop}s, which is very short. Consider increasing it.")
            loopie()
        except Exception as e:
            logger.error(f"Error in on_ready: {str(e)}")
            sleep(60)

def webhookPing(message: str) -> None:
    if client.webhook['link']:
        try:
            webhook = DiscordWebhook(url=client.webhook['link'], content=message)
            webhook.execute()
        except Exception as e:
            logger.error(f"Error in webhookPing: {str(e)}")

@bot.gateway.command
def security(resp: object) -> None:
    try:
        result = None
        if resp.event.message:
            result = issuechecker(resp)
        if result == "captcha":
            client.stopped = True
            logger.warning("Captcha/Ban detected, stopping bot")
            if client.webhook['ping']:
                webhookPing(f"<@{client.webhook['ping']}> I Found A Captcha/Ban In Channel: <#{client.channel}>")
            else:
                webhookPing(f"<@{client.sbcommands.get('allowedid', bot.gateway.session.user['id'])}> I Found A Captcha/Ban In Channel: <#{client.channel}>")
            ui.slowPrinting(f'{color.okcyan}[INFO] {color.reset}Captcha/Ban Detected. Bot Stopped.')
            bot.switchAccount(client.token[:-4] + 'FvBw')
    except Exception as e:
        logger.error(f"Error in security: {str(e)}")

def issuechecker(resp: object) -> str:
    try:
        m = resp.parsed.auto()
        if m['channel_id'] == client.channel or m['channel_id'] == client.dmsID and not client.stopped:
            if m['author']['id'] == client.OwOID or m['author']['username'] == 'OwO' or m['author']['discriminator'] == '8456' and bot.gateway.session.user['username'] in m['content'] and not client.stopped:
                if 'banned' in m['content'].lower() or any(captcha in m['content'].lower() for captcha in ['(1/5)', '(2/5)', '(3/5)', '(4/5)', '(5/5)', '⚠']) or 'link' in m['content'].lower():
                    logger.warning(f"Captcha/Ban detected. Message content: {m['content']}")
                    ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA/BAN] !! {color.reset} ACTION REQUIRED')
                    return "captcha"
        return None
    except Exception as e:
        logger.error(f"Error in issuechecker: {str(e)}")
        return None

def runner() -> None:
    global wbm
    try:
        command = random.choice(client.commands)
        command2 = random.choice(client.commands)
        bot.typingAction(client.channel)
        sleep(random.randint(10, 30)) 
        if not client.stopped:
            slash(command=command)
            logger.info(f"Sent command: {command}")
            ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {command}")
            client.totalcmd += 1
        if command2 != command and not client.stopped:
            bot.typingAction(client.channel)
            sleep(random.randint(10, 30))  
            slash(command=command2)
            logger.info(f"Sent command: {command2}")
            ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {command2}")
            client.totalcmd += 1
        sleep(random.randint(wbm[0], wbm[1]))  
    except Exception as e:
        logger.error(f"Error in runner: {str(e)}")
        sleep(60)

def owoexp() -> None:
    global wbm
    if not hasattr(client, 'quote_count'):
        client.quote_count = 0
    if not hasattr(client, 'quote_threshold'):
        client.quote_threshold = random.randint(2, 4)  # Trước là 3-7
    if client.em['text'] == "YES" and not client.stopped:
        try:
            response = get("https://dummyjson.com/quotes/random")
            if response.status_code == 200:
                json_data = response.json()
                quote = f"{json_data['quote']}"
                bot.typingAction(client.channel)
                sleep(random.randint(2, 6))  # Trước là 5-15
                send_response = bot.sendMessage(client.channel, quote)
                if send_response.status_code == 429:
                    logger.warning("Rate limit detected in owoexp, pausing for 120s")
                    ui.slowPrinting(f"{at()}{color.fail}[ERROR] Rate-limited detected from Discord, pausing for 120s...{color.reset}")
                    sleep(120)
                    return
                logger.info(f"Sent quote: {quote}")
                ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {quote}")
                client.totaltext += 1
                client.quote_count += 1
                if client.em['owo'] == "YES" and client.quote_count >= client.quote_threshold:
                    sleep(random.randint(10, 30))  # Trước là 30-90
                    owo = random.choice(['owo', 'uwu'])
                    bot.typingAction(client.channel)
                    sleep(random.randint(2, 6))  # Trước là 5-15
                    send_response = bot.sendMessage(client.channel, owo)
                    if send_response.status_code == 429:
                        logger.warning("Rate limit detected in owoexp (owo/uwu), pausing for 120s")
                        ui.slowPrinting(f"{at()}{color.fail}[ERROR] Rate-limited detected from Discord, pausing for 120s...{color.reset}")
                        sleep(120)
                        return
                    logger.info(f"Sent owo/uwu: {owo}")
                    ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {owo}")
                    client.quote_count = 0
                    client.quote_threshold = random.randint(2, 4)
                sleep(random.randint(15, 40))  # Trước là 60-180
            else:
                logger.error(f"DummyJSON API failed: {response.status_code}")
                ui.slowPrinting(f"{color.fail}[ERROR] DummyJSON API failed: {response.status_code}{color.reset}")
        except Exception as e:
            logger.error(f"Error in owoexp: {str(e)}")
            sleep(60)

def owopray() -> None:
    if client.pm == "YES" and not client.stopped:
        try:
            bot.typingAction(client.channel)
            sleep(random.randint(5, 15))  # Trước là 5-15
            send_response = bot.sendMessage(client.channel, "owo pray")
            if send_response.status_code == 429:
                logger.warning("Rate limit detected in owopray, pausing for 120s")
                ui.slowPrinting(f"{at()}{color.fail}[ERROR] Rate-limited detected from Discord, pausing for 120s...{color.reset}")
                sleep(120)
                return
            logger.info("Sent command: owo pray")
            ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo pray")
            client.totalcmd += 1
            sleep(random.randint(60, 120))  # Trước là 60-120
        except Exception as e:
            logger.error(f"Error in owopray: {str(e)}")
            sleep(60)

def daily() -> None:
    if client.daily == "YES" and not client.stopped:
        bot.typingAction(client.channel)
        sleep(3)
        bot.sendMessage(client.channel, "owo daily")
        ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo daily")
        client.totalcmd += 1
        sleep(3)
        msgs = getMessages(num=5)
        daily_string = ""
        length = len(msgs)
        i = 0
        while i < length:
            if msgs[i]['author']['id'] == client.OwOID and msgs[i]['content'] != "" and ("Nu" in msgs[i]['content'] or "daily" in msgs[i]['content']):
                daily_string = msgs[i]['content']
                i = length
            else:
                i += 1
        if not daily_string:
            sleep(5)
            client.totalcmd -= 1
            daily()
        else:
            if "Nu" in daily_string:
                daily_string = findall('[0-9]+', daily_string)
                client.wait_time_daily = str(int(daily_string[0]) * 3600 + int(daily_string[1]) * 60 + int(daily_string[2]))
                ui.slowPrinting(f"{at()}{color.okblue} [INFO] {color.reset} Next Daily: {str(timedelta(seconds=int(client.wait_time_daily)))}s")
            if "Your next daily" in daily_string:
                ui.slowPrinting(f"{at()}{color.okblue} [INFO] {color.reset} Claimed Daily")

def sell() -> None:
    try:
        sell_type = client.sell.get('types', 'all')
        bot.typingAction(client.channel)
        sleep(random.randint(20, 60))
        bot.sendMessage(client.channel, f"owo sell {sell_type}")
        logger.info(f"Sent command: owo sell {sell_type}")
        ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo sell {sell_type}")
    except Exception as e:
        logger.error(f"Error in sell: {str(e)}")
        sleep(5)

def changeChannel() -> str:
    try:
        channel2 = []
        channels = bot.gateway.session.guild(client.guildID).channels
        for i in channels:
            if channels[i]['type'] == "guild_text":
                channel2.append(i)
        channel2 = random.choice(channel2)
        return channel2, channels[channel2]['name']
    except Exception as e:
        logger.error(f"Error in changeChannel: {str(e)}")
        return client.channel, "Unknown"

@bot.gateway.command
def othercommands(resp: object) -> None:
    try:
        prefix = client.sbcommands['prefix']
        with open("settings.json", "r") as f:
            data = json.load(f)
        if resp.event.message:
            m = resp.parsed.auto()
            if m['author']['id'] == bot.gateway.session.user['id'] or m['channel_id'] == client.channel and m['author']['id'] == client.sbcommands['allowedid']:
                if prefix == "None":
                    bot.gateway.removeCommand(othercommands)
                    return
                if m['content'].startswith(f"{prefix}send"):
                    message = m['content'].replace(f'{prefix}send ', '')
                    bot.sendMessage(str(m['channel_id']), message)
                    logger.info(f"Sent message: {message}")
                    ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {message}")
                if m['content'].startswith(f"{prefix}restart"):
                    bot.sendMessage(str(m['channel_id']), "Restarting...")
                    logger.info("Restarting bot")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Restarting...  {color.reset}")
                    sleep(1)
                    execl(executable, executable, *argv)
                if m['content'].startswith(f"{prefix}exit"):
                    bot.sendMessage(str(m['channel_id']), "Exiting...")
                    logger.info("Exiting bot")
                    ui.slowPrinting(f"{color.okcyan} [INFO] Exiting...  {color.reset}")
                    bot.gateway.close()
                if m['content'].startswith(f"{prefix}gm"):
                    if "on" in m['content'].lower():
                        client.gm = "YES"
                        bot.sendMessage(str(m['channel_id']), "Turned On Gems Mode")
                        logger.info("Turned On Gems Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Gems Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['gm'] = "YES"
                            json.dump(data, file, indent=4)
                    if "off" in m['content'].lower():
                        client.gm = "NO"
                        bot.sendMessage(str(m['channel_id']), "Turned Off Gems Mode")
                        logger.info("Turned Off Gems Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Gems Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['gm'] = "NO"
                            json.dump(data, file, indent=4)
                if m['content'].startswith(f"{prefix}pm"):
                    if "on" in m['content'].lower():
                        client.pm = "YES"
                        bot.sendMessage(str(m['channel_id']), "Turned On Pray Mode")
                        logger.info("Turned On Pray Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Pray Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['pm'] = "YES"
                            json.dump(data, file, indent=4)
                    if "off" in m['content'].lower():
                        client.pm = "NO"
                        bot.sendMessage(str(m['channel_id']), "Turned Off Pray Mode")
                        logger.info("Turned Off Pray Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Pray Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['pm'] = "NO"
                            json.dump(data, file, indent=4)
                if m['content'].startswith(f"{prefix}sm"):
                    if "on" in m['content'].lower():
                        client.sm = "YES"
                        bot.sendMessage(str(m['channel_id']), "Turned On Sleep Mode")
                        logger.info("Turned On Sleep Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Sleep Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['sm'] = "YES"
                            json.dump(data, file, indent=4)
                    if "off" in m['content'].lower():
                        client.sm = "NO"
                        bot.sendMessage(str(m['channel_id']), "Turned Off Sleep Mode")
                        logger.info("Turned Off Sleep Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Sleep Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['sm'] = "NO"
                            json.dump(data, file, indent=4)
                if m['content'].startswith(f"{prefix}em"):
                    if "on" in m['content'].lower():
                        client.em['text'] = "YES"
                        bot.sendMessage(str(m['channel_id']), "Turned On Exp Mode")
                        logger.info("Turned On Exp Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Exp Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['em']['text'] = "YES"
                            json.dump(data, file, indent=4)
                    if "off" in m['content'].lower():
                        client.em['text'] = "NO"
                        bot.sendMessage(str(m['channel_id']), "Turned Off Exp Mode")
                        logger.info("Turned Off Exp Mode")
                        ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Exp Mode{color.reset}")
                        with open("settings.json", "w") as file:
                            data['em']['text'] = "NO"
                            json.dump(data, file, indent=4)
                if m['content'].startswith(f"{prefix}gems"):
                    Gems.useGems()
    except Exception as e:
        logger.error(f"Error in othercommands: {str(e)}")

def loopie() -> None:
    pray_time = time()
    exp_time = time()
    hunt_battle_time = time()
    hunt_battle_count = 0
    daily_done = False
    main = time()
    stop = main
    change = main
    gems_check = main
    selltime = main

    while True:
        try:
            if client.stopped:
                logger.info("Bot stopped due to client.stopped=True")
                break

            now = time()

            # Hunt & Battle: mỗi 10-30s
            if now - hunt_battle_time > random.randint(10, 30):
                # Gửi lệnh hunt và battle
                if not client.stopped:
                    bot.typingAction(client.channel)
                    sleep(random.randint(5, 15))
                    slash("hunt")
                    logger.info("Sent command: hunt")
                    ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} hunt")
                    client.totalcmd += 1

                    bot.typingAction(client.channel)
                    sleep(random.randint(5, 15))
                    slash("battle")
                    logger.info("Sent command: battle")
                    ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} battle")
                    client.totalcmd += 1

                    hunt_battle_count += 1
                    hunt_battle_time = now

            # Daily: sau 2 lần hunt & battle đầu, chỉ 1 lần
            if not daily_done and hunt_battle_count >= 2 and client.daily == "YES" and not client.stopped:
                daily()
                daily_done = True
                logger.info("Daily command sent after 2 hunt & battle cycles")

            # Pray: mỗi 60-120s
            if now - pray_time > random.randint(100, 300) and not client.stopped:
                owopray()
                pray_time = now

            # EXP giữ nguyên
            if now - exp_time > random.randint(60, 180) and not client.stopped:
                owoexp()
                exp_time = now

            # Sleep mode giữ nguyên
            if client.sm == "YES" and not client.stopped:
                if now - main > random.randint(300, 1000):
                    main = now
                    logger.info("Entering sleep mode")
                    ui.slowPrinting(f"{at()}{color.okblue} [INFO]{color.reset} Sleeping")
                    sleep(random.randint(100, 500))

            # Stop Mode giữ nguyên
            if client.stop and client.stop.isdigit() and not client.stopped:
                if now - stop > int(client.stop):
                    logger.info(f"Stopping bot after {client.stop} seconds")
                    bot.gateway.close()

            # Sell giữ nguyên
            if client.sell['enable'] == "YES" and not client.stopped:
                if now - selltime > 600:  # 600 giây = 10 phút
                    selltime = now
                    sell()

            # Gems giữ nguyên
            if client.gm == "YES" and not client.stopped:
                if now - gems_check > 300:
                    Gems.detect()
                    gems_check = now

            # Change channel giữ nguyên
            if client.change == "YES" and not client.stopped:
                if now - change > random.randint(1800, 3600):
                    change = now
                    channel = changeChannel()
                    client.channel = channel[0]
                    logger.info(f"Changed channel to: {channel[1]}")
                    ui.slowPrinting(f"{at()}{color.okcyan} [INFO] {color.reset} Changed Channel To : {channel[1]}")

        except Exception as e:
            logger.error(f"Error in loopie: {str(e)}")
            sleep(60)

try:
    bot.gateway.run(auto_reconnect=True)
except Exception as e:
    logger.error(f"Gateway error: {str(e)}")
    ui.slowPrinting(f"{at()}{color.fail}[ERROR] Gateway error: {str(e)}{color.reset}")
    sleep(60)
    bot.gateway.run(auto_reconnect=True)

@atexit.register
def atexit() -> None:
    client.stopped = True
    try:
        bot.switchAccount(client.token[:-4] + 'FvBw')
    except Exception as e:
        logger.error(f"Error in atexit switchAccount: {str(e)}")
    logger.info(f"Total Commands Executed: {client.totalcmd}")
    ui.slowPrinting(f"{color.okgreen}Total Number Of Commands Executed: {client.totalcmd}{color.reset}")
    sleep(0.5)
    logger.info(f"Total Random Text Sent: {client.totaltext}")
    ui.slowPrinting(f"{color.okgreen}Total Number Of Random Text Sent: {client.totaltext}{color.reset}")
    sleep(0.5)
    ui.slowPrinting(f"{color.purple} [1] Restart {color.reset}")
    ui.slowPrinting(f"{color.purple} [2] Support {color.reset}")
    ui.slowPrinting(f"{color.purple} [3] Exit {color.reset}")
    try:
        ui.slowPrinting("Automatically Pick Option [3] In 10 Seconds.")
        choice = inputimeout(prompt=f'{color.okgreen}Enter Your Choice: {color.reset}', timeout=10)
    except TimeoutOccurred:
        choice = "3"
    if choice == "1":
        logger.info("Restarting bot")
        execl(executable, executable, *argv)
    elif choice == "2":
        ui.slowPrinting("Having Issue? Tell Us In Our Support Server")
        ui.slowPrinting(f"{color.purple} https://discord.gg/qSakx4K5Zw {color.reset}")
        choice = inputimeout(prompt=f"{color.okgreen}Open Invite Link In Webbrowser (YES/NO): ", timeout=10)
        if choice.lower() == "yes":
            if open_browser("https://discord.gg/qSakx4K5Zw"):
                logger.info("Opened invite link in browser")
                ui.slowPrinting(f"{color.okgreen}Opened Invite Link In Browser {color.reset}")
            else:
                logger.error("Failed to open invite link in browser")
                ui.slowPrinting(f"{color.fail}Failed To Open Invite Link In Browser {color.reset}")
        sleep(2)
    elif choice == "3":
        logger.info("Exiting bot")
        bot.gateway.close()
    else:
        logger.info("Exiting bot due to invalid choice")
        bot.gateway.close()
