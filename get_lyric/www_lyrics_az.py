# -*- coding: utf-8 -*-
from get_lyric.common import scraper_base
import re
import io
import logging
from robobrowser import RoboBrowser

'''
get lyric from "www.lyrics.az"
'''
class www_lyrics_az(scraper_base):
    def __init__(self,artist,song):
        self.site = 'https://www.lyrics.az/'
        self.artist = self.remove_unwanted_chars(artist)
        self.song = self.remove_unwanted_chars(song)
    
    def log_msg(self,msg):
        msg = "%s:site:[%s]artist:[%s]song:[%s]" % (msg,self.site,self.artist,self.song)
        return msg
    
    def get_lyric(self):
        
        browser = RoboBrowser(parser="html.parser",history=True)
        browser.open(self.site)
        
        #search artist
        form = browser.get_form(action='/')
        form['keyword'].value = self.artist
        browser.submit_form(form)
        
        #click artist
        node = browser.find(lambda tag:self.test_tag(tag,'a',self.artist))
        if node is None:
            logging.warn(self.log_msg("artist not found."))
            return ""
        browser.follow_link(node)
        
        #click "View All Songs"
        node = browser.find('a',text='View All songs')
        if node is None:
            logging.warn(self.log_msg("[View All Songs]link not found"))
            return ""
        browser.follow_link(node)
        
        #find song
        node = browser.find(lambda tag:self.test_tag(tag,'a',self.song))
        if node is None:
            logging.warn(self.log_msg("song not found."))
            return ""
        browser.follow_link(node)
        
        lyrics = browser.find_all('span',id="lyrics")
        if lyrics is None or len(lyrics)==0:
            logging.warn(self.log_msg("lyric not found."))
            return ""
        buf = io.StringIO()
        self.get_text(lyrics[0],buf)
        lyric = buf.getvalue()
        if lyric.startswith("We haven't lyrics of this song."):
            logging.warn(self.log_msg("lyric not found."))
            return ""
        lyric=lyric.replace("´", "'")   #remove character that can't be passed to dll
        return lyric
