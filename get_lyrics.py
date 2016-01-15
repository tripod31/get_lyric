#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
#### usage
>python grt_lyrics.py --in_dir "mp3_files_dir" [--out_dir "output_dir"] [--write2tag]

output_dir:  
The script puts lyric to file in "output_dir".  
The format of filename is "artist - song.txt".  
These file is useful for foo_uie_lyrics3(foobar2000 plugin to display lyric).They can be used by "local File Search" source.  
write2tag:  
The script puts lyric to lyrics tag of mp3.
If lyric contains text like
[00:00.00]lyric text
,lyric is saved to synced lyrics tag.Otherwise it is saved to unsynced lyrics tag.
'''

import argparse
import logging
import io,os,re

from mutagen.id3 import ID3, SYLT,USLT

from get_lyric.common import is_all_ascii,find_all_files
from get_lyric.www_lyrics_az import www_lyrics_az
from get_lyric.j_lyric_net import j_lyric_net
from _ctypes import Array

args = None

def get_lyric(artist,song,buf):
    if is_all_ascii(artist) and is_all_ascii(song):
        scrapers = [www_lyrics_az(artist,song)]
    else:
        scrapers = [j_lyric_net(artist,song)]
        
    for scraper in scrapers:
        try:
            ret=scraper.get_lyric()
        except Exception as e:
            logging.error(scraper.log_msg("error:[%s]" % e))
            return False
        if ret == True:
            buf.write(scraper.lyric)
            return True
    return False

def parse_synced_lyric(s):
    lines=s.split('\n')
    arr = []
    for line in lines:
        m= re.match('\[(\d2)\:(\d2)\.(\d2)\]([^\[\]]+)',line)
        if m:
            time = int(m.group(1))*60*1000 + int(m.group(1))*1000 + int(m.group(3))+100 #mill second
            arr.append((m.group(4),time))
    return arr

def write2tag(tag,lyric):
    arr = parse_synced_lyric(lyric)
    if len(arr)>0:
        #synced lyric
        if len(tag.getall('SYLT'))>0:
            tag.delall('SYLT')
        tag.add(
            SYLT(encoding=3,lang=u'eng',
                format=2,    #time foｒmat=mill seconds
                type=1,      #type=lyric
                text=arr    #[(text of lyric,start_time)]
            )
        )
    else:
        #unsynced lyric
        if len(tag.getall('USLT'))>0:
            tag.delall('USLT')        
        tag.add(USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyric))
    tag.save()

def process_mp3(file):
    print(file+":",end="")
    try:
        tag=ID3(file)
        artist = str(tag['TPE1'])
        song =  str(tag['TIT2'])
    except Exception as e:
        msg = "error reading mp3.:"+e
        print(msg)
        logging.error(msg)
        return
    
    buf = io.StringIO() 
    ret = get_lyric(artist, song, buf)
    if ret == False:
        print("not found")
        return
    else:
        print("found")
    lyric = buf.getvalue()
    
    if args.write2tag:
        write2tag(tag,lyric)
        
    if args.out_dir is not None:
        write2file(artist, song, lyric)

def write2file(artist,song,lyric):
    filename = "%s - %s.txt" % (artist,song)
    path = os.path.join(args.out_dir,filename)
    try:
        with open(path,"w") as f:
            f.write(lyric)
    except Exception as e:
        msg = "write error:%s:%s" % (path,e)
        print (msg)
        logging.error(msg)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir')
    parser.add_argument('--out_dir')
    parser.add_argument('--write2tag'   ,action='store_true')
    
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,
                        stream = open("get_lyrics.log",mode="w",encoding="utf-8"))

    if args.out_dir is not None:
        if not os.path.exists(args.out_dir):
            os.makedirs(args.out_dir)
    
    files = find_all_files(args.in_dir)
    for file in files:
        if file.endswith(".mp3"):
            process_mp3(file)
    print("finished")
    