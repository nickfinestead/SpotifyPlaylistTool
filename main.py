from gui import *




if __name__ == "__main__":
    gui = Gui()
    gui.add_option("Help", lambda: gui.help)
    gui.add_option("About", lambda: gui.about)
    gui.add_option("Sort Playlist", lambda: gui.sort)
    gui.add_option("Other", lambda: gui.other)
    gui.run_mainloop()