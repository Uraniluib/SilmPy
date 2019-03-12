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
from scrapy.spiders import Spider,Request,Selector
from treelib import Node, Tree
from Silmspider.items import SilmspiderItem

class Gateway(Spider):
    
    # Basic info, website name and the start_url)
    name = 'Eä'   
    allowed_urls = ['http://www.tolkiengateway.net']
    start_urls = ['http://www.tolkiengateway.net/wiki/Category:' + name]
    
    # Slow down the speed of crawl (sec)
    download_delay = 1
    
    
    # Create a graph (Tree) to sore the category
    category_tree = Tree()
    category_tree.create_node(name, name.lower())
    
    def parse(self, response):
        selector = Selector(response)
        
        # Get items (if url contains "Category:")
        if("Category:" in response.url)：
            item = SilmspiderItem()
            huiji_url = str(response.url)
            huiji_name = str(response.url)
            yield item
        
        # Get sub-category list
        categories = response.xpath(
                '//a[@class="CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory"]/text()'
                ).extract()
        
        for c in categories:        
            # Add new category to the category tree
            global category_tree
            self.category_tree.create_node(c,c.lower(),self.name.lower())
            print(c)
            
            # This is for the page
            
            # Call for another page's crawl
            #yield Request(c, meta={'name:'+c})
        

            