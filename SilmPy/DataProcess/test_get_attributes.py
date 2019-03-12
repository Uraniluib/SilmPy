# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:08:45 2019

@author: xingg
"""

import mwparserfromhell

text = open('..\\Data\\article(Eä)\\1005_Dagor_Bragollach.csv','r',encoding = 'utf-8')

wikicode = mwparserfromhell.parse(text)

