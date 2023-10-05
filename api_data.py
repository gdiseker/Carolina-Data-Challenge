from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from songs import Song_Attributes
import requests

import numpy as np
#from datascience import *


# plotting
import matplotlib
# %matplotlib inline
import matplotlib.pyplot as plots
# plots.style.use('fivethirtyeight')
# import warnings
# warnings.simplefilter('ignore', FutureWarning)



load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")



def get_token():
   auth_string = client_id + ":" + client_secret
   auth_bytes = auth_string.encode("utf-8")
   auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")


   url = "https://accounts.spotify.com/api/token"
   headers = {
   "Authorization": "Basic " + auth_base64,
   "Content-Type": "application/x-www-form-urlencoded"
   }
   data ={"grant_type": "client_credentials"}
   result = post(url, headers=headers, data=data)
   json_result = json.loads(result.content)
   token = json_result["access_token"]
   return token




def get_auth_header(token):
   return{"Authorization": "Bearer " + token}




def search_for_artist(token, artist_name):
   url = "https://api.spotify.com/v1/search"
   headers = get_auth_header(token)
   query = f"?q={artist_name}&type=artist&limit=1"


   query_url = url + query
   result = get(query_url, headers=headers)
   json_result = json.loads(result.content)["artists"]["items"]
   if len(json_result) == 0:
       print("No such artist with this name")
       return None
   return json_result[0]











def search_for_songs(token, start_year, end_year, offset):








   url = "https://api.spotify.com/v1/search"
   start_year_str = str(start_year)
   end_year_str = str(end_year)
   headers = get_auth_header(token)
   query = f"?q=year:{start_year_str}-{end_year_str}&type=track&limit=50&offset={offset}"








   query_url = url + query
   result = get(query_url, headers=headers)
   json_result = json.loads(result.content)["tracks"]
   return json_result








def search_attributes(token, song_ids):
   url = "https://api.spotify.com/v1/audio-features"
   headers = get_auth_header(token)
   query = f"?{song_ids}&limit=50"
   query_url = url + query
   result = get(query_url, headers=headers)
   json_result = json.loads(result.content)
   return json_result


















# for idx, song in enumerate(result["items"]):
#     print(f"{idx + 1} {song['id']}")










# print(song_atts['0d28khcov6AiegSCpG5TuT'].loudness)




def make_playlist(size, dance_min: float, dance_max: float, loudness_min: float, loudness_max:float, valence_min: float, valence_max: float, energy_min:float, energy_max: float, speechiness_min: float, speechiness_max: float):


   playlist: list[Song_Attributes] = []
   offset_idx = 0

   while (len(playlist) < size):
       token = get_token()
       result = search_for_songs(token, 2000, 2010, offset_idx*50)
       song_ids = []
       for song in result["items"]: song_ids.append(song['id'])
       song_id_str = "ids="
       for id in song_ids: song_id_str += f"{id},"
       song_attributes = search_attributes(token, song_id_str)
       # print(song_attributes)


       song_atts = {}


       for song_id, attribute in zip(song_ids, song_attributes["audio_features"]):
           if song_id not in song_atts:
               song_atts[song_id] = Song_Attributes(song_id, attribute)


       for key in song_atts:
           if dance_min <= song_atts[key].danceability <= dance_max and loudness_min <= song_atts[key].loudness <= loudness_max and valence_min <= song_atts[key].valence <= valence_max and energy_min <= song_atts[key].energy <= energy_max and speechiness_min <= song_atts[key].speechiness <= speechiness_max:
               playlist.append(song_atts[key])
               # print("song added")
               if len(playlist) is size: return playlist
      
   return playlist

def get_track_info(token, id):
   url = f"https://api.spotify.com/v1/tracks/{id}"


   headers = {
       "Authorization": f"Bearer {token}",
       "Content-Type": "application/json",
   }
  
   response = requests.get(url, headers=headers)
  
   if response.status_code == 200:
       track_data = response.json()
       artists = [artist['name'] for artist in track_data['artists']]
       song_name = track_data['name']
       return {"artists": artists, "name": song_name}
   else:
       print(f"Error: Unable to retrieve track information (Status Code: {response.status_code})")
       print(response.content)  # Print the response content for debugging
       return None
   

token = get_token()
result=search_for_songs(token, 2000,2010, 0)

song_ids = []
for song in result["items"]: song_ids.append(song['id'])
song_id_str = "ids="

for id in song_ids: song_id_str += f"{id},"
song_attributes = search_attributes(token, song_id_str)
#print(song_attributes)


#playlist_final = make_playlist(30, .5, .8, -15, 0, .3, .7, .7, .9, 0, .33)

# for song in playlist_final:
#     token=get_token()
#     track_id=song.track_id
#     track_info=get_track_info(token, song.track_id)

#     if (track_info):
#         print(track_info['name'] + ", ".join(track_info['artists']))

# for song in playlist_final: print(song.danceability, song.loudness, song.valence, song.energy, song.speechiness, song.id)


