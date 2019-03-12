# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 05:39:23 2019

@author: xingg
"""

from os import listdir
from os.path import isfile, join
from collections import defaultdict

'''
get all attributes with frequency
get category <--> attributes with frequency
category    attribute1    attribute2...
'''



# open the attribute
file = open('../CleanData/attribute.csv','r', encoding = 'utf-8')
allAttribute = set()
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    allAttribute.add(c[0])
file.close()

# open the category data --label
file = open('../CleanData/category_s.csv','r', encoding = 'utf-8')
categories = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    categories[c[0]] = {}
file.close()


# open article <--> category
file = open('../CleanData/article_category.csv', 'r', encoding = 'utf-8')
article_category = []
for cg in file.readlines():
    cg = cg.replace('\n','').replace('_',' ').split('\t')
    # 0 article, 1 category
    if cg[0] in categories.keys():
        article_category.append([cg[1],cg[0]])
    elif cg[1] in categories.keys():
        article_category.append([cg[0],cg[1]])
file.close()

# read all attribute files
mypath = '../CleanData/attribute'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def merge_dict(a,b):
    for k,v in a.items():
        if k in b.keys():
            b[k] += v
        else:
            b[k] = v
    return b


for f in files:
    anum = f.split('_')[0]
    file = open(join(mypath, f), 'r', encoding = 'utf-8')    
    lines = file.readlines()
    file.close()
    defdesc = {}
    for l in lines:
        tempkv = (l.replace('\n','')).split('\t') 
        '''
        # already in attr, count ++
        if tempkv[0] in allAttribute.keys():
            allAttribute[tempkv[0]] += 1
        else: # add a new attr
            allAttribute[tempkv[0]] = 1
        '''   
        if tempkv[0] in allAttribute:
            # already in defdesc, count ++
            if tempkv[0] in defdesc.keys():
                defdesc[tempkv[0]] += 1
            else:# add a new attr
                defdesc[tempkv[0]] = 1
    
    #if article has category, add these attributes to the category dict
    for ac in article_category:
        if anum == ac[0] and ac[1] in categories.keys(): #ac[0] is article
            categories[ac[1]] = merge_dict(defdesc,categories[ac[1]])#{**defdesc, **categories[ac[1]]}
        
        elif anum == ac[1] and ac[0] in categories.keys(): #ac[1] is article
            categories[ac[0]] = merge_dict(defdesc,categories[ac[0]])#{**defdesc, **categories[ac[0]]}
'''            
output = open('../CleanData/attribute.csv', 'w', encoding = 'utf-8')
sorted_by_value = sorted(allAttribute.items(), key=lambda kv: kv[1], reverse=True) 
for s in sorted_by_value:
    output.write(s[0]+'\t'+str(s[1])+'\n')
output.close()
'''

output = open('../CleanData/category_attribute.csv', 'w', encoding = 'utf-8') 
#sorted_by_key = sorted(categories.items(), key=lambda kv: kv[0]) 
for key,value in categories.items():
    sorted_by_value = sorted(value.items(), key=lambda kv: (-kv[1],kv[0])) 
    for s in sorted_by_value:
        output.write(key+'\t'+s[0]+'\t'+str(s[1])+'\n')
output.close()
