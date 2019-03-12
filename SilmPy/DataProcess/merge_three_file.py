# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 02:43:39 2019

@author: xingg
"""

temp = "file"#article, category, file

articleId = open('..\\Data\\' + temp + '(Eä).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
articleIds = {}
count = {}
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[0]] = a[1] #name:id
    if a[0] not in count.keys():
        count[a[0]] = 1
    else:
        count[a[0]] += 1
articleId.close()

articleId = open('..\\Data\\' + temp + '(Real-world).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[0]] = a[1] #name:id
    if a[0] not in count.keys():
        count[a[0]] = 1
    else:
        count[a[0]] += 1
articleId.close()

articleId = open('..\\Data\\' + temp + '(Other_fictional_worlds).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articleIds[a[0]] = a[1] #name:id
    if a[0] not in count.keys():
        count[a[0]] = 1
    else:
        count[a[0]] += 1
articleId.close()

f = open('..\\Data\\' + temp + '.csv', 'w', encoding = 'utf-8')
for k,v in articleIds.items():
    f.write(k + '\t' + v+ '\t' + str(count[k]) + '\n')
f.close()