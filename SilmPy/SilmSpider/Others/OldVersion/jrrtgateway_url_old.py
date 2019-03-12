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
    name = 'empty'   
    allowed_urls = ['http://www.tolkiengateway.net']
    start_urls = ['http://www.tolkiengateway.net/wiki/Category:' + name]
    
    # Slow down the speed of crawl (sec)
    download_delay = 10
    
    # Create a array (Tree) to sore the category
    #category_tree = Tree()
    #category_tree.create_node(name, name.lower())
    def __init__(self):
        # the storage space
        #self.category_category = [] # input label(category) with label(category), just input name, not url, take all categories as Nodes in the Graph not a leaf in a tree
        #self.category_article = {} # input label(category) with article name, just input name, not url, take artiles as the leaves of each category
        #self.head = 'Eä' #the beginning cagetory(usually the last character of url)
        #self.category_category['Eä'] = [] # create a empty dict for 'Eä'
        #write into the file
        self.cu = open('category_url.csv', 'a', encoding = 'utf-8') # this file is for the category url
        self.cn = open('category_name.csv', 'a', encoding = 'utf-8') # this file is for the category name
        self.cc = open('category_category.csv', 'a', encoding = 'utf-8') # this file is for the category - to - category
        self.an = open('article_name.csv', 'a', encoding = 'utf-8') # this file is for the article name
        self.ca = open('category_article.csv', 'a', encoding = 'utf-8') # this file is for the category to article
        #self.f.write('http://www.tolkiengateway.net/wiki/Category:Eä\n')
    
    def parse(self, response):
        
        # create a selector to get the response
        selector = Selector(response)        
        # create a SilmspiderItem to store categories(label), articles(title) and url
        silm = SilmspiderItem()
        
        # for url, this is the root of these categories and articles
        silm['huiji_url'] = str(response.url.encode('utf-8'))
        print(silm['huiji_url']) # check the root url
        
        # root(category) name
        root = silm['huiji_url'].decode("utf-8").replace("http://www.tolkiengateway.net/wiki/Category:", "")
        
        # Category - to - Category
        # for categories, we need to go deeper into them
        silm['huiji_categories'] = selector.xpath(
                '//a[@class="CategoryTreeLabel  CategoryTreeLabelNs14 CategoryTreeLabelCategory"]/text()'
                ).extract()
        
        # for articles, we stop when we get there
        silm['huiji_articles'] = selector.xpath('//tr//li//a/text()').extract()
        # have result(s)/article(s)
        for a in silm['huiji_articles']:
            self.ca.write(root + '\t' + a + '\n') # add category - article
            self.an.write(a + '\n') # add article name
        '''if len(silm['huiji_articles']) > 0: 
            if root not in self.category_article.keys():
                # new category
                self.category_article[root] = silm['huiji_articles']
            else:
                # the category is already exist
                self.category_article[root] += silm['huiji_articles']'''
                
        # go loops
        yield silm
        
        
        # next urls(categories)
        for category in silm['huiji_categories']:
            
            # this is the next start_urls
            url = 'http://www.tolkiengateway.net/wiki/Category:' + category.replace(' ', '_')
            self.cu.write(url + '\n')
            
            # add category-category to category_category list
            self.cc.write(root + '\t' + category + '\n')
            #self.category_category.append([root, category])
            #print (url)
            
            
            # go next url
            yield Request(url, callback = self.parse)

