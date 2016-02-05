# -*- coding: utf-8 -*-

import re
import os
from mutagen.id3 import USLT,TXXX
import logging
import configparser

'''
read ini file and add value to args

args    return object of parsearg()
'''
def read_config(args):
    INI_FILE = 'get_lyric.cnf'
    if not os.path.exists(INI_FILE):
        return
    config = configparser.ConfigParser()
    with open(INI_FILE,'r') as f:
        config.read_file(f)
    f.close()
    d = vars(args)
    for (k,v) in config.items('settings'):
        d[k]=v

'''
arguments:
tag    object createed by 'ID3(file)'
'''
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

