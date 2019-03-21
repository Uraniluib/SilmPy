# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 01:43:29 2019

@author: xingg
"""
import sys
sys.path.append('../../ln2sql/ln2sql')
import ln2sql
import sqlite3
import unidecode
from nltk.corpus import stopwords
import re

def get_keywords(input_sentence,articles):
    lines = re.sub(r'[^\w\s]','',input_sentence).split()
    lines = list(set(lines) - set(stopwords.words('english')))
    keywords = [articles[unidecode.unidecode(line.lower())] for line in lines if unidecode.unidecode(line.lower()) in articles.keys()]
    print(keywords)
    return keywords


def understand_sentence(input_sentence,articles):
    database = 'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\database_store\\article_attribute_9.sql'
    language = 'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\lang_store\\english.csv'
    thesaurus = None#'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\thesaurus_store\\add.dat'
    stopwords = 'E:\\5.Karen\\SilmPy\\ln2sql\\ln2sql\\stopwords\\temp.txt'
    sql = ln2sql.Ln2sql(database_path=database,language_path=language,thesaurus_path=thesaurus,stopwords_path=stopwords).get_query(input_sentence)
    conn = sqlite3.connect('E:\\5.Karen\\SilmPy\\SilmPy\\CleanData\\article_attribute_9.db')
    c = conn.cursor()
    c.execute(sql)
    temp = c.fetchone()
    print (temp)
    conn.close()
    return re.sub(r'[^\w\s]','',str(temp))