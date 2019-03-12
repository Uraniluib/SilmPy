# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 01:16:58 2018

@author: xingg
"""

# extract keyword from article context
from rake_nltk import Rake
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

r = Rake()

f = open('..\\CleanData\\article(Eä)\\1001_War_of_Wrath(clean).csv', 'r', encoding = 'utf-8')
f = f.readlines()
f = ''.join(f)
#print(f)
#print("r.extract_keywords_from_text(f)")
r.extract_keywords_from_text(f)
#print("r.get_ranked_phrases()")
#print(r.get_ranked_phrases())

print(r.get_ranked_phrases_with_scores())
print(r.get_word_frequency_distribution())
'''
print(r.get_ranked_phrases_with_scores())
print("r.get_word_degrees()")
print(r.get_word_degrees())
print("r.get_word_frequency_distribution(f)")
print(r.get_word_frequency_distribution())'''