# https://stackoverflow.com/questions/12064130/is-there-any-way-to-check-if-a-twitch-stream-is-live-using-python

#python
import requests
import time
import pp.external.python.Utils as pUtils
#twitch
#from twitchAPI.twitch import Twitch

client_id = pUtils.getEnvVar("TWITCH_CLIENT_ID")
client_secret = pUtils.getEnvVar("TWITCH_CLIENT_SECRET")

#twitch = Twitch(client_id, client_secret)
#twitch.authenticate_app([])

#TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"

#API_HEADERS = {
#    'Client-ID' : client_id,
#    'Accept' : 'application/vnd.twitchtv.v5+json',
#}

#class Stream:
#
#    def __init__(self, title, streamer, game, thumbnail_url):
#        self.title = title
#        self.streamer = streamer
#        self.game = game
#        self.thumbnail_url = thumbnail_url

def getOAuthToken():
    #print(f"########## getOAuthToken() ##########")

    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }


    try:
        r = requests.post('https://id.twitch.tv/oauth2/token', body)

        keys = r.json()

        if 'access_token' in keys:
            result = keys['access_token']
            #print(f"########## return {result} ##########")
            return result
        else:
            return 0

    except Exception as e:
        result = "An error occured: " + str(e)
        print(f"########## return {result} ##########")
        return result

def checkIfLive(channel):
    #print(f"########## checkIfLive({channel}) ##########")
    url = "https://api.twitch.tv/helix/streams?user_login=" + channel
    token = getOAuthToken()

    if token == 0:
        result = "Failed to get auth token"
        return result

    HEADERS = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + token
    }

    try:
        req = requests.get(url, headers=HEADERS)
        result = req.json()
        print(f"########## return {result} ##########")
        return result

    except Exception as e:
        result = "An error occured: " + str(e)
        print(f"########## return {result} ##########")
        return result

def getChannelData(channel):
    #print(f"########## getChannelData({channel}) ##########")
    url = "https://api.twitch.tv/helix/users?login=" + channel
    token = getOAuthToken()

    HEADERS = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + token
    }

    try:
        req = requests.get(url, headers=HEADERS)
        result = req.json()
        print(f"########## return {result} ##########")
        return result

    except Exception as e:
        result = "An error occured: " + str(e)
        print(f"########## return {result} ##########")
        return result

#def getUserData(user):
#    try:
#        userid = twitch.get_users(logins=[user])['data'][0]['id']
#        url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
#        req = requests.Session().get(url, headers=API_HEADERS)
#        jsondata = req.json()
#        return jsondata
#    except Exception as e:
#        print(f"Error checking user: {e}")
#        return None   

#def checkUser(user): #returns true if online, false if not
#    print(f"Checking if user {user} is live.")
#    try:
#        userid = twitch.get_users(logins=[user])['data'][0]['id']
#        url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
#        req = requests.Session().get(url, headers=API_HEADERS)
#        jsondata = req.json()
#        if 'stream' in jsondata:
#            if jsondata['stream'] is not None: 
#                print(f"{user} is live.")
#                return True
#            else:
#                print(f"{user} is offline.")
#                return False
#    except Exception as e:
#        print(f"Error checking user: {e}")
#        return False