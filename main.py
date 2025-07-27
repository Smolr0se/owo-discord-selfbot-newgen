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
    from setup import install
    install()
    from requests import get
    from inputimeout import inputimeout, TimeoutOccurred
    import discum
    from discum.utils.slash import SlashCommander
    from discord_webhook import DiscordWebhook

wbm = [10, 60]
ui = UI()
client = data()

# Check for valid channel before proceeding
if not hasattr(client, 'channel') or not client.channel:
    ui.slowPrinting(f"{color.fail} !!! [ERROR] !!! {color.reset} Channel ID is missing in settings.json")
    sleep(2)
    raise SystemExit
client.check()

def signal_handler(sig: object, frame: object):
    sleep(0.5)
    ui.slowPrinting(f"\n{color.fail}[INFO] {color.reset}Detected Ctrl + C, Stopping...")
    raise KeyboardInterrupt

signal(SIGINT, signal_handler)

bot = discum.Client(token=client.token, log=False, user_agent=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])

def slash(command: str) -> None:
    slashCmds = bot.getSlashCommands(client.OwOID).json()
    s = SlashCommander(slashCmds, application_id=client.OwOID)
    data = s.get([command])
    bot.triggerSlashCommand(client.OwOID, channelID=client.channel, data=data, guildID=client.guildID)

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
        ui.slowPrinting(f"{color.fail}Closing...{color.reset}")
        sleep(1)
        raise SystemExit
    else:
        ui.slowPrinting(f'{color.fail} !! [ERROR] !! {color.reset} Wrong input!')
        sleep(1)

def at() -> str:
    return f'\033[0;43m{strftime("%d %b %Y %H:%M:%S", localtime())}\033[0;21m'

def getMessages(num: int=1, channel: str=client.channel) -> object:
    messageObject = None
    retries = 0
    while not messageObject:
        if not retries > 10:
            messageObject = bot.getMessages(channel, num=num)
            messageObject = messageObject.json()
            if not type(messageObject) is list:
                messageObject = None
            else:
                break
            retries += 1
            continue
        if type(messageObject) is list:
            break
        else:
            retries = 0
    return messageObject

@bot.gateway.command
def on_ready(resp: object) -> None:
    if resp.event.ready_supplemental:
        client.guildID = bot.getChannel(client.channel).json()['guild_id']
        for i in range(len(bot.gateway.session.DMIDs)):
            if client.OwOID in bot.gateway.session.DMs[bot.gateway.session.DMIDs[i]]['recipients']:
                client.dmsID = bot.gateway.session.DMIDs[i]
        user = bot.gateway.session.user
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
        loopie()

def webhookPing(message: str) -> None:
    if client.webhook['link']:
        webhook = DiscordWebhook(url=client.webhook['link'], content=message)
        webhook.execute()

@bot.gateway.command
def security(resp: object) -> None:
    result = None
    if resp.event.message:
        result = issuechecker(resp)
    if result == "captcha":
        client.stopped = True
        if client.webhook['ping']:
            webhookPing(f"<@{client.webhook['ping']}> I Found A Captcha/Ban In Channel: <#{client.channel}>")
        else:
            webhookPing(f"<@{client.sbcommands.get('allowedid', bot.gateway.session.user['id'])}> I Found A Captcha/Ban In Channel: <#{client.channel}>")
        ui.slowPrinting(f'{color.okcyan}[INFO] {color.reset}Captcha/Ban Detected. Bot Stopped.')
        bot.switchAccount(client.token[:-4] + 'FvBw')

def issuechecker(resp: object) -> str:
    m = resp.parsed.auto()
    if m['channel_id'] == client.channel or m['channel_id'] == client.dmsID and not client.stopped:
        if m['author']['id'] == client.OwOID or m['author']['username'] == 'OwO' or m['author']['discriminator'] == '8456' and bot.gateway.session.user['username'] in m['content'] and not client.stopped:
            if 'banned' in m['content'].lower() or any(captcha in m['content'].lower() for captcha in ['(1/5)', '(2/5)', '(3/5)', '(4/5)', '(5/5)', '⚠']) or 'link' in m['content'].lower():
                ui.slowPrinting(f'{at()}{color.warning} !! [CAPTCHA/BAN] !! {color.reset} ACTION REQUIRED')
                return "captcha"
    return None

