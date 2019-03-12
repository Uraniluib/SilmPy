# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 02:43:39 2019

@author: xingg
"""

temp = "category_graph"#article_category，category_graph

articleId = open('..\\Data\\' + temp + '(Eä).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
articleIds = []
count = []
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    if {a[0],a[1]} not in articleIds:
        articleIds.append({a[0],a[1]})
        count.append(1)
    else:
        count[articleIds.index({a[0],a[1]})] += 1
articleId.close()

articleId = open('..\\Data\\' + temp + '(Real-world).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    if {a[0],a[1]} not in articleIds:
        articleIds.append({a[0],a[1]})
        count.append(1)
    else:
        count[articleIds.index({a[0],a[1]})] += 1
articleId.close()

articleId = open('..\\Data\\' + temp + '(Other_fictional_worlds).csv','r',encoding = 'utf-8')
lines = articleId.readlines()
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    if {a[0],a[1]} not in articleIds:
        articleIds.append({a[0],a[1]})
        count.append(1)
    else:
        count[articleIds.index({a[0],a[1]})] += 1
articleId.close()

f = open('..\\Data\\' + temp + '.csv', 'w', encoding = 'utf-8')
for i in range(len(articleIds)):
    f.write(list(articleIds[i])[0] + '\t' + list(articleIds[i])[1] + '\t' + str(count[i]) + '\n')
f.close()