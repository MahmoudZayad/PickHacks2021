import requests  # for making HTTP requests
from bs4 import BeautifulSoup  # for parsing HTML and XML files
import urllib.request  # for working with URLs
import re  # for regular expressions
import time  # for time operations


class ScrapeArtist:
    def __init__(self):
        self.url = 'https://genius.com/artists/'
        self.response = requests.get(self.url)  # request site response

        self.data = BeautifulSoup(self.response.text, "html.parser")  # parse data
        print(self.data.prettify())
        # get array of alphabetic index
        self.artist_index = self.data.findAll(href=re.compile("https://genius.com/artists-index/[a-z]"))


    # clean up name and capitilize it
    def clean_name(self, name):
        name = name.lower()
        name = name.capitalize()
        name = name.replace(" ", "-")
        return name

    def find_artist(self, name):
        name = self.clean_name(name)
        print(name)
        print("HELLO")

        first_ch = name[0]  # intial of artist to look through index

        print(first_ch)

        link = None

        # print(self.artist_index)

        for l in self.artist_index:
            if first_ch == l.get_text():  # find text index and grab link
                print(l.get('href'))
                link = l.get('href')
                break

        # grab html of index
        link_response = requests.get(link)
        print(link_response)
        link_data = BeautifulSoup(link_response.text, "html.parser")
        
        link = link_data.findAll(href=re.compile("https://genius.com/artists/"+name)) # grab artist
        link = link[0].get('href') 
        print(link)
        return link # return link to artist page

    
    
    



sa = ScrapeArtist()
sa.find_artist("Zach Bryan")
