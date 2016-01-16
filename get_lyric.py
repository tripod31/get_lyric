#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Search lyric from the site,and put it to standard output.
'''

import argparse
import logging
from get_lyric.common import is_all_ascii
from get_lyric.www_lyrics_az import www_lyrics_az
from get_lyric.j_lyric_net import j_lyric_net
import io,sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  #for unicodeerror
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist')
    parser.add_argument('--song')
    
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,
                        stream = open("get_lyric.log",mode="w",encoding="utf-8"))
    logging.info("argument:artist[%s]song[%s]" % (args.artist,args.song))
    if is_all_ascii(args.artist) and is_all_ascii(args.song):
        scrapers = [www_lyrics_az(args.artist,args.song)]
    else:
        scrapers = [j_lyric_net(args.artist,args.song)]
    
    for scraper in scrapers:
        try:
            ret=scraper.get_lyric()
        except Exception as e:
            logging.error(scraper.log_msg("error:[%s]" % e))
            break
        if ret == True:
            print(scraper.lyric,end="")
            break
