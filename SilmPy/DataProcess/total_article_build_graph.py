# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:57:16 2019

@author: xingg
"""

articleId = open('..\\CleanData\\article(Eä).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
articleIds = {}
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[1].lower()] = a[0] #name:id

for c in lines:
    c = c.replace('\n','')
    
    n = c.replace(', ','_')
    articlename = open('..\\Data\\article(Eä)\\'+ n +'(clean).csv','r',encoding = 'utf-8') #id_name.csv
    article = articlename.readlines()
    articlename.close()
    article = ''.join(article)
    
    writenode = open('..\\CleanData\\article(Eä)\\'+ c +'(attribute).csv','w',encoding = 'utf-8') #store attribute
    