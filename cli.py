from typing import Union
from reorderPlaylist import SpotifyInterface, sort_dateadded, sort_alphabetic, sort_artist


#   List of currently supported flags
#   -pn          Playlist Name
#   -pu         Playlist URI
#   -u          Spotify Username
#   -d          Enable debug (FUTURE FLAG)
#   -s          Sort Method Used


def parse_flags(cmd_args: list) -> Union[dict, None]:
    
    flag_dict = {}
    flag_dict['Sort'] = sort_dateadded
    for i in range(1, len(cmd_args)):
        try:
            if cmd_args[i] == "-pn":
                flag_dict['Playlist_name'] = cmd_args[i+1]
                i+=1
            elif cmd_args[i] == "-pu":
                flag_dict['Playlist_uri'] = cmd_args[i+1]
                i+=1
            elif cmd_args[i] == "-u":
                    flag_dict['Username'] = cmd_args[i+1]
            elif cmd_args[i] == "-s":
                sorts = { "Date": sort_dateadded, "Alphabetic": sort_alphabetic, "Artist": sort_artist}
                try:
                    flag_dict['Sort'] = sorts[cmd_args[i+1]]
                    i+=1
                except:
                    print("ERROR: Unknown Sort option, defaulting to Date Added")
            elif cmd_args[i] == "-h":
                help_string = '''
    To use this utility run the program by using "python main.py ..." 
    if no arguments are supplied the GUI will be opened, 
    or if incorrect arguments are supplied the program will exit
                -u        Spotify Username
                -pn        Playlist Name, enclosed in quotes if multiple words
                -pu       Playlist Uri
                -h        Help
                -s        Sort Method(Date added by default, Alphabetic, or Artist)'''
                print(help_string)
                exit(0)
        except IndexError:
                print(f"ERROR: \"{cmd_args[i]}\" Flag cannot be used without value")
                exit(1)
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
        
        si.insert_playlist(sort = flags['Sort'])