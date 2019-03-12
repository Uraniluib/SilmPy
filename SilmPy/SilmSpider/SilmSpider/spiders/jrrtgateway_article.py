# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:39:40 2018

@author: Jinglin Tao
"""

# how to run the file
# scrapy crawl jrrtgateway_article.py 
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
    name = 'article' 
    allowed_urls = ['http://www.tolkiengateway.net']
  
    # Slow down the speed of crawl (sec)
    download_delay = 0.1
    
    article = open('..\\..\\..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
    #article = open('..\\..\\..\\Data\\article(Other_fictional_worlds).csv','r',encoding = 'utf-8')
    #article = open('..\\..\\..\\Data\\article(Real-world).csv','r',encoding = 'utf-8')
    pageIds = []
    for a in article.readlines():
        pageIds.append(a.split('\t')[0])
    start_urls = ['http://tolkiengateway.net/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&pageids=' + pageId for pageId in pageIds]

    def parse(self, response):
        selector = Selector(response)
        content = selector.xpath('//rev/text()').extract()
        page = selector.xpath('//@pageid').extract()
        name = selector.xpath('//@title').extract()
        #f = open('..\\..\\..\\Data\\article(Real-world)\\' + page[0] + '_' + name[0].replace(' ','_').replace('/','_').replace(':','-').replace("\"","'") + '.csv', 'w', encoding = 'utf-8')
        #f = open('..\\..\\..\\Data\\article(Other_fictional_worlds)\\' + page[0] + '_' + name[0].replace(' ','_').replace('/','_').replace(':','-').replace("\"","'") + '.csv', 'w', encoding = 'utf-8')
        f = open('..\\..\\..\\Data\\article(Eä)\\' + page[0] + '_' + name[0].replace(' ','_').replace('/','_').replace(':','-').replace("\"","'") + '.csv', 'w', encoding = 'utf-8')
        f.write(content[0])