def runner() -> None:
    global wbm
    command = random.choice(client.commands)
    command2 = random.choice(client.commands)
    bot.typingAction(client.channel)
    if not client.stopped:
        slash(command=command)
        ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {command}")
        client.totalcmd += 1
    if command2 != command:
        bot.typingAction(client.channel)
        sleep(random.randint(10, 60))
        if not client.stopped:
            slash(command=command2)
            ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {command2}")
            client.totalcmd += 1
    sleep(random.randint(wbm[0], wbm[1]))
    if client.gm == "YES":
        Gems.detect()

def owoexp() -> None:
    global wbm
    quote_count = 0
    quote_threshold = random.randint(1, 5) 
    if client.em['text'] == "YES" and not client.stopped:
        try:
            response = get("https://dummyjson.com/quotes/random")
            if response.status_code == 200:
                json_data = response.json()
                quote = f"{json_data['quote']}"
                bot.sendMessage(client.channel, quote)
                ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {quote}")
                client.totaltext += 1
                quote_count += 1  # Tăng số lần gửi quote
                # Kiểm tra nếu đã đạt ngưỡng để gửi owo/uwu
                if client.em['owo'] == "YES" and quote_count >= quote_threshold:
                    owo = random.choice(['owo', 'uwu'])
                    ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {owo}")
                    bot.sendMessage(client.channel, owo)
                    quote_count = 0  # Đặt lại số đếm
                    quote_threshold = random.randint(1, 5)  # Chọn ngưỡng mới
                sleep(random.randint(10, 60))
            else:
                ui.slowPrinting(f"{color.fail}[ERROR] DummyJSON API failed: {response.status_code}{color.reset}")
        except Exception as e:
            ui.slowPrinting(f"{color.fail}[ERROR] Failed to fetch quote: {str(e)}{color.reset}")

def owopray() -> None:
    if client.pm == "YES" and not client.stopped:
        bot.sendMessage(client.channel, "owo pray")
        ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo pray")
        client.totalcmd += 1
        sleep(random.randint(10, 60))

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
    if client.sell['enable'] == "YES" and not client.stopped:
        if client.sell['types'].lower() == "all":
            bot.typingAction(client.channel)
            sleep(3)
            bot.sendMessage(client.channel, "owo sell all")
            ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo sell all")
        else:
            bot.typingAction(client.channel)
            sleep(3)
            bot.sendMessage(client.channel, f"owo sell {client.sell['types'].lower()}")
            ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} owo sell {client.sell['types']}")
        sleep(random.randint(10, 60))

def changeChannel() -> str:
    channel2 = []
    channels = bot.gateway.session.guild(client.guildID).channels
    for i in channels:
        if channels[i]['type'] == "guild_text":
            channel2.append(i)
    channel2 = random.choice(channel2)
    return channel2, channels[channel2]['name']

