#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
from get_lyric.www_lyrics_az import www_lyrics_az
import sys

if __name__ == '__main__':
    #print( sys.path)
    
    #引数
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist')
    parser.add_argument('--song')
    
    args=parser.parse_args()
    logging.basicConfig(filename='get_lyric.log',level=logging.INFO,filemode = "w")
    logging.info("argument:artist[%s]song[%s]" % (args.artist,args.song))
    obj = www_lyrics_az(args.artist,args.song) 
    
    lyric=""
    try:
        lyric=obj.get_lyric()
    except Exception as e:
        logging.error("artist:[%s]song:[%s]error:[%s]" % (obj.artist,obj.song,e))
    if len(lyric)>0:
        print(lyric,end="")
