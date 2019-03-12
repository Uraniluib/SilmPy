# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:39:40 2018

@author: Jinglin Tao
"""

# how to run the file
# scrapy crawl jrrtgateway_innerlink.py 
# Eä
# Other_fictional_worlds
# Real-world

#import sys, io
# running code: scrapy crawl tolkiengateway
from scrapy.spider import Spider
from scrapy.selector import Selector
#from scrapy.http import Request
#from treelib import Node, Tree
# the way to import classes or modules on different level
#from ..items import SilmspiderItem 

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class Gateway(Spider):
    
    # Basic info, website name and the start_url)
    name = 'innerlink' 
    allowed_urls = ['http://www.tolkiengateway.net']
  
    # Slow down the speed of crawl (sec)
    download_delay = 0.1
    
    article = open('..\\..\\..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
    #article = open('..\\..\\..\\Data\\article(Other_fictional_worlds).csv','r',encoding = 'utf-8')
    #article = open('..\\..\\..\\Data\\article(Real-world).csv','r',encoding = 'utf-8')
    pageIds = []
    pagedict = {}
    for a in article.readlines():
        temp = a.split('\t')
        pagedict[temp[0]] = temp[1].replace("\n","")
        pageIds.append(temp[0])
    article.close()
    start_urls = ['http://tolkiengateway.net/w/api.php?action=query&generator=links&format=xml&gpllimit=max&pageids=' + pageId for pageId in pageIds]
    #start_urls = ['http://tolkiengateway.net/w/api.php?action=query&generator=links&format=xml&gpllimit=max&pageids=952']
    
    def parse(self, response):
        
        selector = Selector(response)
        #selector.attrib
        content = selector.xpath('//pages/page')
        
        store = self.pageIds.pop(0)
        #f = open('..\\..\\..\\Data\\link(Real-world)\\' + store + '_' + self.pagedict[store].replace(' ','_').replace('/','_').replace(':','-').replace("\"","'") + '.csv', 'w', encoding = 'utf-8')
        #f = open('..\\..\\..\\Data\\link(Other_fictional_worlds)\\' + store + '_' + self.pagedict[store].replace(' ','_').replace('/','_').replace(':','-').replace("\"","'") + '.csv', 'w', encoding = 'utf-8')
        f = open('..\\..\\..\\Data\\link(Eä)\\' + store + '_' + self.pagedict[store].replace(' ','_').replace('/','_').replace(':','-').replace("\"","'") + '.csv', 'w', encoding = 'utf-8')
        
        for c in content:
            
            if 'missing' not in c.attrib:
                page = c.attrib['pageid']
                name = c.attrib['title']
                f.write(page +'\t'+name.replace(" ", "_")+'\n') 
                
        f.close()      
