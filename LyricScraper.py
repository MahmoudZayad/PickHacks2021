import requests  # for making HTTP requests
from bs4 import BeautifulSoup  # for parsing HTML and XML files
import re  # for regular expressions
import time  # for time operations
import os

class ScrapeArtist:
    def __init__(self):
        self.url = 'https://genius.com/artists/'
        self.response = requests.get(self.url)  # request site response
        self.data = BeautifulSoup(self.response.text, "html.parser")  # parse data
        self.artist_index = self.data.findAll(href=re.compile("https://genius.com/artists-index/[a-z]"))


    # clean up name and capitilize it
    def clean_name(self, name):
        name = name.lower()
        name = name.capitalize()
        name = name.replace(" ", "-")
        return name

    def find_artist(self, name):
        first_ch = name[0]  # intial of artist to look through index

        link = None
        for l in self.artist_index:
            if first_ch == l.get_text():  # find text index and grab link
                link = l.get('href')
                break

        # grab html of index
        link_response = requests.get(link)
        link_data = BeautifulSoup(link_response.text, "html.parser")
        
        link = link_data.findAll(href=re.compile("https://genius.com/artists/"+name)) # grab artist
        link = link[0].get('href') 
        return link # return link to artist page


    # find the number of songs
    def find_songs(self, artist):
        artist_name = self.clean_name(artist) # for later use
        artist_link = self.find_artist(artist_name)
        response = requests.get(artist_link)
        artist_data = BeautifulSoup(response.text, 'html.parser')
        
        albums = artist_data.findAll('a', href=re.compile("https://genius.com/albums/"+artist_name))
        
        lyrics_list = []
        for a in albums: # go through each album and grab the songs
            a_l = a.get('href')
            a_r=requests.get(a_l)
            a_data = BeautifulSoup(a_r.text, 'html.parser')
            songs = a_data.findAll('a', href=re.compile("https://genius.com/"+artist_name)) # grab songs
            time.sleep(0.2) # dont break site
            for s in songs:
                s_l = s.get('href')
                s_r=requests.get(s_l)
                s_data = BeautifulSoup(s_r.text, 'html.parser')
                lyrics = s_data.find('div', class_='lyrics').get_text()
                #remove identifiers like chorus, verse, etc
                lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
                #remove empty lines
                lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
                lyrics_list.append(lyrics)
                time.sleep(0.2) # dont break site
        return lyrics_list

    def write_file(self, artist):
        f = open(artist.lower() + '.txt', 'wb')
        for song in self.find_songs(artist):
            f.write(song.encode("utf8"))
        f.close()

