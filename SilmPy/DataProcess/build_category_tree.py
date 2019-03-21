# -*- coding: utf-8 -*-
"""
This module provides several functions to examine dependencies in mappings
(usually dictionaries).
>>> pass # Trivial module self-test: See individual self-tests.
"""
import igraph
import random
from os import listdir
from os.path import isfile, join
random.seed(1995)

g = igraph.Graph()



# open the category data
category = open('../CleanData/category_s.csv','r', encoding = 'utf-8')
categories = {}
for c in category.readlines():
    c = c.replace('\n','').split('\t')
    categories[c[0]] = c[1].replace('\n','')
    #g.add_vertex(name = categories[c[0]], label = categories[c[0]][:5], shape ='star' , size = 10, color = 'blue')
    g.add_vertex(name = c[0], shape ='square' , size = 30, color = 'blue')
category.close()

article = open('../CleanData/article.csv','r', encoding = 'utf-8')
articles = {}
for c in article.readlines():
    c = c.replace('\n','').split('\t')
    articles[c[0]] = c[1].replace('\n','')
    #g.add_vertex(name = articles[c[0]], label = articles[c[0]][:5], size = 10, color = 'orange')
    g.add_vertex(name = c[0], size = 12, color = 'green')

# open category <--> category
category_graph = open('../CleanData/category_graph.csv', 'r', encoding = 'utf-8')
for cg in category_graph.readlines():
    cg = cg.replace('\n','').split('\t')
    if cg[0] in g.vs()['name'] and cg[1] in g.vs()['name']:
        #g.add_edge(categories[cg[0]],categories[cg[1]])
        g.add_edge(cg[0],cg[1])
category_graph.close()

article_graph = open('../CleanData/article_category_new.csv', 'r', encoding = 'utf-8')
for cg in article_graph.readlines():
    cg = cg.replace('\n','').split('\t')
    if cg[0] in g.vs()['name'] and cg[1] in g.vs()['name']:
        #g.add_edge(categories[cg[0]],articles[cg[1]])
        g.add_edge(cg[0],cg[1])
    #elif cg[1] in categories.keys() and cg[0] in articles.keys():
        #g.add_edge(articles[cg[0]],categories[cg[1]])
        #g.add_edge(cg[0],cg[1])

article_graph.close()

layout = g.layout("kk")
igraph.plot(g, layout = layout, bbox = (5000, 5000), margin = 50).save("graphs_category_ca.png")


mypath = '../CleanData/link'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for f in files:
    anum = f.split('_')[0] # get 4490
    
    file = open(join(mypath, f), 'r', encoding = 'utf-8')
    lines = file.readlines()
    file.close()
    for line in lines:
        if 'Category:' not in line:
            l = line.replace('\n','').split('\t')[0]
            if anum in g.vs()['name'] and l in g.vs()['name']:
                g.add_edge(anum,l)
        

layout = g.layout("kk")
igraph.plot(g, layout = layout, bbox = (5000, 5000), margin = 50).save("graphs_category_a.png")



#print(vertexList)

#vertexList2 = []
#for r in ["Bridges","Sites_of_civilisation"]:
    #vertexList2 = vertexList2 + g.neighbors(g.vs.find(name=r)) 
#print(vertexList)

def graphTest(grapht,vl):
    '''
    Case 1: Bridges neighbors
    >>> vertexList1 = []
    >>> tempv = [g.neighbors(g.vs.find(name=r)) for r in ["Bridges"]]
    >>> vertexList1 = vertexList1 + tempv
    >>> graphTest(g,vertexList1)
    [[315]]

    Case 2: Bridges and Sites_of_civilisation neighbors
    >>> vertexList2 = []
    >>> tempv = [g.neighbors(g.vs.find(name=r)) for r in ["Bridges","Sites_of_civilisation"]]
    >>> vertexList2 = vertexList2 + tempv
    >>> graphTest(g,vertexList2)
    [[315], [63, 73, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332]]
    '''
    return vl




if __name__ == '__main__':
    import doctest
    doctest.testmod()
