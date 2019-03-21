# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 02:03:24 2019

@author: xingg
"""
#import nltk
#from nltk import load_parser
'''
import nltk
from nltk import load_parser
cp = load_parser('grammars/large_grammars/alvey.fcfg')
#query = 'What cities are located in China'
query = 'What are you talking about?'

trees = list(cp.parse(query.split()))
answer = trees[0].label()['SEM']

answer = [s for s in answer if s]
q = ' '.join(answer)
print(q)
'''
import sys
sys.path.append('../../ln2sql/ln2sql')
import ln2sql
import sqlite3
#from nltk.stem.porter import PorterStemmer

#def mapping(query):
    

#get sql
database = 'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\database_store\\article_attribute_9.sql'
language = 'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\lang_store\\english.csv'
thesaurus = None#'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\thesaurus_store\\add.dat'
stopwords = 'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\stopwords\\temp.txt'
query = 'Count how many owner(s) there are with the object name like Silmarils?'#.replace('the','')
#query = 'Who is the leader of the place named Lindon?'
#query = 'Who is Amras from location'
#st = PorterStemmer()
#query = ' '.join([st.stem(word) for word in query.split()])
#print(query)
sql = ln2sql.Ln2sql(database_path=database,language_path=language,thesaurus_path=thesaurus,stopwords_path=stopwords).get_query(query)

# search
conn = sqlite3.connect('E:\\5.Karen\\SilmPy\\SilmPy\\CleanData\\article_attribute_9.db')
c = conn.cursor()
c.execute(sql)


print (c.fetchone())
conn.close()
'''
def understand_sentence(input_sentence):
    
    pass
'''