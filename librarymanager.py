import os
import shutil

seperator = "\\"

class Album:
    def __init__(self, folderpath):
        self.folder = folderpath
        self.tracklist = []
        with open(self.folder + seperator + "album.txt") as f:
            curmode = "none"
            for line in f:
                if line.strip() == "":
                    continue
                if line[0] == ".":
                    curmode = line[1:].strip()
                    continue
                if curmode == "info":
                    parts = line.split(":")
                    if len(parts) > 1:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        if key == "title":
                            self.title = value
                        elif key == "artist":
                            self.artist = value
                        elif key == "year":
                            self.year = value
                        elif key == "art":
                            self.art = folderpath + seperator + value
                if curmode == "tracklist":
                    self.tracklist.append(line.strip())

class Library:
    def __init__(self, libpath):
        albumdir = os.walk(libpath + seperator + "albums")
        potential_albums = [a[0] for a in albumdir][1:]
        albumfolders = []
        for folder in potential_albums:
            if os.path.isfile(folder + seperator + "album.txt"):
                albumfolders.append(folder)
        self.albums = {index + 1: Album(folder) for index, folder in enumerate(albumfolders)}

    def getAlbums(self):
        return self.albums

    def loadAlbums(self, albumstoload, path):
        if len(albumstoload) == 0:
            return("Please select your album(s)");
        if os.path.exists(path):
            for fileName in os.listdir(path):
                if fileName.endswith(".mp3"):
                    os.remove(path + seperator + fileName)

            songtick = 0
            for a in albumstoload:
                album = self.albums[a]
                for song in album.tracklist:
                    print("Loading... " + song)
                    shutil.copyfile(album.folder + seperator + song, path + seperator + str(songtick) + "-" + song)
                    songtick += 1
            return('Ready to Load<br>(Loaded ' + str(len(albumstoload)) + ' album(s))')
        return('Could not find media device')


