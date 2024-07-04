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

#      DONE:
#     !!     Create CLI structure and logic
#     !!     CMD line parsing, arguments, help option, etc.
#            Alternatively, add gui
#     !!!    Implement Other Sorting options( Alphabetic, Alphanumeric, Length of Song, etc.) 

#      TBD:
#     !!!    Possible cached version of before run to revert changes to playlist
#            TBD


# Comparable to sorting by Date Added
def sort_dateadded(results):
    sorted_res = []
    for _, group in groupby(sorted(results, key = lambda x: x['added_at'], reverse=True), key = lambda x: x['added_at']):
        sorted_group = sorted(group, key = lambda x: (x['track']['album']['name'], x['track']['name']))
        sorted_res.extend(sorted_group)
    return sorted_res


# Sorts based on track name, then based on album name
def sort_alphabetic(results):
    sorted_res = []
    for _, group in groupby(sorted(results, key = lambda x: x['track']['name']), key = lambda x: x['track']['name']):
        sorted_group = sorted(group, key = lambda x: x['track']['album']['name'])
        sorted_res.extend(sorted_group)
    return sorted_res

# Sorts by artist name, then track name
def sort_artist(results):
    sorted_res = []
    for _, group in groupby(sorted(results, key = lambda x: x['track']['album']['artists'][0]['name']), key = lambda x: x['track']['album']['artists'][0]['name']):
        sorted_group = sorted(group, key = lambda x: x['track']['name'])
        sorted_res.extend(sorted_group)
    return sorted_res



class SpotifyInterface:
    def __init__(self):
        if not os.path.exists(".env"):
            print(f"ERROR: .env file is not found in the currently directory")
            exit(1)
        load_dotenv()
        # Spotify API credentials
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")
        self.scope = 'playlist-read-private playlist-modify-private'
        # Authenticate with Spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                    client_secret=self.client_secret,
                                                    redirect_uri='http://localhost:8080/',
                                                    scope=self.scope))
        
        # Get the playlist ID of the playlist you want to reorder
        self.playlist_id = ""
        self.name = ""

    def set_name(self, name):
        self.name = name
    
    def set_playlist(self, id):
        self.playlist_id = id
    def get_playlists(self):
        if self.name == "":
            return
        offset = 0
        playlists = []
        return_list = {}
        while True:
        
            response = self.sp.user_playlists(user=self.name, offset=offset)
            playlists.extend(response['items'])
            offset+=len(response['items'])
            if len(response['items']) == 0:
                break
        for i in playlists:
            try:
                if i['owner']['display_name'] == self.name or self.name in i['owner']['uri']:
                    f"{i['name']}"
                    return_list[i['uri'].split(':')[2]] = i['name']
            except:
                    pass
        return return_list

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
    def get_tracks(self):
        if self.playlist_id == "":
            return
        offset = 0
        tracks = []

        while True:
            response = self.sp.playlist_tracks(self.playlist_id,
                                          offset=offset,
                                          fields='items.track(name,uri,album,),items.added_at,total',
                                          additional_types=['track'])

            tracks.extend(response['items'])
            offset += len(response['items'])

            if len(response['items']) == 0:
                break

        return tracks
    
    def insert_playlist(self, sort = sort_dateadded):
        i = 0
        songs = self.get_tracks()
        song_uris = [song['track']['uri'].split(':')[2] for song in songs]
        #TODO: Add other sorting methods
        sorted_songs = sort(songs)
        sorted_songs_uris = [song['track']['uri'].split(':')[2] for song in sorted_songs]
        while sorted_songs_uris:
            progress = f"     {(i/len(song_uris))*100:5.2f}% Done"
            print(" "*(len(progress)+5) , end = "\r")
            print(progress, end = "\r")
            
            song = sorted_songs_uris.pop(0)
            song_start_pos = song_uris.index(song)
            
            #print(f"i: {i}  Start_pos: {song_start_pos} Song URI: {song} Results Song URI: {tracks[song_start_pos]} ")
            try:
                self.sp.playlist_reorder_items(self.playlist_id, range_start=song_start_pos, insert_before=i)
            except:
                print("ERROR: Exception thrown while trying to insert into the selected playlist")
                break
            song_uris.remove(song)
            song_uris.insert(i,song)
            i = i+1
        print(f"Finished processing {i} songs, have a nice day.")


