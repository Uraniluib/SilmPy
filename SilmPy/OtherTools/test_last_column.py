# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 23:37:58 2019

@author: xingg
"""
import igraph
sg = igraph.Graph()
file = open('../CleanData/category_s.csv','r', encoding = 'utf-8')
categories = {}
for c in file.readlines():
    c = (c.replace('\n','')).split('\t')
    categories[c[0]] = c[1]
    sg.add_vertex(name = c[0], label=c[1], weight=int(c[2]))
file.close()




file = open('../CleanData/category_graph.csv', 'r', encoding = 'utf-8')
category_category = []
for cg in file.readlines():
    cg = cg.replace('\n','').replace('_',' ').split('\t')
    if cg[0] in categories.keys() and cg[1] in categories.keys():
        category_category.append({cg[0],cg[1]})
        # source <--> target , 
        sg.add_edge(source=cg[0],target=cg[1],weight=int(cg[2]),color='grey')
file.close()    

#print (sg.vs[2]['weight'])
for e in sg.es():
  print("source: %s target: %d" % (e.source, e.target))
  print("multiplicity %d" % (sg.count_multiple(e)))
  print("weight %f\n" % e['weight'])