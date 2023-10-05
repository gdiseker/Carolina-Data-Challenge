# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from api_data import get_token, search_for_songs, search_attributes, make_playlist, get_track_info, get_auth_header
# from dotenv import load_dotenv
# import os
# import base64
# from requests import post, get
# import json
# from songs import Song_Attributes

# app = Flask(__name__)
# CORS(app)


# @app.route('/script', methods=['POST'])
# def script():

#     load_dotenv()

#     client_id = os.getenv("CLIENT_ID")
#     client_secret = os.getenv("CLIENT_SECRET")
#     # Get the JSON data from the request
#     data = request.get_json()

#     # Access radio button values using their keys in the JSON data
#     danceability_value = data.get('danceability_options')
#     loudness_value = data.get('loudness_options')
#     valence_value = data.get('valence_options')
#     energy_value = data.get('energy_options')
#     speechiness_value = data.get('speechiness_options')

#     # Process the data as needed
#     # For example, you can print the values to the console
#     print(f'Danceability: {danceability_value}')
#     print(f'Loudness: {loudness_value}')
#     print(f'Valence: {valence_value}')
#     print(f'Energy: {energy_value}')
#     print(f'Speechiness: {speechiness_value}')

#     # Return a response (e.g., a JSON response)
#     response_data = {
#         'message': 'Data received successfully',
#         'danceability': danceability_value,
#         'loudness': loudness_value,
#         'valence': valence_value,
#         'energy': energy_value,
#         'speechiness': speechiness_value
#     }
#     dance_min = 0.0
#     dance_max = 1.0

#     if (danceability_value) == 1:
#         dance_min = 0;
#         dance_max = .2;

#     if (danceability_value) == 2:
#         dance_min = .2;
#         dance_max = .4;

#     if (danceability_value) == 3:
#         dance_min = .4;
#         dance_max = .6;

#     if (danceability_value) == 4:
#         dance_min = .6;
#         dance_max = .8;

#     if (danceability_value) == 5:
#         dance_min = .8;
#         dance_max = 1.0;

#     print(dance_min, dance_max)

#     playlist_final = make_playlist(30, .5, .8, -15, 0, .3, .7, .7, .9, 0, .33)

#     track_info_list = []

#     # for song in playlist_final:
#     #     token = get_token()  # Call the get_token function to get a new token for each request
#     #     track_id = song.track_id
#     #     track_info = get_track_info(token, track_id)
#     #     if track_info:
#     #         track_info_list.append(track_info)

#     # # Print the collected track information
#     # for track_info in track_info_list:
#     #     print(f"Track: {track_info['name']}")
#     #     print(f"Artists: {', '.join(track_info['artists'])}")
#     #     print()  # Separate tracks with an empty line

#     return jsonify(response_data), 200



# if __name__ == '__main__':
#     app.run()
from flask import Flask, request, jsonify
from flask_cors import CORS
from api_data import get_token, search_for_songs, search_attributes, make_playlist, get_track_info, get_auth_header
from dotenv import load_dotenv
import os
import base64
import json
from songs import Song_Attributes


def get_danceability_range(danceability_value):
    # Define danceability range values based on user preference
    if danceability_value == 1:
        return 0.5, 0.6
    elif danceability_value == 2:
        return 0.6, 0.7
    elif danceability_value == 3:
        return 0.7, 0.8
    elif danceability_value == 4:
        return 0.8, 0.9
    elif danceability_value == 5:
        return 0.9, 1.0
    else:
            # Default range (full range)
        return 0.0, 1.0
    
def get_loudness_range(loudness_value):
        # Define loudness range values based on user preference
    if loudness_value == 1:
        return -60.0, -45.0
    elif loudness_value == 2:
        return -45.0, -30.0
    elif loudness_value == 3:
        return -30.0, -15.0
    elif loudness_value == 4:
        return -15.0, -5.0
    elif loudness_value == 5:
        return -5.0, 0.0
    else:
            # Default range (full range from -60 to 0)
        return -60.0, 0.0


