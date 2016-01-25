# -*- coding: utf-8 -*-
from get_lyric.common import is_all_ascii
import io
import logging
from robobrowser import RoboBrowser
from bs4 import element
import re
import urllib

def choose_scrapers(args,artist,song):
    scrapers = [www_lyrics_az,j_lyric_net,petitlyrics_com,www_lyricsfreak_com,letssingit_com,genius_com]
    
    if not is_all_ascii(artist) or not is_all_ascii(song):
        scrapers = [s for s in scrapers if not s.ascii_only]
        
    if args.site is not None:
        scrapers = [s for s in scrapers if args.site in s.site]
    
    if len(scrapers)==0:
        print("no scrapers")
    
    return scrapers

'''
base class for scraping
'''
class scraper_base:
    def __init__(self,artist,song):
        self.artist = self.remove_unwanted_chars(artist)
        self.song = self.remove_unwanted_chars(song)
    
    def log_msg(self,msg):
        msg = "%s:site:[%s]artist:[%s]song:[%s]" % (msg,self.site,self.artist,self.song)
        return msg
            
    '''
    retreive texts under node of beautifulsoup
    buf    StringIO:buffer to output text
    '''
    def get_text(self,node,buf,remove_cr=True):
        if isinstance(node,element.Tag):
            if node.name == "br":
                buf.write("\n")
            for e in node.contents:
                self.get_text(e,buf,remove_cr)
        if isinstance(node,element.NavigableString):
            t = node.string
            if (remove_cr):
                t = re.sub(r'[\r\n]','',t)
            buf.write(t)
            
    def remove_unwanted_chars(self,s):
        s=re.sub('\(.*\)','',s) #(・・・)
        s=re.sub('\[.*\]','',s) #[・・・]
        s=s.strip() #remove white character at head and tail
        return s
    
    #compare str,in lowercase,and after removing space
    def compare_str(self,s1,s2,exact =False):
        s1=re.sub(' ','',s1).lower()
        s2=re.sub(' ','',s2).lower()
        if exact:
            return s1 == s2
        else:
            return s1 in s2
    
    def test_link(self,tag,p_text,exact=False):
        if tag.name != 'a':
            return False
        if not 'href' in tag.attrs:
            return False
        buf = io.StringIO()
        self.get_text(tag, buf)
        text = buf.getvalue()
        return self.compare_str(p_text,text)
    
class www_lyrics_az(scraper_base):
    ascii_only = True   #handle artist/song which name contains only ascii letters
    site = 'https://www.lyrics.az/'   
    
    def __init__(self,artist,song):
        super().__init__(artist,song)
    
    '''
    return value:

    True:success
    Faluse:error
    '''
    def get_lyric(self):    
        browser = RoboBrowser(parser="html.parser",history=True)
        browser.open(self.site)
        
        #search artist
        form = browser.get_form(action='/')
        form['keyword'].value = self.artist
        browser.submit_form(form)
        
        #click artist
        node = browser.find(lambda tag:self.test_link(tag,self.artist))
        if node is None:
            logging.info(self.log_msg("artist not found."))
            return False
        browser.follow_link(node)
        
        #click "View All Songs"
        node = browser.find('a',text='View All songs')
        if node is None:
            logging.info(self.log_msg("[View All Songs]link not found"))
            return False
        browser.follow_link(node)
        
        #find song link
        node = browser.find(lambda tag:self.test_link(tag,self.song))
        if node is None:
            logging.info(self.log_msg("song not found."))
            return False
        browser.follow_link(node)
        
        #find lyric
        node = browser.find('span',id="lyrics")
        if node is None:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        buf = io.StringIO()
        self.get_text(node,buf)
        lyric = buf.getvalue()
        if "We haven't lyrics of this song." in lyric or \
            "At the moment nobody has submitted lyrics for this song to our archive." in lyric:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        logging.info(self.log_msg("lyric *found*"))
        lyric=lyric.replace("´", "'")   #remove character that can't be passed to dll
        self.lyric=lyric
        
        return True



class petitlyrics_com(scraper_base):
    ascii_only = False
    site = 'http://petitlyrics.com/search_lyrics'    
    
    def __init__(self,artist,song):
        super().__init__(artist,song)
    
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
        node = browser.find(lambda tag:self.test_link(tag,self.song))
        if node is None:
            logging.info(self.log_msg("song not found."))
            return False
        browser.follow_link(node)
        
        #find lyric
        node = browser.find('canvas',id="lyrics")
        if node is None:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        logging.info(self.log_msg("lyric *found*"))
        buf = io.StringIO()
        self.get_text(node,buf,remove_cr=False)
        lyric = buf.getvalue()
        
        self.lyric=lyric
        
        return True

