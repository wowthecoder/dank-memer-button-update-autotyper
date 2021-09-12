from http.client import HTTPSConnection
import json
import time
from random import randint
import re
from pynput import keyboard
import threading
from win10toast_click import ToastNotifier
from datetime import datetime

file = open("info.txt")
text = file.read().splitlines()

if len(text)!= 5 or input("Configure bot? (y/n): ") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord server ID: "))
    text.append(input("Discord channel ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()

header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discordapp.com",
    "referrer": text[2]
}

print("Messages will be sent to " + header_data["referrer"] + ".")

def connect():
    return HTTPSConnection("discordapp.com", 443)

def send_message(connection, channel_id, message):
    message_data = {
        "content" : message,
        "tts": False #tts stands for text-to-speech
    }

    try:
        connection.request("POST", f"/api/v9/channels/{channel_id}/messages", json.dumps(message_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300: #everything is alright
            pass
        else:
            print(f"While sending message, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to send message")

def get_response(connection, channel_id):
    channel = connection.request("GET", f"/api/v9/channels/{channel_id}/messages", headers=header_data)
    response = connection.getresponse()

    if 199 < response.status < 300: #everything is alright
        response_dict_str = response.read().decode('utf-8')
        response_dict = json.loads(response_dict_str)
        return response_dict
    else:
        print(f"While fetching message, received HTTP {response.status}: {response.reason}") 

def reply_to_dank_memer(command):
    response_dict = get_response(connect(), text[4])

    if "search" in command or "crime" in command:
        search_crime_response(response_dict)
    elif "pm" in command:
        pm_response(response_dict)
    elif "hl" in command:
        hl_response(response_dict)
    elif "scratch" in command:
        scratch_response(response_dict)

def press_button(connection, channel_id, guild_id, message_id, button_id, button_hash):
    button_data = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_id": message_id,
        "message_flags": 0,
        "application_id": "270904126974590976",
        "data": {"component_type": 2, "custom_id": button_id, "hash": button_hash},
    }

    try:
        connection.request("POST", "/api/v9/interactions", json.dumps(button_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300: #everything is alright
            pass
        else:
            print(f"While pressing button, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to press button")

def scratch_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        buttons = []
        for row in response_dict[0]["components"]:
            for btn in row["components"]:
                buttons.append(btn)
        for i in range(3):
            choice = buttons[randint(0, len(buttons)-1)]
            press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
            buttons.remove(choice)
            time.sleep(0.5)
    except ValueError as e:
        print(e)
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                scratch_response(response_dict[1:])
        
def search_crime_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        answer_options = response_dict[0]["components"][0]["components"] #Options are in the array of dictionary of button info
        choice = answer_options[randint(0,len(answer_options)-1)]
        #now press the button
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
    except:
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                search_crime_response(response_dict[1:])

def pm_response(response_dict):
    try:
        response = response_dict[0]["content"]
        if "need to buy" in response:
            send_message(connect(), text[4], "pls with 5000")
            time.sleep(2)
            send_message(connect(), text[4], "pls buy laptop")
        message_id = response_dict[0]["id"]
        pm_options = response_dict[0]["components"][0]["components"]
        choice = pm_options[randint(0, len(pm_options)-1)]
        #now press the button
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
    except:
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                pm_response(response_dict[1:])

def hl_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        hint_message = response_dict[0]["embeds"][0]["description"]
        bold_asterisks = [a.start() for a in re.finditer("\*\*", hint_message)]
        hint_num = int(hint_message[(bold_asterisks[0]+2):bold_asterisks[1]])
        if hint_num >= 50:
            low_button = response_dict[0]["components"][0]["components"][0]
            press_button(connect(), text[4], text[3], message_id, low_button["custom_id"], low_button["hash"])
        else:
            high_button = response_dict[0]["components"][0]["components"][2]
            press_button(connect(), text[4], text[3], message_id, high_button["custom_id"], high_button["hash"])
    except:
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                hl_response(response_dict[1:])

keep_running = True
open_daily = True
command_list = ["pls with 4003=2", "pls se 1001=3", "pls gamble 1001=2", "pls slots max=2", "pls scratch 1001=2", "pls dep all=2"]
daily_duration = time.time() - 601

def on_press(key):
    global keep_running, open_daily
    try:
        if key.char == '$':
            print("Welp, I will stop opening daily boxes.")
            open_daily = False
    except AttributeError:
        if key == keyboard.Key.esc:
            print("Ok, time to stop.")
            keep_running = False
            return False

def main():
    '''
    #For testing
    send_message(connect(), text[4], "pls scratch 1001")
    time.sleep(2)
    reply_to_dank_memer("pls scratch 1001")
    #time.sleep(randint(29, 35))
    '''
    search_cooldown = time.time() - 31
    crime_cooldown = time.time() - 46
    beg_cooldown = time.time() - 46
    pm_cooldown = time.time() - 41
    hl_cooldown = time.time() - 31
    while True:
        if not keep_running:
            return
        if time.time() - daily_duration > 600 and open_daily is True: #The response captured in the event thread
            send_message(connect(), text[4], "pls use daily")
            time.sleep(2)

        for command in command_list:
            command_text = command.split("=")[0]
            command_wait = int(command.split("=")[1])
            send_message(connect(), text[4], command_text)
            time.sleep(command_wait)
            if "scratch" in command_text:
                reply_to_dank_memer(command_text)
                time.sleep(1)
        if time.time() - search_cooldown > 30:
            send_message(connect(), text[4], "pls search")
            search_cooldown = time.time()
            time.sleep(2)
            reply_to_dank_memer("pls search")
            time.sleep(1)
        if time.time() - crime_cooldown > 45:
            send_message(connect(), text[4], "pls crime")
            crime_cooldown = time.time()
            time.sleep(2)
            reply_to_dank_memer("pls crime")
            time.sleep(1)
        if time.time() - beg_cooldown > 45:
            send_message(connect(), text[4], "pls beg")
            beg_cooldown = time.time()
            time.sleep(1)
        if time.time() - pm_cooldown > 40:
            send_message(connect(), text[4], "pls pm")
            pm_cooldown = time.time()
            time.sleep(2)
            reply_to_dank_memer("pls pm")
            time.sleep(1)
        if time.time() - hl_cooldown > 30:
            send_message(connect(), text[4], "pls hl")
            hl_cooldown = time.time()
            time.sleep(2)
            reply_to_dank_memer("pls hl")
            time.sleep(1)
 
def capture_events():
    while True:
        if not keep_running:
            return
        global daily_duration
        try:
            event_dict = get_response(connect(), text[4])
            event_str = event_dict[0]["content"]
            event_str = event_str.replace("\\ufeff", "")
            event_str = event_str.replace("\\", "")
            if "Type" in event_str or "Retype" in event_str or "typing" in event_str:
                backticks = [j for j, letter in enumerate(event_str) if letter == "`"]
                type_this = event_str[(backticks[0]+1):backticks[1]]
                print(type_this)
                type_this = ''.join(c for c in type_this if c.isprintable())
                print(type_this)
                time.sleep(1)
                send_message(connect(), text[4], type_this)
            if "Box Contents" in event_str or "Opening Daily Box" in event_str:
                print(event_str)
                daily_duration = time.time()
                print("Ok daily opened at:", datetime.now())
            if "active right now" in event_str:
                daily_duration = time.time()
            time.sleep(1)
        except:
            pass

listener = keyboard.Listener(on_press=on_press)
listener.start()
main_thread = threading.Thread(target=main)
main_thread.start()
event_thread = threading.Thread(target=capture_events)
event_thread.start()
