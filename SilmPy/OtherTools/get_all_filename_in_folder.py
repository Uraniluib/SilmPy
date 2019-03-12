# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 01:16:58 2018

@author: xingg
"""

# get all the file name in the fold
import os

'''
# Walk throught sub folder
filePath = ''
for i,j,k in os.walk(filePath):
    print(i,j,k)
'''


# Only get specific folder
filePath = '..\\Data\\article(Eä)\\'
# record total
f = open(filePath + 'filename.txt','w', encoding = 'utf8')
for o in os.listdir(filePath):
    f.write(o)
    f.write('\n')
f.close()

#record name
f = open(filePath + 'name.txt','w', encoding = 'utf8')
for o in os.listdir(filePath):
    temp = o.replace('.csv','').split('_',1)
    f.write(temp[1])
    f.write('\n')
f.close() 

#record id
f = open(filePath + 'id.txt','w', encoding = 'utf8')
for o in os.listdir(filePath):
    temp = o.replace('.csv','').split('_',1)
    f.write(temp[0])
    f.write('\n')
f.close() 
