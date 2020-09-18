import config
import utils
import socket
import re
from time import *
import _thread
import threading


def logic(m, channel):
    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    username = re.search(r"\w+", m).group(0)
    message = chat_message.sub("", m)
    if message.strip() == "!time":
        utils.sendmsg(s, channel, "it's currently: " + time.strftime("%I:%M %p %Z on %A %B %d %Y"))
    # elif username not in utils.fillOpList(channel):
    #     utils.ban(s, channel, username)
    # print(message)
    if m.__contains__(f"@{config.NICK}.tmi.twitch.tv") and username == config.NICK:
        print(f"Connected to channel {channel} successfully")
    elif not m.__contains__(f":tmi.twitch.tv 001 {config.NICK} :Welcome, GLHF!") and username != "twi" \
            and username != config.NICK and username != "tmi":
        print(channel, username, message)


def connect(channel):
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(channel).encode("utf-8"))
    text = f"Bot connected"
    utils.sendmsg(s, channel, text)
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            # utils.sendmsg(s, channel, "it's currently: " + asctime(localtime()))
            # print(response)
            messages = response.split("\r\n")
            [logic(m, channel) for m in messages if m != ""]


# if message.strip() == "!messages" and utils.isOp(username):
#     utils.mess(s, "Do something awesome!")
#     utils.mess(s, "Go and click the subscribe button there!")

threads = [threading.Thread(target=connect, args=["mazzy_max"])]
# threads = [threading.Thread(target=connect, args=["mazzy_max"]),
#            threading.Thread(target=connect, args=["potatohd404"])]
for j in threads:
    j.start()
# for j in threads:
#     j.join()
print("done")
