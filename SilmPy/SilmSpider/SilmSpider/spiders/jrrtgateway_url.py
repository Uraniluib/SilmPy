# -*- coding: utf-8 -*-
"""
Created on Tue Nov 6 07:39:40 2018

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
    #name = 'Eä'   #<cm pageid="28570" ns="14" title="Category:Eä"/>
    #name = 'Real-world' #<cm pageid="15334" ns="14" title="Category:Real-world" />
    name = 'Other_fictional_worlds' #<cm pageid="35016" ns="14" title="Category:Other fictional worlds" />
    allowed_urls = ['http://www.tolkiengateway.net']
    start_urls = ['http://tolkiengateway.net/w/api.php?action=query&list=categorymembers&cmlimit=1000&format=xml&cmtitle=Category:' + name]
    
    # Slow down the speed of crawl (sec)
    download_delay = 0.1
    
    # Create a array (Tree) to sore the category
    def __init__(self):
        # the storage space
        #self.category_category = [] # input label(category) with label(category), just input name, not url, take all categories as Nodes in the Graph not a leaf in a tree
        #self.category_article = {} # input label(category) with article name, just input name, not url, take artiles as the leaves of each category
        #self.head = 'Eä' #the beginning cagetory(usually the last character of url)
        #self.category_category['Eä'] = [] # create a empty dict for 'Eä'
        #write into the file
        self.f = open('raw_data(Other_fictional_worlds).csv', 'a', encoding = 'utf-8')
        '''self.cu = open('category_url.csv', 'a', encoding = 'utf-8') # this file is for the category url
        self.cn = open('category_name.csv', 'a', encoding = 'utf-8') # this file is for the category name
        self.cc = open('category_category.csv', 'a', encoding = 'utf-8') # this file is for the category - to - category
        self.an = open('article_name.csv', 'a', encoding = 'utf-8') # this file is for the article name
        self.ca = open('category_article.csv', 'a', encoding = 'utf-8') # this file is for the category to article'''
        #self.f.write('http://www.tolkiengateway.net/wiki/Category:Eä\n')
    
    def parse(self, response):
        
        # create a selector to get the response
        selector = Selector(response)        
        # create a SilmspiderItem to store categories(label), articles(title) and url
        silm = SilmspiderItem()
        
        # for url, this is the root of these categories and articles
        silm['huiji_url'] = response.url
        #print(silm['huiji_url']) # check the root url
        
        # root(category) name
        root = silm['huiji_url'].replace('http://tolkiengateway.net/w/api.php?action=query&list=categorymembers&cmlimit=1000&format=xml&cmtitle=Category:', '')
        
        # pageID and pageContent
        pageId = selector.xpath('//@pageid').extract()
        pageName = selector.xpath('//@title').extract()
        
        # Category - to - Category
        # for categories, we need to go deeper into them
        silm['huiji_categories'] = dict((pi, pc.replace('Category:', '').replace(' ', '_')) for (pi, pc) in zip(pageId, pageName) if 'Category:' in pc)
        # have result(s)/article(s)
        for k, v in silm['huiji_categories'].items():
            # category,@number,@categoryName
            self.f.write(root + ', @' + k + ',  @' + v + '\n') # add category - category, add "@" in front of the categories
            #self.an.write(k + ',' + v + '\n') # add article id and name
        
        # for articles, we stop when we get there
        silm['huiji_articles'] = dict((pi, pc.replace(' ', '_')) for (pi, pc) in zip(pageId, pageName) if 'Category:' not in pc)
        # have result(s)/article(s)
        for k, v in silm['huiji_articles'].items():
            # category,number,articleName
            self.f.write(root + ', ' + k + ', ' + v + '\n') # add category - article
            #self.an.write(k + ',' + v + '\n') # add article id and name
                
        # go loops
        yield silm
        # next urls(categories)
        for k, v in silm['huiji_categories'].items():
            
            # this is the next start_urls
            url = 'http://tolkiengateway.net/w/api.php?action=query&list=categorymembers&cmlimit=1000&format=xml&cmtitle=Category:' + v
            #self.cu.write(url + '\n')
            #print(url)
            
            # add category-category to category_category list
            #self.cc.write(root + ',' + v + '\n')
            
            # add category id and name to file
            #self.cn.write(k + ',' + v + '\n')
            
            # go next url
            yield Request(url, callback = self.parse)

