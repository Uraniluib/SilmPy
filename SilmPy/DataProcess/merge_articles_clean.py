# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 05:28:45 2019

@author: xingg
"""
import matplotlib.pyplot as plt
import networkx as nx
from sys import maxsize
import os,re,string,time
from nltk.corpus import stopwords

import unidecode

path = "..\\CleanData\\article"


'''
writenode = open('..\\Data\\PlainData\\article_merge.txt','w',encoding = 'utf-8')

for filename in os.listdir(path):
    articlename = open(path + '\\' + filename,'r',encoding = 'utf-8') #id_name.csv
    articles = articlename.readlines()
    articlename.close()
    str1 = ''
    for article in articles:
        
        if "=" not in article:
            regex = re.compile('[%s]' % re.escape(string.punctuation))
    
            article = regex.sub(' ', unidecode.unidecode(article.lower()))
            article = article.replace('\r\n','').replace('\n','')
            
            str1 += article + ' '
    writenode.write(str1)


writenode.close()
'''
start_time1 = time.time()

writenode = open('..\\Data\\PlainData\\article_merge.txt','r',encoding = 'utf-8')
str1 = ''
for line in writenode.readlines():
    str1 += line
writenode.close()


articleId = open('..\\CleanData\\article.csv','r',encoding = 'utf-8')
lines = articleId.readlines()
articles = []
for c in lines:
    c = c.replace('\n','')
    a = c.split('\t')
    articles.append(unidecode.unidecode(a[1].lower()))

start_time2 = time.time()

print (start_time2-start_time1)

wordList1 = str1.split()

dG = nx.DiGraph()

for i, word in enumerate(wordList1):
    try:
        next_word = wordList1[i + 1]
        if not dG.has_node(word):
            dG.add_node(word)
            dG.nodes[word]['count'] = 1
        else:
            dG.nodes[word]['count'] += 1
        if not dG.has_node(next_word):
            dG.add_node(next_word)
            dG.node[next_word]['count'] = 0

        if not dG.has_edge(word, next_word):
            dG.add_edge(word, next_word, weight=maxsize - 1)
        else:
            dG.edges[word,next_word]['weight'] -= 1
    except IndexError:
        if not dG.has_node(word):
            dG.add_node(word)
            dG.nodes[word]['count'] = 1
        else:
            dG.nodes[word]['count'] += 1
    except:
        raise

start_time3 = time.time()
print (start_time3-start_time2)

'''
writenode = open('..\\Data\\PlainData\\article_merge_node.txt','w',encoding = 'utf-8')
for node in dG.nodes():
    writenode.write('%s:%d\n' % (node, dG.nodes[node]['count']))
writenode.close()

writenode = open('..\\Data\\PlainData\\article_merge_edge.txt','w',encoding = 'utf-8')
for edge in dG.edges():
    writenode.write('%s:%d\n' % (edge, maxsize - dG.edges[edge[0],edge[1]]['weight']))
writenode.close()
'''

sentence = 'fingolfin told feanor that you shalt lead and I will follow'
regex = re.compile('[%s]' % re.escape(string.punctuation))
sentence = regex.sub(' ', sentence.lower())
words = set(sentence.split()).intersection(set(wordList1)) 

stoplist = stopwords.words("english")
wset = list(words - set(words.intersection(set(stoplist))))


#shortest_path = nx.all_shortest_paths(dG, source='feanor'.lower(), target='fingolfin'.lower(), weight='weight')
#shortest_path = nx.multi_source_dijkstra_path(dG, source=set(words), cutoff=len(words), weight='weight')
#shortest_path = nx.all_simple_paths(dG, source='feanor'.lower(), target='fingolfin'.lower(),cutoff=10)

def get_source(wset,articles):
    for w in wset:
        if w in articles:
            print(w)
            return w
    return wset[0]

sou = get_source(wset,articles)
wset.remove(sou)
tar = get_source(wset,articles)
wset.remove(tar)

pathList= nx.all_simple_paths(dG,source=sou, target=tar,cutoff=5) #Target not specified 
start_time4 = time.time()

print (len(list(pathList)))

print (start_time4-start_time3)
def isSubList(p,wset):
    return all(True if w in p else False for w in wset)
    '''
    if len(set(p).intersection(set(wset))) > 0.5*len(wset):
        return True
    return False
    '''

paths= [w for w in pathList if isSubList(w,wset)]
start_time5 = time.time()
print (start_time5-start_time4)

#print(paths)
for s in paths:
    print (s)

#shortest_paths = nx.shortest_path(dG, source='also'.lower(), weight='weight')
#print (shortest_paths)
'''
nx.draw_kamada_kawai(dG, with_labels=True)
plt.show()
plt.draw()
    
fig1 = plt.gcf()
fig1.savefig('word_prase.png', dpi=400)
'''