# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 04:34:13 2019

@author: xingg
"""

# change article_category.csv to article --> category

# open the category data --label
file = open('../CleanData/category_s.csv','r', encoding = 'utf-8')
categories = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    categories[c[0]] = c[1]
file.close()

# open article data --node
file = open('../CleanData/article.csv','r', encoding = 'utf-8')
articles = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    articles[c[0]] = c[1]
file.close()


# open article <--> category
file = open('../CleanData/article_category.csv', 'r', encoding = 'utf-8')
article_category = {}
for cg in file.readlines():
    cg = cg.replace('\n','').replace('_',' ').split('\t')
    # 0 article, 1 category
    if cg[0] in categories.keys() and cg[1] in articles.keys():
        article_category.append([cg[1],cg[0]])
    elif cg[1] in categories.keys() and cg[0] in articles.keys():
        article_category.append([cg[0],cg[1]])
file.close()