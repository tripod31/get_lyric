#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Search lyric from the site,and put it to standard output.
'''

import argparse
import logging
import sys,io

# sites classes
from get_lyric.sites import choose_scrapers

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  #for unicodeerror
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist')
    parser.add_argument('--song')
    parser.add_argument('--site',       help="specify the site to search")
        
    args=parser.parse_args()
    logging.basicConfig(level=logging.INFO,
                        stream = open("get_lyric.log",mode="w",encoding="utf-8"))
    logging.info("argument:artist[%s]song[%s]" % (args.artist,args.song))
    scrapers = choose_scrapers(args, args.artist, args.song)
    for scraper in scrapers:    
        try:
            obj = scraper(args.artist, args.song)
            ret=obj.get_lyric()
        except Exception as e:
            logging.error(obj.log_msg("error:[%s]" % e))
            continue

        if ret == True:
            print(obj.lyric,end="")
            break