class j_lyric_net(scraper_base):
    ascii_only = False
    site = 'http://j-lyric.net/'
    
    def __init__(self,artist,song):
        super().__init__(artist,song)
    
    '''
    return value:

    True:success
    Faluse:error
    '''
    def get_lyric(self):    
        browser = RoboBrowser(parser="html.parser",history=True)
        browser.open(self.site)
        
        #search artist
        form = browser.get_form(action='http://search.j-lyric.net/index.php')
        form['kt'].value = self.song
        form['ka'].value = self.artist
        browser.submit_form(form)
        
        #find song link
        node = browser.find(lambda tag:self.test_link(tag,self.song))
        if node is None:
            logging.info(self.log_msg("song not found."))
            return False
        browser.follow_link(node)
        
        #find lyric
        node = browser.find('p',id="lyricBody")
        if node is None:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        logging.info(self.log_msg("lyric *found*"))
        buf = io.StringIO()
        self.get_text(node,buf)
        lyric = buf.getvalue()
        
        self.lyric=lyric
        
        return True

class www_lyricsfreak_com(scraper_base):
    ascii_only = True
    site = 'http://www.lyricsfreak.com/'
    
    def __init__(self,artist,song):
        super().__init__(artist,song)
    
    '''
    return value:

    True:success
    Faluse:error
    '''
    def get_lyric(self):    
        browser = RoboBrowser(parser="html.parser",history=True)
        query = {'q': self.artist}
        query = urllib.parse.urlencode(query)
        url = "http://www.lyricsfreak.com/search.php?a=search&type=band&" +query
        browser.open(url)
        
        #find artist link
        node = browser.find(lambda tag:self.test_link(tag,self.artist))
        if node is None:
            logging.info(self.log_msg("artist not found."))
            return False
        browser.follow_link(node)
        
        #find song link
        node = browser.find(lambda tag:self.test_link(tag,self.song))
        if node is None:
            logging.info(self.log_msg("song not found."))
            return False
        browser.follow_link(node)       
        
        #find lyric
        node = browser.find('div',id="content_h")
        if node is None:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        logging.info(self.log_msg("lyric *found*"))
        buf = io.StringIO()
        self.get_text(node,buf)
        lyric = buf.getvalue()
        
        self.lyric=lyric
        
        return True

class letssingit_com(scraper_base):
    ascii_only = True
    site = 'http://www.letssingit.com/'
    
    def __init__(self,artist,song):
        super().__init__(artist,song)
    
    '''
    return value:

    True:success
    Faluse:error
    '''
    def get_lyric(self):    
        browser = RoboBrowser(parser="html.parser",history=True)
        query = {'s':"%s - %s" % (self.artist,self.song)}
        query = urllib.parse.urlencode(query)
        url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&" + query
        browser.open(url)
        
        #find song link
        node = browser.find(lambda tag:self.test_link(tag,self.song,True))
        if node is None:
            logging.info(self.log_msg("song not found."))
            return False
        browser.follow_link(node)       
        
        #find lyric
        node = browser.find('div',id="lyrics")
        if node is None:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        logging.info(self.log_msg("lyric *found*"))
        buf = io.StringIO()
        self.get_text(node,buf)
        lyric = buf.getvalue()
        if "Unfortunately we don't have the lyrics for the song" in lyric:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        self.lyric=lyric
        
        return True

class genius_com(scraper_base):
    ascii_only = True
    site = 'http://genius.com/'
    
    def __init__(self,artist,song):
        super().__init__(artist,song)
    
    '''
    return value:

    True:success
    Faluse:error
    '''
    def get_lyric(self):    
        browser = RoboBrowser(parser="html.parser",history=True)
        query = {'q':"%s %s" % (self.artist,self.song)}
        query = urllib.parse.urlencode(query)
        url = "http://genius.com/search?" + query
        browser.open(url)
        
        #find song link
        node = browser.find(lambda tag:self.test_link(tag,self.song,True))
        if node is None:
            logging.info(self.log_msg("song not found."))
            return False
        browser.follow_link(node)
        
        #find lyric
        node = browser.find('lyrics',attrs={'class':"lyrics"})
        if node is None:
            logging.info(self.log_msg("lyric not found."))
            return False
        
        logging.info(self.log_msg("lyric *found*"))
        buf = io.StringIO()
        self.get_text(node,buf)
        lyric = buf.getvalue()
        """
        if "Unfortunately we don't have the lyrics for the song" in lyric:
            logging.info(self.log_msg("lyric not found."))
            return False
        """
        self.lyric=lyric
        
        return True
