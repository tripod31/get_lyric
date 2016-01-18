#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
For mp3 files in specified directory,Search lyric from the site,and put it to file or tag of mp3.
'''

import argparse
import logging
import io,os

from mutagen.id3 import ID3

from get_lyric.common import find_all_files,write2tag
from get_lyric.sites import choose_scrapers

args = None

def get_lyric(artist,song,buf):
    scrapers = choose_scrapers(args, artist, song)
    
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
                
    #read tag
    try:
        tag=ID3(file)
        artist = str(tag['TPE1'])
        song =  str(tag['TIT2'])
        if len(tag.getall('SYLT'))>0 or len(tag.getall('USLT'))>0 or len(tag.getall('TXXX:LIRICS'))>0:
            tag_exist = True
        else:
            tag_exist = False
    except Exception as e:
        msg = "error reading mp3.:%s:%s" % (file,e)
        print(msg)
        logging.error(msg)
        return
    
    if args.out_dir is not None:
        filename = "%s - %s.txt" % (artist,song)
        path = os.path.join(args.out_dir,filename)
        if os.path.exists(path):
            file_exist = True
        else:
            file_exist = False
    
    if args.write2tag and not tag_exist:
        write_tag = True
    else:
        write_tag = False
    
    if args.out_dir is not None and not file_exist:
        write_file = True
    else:
        write_file = False
    
    if not write_tag and not write_file:
        return
    
    print(file+":",end="")
    #get lyric
    buf = io.StringIO() 
    ret = get_lyric(artist, song, buf)
    if ret == False:
        print("not found")
        return
    else:
        print("*found*")
    lyric = buf.getvalue()
    
    if write_tag:
        write2tag(tag,lyric)
        
    if write_file:
        write2file(path, lyric)

def write2file(path,lyric):
    try:
        with open(path,"w") as f:
            f.write(lyric)
    except Exception as e:
        msg = "write error:%s:%s" % (path,e)
        print (msg)
        logging.error(msg)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir',     help="specify the directory where mp3 files are")
    parser.add_argument('--out_dir',    help="specify the directory where the script put lyric to file")
    parser.add_argument('--write2tag',  action='store_true',   help="When specified,the script puts lyric to tag of mp3")
    parser.add_argument('--overwrite',  action='store_true',   help="When specified,the script overwrites existing file or tag.")
    parser.add_argument('--site',       help="specify the site to search")
    
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
    