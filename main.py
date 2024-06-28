from gui import *
from reorderPlaylist import *



if __name__ == "__main__":
    
    si = SpotifyInterface()
    si.playlist_id = "050MT3lxwGbDL6S1byaBRG" # Hardcoded for testing, will query for all options when implemented in gui 
    songs = si.get_tracks()
    song_uris = [song['track']['uri'].split(':')[2] for song in songs]
    sorted_songs = si.sort_tracks(songs)
    sorted_songs_uris = [song['track']['uri'].split(':')[2] for song in sorted_songs]
    #DEBUG
    #for i in range(0, len(songs)):
    #    print(f"{i:>3} {songs[i]['track']['name']:<70}| {sorted_songs[i]['track']['name']}")
    #gui = Gui(si)
    #gui.add_option("Help", lambda: gui.help)
    #gui.add_option("About", lambda: gui.about)
    #gui.add_option("Sort Playlist", lambda: gui.sort)
    #gui.add_option("Other", lambda: gui.other)
    #gui.run_mainloop()