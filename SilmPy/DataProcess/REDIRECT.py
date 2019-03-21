# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 04:16:24 2019

@author: xingg
"""

from os import listdir
from os.path import isfile, join
from collections import defaultdict

dictionary = defaultdict(set)

# open article data --node
file = open('../CleanData/article.csv','r', encoding = 'utf-8')
articles = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    articles[c[0]] = c[1]
file.close()

# read all files
mypath = '../CleanData/article'
path = '../CleanData/attribute'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# get those files who have alias and #REDIRECT
for f in files:
    anum = f.split('_')[0] # get 4490
    aname = articles[anum].replace('_',' ')
    
    # #REDIRECT
    file = open(join(mypath, f), 'r', encoding = 'utf-8')
    lines = file.readlines()
    file.close()
    
    if "#REDIRECT" in lines[0]:
        name = lines[0].split(" ")
        wheretogo = name[-1].replace("[[","").replace("]]","").replace('_',' ').replace('\n','').replace('#REDIRECT','')
        dictionary[aname].add(wheretogo) # add where to go to dict
        dictionary[wheretogo].add(aname) # add where to go to dict
    
    # alias
    file = open(join(path, f), 'r', encoding = 'utf-8')
    lines = file.readlines()
    file.close()
    
    for line in lines:
        if 'othernames' in line:
            othername = articles[(line.replace('\n','')).split('\t')[1]].replace('_',' ')
            dictionary[aname].add(othername) # add where to go to dict
            dictionary[othername].add(aname) # add where to go to dict
            
dlist = list(dictionary.keys())
dlist.sort()


writefile = open('../Data/add.dat', 'w', encoding = 'utf-8')
for k in dlist:
    writefile.write(k+'|1\n')
    writefile.write('(noun)|'+'|'.join(dictionary[k])+'\n')
writefile.close()
