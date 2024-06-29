from tkinter import *
from tkinter import ttk
from threading import Thread
import time


class Gui:   
    def __init__(self, si):
        self.spotifyInterface = si #SpotifyInterface object
        self.buttons = []
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Playlist Reorder Tool")
        self.root.geometry("600x600")
        self.options = Frame(self.root, width = 200, height = 800)
        self.options.pack(side=LEFT)
        self.bar = Frame(self.root)
        self.bar.pack(side=LEFT)
        self.bar.configure(height = 800, width = 2, bg="#000000")
        self.frame = Frame(self.root)
        self.frame.pack(side=LEFT)
        self.frame.configure(height=800, width=400)
        self.x = 0
        self.y = 0
        self.main_screen()
        
        self.playlists = {}
        self.add_option("Main", lambda: self.main_screen)
        self.add_option("Help", lambda: self.help)
        self.add_option("About", lambda: self.about)
        self.add_option("Sort Playlist", lambda: self.sort)
        self.add_option("Other", lambda: self.other)

    def main_screen(self):
        bozo_frame = Frame(self.frame)
        bozo_frame.place(x=0,y=0)
        Label(bozo_frame, text = "Please enter your spotify username").grid(row=1, column = 0, sticky = 'w')
        username = Entry(bozo_frame, width = 40)
        username.grid(column = 1, row = 1, stick = 'w')
        def do_processing():
            self.spotifyInterface.set_name(username.get().strip())
            self.playlists = self.spotifyInterface.get_playlists() # key is uri, value is name
            
        submit_btn = Button(bozo_frame, text = "Submit", command = lambda: Thread(target = do_processing).start())
        
            
        submit_btn.grid(column = 0, row = 2, sticky = 'w')
        # TODO: Add text input box
        # TODO: Pass input to spotifyInterface object, then grab playlists if username != ""
    def add_option(self, title :str, command):
        button = Button(self.options, text = title, width = 30, command = lambda: self.clear_pages(command()))
        button.place(x=self.x, y = self.y)
        self.buttons.append(button)
        self.y +=100
    
    def about(self):
        bozo_frame = Frame(self.frame)
        bozo_frame.place(x=0,y=0)
        Label(bozo_frame, text = "A simple tool/GUI to sort spotify playlists using Spotify's public API").grid(row=1, column = 0, sticky = 'w')
        
    def help(self):
        bozo_frame = Frame(self.frame)
        bozo_frame.place(x=0,y=0)
        Label(bozo_frame, text = "For support please open a issue on github").grid(row=1, column = 0, sticky = 'w')
        
    def other(self):
        bozo_frame = Frame(self.frame)
        bozo_frame.place(x=0,y=0)
        Label(bozo_frame, text = "TBD").grid(row=1, column = 0, sticky = 'w')
        
    def sort(self):        
        bozo_frame = Frame(self.frame)
        bozo_frame.place(x=0,y=0)
        Label(bozo_frame, text = "Select a playlist from the dropdown below then select sort.").grid(row=1, column = 0, sticky = 'w')
        playlist = StringVar()
        playlist.set("")
        playlist_dropdown = ttk.Combobox(bozo_frame,textvariable=playlist, values=list(self.playlists.values()), width = 40)
        playlist_dropdown.grid(row = 2, column = 0, sticky = 'w')
        def get_playlists():
            while len(playlist_dropdown['values']) == 0:
                try:
                    playlist_dropdown['values'] = list(self.playlists.values())
                except:
                    pass
        t = Thread(target = get_playlists)
        t.start()
        # TODO: Figure out why bug with running sort twice
        def get_key(val, dict):
            for (key, value) in dict.items():
                if val == value:
                    return key
        sort_btn = Button(bozo_frame, text = "Sort", width = 30, command = lambda: Thread(target = lambda: (self.spotifyInterface.set_playlist(get_key(playlist.get(),self.playlists)),self.spotifyInterface.insert_playlist())).start() )
        sort_btn.grid(row = 3, column = 0, sticky = 'w')
    
    def clear_pages(self, function):
        if self.spotifyInterface.name == "":
            #TODO: Add error message indicating that username isn't set yet
            return
        for frame in self.frame.winfo_children():
            frame.destroy()
        function()
        
    def run_mainloop(self):
        self.root.mainloop()