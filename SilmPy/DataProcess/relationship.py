# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 03:08:57 2018

@author: xingg
"""

# how to run the file
# python relationship.py 28570 Eä
# or
# python relationship.py 35016 Other_fictional_worlds
# or
# python relationship.py 15334 Real-world

import sys

sys.argv.append('28570')
sys.argv.append('Eä')

c_w_c = [] # category <--> category
c_w_c_c = [] 
c_w_a = [] # category <-- article
c_w_a_c = [] 

# open the category data
category = open('..\\Data\\category(' + sys.argv[2] + ').csv','r',encoding = 'utf-8')
categories = {}
for c in category.readlines():
    c = c.split('\t')
    categories[c[1].replace('\n','')] = c[0].replace('\n','')
category.close()
'''article = open('..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
articles = {}
for a in article.readlines():
    a = a.split(', ')
    articles[a[1].replace('\n','')] = a[0]'''

# open raw data
raw = open('..\\Data\\raw_data(' + sys.argv[2] + ').csv','r',encoding = 'utf-8')

for r in raw.readlines():
    # root(all are category),id,name --> article
    # root,@id,@name --> category
    # root,id,File:name --> file
    r = r.split(', ') # use commat to split the data, len(d) = 3   
    if r[0] in categories.keys():
        rootId = categories[r[0]] # use name get root id
        
        # category <--> category
        if ('@' in r[1]) and ('Images_of_' not in r[2]):
            categoryId = r[1].replace('@', '') # get child id
            if {rootId,categoryId} not in c_w_c:
                c_w_c.append({rootId,categoryId})
                c_w_c_c.append(1)
            else:
                c_w_c_c[c_w_c.index({rootId,categoryId})] += 1
    
        # category <-- article
        if all(s not in r[2] for s in ['Forum:', 'User:', 'Tolkien_Gateway:', 'Index:', 'Portal:', 'File:', '@']):
            if {r[1],rootId} not in c_w_a:
                c_w_a.append({r[1],rootId})
                c_w_a_c.append(1)
            else:
                c_w_a_c[c_w_a.index({rootId,categoryId})] += 1
raw.close()  
    
# write category <--> category
f = open('..\\Data\\category_graph(' + sys.argv[2] + ').csv', 'w', encoding = 'utf-8')
for i in range(len(c_w_c)):
    f.write(list(c_w_c[i])[0] + '\t' + list(c_w_c[i])[1] + '\t' + str(c_w_c_c[i]) + '\n')
f.close()

# write article <--> category 
f = open('..\\Data\\article_category(' + sys.argv[2] + ').csv', 'w', encoding = 'utf-8')
for i in range(len(c_w_a)):
    f.write(list(c_w_a[i])[0] + '\t' + list(c_w_a[i])[1] + '\t' + str(c_w_a_c[i]) + '\n')
f.close()

