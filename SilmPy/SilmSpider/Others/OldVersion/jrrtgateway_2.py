# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:39:40 2018

@author: Jinglin Tao
"""

#import sys, io
# running code: scrapy crawl tolkiengateway
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
#from treelib import Node, Tree
# the way to import classes or modules on different level
from ..items import SilmspiderItem 

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

class Gateway(Spider):
    
    # Basic info, website name and the start_url)
    name = 'Eä'   
    allowed_urls = ['http://www.tolkiengateway.net']
    start_urls = ['http://www.tolkiengateway.net/wiki/Category:' + name]
    
    # Slow down the speed of crawl (sec)
    download_delay = 10
    
    # Create a array (Tree) to sore the category
    #category_tree = Tree()
    #category_tree.create_node(name, name.lower())
    def __init__(self):
        self.category_category = [] #input label(category) with label(category), just input name, not url
        self.category_article = {} #input label(category) with article name, 
        self.head = 'Eä'
        #write into the file
        self.f = open('categoryies_url.csv', 'a', encoding = 'utf-8')
        self.f.write('http://www.tolkiengateway.net/wiki/Category:Eä\n')
    
    def parse(self, response):
        selector = Selector(response)
        
        # set a items = [] to store name(title) and url
        silm = SilmspiderItem()
        silm['huiji_name'] = selector.xpath(
                '//a[@class="CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory"]/text()'
                ).extract()
        silm['huiji_url'] = str(response.url.encode('utf-8'))     
        print(silm['huiji_url'])
        yield silm
        
        # next urls
        for category in silm['huiji_name']:
            url = 'http://www.tolkiengateway.net/wiki/Category:' + category
            #print (url)
            #f = open('categoryies_url.csv', 'a')
            self.f.write(url + '\n')
            yield Request(url, callback = self.parse)

