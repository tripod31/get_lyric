# coding:utf-8
import unittest
from get_lyric.common import write2tag
from mutagen.id3 import ID3
import pprint
import logging
            
from get_lyric.sites import \
    www_lyrics_az,\
    j_lyric_net,\
    petitlyrics_com,\
    www_lyricsfreak_com,\
    letssingit_com,\
    genius_com,\
    www_azlyrics_com
    
class Test1(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_j_lyric_net(self):
        scraper = j_lyric_net("smap","stay",None)
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)
    
    def test_www_lyrics_az(self):
        scraper = www_lyrics_az("beatles","a day in the life",None)
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)
        
    def test_petitlyrics_com(self):
        scraper = petitlyrics_com("beatles","a day in the life",None)
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)
    
    def test_www_lyricsfreak_com(self):
        scraper = www_lyricsfreak_com("beatles","a day in the life",None)
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)   
    
    def test_letssingit_com(self):
        scraper = letssingit_com("beatles","a day in the life",None)
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)        
    
    def test_genius_com(self):
        scraper = genius_com("beatles","a day in the life",None)
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)   
    
    def test_www_azlyrics_com(self):
        scraper = www_azlyrics_com("beatles","a day in the life","azlyrics,64.147.136.88:80")
        ret = scraper.get_lyric()
        self.assertEqual(ret, True)       
    
    def _test_mp3(self):
        with open("test/syncedlyric.txt","r",encoding='utf-8') as f:
            s = f.read()
        path = "D:\\yoshi\\Music\\test\\01test.mp3"
        tag=ID3(path)
        pp = pprint.PrettyPrinter()
        pp.pprint(tag)
        print ("↓")
        write2tag(tag, s)
        tag=ID3(path)
        pp.pprint(tag)    
    

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
if __name__ == '__main__':
    logf = open("get_lyric.log",mode="w",encoding="utf-8")
    logging.basicConfig(level=logging.INFO,
                        stream = logf)
    unittest.main()