def get_valence_range(valence_value):
        # Define valence range values based on user preference
    if valence_value == 1:
        return 0.0, 0.2
    elif valence_value == 2:
        return 0.2, 0.4
    elif valence_value == 3:
        return 0.4, 0.6
    elif valence_value == 4:
        return 0.6, 0.8
    elif valence_value == 5:
        return 0.8, 1.0
    else:
            # Default range (full range from 0 to 1)
        return 0.0, 1.0
        

def get_speechiness_range(speechiness_value):
        # Define speechiness range values based on user preference
    if speechiness_value == 1:
        return 0.0, 0.066  # 0.0 to 0.066 corresponds to low speechiness
    elif speechiness_value == 2:
        return 0.066, 0.132  # 0.066 to 0.132 corresponds to somewhat low speechiness
    elif speechiness_value == 3:
        return 0.132, 0.198  # 0.132 to 0.198 corresponds to moderate speechiness
    elif speechiness_value == 4:
        return 0.198, 0.264  # 0.198 to 0.264 corresponds to somewhat high speechiness
    elif speechiness_value == 5:
        return 0.264, 0.33  # 0.264 to 0.33 corresponds to high speechiness
    else:
            # Default range (full range from 0 to 0.33)
        return 0.0, 0.33
        

def get_energy_range(energy_value):
        # Define energy range values based on user preference
    if energy_value == 1:
        return 0.0, 0.2  # 0.0 to 0.2 corresponds to low energy
    elif energy_value == 2:
        return 0.2, 0.4  # 0.2 to 0.4 corresponds to somewhat low energy
    elif energy_value == 3:
        return 0.4, 0.6  # 0.4 to 0.6 corresponds to moderate energy
    elif energy_value == 4:
        return 0.6, 0.8  # 0.6 to 0.8 corresponds to somewhat high energy
    elif energy_value == 5:
        return 0.8, 1.0  # 0.8 to 1.0 corresponds to high energy
    else:
            # Default range (full range from 0.0 to 1.0)
        return 0.0, 1.0


app = Flask(__name__)
CORS(app)

# Define a variable to store the Spotify access token
spotify_token = None

@app.route('/script', methods=['POST'])
def script():
    global spotify_token

    # Load environment variables
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Get the JSON data from the request
    data = request.get_json()

    # Access user preferences
    danceability_value = data.get('danceability_options')
    loudness_value = data.get('loudness_options')
    valence_value = data.get('valence_options')
    energy_value = data.get('energy_options')
    speechiness_value = data.get('speechiness_options')

    # Process user preferences and set the range values
    dance_min, dance_max = get_danceability_range(danceability_value)
    loudness_min, loudness_max = get_loudness_range(loudness_value)
    valence_min, valence_max = get_valence_range(valence_value)
    energy_min, energy_max = get_energy_range(energy_value)
    speechiness_min, speechiness_max = get_speechiness_range(speechiness_value)

    # Get or renew Spotify access token
    if spotify_token is None:
        spotify_token = get_token()

    # Generate the playlist based on user preferences
    playlist_final = make_playlist(
        size=30,
        dance_min=dance_min,
        dance_max=dance_max,
        loudness_min=loudness_min,
        loudness_max=loudness_max,
        valence_min=valence_min,
        valence_max=valence_max,
        energy_min=energy_min,
        energy_max=energy_max,
        speechiness_min=speechiness_min,
        speechiness_max=speechiness_max,
    )

    # Print the generated playlist
    for song in playlist_final:
        token=get_token()
        track_id=song.track_id
        track_info=get_track_info(token, song.track_id)

        if (track_info):
            print(track_info['name'] + ", "+(", ").join(track_info['artists']))

    # Return a response (e.g., a JSON response)
    response_data = {
        'message': 'Playlist generated successfully'
    }
    
    print(dance_max)
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run()