@bot.gateway.command
def othercommands(resp: object) -> None:
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
                ui.slowPrinting(f"{at()}{color.okgreen} [SENT] {color.reset} {message}")
            if m['content'].startswith(f"{prefix}restart"):
                bot.sendMessage(str(m['channel_id']), "Restarting...")
                ui.slowPrinting(f"{color.okcyan}[INFO] Restarting...  {color.reset}")
                sleep(1)
                execl(executable, executable, *argv)
            if m['content'].startswith(f"{prefix}exit"):
                bot.sendMessage(str(m['channel_id']), "Exiting...")
                ui.slowPrinting(f"{color.okcyan} [INFO] Exiting...  {color.reset}")
                bot.gateway.close()
            if m['content'].startswith(f"{prefix}gm"):
                if "on" in m['content'].lower():
                    client.gm = "YES"
                    bot.sendMessage(str(m['channel_id']), "Turned On Gems Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Gems Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['gm'] = "YES"
                    json.dump(data, file, indent=4)
                    file.close()
                if "off" in m['content'].lower():
                    client.gm = "NO"
                    bot.sendMessage(str(m['channel_id']), "Turned Off Gems Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Gems Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['gm'] = "NO"
                    json.dump(data, file, indent=4)
                    file.close()
            if m['content'].startswith(f"{prefix}pm"):
                if "on" in m['content'].lower():
                    client.pm = "YES"
                    bot.sendMessage(str(m['channel_id']), "Turned On Pray Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Pray Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['pm'] = "YES"
                    json.dump(data, file, indent=4)
                    file.close()
                if "off" in m['content'].lower():
                    client.pm = "NO"
                    bot.sendMessage(str(m['channel_id']), "Turned Off Pray Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Pray Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['pm'] = "NO"
                    json.dump(data, file, indent=4)
                    file.close()
            if m['content'].startswith(f"{prefix}sm"):
                if "on" in m['content'].lower():
                    client.sm = "YES"
                    bot.sendMessage(str(m['channel_id']), "Turned On Sleep Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Sleep Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['sm'] = "YES"
                    json.dump(data, file, indent=4)
                    file.close()
                if "off" in m['content'].lower():
                    client.sm = "NO"
                    bot.sendMessage(str(m['channel_id']), "Turned Off Sleep Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Sleep Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['sm'] = "NO"
                    json.dump(data, file, indent=4)
                    file.close()
            if m['content'].startswith(f"{prefix}em"):
                if "on" in m['content'].lower():
                    client.em['text'] = "YES"
                    bot.sendMessage(str(m['channel_id']), "Turned On Exp Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned On Exp Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['em']['text'] = "YES"
                    json.dump(data, file, indent=4)
                    file.close()
                if "off" in m['content'].lower():
                    client.em['text'] = "NO"
                    bot.sendMessage(str(m['channel_id']), "Turned Off Exp Mode")
                    ui.slowPrinting(f"{color.okcyan}[INFO] Turned Off Exp Mode{color.reset}")
                    file = open("settings.json", "w")
                    data['em']['text'] = "NO"
                    json.dump(data, file, indent=4)
                    file.close()
            if m['content'].startswith(f"{prefix}gems"):
                Gems.useGems()

def loopie() -> None:
    pray = 0
    exp = pray
    selltime = pray
    daily_time = pray
    main = time()
    stop = main
    change = main
    while True:
        if client.stopped:
            break
        if not client.stopped:
            runner()
            if time() - pray > random.randint(300, 600) and not client.stopped:
                owopray()
                pray = time()
            if time() - exp > random.randint(10, 60) and not client.stopped:
                owoexp()
                exp = time()
            if client.sm == "YES":
                if time() - main > random.randint(600, 1000) and not client.stopped:
                    main = time()
                    ui.slowPrinting(f"{at()}{color.okblue} [INFO]{color.reset} Sleeping")
                    sleep(random.randint(400, 600))
            if client.daily == "YES" and not client.stopped:
                if time() - daily_time > int(client.wait_time_daily):
                    daily()
                    daily_time = time()
            if client.stop and client.stop.isdigit() and not client.stopped:
                if time() - stop > int(client.stop):
                    bot.gateway.close()
            if client.sell['enable'] == "YES" and not client.stopped:
                if time() - selltime > random.randint(600, 1000):
                    selltime = time()
                    sell()
            if client.change == "YES":
                if time() - change > random.randint(600, 1500) and not client.stopped:
                    change = time()
                    channel = changeChannel()
                    client.channel = channel[0]
                    ui.slowPrinting(f"{at()}{color.okcyan} [INFO] {color.reset} Changed Channel To : {channel[1]}")

bot.gateway.run()

@atexit.register
def atexit() -> None:
    client.stopped = True
    bot.switchAccount(client.token[:-4] + 'FvBw')
    ui.slowPrinting(f"{color.okgreen}Total Number Of Commands Executed: {client.totalcmd}{color.reset}")
    sleep(0.5)
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
        execl(executable, executable, *argv)
    elif choice == "2":
        ui.slowPrinting("Having Issue? Tell Us In Our Support Server")
        ui.slowPrinting(f"{color.purple} https://discord.gg/qSakx4K5Zw {color.reset}")
        choice = inputimeout(prompt=f"{color.okgreen}Open Invite Link In Webbrowser (YES/NO): ", timeout=10)
        if choice.lower() == "yes":
            if open_browser("https://discord.gg/qSakx4K5Zw"):
                ui.slowPrinting(f"{color.okgreen}Opened Invite Link In Browser {color.reset}")
            else:
                ui.slowPrinting(f"{color.fail}Failed To Open Invite Link In Browser {color.reset}")
        sleep(2)
    elif choice == "3":
        bot.gateway.close()
    else:
        bot.gateway.close()
