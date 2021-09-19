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

with open("shop_items.json", "r") as f:
    shop_item_dict = json.load(f)

with open("trivia_answers.json", "r") as f:
    trivia_answers_map = json.load(f)

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
    elif "hunt" in command or "fish" in command or "dig" in command:
        hunt_fish_dig_response(response_dict)

def press_button(connection, guild_id, channel_id, message_id, button_id, button_hash):
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
            press_button(connect(), text[3], text[4], message_id, choice["custom_id"], choice["hash"])
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
        press_button(connect(), text[3], text[4], message_id, choice["custom_id"], choice["hash"])
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
        press_button(connect(), text[3], text[4], message_id, choice["custom_id"], choice["hash"])
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
            press_button(connect(), text[3], text[4], message_id, low_button["custom_id"], low_button["hash"])
        else:
            high_button = response_dict[0]["components"][0]["components"][2]
            press_button(connect(), text[3], text[4], message_id, high_button["custom_id"], high_button["hash"])
    except:
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                hl_response(response_dict[1:])

def hunt_fish_dig_response(response_dict):
    try:
        reply_content = response_dict[0]["content"]
        minigames_or_ping = ["Dodge the the Fireball", "Catch the fish", "<@!484673336534892546>"]
        if any(phrase in reply_content for phrase in minigames_or_ping):
            print(reply_content)
            toaster = ToastNotifier()
            toaster.show_toast("Caught something in hunt or fish", "Needs human intervention", duration=10, threaded=False)
    except Exception as e:
        print("Encountered exception during fish or dig:", e)

keep_running = True
open_daily = True
gamble_list = ["pls with 4003=2", "pls se 1001=3", "pls gamble 1001=2", "pls slots max=2", "pls scratch 1001=2", "pls dep all=2"]
grind_list = [["pls search=2", "pls crime=2", "pls beg=1", "pls pm=2", "pls hl=2"], ["pls search=2", "pls hunt=2", "pls fish=2", "pls dig=2"]]
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
    send_message(connect(), text[4], "pls trivia")
    #time.sleep(2)
    #reply_to_dank_memer("pls slots max")
    #time.sleep(randint(29, 35))
    '''
    loop_count = 0
    no_need_wait = ["hunt", "fish", "dig"]
    global normal_hl
    while True:
        if not keep_running:
            return

        if time.time() - daily_duration > 600 and open_daily is True: #The response captured in the event thread
            send_message(connect(), text[4], "pls use daily")
            time.sleep(2)

        for command in gamble_list:
            command_text = command.split("=")[0]
            command_wait = int(command.split("=")[1])
            send_message(connect(), text[4], command_text)
            time.sleep(command_wait)
            if "scratch" in command_text:
                reply_to_dank_memer(command_text)
                time.sleep(1)

        grind_commands = grind_list[loop_count % 2]
        for command in grind_commands:
            command_text = command.split("=")[0]
            command_wait = int(command.split("=")[1])
            if "hl" in command_text:
                normal_hl = True
            send_message(connect(), text[4], command_text)
            time.sleep(command_wait)
            if "beg" not in command_text and "hl" not in command_text:
                reply_to_dank_memer(command_text)
                if any(word in command_text for word in no_need_wait):
                    continue
                else:
                    time.sleep(1)
        
        loop_count += 1
        print("LOOP NO. ", loop_count)

def press_event_button(connection, guild_id, channel_id, message_id, custom_id):
    button_data = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_id": message_id,
        "message_flags": 0,
        "application_id": "270904126974590976",
        "data": {"component_type": 2, "custom_id": custom_id},
    }

    try:
        connection.request("POST", "/api/v9/interactions", json.dumps(button_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300: #everything is alright
            pass
        else:
            print(f"While pressing event button, received HTTP {response.status}: {response.reason}")
    except Exception as e:
        print("Encountered exception when pressing event button:", e)
        
def capture_events():
    events = []
    while True:
        if not keep_running:
            return
        global daily_duration, daily_count
        try:
            event_dict = get_response(connect(), text[4])
            daily_str = event_dict[0]["content"]             
            if "Box Contents" in daily_str or "Opening Daily Box" in daily_str:
                print(daily_str)
                daily_duration = time.time()
                print(f"Ok daily opened at:", datetime.now())
            if "active right now" in daily_str:
                daily_duration = time.time()

            message_id = event_dict[0]["id"]
            shop_sales = ["What is the **type**", "What is the **name**", "What is the **cost**"]
            if len(event_dict[0]["components"]) > 0 and len(event_dict[0]["components"][0]["components"]) == 1: #Boss fight
                print("Boss Event!")
                press_event_button(connect(), text[3], text[4], message_id, event_dict[0]["components"][0]["components"][0]["custom_id"])
            elif len(event_dict[0]["embeds"]) > 0 and len(event_dict[0]["components"]) > 0:
                event_embed = event_dict[0]["embeds"][0]
                embed_description = event_embed["description"]
                button_options = event_dict[0]["components"][0]["components"]
                if "chose a secret number" in embed_description:
                    hl_response(event_dict)
                elif any(phrase in embed_description for phrase in shop_sales):
                    print("Yooo it's SHOP SALE mannnnn")
                    if event_embed["image"]["url"] in shop_item_dict:
                        item_info = shop_item_dict[event_embed["image"]["url"]]
                        bold_asterisks = [a.start() for a in re.finditer("\*\*", embed_description)]
                        wanted_property = embed_description[(bold_asterisks[0]+2):bold_asterisks[1]] #name, cost, or type
                        print("wanted property:", wanted_property)
                        for button in button_options:
                            if button["label"].lower() == item_info[wanted_property]:
                                answer_button = button
                                break
                        press_event_button(connect(), text[3], text[4], message_id, answer_button["custom_id"])
                    else:
                        print("Eh I found no answer")
                        choice = button_options[randint(0, len(button_options)-1)]
                        press_event_button(connect(), text[3], text[4], message_id, choice["custom_id"]) 
                elif "seconds to answer" in embed_description:
                    print("Trivia night boiiiiiiiiiiii")
                    button_options = event_dict[0]["components"][0]["components"]
                    #Get the category
                    category = event_dict[0]["embeds"][0]["fields"][1]["value"][1:-1]
                    print(category)
                    question = event_dict[0]["embeds"][0]["description"]
                    bold_asterisks = [a.start() for a in re.finditer("\*\*", question)]
                    question = question[(bold_asterisks[0]+2):bold_asterisks[1]]
                    if category in trivia_answers_map and question in trivia_answers_map[category]:
                        print("Found trivia answer")
                        answer_text = trivia_answers_map[category][question]
                        ans_btn = button_options[0] #fail safe
                        for button in button_options:
                            if button["label"] == answer_text:
                                choice = button
                                break  
                    else:
                        print("Can't find answer for trivia soz")
                        choice = button_options[randint(0, len(button_options)-1)]
                    press_event_button(connect(), text[3], text[4], message_id, choice["custom_id"])
                        
            time.sleep(1)
        except Exception as e:
            print("Encountered exception while capturing events:", e)

listener = keyboard.Listener(on_press=on_press)
listener.start()
main_thread = threading.Thread(target=main)
main_thread.start()
event_thread = threading.Thread(target=capture_events)
event_thread.start()
