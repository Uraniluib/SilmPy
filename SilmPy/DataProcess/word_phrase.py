# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:17:51 2019

@author: xingg
"""
import matplotlib.pyplot as plt
import networkx as nx
from sys import maxsize
import re,string,igraph

str1 = """Thorin II (Third Age 2746 - 2941), also known as Thorin Oakenshield, was the King of Durin's Folk from T.A. 2850 until his death in T.A. 2941, being the son of Thráin II, grandson of Thrór and older brother to Frerin and Dís. Thorin led Durin's Folk of the Blue Mountains during their time in exile. In T.A. 2941 he led the quest for Erebor accompanied by twelve Dwarves, Bilbo Baggins, and Gandalf the Grey; he briefly became King under the Mountain until he perished following the Battle of Five Armies."""

regex = re.compile('[%s]' % re.escape(string.punctuation))

str1 = regex.sub(' ', str1.lower())

wordList1 = str1.split(None)

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
        
for node in dG.nodes():
    print ('%s:%d\n' % (node, dG.nodes[node]['count']))

for edge in dG.edges():
    print ('%s:%d\n' % (edge, maxsize - dG.edges[edge[0],edge[1]]['weight']))
    
shortest_path = nx.shortest_path(dG, source='also'.lower(), target='thorin', weight='weight')

print (shortest_path)

shortest_paths = nx.shortest_path(dG, source='also'.lower(), weight='weight')
print (shortest_paths)

nx.draw_circular(dG, with_labels=True)
plt.show()