# https://stackoverflow.com/questions/12064130/is-there-any-way-to-check-if-a-twitch-stream-is-live-using-python

#python
import requests
import time
import pp.external.python.Utils as pUtils
#twitch
from twitchAPI.twitch import Twitch

client_id = pUtils.getEnvVar("TWITCH_CLIENT_ID")
client_secret = pUtils.getEnvVar("TWITCH_CLIENT_SECRET")

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])

TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"

API_HEADERS = {
    'Client-ID' : client_id,
    'Accept' : 'application/vnd.twitchtv.v5+json',
}

def checkUser(user): #returns true if online, false if not
    print(f"Checking if user {user} is live.")
    try:
        userid = twitch.get_users(logins=[user])['data'][0]['id']
        url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
        req = requests.Session().get(url, headers=API_HEADERS)
        jsondata = req.json()
        if 'stream' in jsondata:
            if jsondata['stream'] is not None: 
                print(f"{user} is live.")
                return True
            else:
                print(f"{user} is offline.")
                return False
    except Exception as e:
        print(f"Error checking user: {e}")
        return False