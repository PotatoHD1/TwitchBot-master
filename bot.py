import config
import utils
import socket
import re
from time import *
import _thread
import threading
import codecs


def logic(s, m, channel, badWords):
    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    username = re.search(r"\w+", m).group(0)
    message = chat_message.sub("", m)
    if m.__contains__(f"@{config.NICK}.tmi.twitch.tv") and username == config.NICK:
        print(f"Connected to channel {channel} successfully")
    elif not m.__contains__(f":tmi.twitch.tv 001 {config.NICK} :Welcome, GLHF!") and username != "twi" \
            and username != config.NICK and username != "tmi":
        print(f"{channel}@{username}: {message}")
        message = message.strip()
        for word in message.split():
            if word in badWords:
                utils.timeout(s, channel, username, 55)
        if message == "!time":
            utils.sendmsg(s, channel, "it's currently: " + asctime(localtime()))
        elif message.strip().__contains__("!ban"):
            utils.timeout(s, channel, username,
                          30 if message.strip() == "!ban" else int(message.strip().split("!ban")[1]))


def connect(channel, badWords):
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(channel).encode("utf-8"))
    # text = f"Bot connected"
    # utils.sendmsg(s, channel, text)
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            messages = response.split("\r\n")
            [logic(s, m, channel, badWords) for m in messages if m != ""]


# if message.strip() == "!messages" and utils.isOp(username):
#     utils.mess(s, "Do something awesome!")
#     utils.mess(s, "Go and click the subscribe button there!")
if __name__ == "__main__":
    lineList = [line.rstrip('\r\n') for line in codecs.open(config.WORDSPATH, 'r', 'utf-8')]
    lineList = set(lineList)
    threads = [threading.Thread(target=connect, args=["mazzy_max", lineList]),
               threading.Thread(target=connect, args=["potatohd404", lineList])]
    for j in threads:
        j.start()
    # for j in threads:
    #     j.join()
    print("done")
