from http.client import HTTPSConnection
import json
from time import sleep
from random import randint
import re

alt_acc = "Random Guy#8513"

file = open("info.txt")
text = file.read().splitlines()

if len(text) != 4 or input("Configure bot?: (y/n)") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
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
        print(f"While sending message, received HTTP {response.status}: {response.reason}")

def main():
    send_message(connect(), text[3], "pls inv")
    sleep(2)
    response_dict = get_response(connect(), text[3])
    footer = response_dict[0]["embeds"][0]["footer"]["text"]
    keyword_of = [k.start() for k in re.finditer("of", footer)]
    total_page_num = int(footer[(keyword_of[0]+3):])
    print(total_page_num)
    for page in range(1, total_page_num+1):
        send_message(connect(), text[3], "pls inv")
        sleep(1)
        response_dict = get_response(connect(), text[3])
        fields = response_dict[0]["embeds"][0]["fields"][0]["value"]

        #Get the number of items
        bold_asterisks = [a.start() for a in re.finditer("\*\*", fields)]
        #The asterisks will be in pairs(eg, **haha**), and only the second one is needed
        num_of_items = []
        for i in range(1, len(bold_asterisks), 2):
            num_start_pos = bold_asterisks[i] + 5
            num_str = ""
            while fields[num_start_pos].isdigit():
                num_str += fields[num_start_pos]
                num_start_pos += 1
            num_of_items.append(int(num_str))

        #Get the item id/name
        backticks = [b.start() for b in re.finditer("`", fields)]
        name_of_items = []
        for m in range(0, len(backticks), 2):
            item_name = fields[(backticks[m]+1):backticks[m+1]]
            name_of_items.append(item_name)
        
        for n in range(len(num_of_items)):
            send_message(connect(), text[3], f"pls gift {num_of_items[n]} {name_of_items[n]} {alt_acc}")
            sleep(1)
            response_dict = get_response(connect(), text[3])
            reply_content = response_dict[0]["content"]
            if "Are you sure" in reply_content:
                send_message(connect(), text[3], "yes")
            sleep(randint(20, 30))
            
main()
