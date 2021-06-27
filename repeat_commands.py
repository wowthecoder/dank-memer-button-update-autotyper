# used to repeat commands such as pls use cheese and pls steal
from http.client import HTTPSConnection
import json
from time import sleep
from random import randint
import re

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
    "user-agent" : text[0],
    "authorization": text[1],
    "host": "discordapp.com",
    "referrer": text[2],
}

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
            print(f"While sending message, received HTTP status {response.status}: {response.reason}")
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
        print(f"WHile fetching message, received HTTP {response.status}: {response.reason}")

def main():
    command = input("What command do you wish to repeat? (steal <User_tag> / use cheese): ")
    if "cheese" in command:
        send_message(connect(), text[3], "pls item cheese")
        sleep(2)
        cheese_reply_dict = get_response(connect(), text[3])
        cheese_reply = cheese_reply_dict[0]["embeds"][0]["title"]
        if "owned" in cheese_reply:
            #Get the number of cheese
            num_list = re.findall('[0-9]+', cheese_reply)
            cheese_count = int(num_list[0])
            print(cheese_count)
            for i in range(cheese_count):
                send_message(connect(), text[3], "pls use cheese")
                sleep(2)
                send_message(connect(), text[3], "y")
                sleep(randint(4,6))
        else:
            print("You don't have any cheese dei")
    else: #pls steal
        while True:
            send_message(connect(), text[3], command)
            sleep(randint(125, 150))

main()
