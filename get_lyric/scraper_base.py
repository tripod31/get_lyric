# -*- coding: utf-8 -*-
from bs4 import element
import re

'''
base class for scraping
'''
class scraper_base:

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
            t = re.sub(r'[\n\xa0]','',node.string)
            buf.write(t)
