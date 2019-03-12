# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 01:16:58 2018

@author: xingg
"""

'''
This is a program used to clean the test of each page
and seperate the result into attributes, labels, text and hyperlink(node-edge-node)
'''
import re
# read in the file
#articleId = open('..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
articleId = open('..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
articleIds = {}
articleIdsT = {}
for c in lines:
    c = c.replace('\n','')
    a = c.split(', ')
    articleIds[a[1].lower()] = a[0] #name:id
    articleIdsT[a[0]] = a[1] #name:id

for c in lines:
    c = c.replace('\n','')
    
    n = c.replace(', ','_')
    articlename = open('..\\Data\\article(Eä)\\'+ n +'.csv','r',encoding = 'utf-8') #id_name.csv
    article = articlename.readlines()
    articlename.close()
    article = ''.join(article)
    temp = re.sub(r'{{.+?}}', '', article)
    temp = temp.replace('\n|', '|')
    temp = re.sub(r'{{[\s\S]*}}', '', temp)
    temp = re.sub(r'<.+?>', '', temp)
    temp = temp.replace(' | ', '|')
    temp = temp.replace(' |', '|')
    temp = temp.replace('| ', '|')
    temp = temp.replace('[[ ', '[[')
    temp = temp.replace(' ]]', ']]')
    result = re.findall(r'\[\[(.*?)\]\]',temp)
    # clean string after |
    for i in range(0,len(result)):
        result[i] = result[i].split('|')
        result[i] = result[i][0]
        result[i] = result[i].replace(' ','_')
    
    resultId = []
    for r in result:
        if r.lower() in articleIds.keys():
            resultId.append(articleIds[r.lower()] + ' ' + articleIdsT[articleIds[r.lower()]])
        #else:
            #resultId.append(r)
        
    temp = re.sub(r'\|.+?\]', '', temp)
    temp = temp.replace('[', '')
    temp = temp.replace(']', '')
    temp = temp.replace('\'', '')
    temp = temp.replace('\n\n', '\n')
    writeatricle = open('..\\CleanData\\article(Eä)\\'+ c.split(', ')[1] + '(clean).csv','w',encoding = 'utf-8') #store clean data
    writeatricle.write(temp)
    writeatricle.close()
    writenode = open('..\\CleanData\\article(Eä)\\'+ c.split(', ')[1] +'(node).csv','w',encoding = 'utf-8') #store node relationship data
    for r in resultId:
        writenode.write(r + '\n')
    writenode.close()
    writeattribute = open('..\\CleanData\\article(Eä)\\'+ c.split(', ')[1] +'(attribute).csv','w',encoding = 'utf-8')
    writeattribute.close()
    