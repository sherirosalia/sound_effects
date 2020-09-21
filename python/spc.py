# spc = spotify playlist country
# https://developer.spotify.com/documentation/web-api/reference/search/search/#writing-a-query---guidelines
import requests
import base64
import json
import sys
import pandas as pd
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
    'q':'"hip hop romance"',
    'type':'playlist',
    'limit':'50',
}

res = requests.get(url=searchUrl, headers=request_header, params=search_params)
# print(res)
# print(res.json())

# with open('playlists.json', 'w') as playlists:
#     json.dump(res.json(), playlists)

# print(res.json()['playlists']['items'][0]['id'])

playlists_items={}

# exit()
# exit above prevents this from running, however keeping this so possible to do playlist search or something similar
# playlistId = res.json()['playlists']['items'][0]['id']
playlists = res.json()['playlists']['items']

for playlist in playlists:
    playlistId = playlist['id']
    playlistName = playlist['name']


    playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
    
    pl_results = requests.get(url=playlistUrl, headers=request_header)

    # songs = pl_results.json()['tracks']['items']
    # for song in songs:
    
    ## shorter -->
    for song in pl_results.json()['tracks']['items']:
        song_added = song["added_at"]
        song_album = song['track']['album']["name"] 
        song_name = song['track']['name']
        song_id = song['track']['id']
        song_release_date = song['track']['album']["release_date"] 
        # one way
        # if song['track']['album']["artists"] != []
           

        # better way
        
        if len(song['track']['album']["artists"]) > 0:
            song_artist = song['track']['album']["artists"][0]["name"]
        else: 
            song_artist = ''

        current_entry={
            'Artist' : song_artist,
            'song_album' : song_album,
            'Title' : song_name,
            'song_release_date' : song_release_date,
        }


        playlists_items[song_id] = current_entry


        # playlists_items[current_entry]
        print(f'song added date is: {song_added} song name is: {song_name} song id is: {song_id}')

    # print(pl_results.json()['tracks']['items'][0]['track']['album']["artists"][0]["name"])

    # with open('playlist_content.json', 'w') as playlist_content:
    #     json.dump(pl_results.json(), playlist_content)
    # print(playlist['id'])

with open('song_list.json', 'w') as playlist_content:
    json.dump(list(playlists_items.values()), playlist_content)

df = pd.DataFrame(list(playlists_items.values()))
df.head()
df.to_csv('hip_hop_list.csv', index=False)

# exit()
# # playlistUrl = 'https://open.spotify.com/playlist/6MOrRQeuTjbebAQW9xhfsc?si=JgzgWwQ-S5Os07ELi736pw'
# playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
# # request_header = {
# #     "Authorization": "Bearer " + token
# # }

# pl_results = requests.get(url=playlistUrl, headers=request_header)
# print(pl_results)
# # print(res.text)
# # print(json.dumps(res.json(), indent=2))
# print(pl_results.json()['tracks']['items'][0]['track']['album']["artists"][0]["name"])

# # with open('playlist_content.json', 'w') as playlist_content:
# #     json.dump(pl_results.json(), playlist_content)