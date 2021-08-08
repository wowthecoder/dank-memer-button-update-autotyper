from http.client import HTTPSConnection
import json
from time import sleep
from random import randint
import re
from pynput import keyboard
import threading
from win10toast_click import ToastNotifier

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
    

comm_file = open("dank_commands.txt")
command_list = comm_file.read().splitlines()

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

    if "search" in command:
        search_response(response_dict)
    elif "crime" in command:
        crime_response(response_dict)
    elif "trivia" in command:
        trivia_response(response_dict)
    elif "pm" in command:
        pm_response(response_dict)
    elif "hl" in command:
        hl_response(response_dict)
    elif "fish" in command or "dig" in command:
        fish_dig_response(response_dict)

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
    
#separate search response to prioritise area51, grass, and mels room
def search_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        search_options = response_dict[0]["components"][0]["components"]
        option_labels = []
        for i in range(len(search_options)):
            option_labels.append(search_options[i]["label"])
        print(option_labels)
        if "area51" in option_labels:
            choice = search_options[option_labels.index("area51")]
        elif "grass" in option_labels:
            choice = search_options[option_labels.index("grass")]
        elif "mels room" in option_labels:
            choice = search_options[option_labels.index("mels room")]
        else:
            choice = search_options[randint(0, len(search_options)-1)]
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
    except Exception as e:
        print("Encountered exception:", e)

#separate crime response to prioritise tax evasion for badosz card
def crime_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        crime_options = response_dict[0]["components"][0]["components"]
        option_labels = []
        for i in range(len(crime_options)):
            option_labels.append(crime_options[i]["label"])
        if "tax evasion" in option_labels:
            choice = crime_options[option_labels.index("tax evasion")]
        else:
            choice = crime_options[randint(0, len(crime_options)-1)]
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
    except:
        pass

def trivia_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        answer_options = response_dict[0]["components"][0]["components"] #Options are in the array of dictionary of button info
        choice = answer_options[randint(0,len(answer_options)-1)]
        #now press the button
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
    except:
        pass

def pm_response(response_dict):
    try:
        response = response_dict[0]["content"]
        if "need to buy" in response:
            send_message(connect(), text[4], "pls with 5000")
            sleep(2)
            send_message(connect(), text[4], "pls buy laptop")
        message_id = response_dict[0]["id"]
        pm_options = response_dict[0]["components"][0]["components"]
        choice = pm_options[randint(0, len(pm_options)-1)]
        #now press the button
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"], choice["hash"])
        sleep(1)
        result_dict = get_response(connect(), text[4])
        result_msg = result_dict[0]["embeds"][0]["description"]
        print(result_msg)
        if "broke" in result_msg:
            send_message(connect(), text[4], "pls item laptop")
            sleep(2)
            laptop_reply_dict = get_response(connect(), text[4])
            laptop_reply = laptop_reply_dict[0]["embeds"][0]["title"]
            if "owned" not in laptop_reply:
                send_message(connect(), text[4], "pls with 5000")
                sleep(1)
                send_message(connect(), text[4], "pls buy laptop")
    except:
        pass

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
        pass
        
def fish_dig_response(response_dict):
    try:
        reply_content = response_dict[0]["content"]
        if "fish is too strong" in reply_content or "what's in the dirt" in reply_content:
            if "Type" not in reply_content or "reverse" not in reply_content:
                toaster = ToastNotifier()
                toaster.show_toast("Caught something in fish or dig", "Needs human intervention", duration=10, threaded=False)
    except:
        pass

keep_running = True

def on_press(key):
    global keep_running
    if key == keyboard.Key.esc:
        print("Ok, time to stop.")
        keep_running = False
        return False

def main():
    '''For testing
    send_message(connect(), text[4], "pls search")
    sleep(2)
    reply_to_dank_memer("pls search")
    sleep(randint(29, 35))
    '''
    while True:
        for command in command_list:
            command = command.split("=")[0].strip()
            if not keep_running:
                return
            send_message(connect(), text[4], command)
            sleep(2)
            reply_to_dank_memer(command) #sleep in this function, get the reply first
            sleep(randint(3,6))
    
def capture_events():
    while True:
        if not keep_running:
            return
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
                sleep(1)
                send_message(connect(), text[4], type_this)
            if "reverse" in event_str:
                backticks = [j for j, letter in enumerate(event_str) if letter == "`"]
                reverse_this = event_str[(backticks[0]+1):backticks[1]]
                print(reverse_this)
                reverse_this = ''.join(c for c in reverse_this if c.isprintable())
                reverse_this = reverse_this[::-1]
                print(reverse_this)
                sleep(1)
                send_message(connect(), text[4], reverse_this)
            sleep(1)
        except:
            pass

listener = keyboard.Listener(on_press=on_press)
listener.start()
main_thread = threading.Thread(target=main)
main_thread.start()
event_thread = threading.Thread(target=capture_events)
event_thread.start()
