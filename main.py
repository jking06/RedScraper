# Simple web scraper for reddit image posts.
# Allows user input of subreddits and time range to search for imgur posts to download. Logs the post and top comments.
# If continuously run, will update comments in posts up to a timelimit, and grab new submissions from subreddit/new.

# Manager: tracks subreddit objects, handles root folder,
#  - subReddits: handles folders and file IO. Gets/tracks images and a text log with comments.

import time
import os
import requests
import urllib
import urllib2
from bs4 import BeautifulSoup

class Manager:
    def __init__(self):
        self.subDict = {}
        
    def add_sub(self, sub):
        if sub in self.subDict.keys():
            return 'ERROR: already exists'
        else:
            # Should check if reddit.com/r/<sub> exists too
            self.subDict[sub] = Subreddit(sub)

    def run(self):
        pass
        #loop while no user interrupt
        while(#no user input)
            #pass control to each subreddit's run command in turn
            for sub in self.subList.values():
                sub.run()
        #any additional maintanence?


class Subreddit:
    def __init__(self, name):
        self.name = name
        self.url = 'http://www.reddit.com/r/'+name
    def run(self):
        pass
        #check the posts in the subreddit
        self.page = requests.get(self.url)
        self.souped = BeautifulSoup(self.page.text)
        self.posts = self.souped.findAll("a", {"class":"title"})
        #check local to disregard already-downloaded
            
        #process to find those that meet requirements
        for post in self.posts:
            link = post.get('href')
            if link[:16] == "http://imgur.com":
                pic = "http://i.imgur.com/"+link[-7:]+".jpg"
            if link[:18] == "http://i.imgur.com":
                pic = link
                    
        #either download or request download to Manager
        