# spc = spotify playlist country

import requests
import base64
import json
import sys
from config import clientId, clientSecret

# Step 1 - Authorization 
url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}
## O.auth customization for spotify api
# Encode as Base64
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')


headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"

#another option instead of lines 9 and 19
# headers = {
#     'Authorization': f"Basic {base64Message}",
# }

## end of setup for O.Auth... line 23 begins actual use of O.Auth
r = requests.post(url, headers=headers, data=data)
# token will expire in an hour but since this is not an industrial sized app I'm not 
# going to stress about pulling in an expiration and will get a token each time the script runs
token = r.json()['access_token']
print(token)

# Step 2 - Use Access Token to get a list of playlists
# search url add specifics to endpoint https://api.spotify.com/v1/search
searchUrl='https://api.spotify.com/v1/search'
request_header = {
    "Authorization": "Bearer " + token
}


search_params = {
    'q':'"country romance"',
    'type':'playlist',
    'limit':'50',
}

res = requests.get(url=searchUrl, headers=request_header, params=search_params)
# print(res)
# print(res.json())

with open('playlists.json', 'w') as playlists:
    json.dump(res.json(), playlists)

print(res.json()['playlists']['items'][0]['id'])

playlists_items=[]

# exit()
# exit above prevents this from running, however keeping this so possible to do playlist search or something similar
playlistId = res.json()['playlists']['items'][0]['id']
# playlistUrl = 'https://open.spotify.com/playlist/6MOrRQeuTjbebAQW9xhfsc?si=JgzgWwQ-S5Os07ELi736pw'
playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
# request_header = {
#     "Authorization": "Bearer " + token
# }

pl_results = requests.get(url=playlistUrl, headers=request_header)
print(pl_results)
# print(res.text)
# print(json.dumps(res.json(), indent=2))
print(pl_results.json()['tracks']['items'][0]['track']['album']["artists"][0]["name"])

# with open('playlist_content.json', 'w') as playlist_content:
#     json.dump(pl_results.json(), playlist_content)