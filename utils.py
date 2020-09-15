import config
import urllib3
import json
import time
import _thread
from time import sleep


def sendmsg(sock, channel, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(channel, message).encode("utf-8"))


def ban(sock, channel, user):
    sendmsg(sock, channel, ".ban {}".format(user))


def timeout(sock, channel, user, seconds=500):
    sendmsg(sock, channel, ".timeout {}".format(user, seconds))


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
        "Something went wrong...do nothing"
    return oplist
