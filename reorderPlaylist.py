# pip install spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# pip install python-dotenv
from dotenv import load_dotenv

import os

load_dotenv()
# Spotify API credentials
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_uri")
scope = 'playlist-modify-private'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Get the playlist ID of the playlist you want to reorder
playlist_id = '1YwheUbfRYSbNVBMISwcRS'


# Spotify API limits to 100 tracks per request
def get_playlist_tracks(sp, playlist_id):
    offset = 0
    tracks = []

    while True:
        response = sp.playlist_tracks(playlist_id,
                                      offset=offset,
                                      fields='items.track(name,uri,),items.added_at,total',
                                      additional_types=['track'])

        tracks.extend(response['items'])
        offset += len(response['items'])

        if len(response['items']) == 0:
            break

    return tracks

# Get tracks from the playlist
results = get_playlist_tracks(sp, playlist_id)


sorted_res = sorted(results, key = lambda x: x['added_at'])
for i in range(0, len(results)):
    print(f"{i:>3}: {results[i]['track']['name']:<60} {results[i]['track']['uri']} {results[i]['added_at']}")

tracks = [track['track']['uri'].split(':')[2] for track in results]
sorted_track_uris = [track['track']['uri'].split(':')[2] for track in sorted_res]

i = 0
exit(0)
while sorted_track_uris:
    
    song = sorted_track_uris.pop()
    song_start_pos = tracks.index(song)
    
    print(f"i: {i}  Start_pos: {song_start_pos} Song URI: {song} Results Song URI: {tracks[song_start_pos]} ")
    sp.playlist_reorder_items(playlist_id, range_start=song_start_pos, insert_before=i)
    tracks.remove(song)
    tracks.insert(i,song)
    i = i+1
