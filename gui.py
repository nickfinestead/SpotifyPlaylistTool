from tkinter import *
class Gui:
    
    def __init__(self, si):
        self.spotifyInterface = si #SpotifyInterface object
        self.buttons = []
        self.root = Tk()
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
        #Label(bozo_frame, text = "TBD").grid(row=1, column = 0, sticky = 'w')
    def clear_pages(self, function):
        for frame in self.frame.winfo_children():
            frame.destroy()
        function()
        
    def run_mainloop(self):
        self.root.mainloop()