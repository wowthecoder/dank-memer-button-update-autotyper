from http.client import HTTPSConnection
import json
from time import sleep
from random import randint
import re

file = open("info.txt")
text = file.read().splitlines()

if len(text)!= 4 or input("Configure bot? (y/n)") == "y":
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
        connection.request("POST", f"/api/v6/channels/{channel_id}/messages", json.dumps(message_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300: #everything is alright
            pass
        else:
            print(f"While sending message, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to send message")

def get_response(connection, channel_id):
    channel = connection.request("GET", f"/api/v6/channels/{channel_id}/messages", headers=header_data)
    response = connection.getresponse()

    if 199 < response.status < 300: #everything is alright
        response_dict_str = response.read().decode('utf-8')
        response_dict = json.loads(response_dict_str)
        return response_dict
    else:
        print(f"While fetching message, received HTTP {response.status}: {response.reason}") 

def reply_to_dank_memer(command):
    response_dict = get_response(connect(), text[3])

    if "search" in command:
        send_message(connect(), text[3], search_response(response_dict))
    elif "hl" in command:
        send_message(connect(), text[3], hl_response(response_dict))
    elif "pm" in command:
        pm_response()
    elif "trivia" in command:
        ans_choices = ['a', 'b', 'c', 'd']
        send_message(connect(), text[3], ans_choices[randint(0,3)])

def search_response(response_dict):
    response = response_dict[0]["content"]
    response = response.replace("\\ufeff", "") #\\ufeff is a character called the Byte Order Mark, which is invisible
    response = response.replace("\\", "")

    search_options = []
    #indexes of backticks
    backticks = [i for i, letter in enumerate(response) if letter == '`']
    search_options.append(response[(backticks[0]+1):backticks[1]])
    search_options.append(response[(backticks[2]+1):backticks[3]])
    search_options.append(response[(backticks[4]+1):backticks[5]])
    print(search_options)
    return search_options[randint(0,2)]

def hl_response(response_dict):
    response = response_dict[0]["embeds"][0]["description"]
    response = response.replace("\\ufeff", "")
    response = response.replace("\\", "")

    bold_asterisks = [a.start() for a in re.finditer("\*\*", response)]
    hint = int(response[(bold_asterisks[0]+2):bold_asterisks[1]])
    if hint <= 50:
        return "h"
    else:
        return "l"

def pm_response():
    pm_options = ['f', 'r', 'i', 'c', 'k']
    send_message(connect(), text[3], pm_options[randint(0,4)])
    sleep(3)
    pm_result_dict = get_response(connect(), text[3])
    pm_result = pm_result_dict[0]["content"]
    if "is broken" in pm_result:
        #check whether user still has laptops
        send_message(connect(), text[3], "pls item laptop")
        sleep(2)
        laptop_reply_dict = get_response(connect(), text[3])
        laptop_reply = laptop_reply_dict[0]["embeds"][0]["title"]
        if "owned" not in laptop_reply:
            send_message(connect(), text[3], "pls with 3500")
            sleep(1)
            send_message(connect(), text[3], "pls buy laptop")

def main():
    while True:
        '''For testing
        send_message(connect(), text[3], "pls trivia")
        sleep(3)
        reply_to_dank_memer("pls trivia")
        sleep(randint(29, 35))
        '''
        for command in command_list:
            command = command.split("=")[0].strip()
            send_message(connect(), text[3], command)
            sleep(2)
            reply_to_dank_memer(command)
            sleep(randint(3,6))

main()
