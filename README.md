# dank-memer-hack
## This script is compatible with the July 31 2021 button update!!
### The maintenance of this project has paused, as of now it is updated to function with the October 9.4.4 update
Prerequisite: You have to install python in your computer and configure python to be in your PATH variables first.\
![image](https://user-images.githubusercontent.com/82577844/135723075-b9ce055d-6e37-4c8e-8169-6e3838b059a6.png)
> (Tick the box that says "Add python 3.xx to PATH" when installing Python)

Just clone the repository to your local device(including the info.txt file) and run it. As simple as that.\
Install the missing modules via command prompt if you are seeing errors about missing modules:
```
pip install pynput
pip install win10toast_click
```

The first time you run the program, the program will prompt you to enter the 5 types of information below:
1. User agent
   - Google search "what is my user agent" and you will see the results
2. Discord Token
   - See this video https://www.youtube.com/watch?v=YEgFvgg7ZPI 
3. Discord Channel URL
   - That's the url in the browser address bar when you are currently viewing a text channel.
   - It is in the format: https://discord.com/channels/{a bunch of numbers}/{another bunch of numbers}
4. Discord Server ID
   - This is the first group of numbers in the Discord Channel URL.
   - Eg. if channel url = "https://discord.com/channels/238746123/8937492374" then the server ID would be 238746123
5. Discord Channel ID
   - That's the string of numbers that is at the last part of the Discord Channel URL.
   - Eg. if channel url = "https://discord.com/channels/238746123/8937492374" then the channel ID would be 8937492374

You only have to enter all this info once. In the future every time you run the program, it will ask you whether you want to configure the bot or not. Just press the enter/return key and the program will start normally.

Note:\
The discord_autotyper\[new\].py is not that frequently maintained, please use the gamble_for_lvls_macro.py script.\
This script **automatically opens daily boxes** but does **NOT** automatically use tidepods and pizzas(you have to use this two items manually)\
Pressing the ESC key will stop the program automatically, while pressing the $ key will stop opening daily boxes.

\[Works in both browser and desktop Discord app\]\
\[You don't have to stay in the Discord window/tab for it to work, this script will not interfere with your keyboard and mouse.\]
