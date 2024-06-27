# pip install spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# pip install python-dotenv
from dotenv import load_dotenv
from itertools import groupby
import os

#   Priority List:
#       Low         !!!
#       Medium      !!
#       High:       !

#      TODO:
#     !!     Create CLI structure and logic
#     !!     CMD line parsing, arguments, help option, etc.
#            Alternatively, add gui
#     !!!    Implement Other Sorting options( Alphabetic, Alphanumeric, Length of Song, etc.) 
#     !!!    Possible cached version of before run to revert changes to playlist
#            TBD


#      Implemented (Needs Testing):
#            Finish logic for current sorting ( using the front of the list instead of popping the last item of the list )
#
#
#
#
#


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
playlist_id = '050MT3lxwGbDL6S1byaBRG'


# Spotify API limits to 100 tracks per request
#
#   Input:
#           sp: spotify object containing required information for API interaction
#           playlist_id: Spotify playlist ID for the playlist to retrieve the songs for
#
#   Description:
#           Use Spotify's public API to get up to 100 songs, while there are still songs to retrieve continue looping
#
#   Output: Returns a list of dictionaries containing song/playlist information.
def get_playlist_tracks(sp, playlist_id):
    offset = 0
    tracks = []

    while True:
        response = sp.playlist_tracks(playlist_id,
                                      offset=offset,
                                      fields='items.track(name,uri,album,),items.added_at,total',
                                      additional_types=['track'])

        tracks.extend(response['items'])
        offset += len(response['items'])

        if len(response['items']) == 0:
            break

    return tracks

# Get tracks from the playlist
results = get_playlist_tracks(sp, playlist_id)
sorted_res = []
for _, group in groupby(sorted(results, key = lambda x: x['added_at'], reverse=True), key = lambda x: x['added_at']):
    sorted_group = sorted(group, key = lambda x: (x['track']['album']['name'], x['track']['name']))
    sorted_res.extend(sorted_group)


#for i in range(0, len(results)):
#    print(f"{i:>3}: {results[i]['track']['name']:<60} {results[i]['track']['uri']} {results[i]['added_at']}")


# * DEBUG STATEMENT *
for i in range(0, len(results)):
    print(f"{i:>3}: {sorted_res[i]['track']['name']:<60} {sorted_res[i]['added_at']} {sorted_res[i]['track']['album']['name']}")
    
tracks = [track['track']['uri'].split(':')[2] for track in results]
sorted_track_uris = [track['track']['uri'].split(':')[2] for track in sorted_res]

i = 0
while sorted_track_uris:
    
    song = sorted_track_uris.pop(0)
    song_start_pos = tracks.index(song)
    
    #print(f"i: {i}  Start_pos: {song_start_pos} Song URI: {song} Results Song URI: {tracks[song_start_pos]} ")
    sp.playlist_reorder_items(playlist_id, range_start=song_start_pos, insert_before=i)
    tracks.remove(song)
    tracks.insert(i,song)
    i = i+1
print(f"Finished processing {i} songs, have a nice day.")