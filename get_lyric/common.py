# -*- coding: utf-8 -*-
from bs4 import element
import re
import io,os
from mutagen.id3 import USLT,TXXX
import logging

def write2tag(tag,lyric):
    arr = parse_synced_lyric(lyric)
    if len(arr)>0:
        #synced lyric
        """
        'SYLT' is not displayed.
        
        if len(tag.getall('SYLT'))>0:
            tag.delall('SYLT')
        tag.add(
            SYLT(encoding=3,lang=u'eng',desc=u'desc', 
                format=2,    #time foｒmat=mill seconds
                type=1,      #type=lyric
                text=arr    #[(text of lyric,start_time)]
            )
        )
        """
        if len(tag.getall('TXXX:LIRICS'))>0:
            tag.delall('TXXX:LIRICS')
        tag.add(
            TXXX(encoding=3,desc='LYRICS', 
                text=[lyric]
            )
        )        
    else:
        #unsynced lyric
        if len(tag.getall('USLT'))>0:
            tag.delall('USLT')        
        tag.add(USLT(encoding=3, lang='eng', desc='desc', text=lyric))
    try:
        tag.save()
    except Exception as e:
        msg = "error at saving mp3.:"+str(e)
        print(msg)
        logging.error(msg)
        
def is_all_ascii(s):
    re1 = re.compile(r'^[\x20-\x7E]+$')
    if re1.search(s) is None:
        return False
    else:
        return True

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def parse_synced_lyric(s):
    lines=s.split('\n')
    arr = []
    for line in lines:
        m= re.match('\[(\d{2})\:(\d{2})\.(\d{2})\]([^\[\]]+)',line)
        if m:
            min,sec,millsec = (m.group(1),m.group(2),m.group(3))
            time = int(min)*60*100 + int(sec)*100 + int(millsec) #in mill second
            arr.append((m.group(4),time))
    return arr

'''
base class for scraping
'''
class scraper_base:
    def __init__(self,site,artist,song):
        self.site = site
        self.artist = self.remove_unwanted_chars(artist)
        self.song = self.remove_unwanted_chars(song)
    
    def log_msg(self,msg):
        msg = "%s:site:[%s]artist:[%s]song:[%s]" % (msg,self.site,self.artist,self.song)
        return msg
            
    '''
    retreive texts under node of beautifulsoup
    buf    StringIO:buffer to output text
    '''
    def get_text(self,node,buf):
        if isinstance(node,element.Tag):
            if node.name == "br":
                buf.write("\n")
            for e in node.contents:
                self.get_text(e,buf)
        if isinstance(node,element.NavigableString):
            t = re.sub(r'[\r\n\xa0]','',node.string)
            buf.write(t)
            
    def remove_unwanted_chars(self,s):
        s=re.sub('\(.*\)','',s) #(・・・)
        s=re.sub('\[.*\]','',s) #[・・・]
        s=s.strip() #remove white character at head and tail
        return s
    
    def test_tag(self,tag,name,p_text):
        if tag.name !=name:
            return False
        buf = io.StringIO()
        self.get_text(tag, buf)
        text = buf.getvalue()
        if p_text.lower() in text.lower():  #compare in lower case
            return True
        return False