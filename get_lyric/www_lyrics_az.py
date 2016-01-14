# -*- coding: utf-8 -*-
from get_lyric.scraper_base import scraper_base
import re
import io
import logging
from robobrowser import RoboBrowser

'''
get lyric from "www.lyrics.az"
'''
class www_lyrics_az(scraper_base):
    def __init__(self,artist,song):
        self.artist = self.remove_unwanted_chars(artist)
        self.song = self.remove_unwanted_chars(song)
        
    def remove_unwanted_chars(self,s):
        s=re.sub('\(.*\)','',s) #(・・・)
        s=re.sub('\[.*\]','',s) #[・・・]
        s= re.sub('[^A-Za-z0-9 \']+',' ',s) #allowed char:alphanumeric character,number,space,"'"
        s=s.strip() #remove white character at head and tail
        return s
    
    def test_tag(self,tag):
        if tag.name !='a':
            return False
        buf = io.StringIO()
        self.get_text(tag, buf)
        if re.match(r'^%s$' % self.song,buf.getvalue(),re.IGNORECASE) is None:
            return False       
        return True
    
    def get_lyric(self):
        
        browser = RoboBrowser(parser="html.parser",history=True)
        browser.open('https://www.lyrics.az/')
        
        #search artist
        form = browser.get_form(action='/')
        form['keyword'].value = self.artist
        browser.submit_form(form)
        
        #click artist
        node = browser.find('a',text=re.compile(r'^%s$' % self.artist,re.IGNORECASE))
        if node is None:
            logging.warn("artist not found.artist:[%s]song:[%s]" % (self.artist,self.song))
            return ""
        browser.follow_link(node)
        
        #click "View All Songs"
        node = browser.find('a',text=re.compile(r'View All songs'))
        if node is None:
            logging.warn("[View All Songs]link not found.artist:[%s]song:[%s]" % (self.artist,self.song))
            return ""
        browser.follow_link(node)
        
        #find song
        node = browser.find(lambda tag:self.test_tag(tag))
        if node is None:
            logging.warn("song not found.artist:[%s]song:[%s]" % (self.artist,self.song))
            return ""
        browser.follow_link(node)
        
        lyrics = browser.find_all('span',id="lyrics")
        if lyrics is None or len(lyrics)==0:
            logging.warn("lyric not found.artist:[%s]song:[%s]" % (self.artist,self.song))
            return ""
        buf = io.StringIO()
        self.get_text(lyrics[0],buf)
        lyric = buf.getvalue()
        if lyric.startswith("We haven't lyrics of this song."):
            logging.warn("lyric not found.artist:[%s]song:[%s]" % (self.artist,self.song))
            return ""
        lyric=lyric.replace("´", "'")   #remove character that can't be passed to dll
        return lyric
