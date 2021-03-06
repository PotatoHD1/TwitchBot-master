import config
import urllib3
import json
import time
import _thread
from time import sleep


def sendmsg(sock, channel, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(channel, message).encode("utf-8"))


def ban(sock, channel, user):
    if not (user in fillOpList(channel) or user == channel):
        sendmsg(sock, channel, f"/ban {user}")
        print(f"Ban user {user} on channel {channel} for OVER 9000 seconds")


def timeout(sock, channel, user, seconds=30):
    if not (user in fillOpList(channel) or user == channel):
        sendmsg(sock, channel, f"/timeout {user} {seconds}")
        print(f"Timeout user {user} on channel {channel} for {seconds} seconds")


# req = request
# res = response
def fillOpList(channel):
    oplist = {}
    try:
        http = urllib3.PoolManager()
        url = f"http://tmi.twitch.tv/group/user/{channel}/chatters"
        req = http.request('GET', url, headers={"accept": "*/*"})
        res = req.data.decode('utf-8')
        if res.find("502 bad gateway") == - 1:
            data = json.loads(res)
            for p in data["chatters"]["moderators"]:
                oplist[p] = "mod"
            for p in data["chatters"]["global_mods"]:
                oplist[p] = "global_mod"
            for p in data["chatters"]["admins"]:
                oplist[p] = "admin"
            for p in data["chatters"]["staff"]:
                oplist[p] = "staff"
    finally:
        "Nothing happened"
    return oplist
