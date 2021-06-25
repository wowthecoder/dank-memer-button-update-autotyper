from http.client import HTTPSConnection
from json import dumps
from time import sleep
from random import randint

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
        connection.request("POST", f"/api/v6/channels/{channel_id}/messages", dumps(message_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:
            pass
        else:
            print(f"While sending message, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to send message")

def cycle(period, command):
    send_message(connect(), text[3], command)
    sleep(period)

def main():
    while True:
        cycle(randint(46, 55), command_list)

main()
