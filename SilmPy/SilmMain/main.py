# -*- coding: utf-8 -*-
"""
@author: xingg
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

import os
import webbrowser
import numpy as np
import igraph

from rake_nltk import Rake
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

class RootWidget(BoxLayout):
    '''
    This is the a Box Layout class. We will then add CustomLayout on it.
    '''
    pass

class ShowLayout(GridLayout):
    '''
    This is a Grid Layout that contains graph figure and article text.
    '''
    
    def __init__(self, **kwargs):
        
        '''
        Initial the show layout with a default picture and an empty input box.
        '''
        
        super(ShowLayout, self).__init__(**kwargs)
        self.rows = 2
        self.row_default_height = 300
        self.picture = AsyncImage(
                source="..//DataProcess//graphs.png",
                size_hint= (1, .5),
                pos_hint={'center_x':.5, 'center_y':.5})
        self.frequency_text = ''
        self.frequency = TextInput(text = self.frequency_text)
        
        self.add_widget(self.frequency)
        self.add_widget(self.picture)
        

class TextLayout(GridLayout):
    
    '''
    This is a Text Layout that contains inputbox and functional button.
    '''
    
    def __init__(self, sg = None, **kwargs):
        
        '''
        Initial the text layout with 5 functions: open explorer, calculate the word relationship gram, search category in graph, search articles in graph and exit.
        '''
        
        super(TextLayout, self).__init__(**kwargs)
        #self.cols = 3
        self.rows = 20
        self.row_default_height = 8
        
        '''articleId = open('..\\Data\\article(Eä).csv','r',encoding = 'utf-8')
        lines = articleId.readlines()
        self.articleIds = {}
        for c in lines:
            c = c.replace('\n','')
            a = c.split(', ')
            self.articleIds[a[1].lower()] = a[0] #name:id
        articleId.closed()'''
        self.gc = igraph.Graph()
    
        # open the category data
        category = open('..\\Data\\category(Eä).csv','r',encoding = 'utf-8')
        categories = {}
        for c in category.readlines():
            c = c.split(', ')
            categories[c[0]] = c[1].replace('\n','')
            self.gc.add_vertex(name = categories[c[0]], label = categories[c[0]], size = 40, color = 'blue')
            
        # open category <--> category
        category_graph = open('..\\Data\\category_graph(Eä).csv', 'r', encoding = 'utf-8')
        for cg in category_graph.readlines():
            cg = cg.split(', ')
            self.gc.add_edge(categories[cg[0]],categories[cg[1].replace('\n','')])
        
        #attributes
        self.name_text = ''
        self.openfile_text = ''
        self.sg_t = sg
        #self.show_text = sg.frequency_text
        
        # spyder
        self.add_widget(Label(halign="center",text="==================================================\nInput Your Spyder Name\n==================================================")) #row=0 empty row
        #self.add_widget(Label(text="Input Your Spyder Name:")) #row=1
        self.spyder_name = TextInput(multiline = False) 
        self.spyder_name.bind(text = self.name_get_text)
        self.spyder_button = Button(text = 'Spyder') 
        self.spyder_button.bind(on_press = self.spyder_button_search)
        self.add_widget(self.spyder_name) #row=2
        self.add_widget(self.spyder_button) #row=3
        self.add_widget(Label(halign="center",text="==================================================\nCalculate Word Frequency\n==================================================")) #row=4 empty row
        
        # load file
        #self.add_widget(Label(text="Calculate Word Frequency:")) #row=5
        self.load_name = TextInput(multiline = False) 
        self.load_name.bind(text = self.name_get_text)
        self.openfile_button = Button(text = 'Load File') 
        self.openfile_button.bind(on_press = self.load)
        self.openfile_text = ''
        self.add_widget(self.load_name) 
        self.add_widget(self.openfile_button) #row=6
        self.add_widget(Label(halign="center",text="==================================================\nSearch Categories Relationships in Graph\n==================================================")) #row=7
        
        # search the category
        #self.add_widget(Label(text="Graph Searching:")) #row=8
        self.search_category = TextInput(multiline = False) 
        self.search_category.bind(text = self.name_get_text)
        self.category_button = Button(text = 'Search Category') 
        self.category_button.bind(on_press = self.category)
        self.add_widget(self.search_category) #row=9
        self.add_widget(self.category_button) #row=10
        self.add_widget(Label(halign="center",text="==================================================\nSearch Keywords in Graph\n==================================================")) #row=7
        
        # search the graph
        #self.add_widget(Label(text="Graph Searching:")) #row=8
        self.search_keyword = TextInput(multiline = False) 
        self.search_keyword.bind(text = self.name_get_text)
        self.search_button = Button(text = 'Search Entity') 
        self.search_button.bind(on_press = self.search)
        self.add_widget(self.search_keyword) #row=9
        self.add_widget(self.search_button) #row=10
        self.add_widget(Label(halign="center",text="==================================================\nExit App\n==================================================")) #row=11
        
        # exit app
        self.exit_button = Button(text = 'Exit')
        self.exit_button.bind(on_press = self.exit_app)
        self.add_widget(self.exit_button)
        
        
    def name_get_text(self, instance, value):
        
        '''
        Get value from input box
        '''
        
        self.name_text = value
    
    def search(self, instance):
        
        '''
        search articles (as well as attributes) in the graph
        '''
        
        if self.name_text == '':
            pass
        else:
            attribute_word = ['date','weapons','age']
            sgraph = igraph.Graph()
            searchList = self.name_text.split(' ')
            sl = searchList[0]
            if len(searchList) != 1:
                sl = searchList[2]
            
            sgraph.add_vertex(name = sl, label = sl, size = 200, color = 'red')
            search_file = open('..\\CleanData\\article(Eä)\\'+sl+'(clean).csv','r',encoding = 'utf-8')
            search_file_t = search_file.readlines()
            search_file.close()
            self.sg_t.frequency.text = ''.join(search_file_t) #update text on left
            #node
            search_file = open('..\\CleanData\\article(Eä)\\'+sl+'(node).csv','r',encoding = 'utf-8')
            search_file_tt = search_file.readlines()
            search_file.close()
            for node_t in search_file_tt:
                sgraph.add_vertex(name = node_t.split(' ')[1], label = node_t.split(' ')[1], size = 40, color = 'blue')
                sgraph.add_edge(sl,node_t.split('   ')[1])
            #attribute
            if len(searchList) == 3:
                search_file = open('..\\CleanData\\article(Eä)\\'+sl+'(attribute).csv','r',encoding = 'utf-8')
                search_file_ta = search_file.readlines()
                search_file.close()
                for sfta in search_file_ta:
                    print(sfta)
                    sfta = sfta.split('=')
                    if sfta[0] in attribute_word:
                        sgraph.add_vertex(name = sfta[0]+':'+sfta[1], label = sfta[0]+':'+sfta[1], size = 100, color = 'red')
                    else:
                        sgraph.add_vertex(name = sfta[0]+':'+sfta[1], label = sfta[0]+':'+sfta[1], size = 50, color = 'yellow')
                    sgraph.add_edge(sl,sfta[0]+':'+sfta[1])
            layout = sgraph.layout("kk")
            igraph.plot(sgraph, layout = layout, bbox = (1300, 1000), margin = 100, edge_width = 10, vertex_label_size = 50).save(sl + "_search.png")
            self.sg_t.picture.source = sl + "_search.png"
            
    
    def category(self, instance):
        
        '''
        search category in the category 
        '''
        
        print('Creat graph')
        if self.name_text == '':
            self.sg_t.picture.source = 'graphs.png'
        else:
            #vertexList = []
            #vertexList.append(g.vs.find(name=temp_name) )
            vertexList = self.name_text.split(' ')
            for temp_name in self.name_text.split(' '):
                tTT = self.gc.neighbors(self.gc.vs.find(name=temp_name))
                for element in tTT:
                    vertexList.append(self.gc.vs[element]["name"])
                    
            subg = self.gc.subgraph(vertexList, implementation="auto")
            layout = subg.layout("kk")
            igraph.plot(subg, layout = layout, bbox = (1200, 1000), margin = 100, edge_width = 10, vertex_label_size = 50).save(self.name_text + "_category.png")
            self.sg_t.picture.source = self.name_text + "_category.png"
        
        
    def spyder_button_search(self, instance):
        '''
        open a url in explorer
        '''
        
        webbrowser.open('http://www.tolkiengateway.net/wiki/' + self.name_text)
        
    def load(self, instance):
        
        '''
        load an article with the keyword, update the inputbox
        '''
        
        file_text = open('..\\CleanData\\article(Eä)\\' + self.name_text.replace(', ','_') + '(clean).csv', 'r', encoding = 'utf-8')
        read_lines = file_text.readlines()
        read_lines = ''.join(read_lines)
        read_lines = read_lines.replace('=','')
        read_lines = read_lines.replace('"','')
        r = Rake()
        r.extract_keywords_from_text(read_lines)
        show_text = ''
        for temp in r.get_ranked_phrases_with_scores():
            if temp[0] > 7.0 and temp[0] < 16.0:
                show_text = show_text + str(np.around(temp[0], decimals=2)) + '\t\t' + temp[1] + '\n'
        print(show_text)
        self.sg_t.frequency.text = show_text
        
    
    def exit_app(self, instance):  
        
        '''
        exit app
        '''
        App.get_running_app().stop()
        Window.close()
    
    def on_text(self, instance, value):
        print('The widget', instance, 'have:', value)    
        
    


class CustomLayout(GridLayout):
    
    '''
    Here's a custom layout. Contain a show layout and text layout
    '''
    
    def __init__(self, **kwargs):
        super(CustomLayout, self).__init__(**kwargs)
        self.cols = 2
        
        #self.frequency_text = ''
        
        self.show_grid = ShowLayout()
        self.add_widget(self.show_grid)
        self.text_grid = TextLayout(self.show_grid)
        self.add_widget(self.text_grid)
            
class MainApp(App):
    '''
    Start the application.
    :return: root
    '''
    def build(self):
        root = RootWidget()
        c = CustomLayout()
        root.add_widget(c)
        return root
    
if __name__ == '__main__':
    MainApp().run()