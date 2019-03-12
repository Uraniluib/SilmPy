# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 22:22:59 2018

@author: xingg
"""

# how to run the file
# python seperate_into_category_and_article.py 28570 Eä
# or
# python seperate_into_category_and_article.py 35016 Other_fictional_worlds
# or
# python seperate_into_category_and_article.py 15334 Real-world
import sys

# storage space
files = {} # file id and name
categories = {} # category id and name
articles = {} # article id and name

# open the raw data: argv --> 28570 Eä, 35016 Other_fictional_worlds, 15334 Real-world
data = open('..\\Data\\raw_data(' + sys.argv[2] + ').csv','r',encoding = 'utf-8')
#data = open('..\\Data\\raw_data(Real-world).csv','r')
#data = open('..\\Data\\raw_data(Other_fictional_worlds).csv','r')


for d in data.readlines():
    # root(all are category),id,name --> article
    # root,@id,@name --> category
    # root,id,File:name --> file
    d = d.split(', ') # use commat to split the data, len(d) = 3
    
    # Save id and name
    if ('File:' in d[2]) and (d[1] not in files.keys()):
        # {fileId:fileName}
        files[d[1]] = d[2].replace('File:', '')
    elif ('@' in d[1]) and (d[1].replace('@', '') not in categories.keys()):
        # {categoryId:categoryName}
        categories[d[1].replace('@', '')] = d[2].replace('@', '')
    elif all(s not in d[2] for s in ['Forum:', 'User:', 'Tolkien_Gateway:', 'Index:', 'Portal:', 'File:', '@']) and (d[1] not in articles.keys()):
        # {articleId:articleName}
        articles[d[1]] = d[2]
     
data.close()

# write file id and name
f = open('..\\Data\\file(' + sys.argv[2] + ').csv', 'w', encoding = 'utf-8')
for k,v in files.items():
    f.write(k + '\t' + v)
f.close()

# write category id and name
f = open('..\\Data\\category_withImages(' + sys.argv[2] + ').csv', 'w', encoding = 'utf-8')
f.write(sys.argv[1] + ', ' + sys.argv[2] + '\n') # add category root
for k,v in categories.items():
    f.write(k + '\t' + v)
f.close()

# write category id and name
f = open('..\\Data\\category(' + sys.argv[2] + ').csv', 'w', encoding = 'utf-8')
f.write(sys.argv[1] + ', ' + sys.argv[2] + '\n') # add category root
for k,v in categories.items():
    if 'Images_of_' not in v:
        f.write(k + '\t' + v)
f.close()

# write article id and name
f = open('..\\Data\\article(' + sys.argv[2] + ').csv', 'w', encoding = 'utf-8')
for k,v in articles.items():
    f.write(k + '\t' + v)
f.close()
