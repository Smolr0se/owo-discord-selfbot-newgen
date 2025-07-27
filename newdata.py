from menu import UI
from json import load, dump
from time import sleep
from color import color

ui = UI()

def main():
    with open("settings.json", "r") as f:
        data = load(f)
    ui.newData()
    choice = input(f"{color.okgreen}Enter Your Choice: {color.reset}")
    if choice == "0":
        pass
    elif choice == "1":
        change_token(data, True)
        change_channel(data, True)
        change_pray_mode(data, True)
        change_gems_mode(data, True)
        change_exp_mode(data, True)
        change_sleep_mode(data, True)
        change_webhook(data, True)
        change_selfbot_commands(data, True)
        change_daily_mode(data, True)
        change_stop_time(data, True)
        change_sell_mode(data, True)
        change_switch_channel(data, True)
    elif choice == "2":
        change_token(data, False)
    elif choice == "3":
        change_channel(data, False)
    elif choice == "4":
        change_pray_mode(data, False)
    elif choice == "5":
        change_gems_mode(data, False)
    elif choice == "6":
        change_exp_mode(data, False)
    elif choice == "7":
        change_sleep_mode(data, False)
    elif choice == "8":
        change_webhook(data, False)
    elif choice == "9":
        change_selfbot_commands(data, False)
    elif choice == "10":
        change_daily_mode(data, False)
    elif choice == "11":
        change_stop_time(data, False)
    elif choice == "12":
        change_sell_mode(data, False)
    elif choice == "13":
        change_switch_channel(data, False)
    else:
        ui.slowPrinting(f"{color.fail}[INFO] {color.reset}Invalid Choice")
        sleep(1)
        main()

def change_token(data, all_settings):
    data['token'] = input("Please Enter Your Account Token: ")
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_channel(data, all_settings):
    data['channel'] = input("Please Enter Your Channel ID: ")
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_pray_mode(data, all_settings):
    data['pm'] = "YES" if input("Toggle Automatically Sending Pray (YES/NO): ").lower() == "yes" else "NO"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_gems_mode(data, all_settings):
    data['gm'] = "YES" if input("Toggle Automatically Using Gems (YES/NO): ").lower() == "yes" else "NO"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_exp_mode(data, all_settings):
    data['em']['text'] = "YES" if input("Toggle Automatically Sending Random Text To Level Up (YES/NO): ").lower() == "yes" else "NO"
    if data['em']['text'] == "YES":
        data['em']['owo'] = "YES" if input("\t +)Do You Want To Enable Automatically Sending \"OwO\" Also? (YES/NO): ").lower() == "yes" else "NO"
    else:
        data['em']['owo'] = "NO"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_sleep_mode(data, all_settings):
    data['sm'] = "YES" if input("Toggle Sleep Mode (YES/NO): ").lower() == "yes" else "NO"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_webhook(data, all_settings):
    data['webhook']['link'] = input("Toggle Discord Webhook (Enter Webhook Link, It'll Ping You If OwO Ask For Captcha. Otherwise Enter \"None\"): ")
    if data['webhook']['link'].lower() != "none":
        data['webhook']['ping'] = input("\t +)Do You Want To Ping A Specified User When OwO Asked Captcha? If Yes Enter User ID. Otherwise Enter \"None\": ")
    if data['webhook']['link'].lower() == "none":
        data['webhook']['link'] = None
    if data['webhook']['ping'] and data['webhook']['ping'].lower() == "none":
        data['webhook']['ping'] = None
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_selfbot_commands(data, all_settings):
    data['sbcommands']['enable'] = "YES" if input("Toggle Selfbot Commands, You Can Control Your Selfbot Using Commands (YES/NO): ").lower() == "yes" else "NO"
    if data['sbcommands']['enable'] == "YES":
        data['sbcommands']['prefix'] = input("\t +)Enter Your Selfbot Prefix: ")
        data['sbcommands']['allowedid'] = input("\t +)Do You Want Allow An User To Use Your Selfbot Commands? If Yes Enter The Account ID, Otherwise Enter \"None\": ")
        ui.slowPrinting("Great! You Can View Selfbot Commands At Option [3] Info At The Main Menu!")
        sleep(1)
    if data['sbcommands']['allowedid'] and data['sbcommands']['allowedid'].lower() == "none":
        data['sbcommands']['allowedid'] = None
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_daily_mode(data, all_settings):
    data['daily'] = "YES" if input("Toggle Automatically Claiming Daily (YES/NO): ").lower() == "yes" else "NO"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_stop_time(data, all_settings):
    data['stop'] = input("Toggle Stop After A Specific Time (YES/NO): ").lower() == "yes"
    if data['stop'] == "YES":
        data['stop'] = input("Enter Stop Time (Seconds): ")
    else:
        data['stop'] = "0"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_sell_mode(data, all_settings):
    data['sell']['enable'] = "YES" if input("Toggle Automatically Selling Animals (YES/NO): ").lower() == "yes" else "NO"
    if data['sell']['enable'] == "YES":
        ui.slowPrinting("Animal Type: C, U, R, M... (Type \"all\" To Sell All Animals)")
        ui.slowPrinting("C = Common, U = Uncommon, etc...")
        data['sell']['types'] = input("Enter Animal Type: ")
    else:
        data['sell']['types'] = "all"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

def change_switch_channel(data, all_settings):
    data['change'] = "YES" if input("Toggle Automatically Change Channel (YES/NO): ").lower() == "yes" else "NO"
    with open("settings.json", "w") as f:
        dump(data, f, indent=4)
    ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
    if not all_settings:
        main()

if __name__ == "__main__":
    main()