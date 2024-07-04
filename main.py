from gui import Gui
from reorderPlaylist import SpotifyInterface
from cli import parse_flags,execute_flags
import sys


if __name__ == "__main__":
    
    si = SpotifyInterface()
    if len(sys.argv) < 1:
        gui = Gui(si)
        gui.run_mainloop()
    else:
        # Call parse_flags() method
        flags = parse_flags(sys.argv) # Will return a dict containing the flags or none if format isn't recognized      
        if len(flags) == 0:
            print("ERROR: No supported arguments supplied")
            exit(1)
        execute_flags(flags,si)