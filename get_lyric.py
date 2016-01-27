#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Search lyric from the site,and put it to standard output.
'''

import argparse
import logging
import sys,io

# sites classes
from get_lyric.sites import list_scrapers,choose_scrapers
from get_lyric.common import read_config

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  #for unicodeerror
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--artist')
    parser.add_argument('--song')
    parser.add_argument('--site',       help="specify the site to search,in regular expression")
    parser.add_argument('--proxy',      help="proxy url:port")
    parser.add_argument('--list',       action='store_true',  help="print scraper classes and exit")
    
    args=parser.parse_args()
    if args.list:
        for s in list_scrapers():
            print(s.site)
        sys.exit(0)
    
    
    read_config(args)
    
    logging.basicConfig(level=logging.INFO,
                        stream = open("get_lyric.log",mode="w",encoding="utf-8"))
    logging.info("argument:" + str(args))
    scrapers = choose_scrapers(args.site, args.artist, args.song)
    ret = False
    for scraper in scrapers:    
        try:
            obj = scraper(args.artist, args.song,args.proxy)
            ret=obj.get_lyric()
        except Exception as e:
            logging.error(obj.log_msg("error:[%s]" % e))
            continue

        if ret == True:
            print(obj.lyric,end="")
            break
    
    if ret==False:
        logging.info("no lyrics at all sites")
