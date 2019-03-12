# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 15:24:18 2019

@author: xingg
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.rst import RstDocument
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
import plotly.graph_objs as go
import json
import urllib.request
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

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
        self.cols = 2
        self.col_force_default = True
        self.col_default_width = 550
        self.row_force_default=True
        self.row_default_height= 550
        
        data = []
        urlData = "https://raw.githubusercontent.com/plotly/datasets/master/miserables.json"
        webURL = urllib.request.urlopen(urlData)
        readData = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        data = json.loads(readData.decode(encoding))
        N=len(data['nodes'])
        L=len(data['links'])
        Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]
        
        G=igraph.Graph(Edges, directed=False)
        labels=[]
        group=[]
        for node in data['nodes']:
            labels.append(node['name'])
            group.append(node['group'])

        layt=G.layout('kk', dim=3) 
        Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
        Yn=[layt[k][1] for k in range(N)]# y-coordinates
        Zn=[layt[k][2] for k in range(N)]# z-coordinates
        Xe=[]
        Ye=[]
        Ze=[]
        for e in Edges:
            Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
            Ye+=[layt[e[0]][1],layt[e[1]][1], None]  
            Ze+=[layt[e[0]][2],layt[e[1]][2], None]  
        trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

        trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=6,
                             color=group,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

        axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

        layout = go.Layout(
            title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
            width=1000,
            height=1000,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
                ),
            margin=dict(
                t=100
            ),
            hovermode='closest',
        annotations=[
            dict(
            showarrow=False,
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],)
        data=[trace1, trace2]
        fig=go.Figure(data=data, layout=layout)
        htmlFile = plot(fig,filename='my-graph.html',output_type='div')
        self.picture = RstDocument(text=htmlFile)
        self.add_widget(self.picture)
        
        self.frequency_text = ''
        self.frequency = TextInput(text = self.frequency_text)
        
        self.add_widget(self.frequency)
        
