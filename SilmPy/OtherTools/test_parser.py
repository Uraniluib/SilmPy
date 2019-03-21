# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 07:38:54 2019

@author: xingg
"""
'''
from nltk import load_parser
cp = load_parser('grammars/book_grammars/sql0.fcfg')
query = 'What cities are located in China'
trees = list(cp.parse(query.split()))
answer = trees[0].label()['SEM']
answer = [s for s in answer if s]
q = ' '.join(answer)
print(q)
'''

