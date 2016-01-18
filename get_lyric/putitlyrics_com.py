# -*- coding: utf-8 -*-
from get_lyric.common import scraper_base
import io
import logging
from robobrowser import RoboBrowser

'''
get lyric from site
'''
class putitlyrics_com(scraper_base):
    def __init__(self,artist,song):
        site = 'http://petitlyrics.com/search_lyrics'
        super().__init__(site,artist,song)
    
    '''
    return value:

    True:success
    Faluse:error
    '''
    def get_lyric(self):    
        browser = RoboBrowser(parser="html.parser",history=True)
        browser.open(self.site)
        
        #search artist
        form = browser.get_form(action='/search_lyrics')
        form['title'].value = self.song
        form['artist'].value = self.artist
        browser.submit_form(form)
        
        #find song link
        nodes = browser.find_all(name='a')
        node = None
        for n in nodes:
            if self.test_link(n,self.song):
                node = n
                break;
        if node is None:
            logging.warn(self.log_msg("song not found."))
            return False
        browser.follow_link(node)
        
        #find lyric
        node = browser.find('canvas',id="lyrics")
        if node is None:
            logging.warn(self.log_msg("lyric not found."))
            return False
        
        buf = io.StringIO()
        self.get_text(node,buf,remove_cr=False)
        lyric = buf.getvalue()
        
        self.lyric=lyric
        
        return True
