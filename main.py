# Simple web scraper for reddit image posts.
# Allows user input of subreddits, submission score minimums, comment score minimums, and time range
# Finds imgur posts to download. Logs the post and top comments.
# If continuously run, will update comments in posts up to a timelimit (default 48hrs after submission)
#   and grab new submissions from subreddit/new.

# main: gives welcome. Then handles between UI and Manager until exit
# UI: Displays current Manager state, user options, and run command
# Manager: tracks subreddit objects, handles root folder,
#  - subReddits: handles folders and file IO. Gets/tracks images and a text log with comments.

# In the context of the UI and Manager: When do I want a function, and when a object?
# In terms of development and 'unit testing': after outlining from "top-down" view, I made the 
#   subReddits object first then imported as module into a test, then did the same with the manager. 
#   Is this "top-down" outline -> "bottom-up" development/testing advised?

import time
import os
import requests
import urllib
import urllib2
from bs4 import BeautifulSoup

commentTimeLimit = '24 hrs'
headers = {'User-Agent': 'WebScrapperTest'}

def UI(subreddits = [], minPostScore = 500, minCommentScore = 200):
    """ Display manager state, user options. Return user input to main """
    # Can take args from main: most often the current Manager state
    # Will return list of options to main, typically desired Manager state (or exit)
    # If manager doesn't like something, or user interrupt, main will call UI with some arg flags
    menuChoice = "welcommenSie"
    while menuChoice != "1":
        if menuChoice == "welcommenSie":
            print "Welcome! Select an option from the below\n"
        print "1: Run the program"
        print "2: Add subreddits.",
        print " Currently tracking", subreddits
        print "3: Change post/comment minimums",
        print " Post Score: %d Comment Score: %d" % (minPostScore, minCommentScore)
        menuChoice = raw_input("> ")
        if menuChoice == "2":
            print "List desired subreddits, separated by spaces"
            desiredSubs = raw_input("> ")
            for sub in desiredSubs.split():
                subreddits.append(sub)
        elif menuChoice == "3":
            minPostScore = int(raw_input("Enter minimum post score > "))
            minCommentScore = int(raw_input("Enter minimum comment score > "))
        elif menuChoice != "1":
            print "Error, enter a number broham"
    return subreddits, minPostScore, minCommentScore

class Manager:
    def __init__(self):
        self.subDict = {}
        
    def __add_sub(self, sub, scores):
        if sub in self.subDict.keys():
            return 'ERROR: already exists'
        #elif # Check if reddit.com/r/<sub> exists
        else:
            self.subDict[sub] = Subreddit(sub, scores[0], scores[1])
    def add_dictSubs(self, subDict):
        # subDict will be { <subreddit: (minPostScore, minCommentScore)> )
        for key, value in subDict:
            self.__add_sub(key, value)
        # Must handle/return errors...
    def run(self):
        pass
        #loop while no user interrupt
        
        #while(no user input)
        #    pass control to each subreddit's run command in turn
        #    for sub in self.subList.values():
        #        sub.run()
        #any additional maintanence?
        #Screen output of downloads and whatnot
    def getState(self):
        return self.subDict

class Subreddit:
    def __init__(self, name, minPostScore, minCommentScore):
        self.name = name
        self.url = 'http://www.reddit.com/r/'+name
        self.minPostScore = minPostScore
        self.minCommentScore = minCommentScore
    def run(self):
        #check the posts in the subreddit
        self.page = requests.get(self.url, headers=headers)
        self.souped = BeautifulSoup(self.page.text)
        self.posts = self.souped.findAll("a", {"class":"title"})
        #Get only imgur links, and those meeting requirements
        for post in self.posts:
            link = post.get('href')
            if not ('http://imgur.com' in link or 'http://i.imgur.com' in link):
                self.posts.remove(post)
            score = post.parent.parent.parent.find('div', {"class":"score unvoted"}).text
            if int(score) < self.minPostScore:
                self.posts.remove(post)
        #Download images of those remaining, if don't have it yet. Currently skips albums
        for post in self.posts:
            postUrl = post.get('href')
            if postUrl[-1] == '/':
                postUrl = postUrl[-8:-1]
            elif postUrl[-4:] == '.jpg':
                postUrl = postUrl[-11:-4]
            else:
                postUrl = postUrl[-7:]
            if "/" in postUrl: # Albums have imgur codes shorter than 7 characters. Will leave "/a/" in code, so removed here
                continue
            postName = postUrl #+ post.text
            tempPath = r"C:\Users\Jack\RedditScraper\results\%s.jpg" % postName
            if not os.path.isfile(tempPath):
                urllib.urlretrieve(post.get('href'), tempPath)[0]
        #finally, goes to the comment section and grabs comments over the score minimum
        # TO IMPLEMENT
        
def main():
    print """  RedditScraper
        Searches designated subreddits for imgur links.
        Downloads and catalogs images and top comments
        """
    theManager = Manager
    setManager = UI()
    # Process setManager: probably quitting or setting theManager to some settings
    for sub in desiredList:
        theManager.add(sub)
    # Output from attempt to add subs
    # Output current manager state: What it will be downloading from
    #while # no user input:
    #    theManager.run()
    print "Keyboard interrupt"

if __name__ == '__main__':
    main()