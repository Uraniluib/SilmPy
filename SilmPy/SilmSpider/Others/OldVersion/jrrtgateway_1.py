# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 12:24:55 2018

@author: xingg
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:39:40 2018

@author: Jinglin Tao
"""

# running code: scrapy crawl tolkiengateway
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from treelib import Node, Tree
# the way to import classes or modules on different level
from ..items import SilmspiderItem 

class Gateway(Spider):
    
    # Basic info, website name and the start_url)
    name = 'Eä'   
    allowed_urls = ['http://www.tolkiengateway.net']
    start_urls = ['http://www.tolkiengateway.net/wiki/Category:' + name]
    
    # Slow down the speed of crawl (sec)
    download_delay = 3
    
    
    # Create a graph (Tree) to sore the category
    category_tree = Tree()
    category_tree.create_node(name, name.lower())
    
    def parse(self, response):
        selector = Selector(response)
        
        # set a items = [] to store name(title) and url
        name_list = selector.xpath(
                    '//a[@class="CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory"]/text()'
                    ).extract()
        
        
        #yield silm
        
        # next urls
        for category in silm['huiji_name']:
            url = 'http://www.tolkiengateway.net/wiki/Category:' + category
            print (url)
            silm = SilmspiderItem()
            silm['huiji_name'] = 
            #huiji_url = str(response.url)
            
            #silm['huiji_name'] = [category.encode('utf-8') for category in huiji_name]
            silm['huiji_url'] = huiji_url.encode('utf-8')
            #yield Request(url, callback = self.parse)

