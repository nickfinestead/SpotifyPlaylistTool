from typing import Union
from reorderPlaylist import SpotifyInterface

#   List of currently supported flags
#   -p          Playlist Name
#   -pu         Playlist URI
#   -u          Spotify Username
#   -d          Enable debug
def parse_flags(cmd_args: list) -> Union[dict, None]:
    p_flag = False
    pu_flag = False
    u_flag = False
    d_flag = False
    flag_dict = {}
    for i in range(1, len(cmd_args)):
        #print(cmd_args[i])
        if cmd_args[i] == "-p":
            if not p_flag:
                flag_dict['Playlist_name'] = cmd_args[i+1]
                i+=1
                p_flag = True
        elif cmd_args[i] == "-pu":
            if not pu_flag:
                flag_dict['Playlist_uri'] = cmd_args[i+1]
                i+=1
                pu_flag = True
        elif cmd_args[i] == "-u":
            if not u_flag:
                flag_dict['Username'] = cmd_args[i+1]
        elif cmd_args[i] == "-d":
            pass
    return flag_dict
    
    
    #raise NotImplementedError("parse_flags is not implemented yet")
	
	
def execute_flags(flags:dict,  si: SpotifyInterface) -> None:
    keys = list(flags.keys())
    if 'Playlist_name' not in keys or ('Playlist_uri' not in keys and 'Username' not in keys):
        print("ERROR: Needed parameters to use this tool are not set")
        return
    if 'Playlist_uri' in keys:
        si.set_playlist(flags['Playlist_uri'])
        si.insert_playlist()
    else:
        si.set_name(flags['Username'])
        playlists = si.get_playlists()
        
        for (key, value) in playlists.items():
            if flags['Playlist_name'] == value:
                si.set_playlist(key)
        si.insert_playlist()