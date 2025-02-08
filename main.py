from gui import Gui
import argparse
from datetime import datetime
from reorderPlaylist import SpotifyInterface
import sys



if __name__ == "__main__":
    si = SpotifyInterface()
    if len(sys.argv) < 2:
        gui = Gui(si)
        gui.run_mainloop()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", type=str, help = "Spotify Username", required=True, default = "")
        parser.add_argument("-d", "--diff", type=str, nargs=2, help = "Diff Playlists", metavar=("PLAYLIST_1", "PLAYLIST_2"))
        parser.add_argument("-p", "--playlist", type=str, help = "Playlist name")
        parser.add_argument("-s", "--sort", type=str, help = "Sort Method", choices=["date", "alphabetic", "artist"], default="date")
        parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity.')
        args = parser.parse_args()
        def log(msg):
            if args.verbose:
                print(f"[DEBUG] {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {msg}")

        si.set_name(args.username) 
        log("START Fetching playlists ")
        si.get_playlists()
        log("END Fetching playlists ")
        if args.diff:
            log(f"Diff detected playlists \"{args.diff[0]}\"  \"{args.diff[1]}\"")
            si.diff(args.diff[0], args.diff[1])
        else:
            log(f"Sort \"{args.sort}\" for playlist \"{args.playlist}\"")
            # TODO: Add call to sort function, and add some sort of logic to convert string to function name, probably inside reorder file
