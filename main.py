from gui import *
from reorderPlaylist import *



if __name__ == "__main__":
    
    si = SpotifyInterface()
    gui = Gui(si)
    gui.run_mainloop()