class SearchLayout(GridLayout):
    
    '''
    Here's a custom layout. Contain a show layout and text layout
    '''
    
    def __init__(self, sg = None, **kwargs):
        super(SearchLayout, self).__init__(**kwargs)
        self.cols = 2
        self.sg_t = sg
        
        self.search_keyword = TextInput(multiline = False, size_hint_y=None, height = 40) 
        self.search_keyword.bind(text = self.name_get_text)
        
        self.search_button = Button(text='Search Entity', size_hint_y=None, height = 40, size_hint_x=None, width=250)
        self.search_button.bind(on_press = self.search)
        
        
        
        #print("Hello")
        #runTouchApp(self.search_button)
        
        #self.search_button = Button(text = 'Search Entity') 
        #self.search_button.bind(on_press = self.search)
        self.add_widget(self.search_keyword) #row=9
        self.add_widget(self.search_button) #row=10 
        
    def name_get_text(self, instance, value):
        
        '''
        Get value from input box
        '''
        self.name_text = value
        #print(")((**")
        
    def search(self, instance):
        
        '''
        search articles (as well as attributes) in the graph
        '''
        
        if self.name_text == '':
            pass
        else:
            self.dropdown = DropDown()
            file = open('..\\IdWithTitle.csv','r',encoding = 'utf-8')
            lines = file.readlines()
            file.close()
            show_text = ''
            self.idWithTitle = {}
            for line in lines:
                temp = line.split('\t')
                if self.name_text.lower() in temp[1].lower():
                    #print("!!!!")
                    self.idWithTitle[temp[0]] = temp[1]
                    show_text += temp[1]
            for k,v in self.idWithTitle.items():
                #print(v)
                btn = Button(text=v, size_hint_y=None, height=35)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                btn.bind(on_press = self.graphSearch)
                self.dropdown.add_widget(btn)
            
            self.search_button.bind(on_release=self.dropdown.open)
            self.dropdown.bind(on_select=lambda instance, x: setattr(self.search_button, 'text', x))
            
            #self.sg_t.frequency.text = show_text
    def graphSearch(self, instance):
        #print(instance)
        #print(value)
        #self.sg_t.frequency.text = instance.text
        file = open('..\\idWithAliasWithUniverse.csv','r',encoding = 'utf-8')
        lines = file.readlines()
        file.close()
        file1 = open('..\\Full_Info_Data.csv','r',encoding = 'utf-8')
        person = file1.readlines()
        file1.close()
        
        #print(instance.text)
        self.universe = ''
        self.pid = ''
        self.alias = ''
        self.universeWithCharacters = {}
        
        for line in person:
            temp = line.split('\t')
            if temp[1] in instance.text:
                self.pid = temp[0]
            
        for line in lines:
            temp = line.split('\t')
            if self.pid == temp[0]:
                self.universe = temp[2].replace('\n','')
                self.alias = temp[1]
                
        for line in lines:
            temp = line.split('\t')
            if temp[2].replace('\n','') in self.universe.replace('\n','') and temp[0] != self.pid:
                self.universeWithCharacters[temp[0]] = [temp[1]]
                
        for line in person:
            temp = line.split('\t')
            if temp[1].replace('\n','') in instance.text.replace('\n',''):
                self.sg_t.frequency.text = "<id>\t" + temp[0] + "\n<title>\t" + temp[1] + "<RealName>\t" + temp[2] + "\n<CurrentAlias>\t" + temp[3] + "\n<Affiliation>\t" + temp[4] + "\n<Relatives>\t" + temp[5] + "\n<Universe>\t" + temp[6] + "\n<Gender>\t" + temp[7] + "\n<Height>\t" + temp[8] + "\n<Weight>\t" + temp[9] + "\n<Eyes>\t" + temp[10] + "\n<Hair>\t" + temp[11] + "\n<Citizenship>\t" + temp[12] + "\n<Quotation>\t" + temp[13] + "\n"
            
        for line in person:
            temp = line.split('\t')
            if temp[0] in self.universeWithCharacters.keys():
                tempName = self.universeWithCharacters[temp[0]]
                self.universeWithCharacters[temp[0]] = [tempName,temp[5]]
        #print(self.universe)       
        #print(self.pid)
        #print(self.alias)
        #print("I'm here")
        count1 = 0
        #count2 = 0
        sgraph = igraph.Graph()
        sgraph.add_vertex(name = self.alias.replace('\n',''), label = self.alias.replace('\n',''), size = 150, color = 'red')
        sgraph.add_vertex(name = self.universe.replace('\n',''), label = self.universe.replace('\n',''), size = 200, color = 'orange')
        sgraph.add_edge(self.universe.replace('\n',''),self.alias.replace('\n',''))
        for k,v in self.universeWithCharacters.items():
            #print(v[0])
            count1 += 1
            if self.alias.replace('\n','') in v[1].replace('\n',''):
                sgraph.add_vertex(name = v[0][0].replace('\n',''), label = v[0][0].replace('\n',''), size = 100, color = 'blue')
                sgraph.add_edge(v[0][0].replace('\n',''),self.alias.replace('\n',''))
                sgraph.add_edge(self.universe.replace('\n',''),v[0][0].replace('\n',''))
            elif count1 < 25:
                sgraph.add_vertex(name = v[0][0].replace('\n',''), label = v[0][0].replace('\n',''), size = 50, color = 'grey')
                sgraph.add_edge(self.universe.replace('\n',''),v[0][0].replace('\n',''))
        layout = sgraph.layout("kk")
        igraph.plot(sgraph, layout = layout, bbox = (1300, 1000), margin = 100, edge_width = 10, vertex_label_size = 50).save(self.alias.replace('\n','') + self.universe + "_search.png")
        self.sg_t.picture.source = self.alias.replace('\n','') + self.universe + "_search.png"
        
        

class CustomLayout(GridLayout):
    
    '''
    Here's a custom layout. Contain a show layout and text layout
    '''
    
    def __init__(self, **kwargs):
        super(CustomLayout, self).__init__(**kwargs)
        self.rows = 2
        self.row_force_default=True
        self.row_default_height=550
        #self.frequency_text = ''
        self.show_grid = ShowLayout()
        self.add_widget(self.show_grid)
        
        self.search_grid = SearchLayout(self.show_grid)
        self.add_widget(self.search_grid)
            
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