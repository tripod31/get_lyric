#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
For mp3 files in specified directory,Search lyric from the site,and put it to file.
output filename is "artist - song.txt".
'''

import argparse
import logging
from get_lyric.www_lyrics_az import www_lyrics_az
import io,os
import stagger

args = None

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def get_lyric(artist,song,buf):
    scrapers = [www_lyrics_az(artist,song)] 
    
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

def process_mp3(file):
    print(file+":",end="")
    tag=stagger.read_tag(file)
    artist = tag.artist
    song =  tag.title
    buf = io.StringIO()        
    ret = get_lyric(artist, song, buf)
    if ret == False:
        print("not found")
        return
    else:
        print("found")
    lyric = buf.getvalue()
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
    
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,
                        stream = open("get_lyrics.log",mode="w",encoding="utf-8"))

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    
    files = find_all_files(args.in_dir)
    for file in files:
        if file.endswith(".mp3"):
            process_mp3(file)
    print("finished")