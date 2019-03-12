# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 00:59:28 2018

@author: xingg
"""

import re,os
# read in the file
#articleId = open('..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
articleId = open('..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
articleIds = {}
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[1].lower()] = a[0] #name:id
articleId.close()

articleId = open('..\\Data\\article(Real-world).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[1].lower()] = a[0] #name:id
articleId.close()

articleId = open('..\\Data\\article(Other_fictional_worlds).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[1].lower()] = a[0] #name:id
articleId.close()

path = "..\\Data\\article(Eä)"
#path = "..\\Data\\article(Real-world)"
#path = "..\\Data\\article(Other_fictional_worlds)"


def articlesJudge(article,writenode):
    if article == "}}\n" or article.count("=") > 1:
        return 
        
    equal = article.split("=")
    
    if len(equal) <= 1:
        return 
    
    temp0 = equal[0].split()
    attributeName = temp0[-1].replace("|","")
    
    if attributeName == "name":
        return 
    
    temp1 = re.findall(re.compile(r'[[](\[.*?\])[]]', re.S), equal[1])    
        
    if attributeName == "image" and len(temp1) > 0:
        writenode.write(attributeName + '\t' + temp1[0].replace("[","").replace("]","").split("|")[0] + '\n')
        return 
        
    attributes = [articleIds[t.split("|")[0].replace("[","").replace("]","").replace(" ","_").lower()] for t in temp1 if t.split("|")[0].replace("[","").replace("]","").replace(" ","_").lower() in articleIds.keys()]
    
    for attr in attributes:
        if len(attr) > 0:
            writenode.write(attributeName + '\t' + attr + '\n')


for filename in os.listdir(path):
    
    
    articlename = open(path + '\\' + filename,'r',encoding = 'utf-8') #id_name.csv
    articles = articlename.readlines()
    articlename.close()
    
    writenode = open('..\\Data\\attribute(Eä)\\'+ filename,'w',encoding = 'utf-8') #store attribute
    #writenode = open('..\\Data\\attribute(Real-world)\\'+ filename,'w',encoding = 'utf-8') #store attribute
    #writenode = open('..\\Data\\attribute(Other_fictional_worlds)\\'+ filename,'w',encoding = 'utf-8') #store attribute
    
    for article in articles:
        articlesJudge(article,writenode)
    
    writenode.close()