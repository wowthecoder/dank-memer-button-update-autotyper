from http.client import HTTPSConnection
import json
from time import sleep
from random import randint
import re

alt_acc = "AngeryBirdie#8513"

file = open("info_two.txt")
text = file.read().splitlines()

if len(text) != 5 or input("Configure bot?: (y/n): ") == "y":
    file.close()
    file = open("info_two.txt", "w")
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
    "referrer": text[2],
}

print("Messages will be sent to " + header_data["referrer"] + ".")

def connect():
    return HTTPSConnection("discordapp.com", 443)

def send_message(connection, channel_id, message):
    message_data = {
        "content": message,
        "tts": False,
    }

    try:
        connection.request("POST", f"/api/v6/channels/{channel_id}/messages", json.dumps(message_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:
            pass
        else:
            print(f"While sending message, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to send message")

def get_response(connection, channel_id):
    channel = connection.request("GET", f"/api/v6/channels/{channel_id}/messages", headers=header_data)
    response = connection.getresponse()

    if 199 < response.status < 300:
        response_dict_str = response.read().decode('utf-8')
        response_dict = json.loads(response_dict_str)
        return response_dict
    else:
        print(f"While fetching message, received HTTP {response.status}: {response.reason}")

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

def main():
    try:
        send_message(connect(), text[4], "pls inv")
        sleep(2)
        response_dict = get_response(connect(), text[4])
        footer = response_dict[0]["embeds"][0]["footer"]["text"]
        numbers = list(map(int, re.findall(r'\d+', footer)))
        total_page_num = numbers[-1]
        print(total_page_num)
        for page in range(1, total_page_num+1):
            send_message(connect(), text[4], "pls inv")
            sleep(1)
            response_dict = get_response(connect(), text[4])
            fields = response_dict[0]["embeds"][0]["description"]

            #Get the number of items
            item_count = list(map(lambda x: int(x.replace(",", "")), re.findall(r'\d+[0-9,]*', fields))) #to include commas becuz dank memer is annoying this way
            #remove all ids of emojis
            item_count = [count for count in item_count if count < 10000000]
            print(item_count)

            #Get the item id/name
            backticks = [b.start() for b in re.finditer("`", fields)]
            name_of_items = []
            for m in range(0, len(backticks), 2):
                item_name = fields[(backticks[m]+1):backticks[m+1]]
                name_of_items.append(item_name)
        
            for n in range(len(item_count)):
                send_message(connect(), text[4], f"pls gift {item_count[n]} {name_of_items[n]} {alt_acc}")
                sleep(1)
                response_dict = get_response(connect(), text[4])
                if len(response_dict[0]["components"]) > 0:
                    yes_button = response_dict[0]["components"][0]["components"][1]
                    press_button(connect(), text[3], text[4], response_dict[0]["id"], yes_button["custom_id"], yes_button["hash"])
                sleep(randint(19, 20))
    except Exception as e:
        print(e)
            
main()
