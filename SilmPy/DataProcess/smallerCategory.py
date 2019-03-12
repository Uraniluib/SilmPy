# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 04:37:27 2019

@author: xingg
"""



category = open('../CleanData/category.csv','r', encoding = 'utf-8')
categories = {}
for c in category.readlines():
    c = c.split('\t')
    if 'Images_' not in c[1] and 'Posters_' not in c[1] and 'Screenshots_' not in c[1] and 'Maps_' not in c[1] and 'The_Lord_of_the_Rings_Online_concept_art' not in c[1]:
        categories[c[0]] = [c[1],c[2]]
category.close()

f = open('..\\CleanData\\category_s.csv', 'w', encoding = 'utf-8')
for k,v in categories.items():
    f.write(k + '\t' + v[0] + '\t' + v[1])
f.close()
