# -*- coding: utf-8 -*-
"""
Created on Mon Feb  18 01:17:22 2019

@author: xingg
"""

# for dash
import dash
from dash.dependencies import Input, Output, State
import spacy
#import plotly
import dash_html_components as html
import dash_core_components as dcc
#import pandas as pd
import os
from bs4 import BeautifulSoup
from nlp import understand_sentence 
import igraph
import urllib.request
#from plotly.offline import plot
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import unidecode
from collections import defaultdict, Counter

app = dash.Dash('Silm-Graph-Search')
server = app.server

# build a graph for category and article
sg = igraph.Graph()
SILM_CACHE = []
if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

# open the attribute frequency
file = open('../CleanData/attribute.csv','r', encoding = 'utf-8')
allAttribute = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    allAttribute[c[0]] = int(c[1])
file.close()

# category <--> attributes with frequency
file = open('../CleanData/category_attribute.csv', 'r', encoding = 'utf-8') 
category_attribute = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    if c[0] not in category_attribute.keys():
        category_attribute[c[0]] = {}
    category_attribute[c[0]][c[1]] = int(c[2])
file.close()
    
# open the category data --label
file = open('../CleanData/category_s.csv','r', encoding = 'utf-8')
categories = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    categories[c[0]] = c[1]
    # name is '12846', label is 'Arda', size is weight, color green is category
    sg.add_vertex(name = c[0], label = c[1], size = int(c[2])*5+10, color = '#51d0d1', group = 6, symbol = 'square') 
file.close()

# open article data --node
file = open('../CleanData/article.csv','r', encoding = 'utf-8')
articles = {}
for c in file.readlines():
    c = (c.replace('\n','').replace('_',' ')).split('\t')
    articles[c[0]] = c[1]
    # name is '4490', label is 'Silmaril', size is weight, color red is article
    sg.add_vertex(name = c[0], label = c[1], size = int(c[2])*5+5, color = '#c379af', group = 6, symbol = 'circle') 
file.close()

# open category <--> category
file = open('../CleanData/category_graph.csv', 'r', encoding = 'utf-8')
category_category = []
for cg in file.readlines():
    cg = cg.replace('\n','').replace('_',' ').split('\t')
    if cg[0] in categories.keys() and cg[1] in categories.keys():
        category_category.append([cg[0],cg[1]])
        # source <--> target , source, target, weight, color grey is category
        sg.add_edge(source = cg[0], target = cg[1], weight = int(cg[2]), color = 'grey')
file.close()

# open article <--> category
file = open('../CleanData/article_category_new.csv', 'r', encoding = 'utf-8')
article_category = []
for cg in file.readlines():
    cg = cg.replace('\n','').replace('_',' ').split('\t')
    # 0 article, 1 category
    if cg[0] in categories.keys() and cg[1] in articles.keys():
        article_category.append([cg[1],cg[0]])
        # source <--> target , source is article, target is category, weight, color black is category
        sg.add_edge(source=cg[1],target=cg[0],weight=int(cg[2]),color='black')
    elif cg[1] in categories.keys() and cg[0] in articles.keys():
        article_category.append([cg[0],cg[1]])
        # source <--> target , source, target, weight, color black is category
        sg.add_edge(source=cg[0],target=cg[1],weight=int(cg[2]),color='black')
file.close()
  
def get_description(desc_keyword):
    defdesc = defaultdict(list)
    if desc_keyword in articles.keys():
        file = open('../CleanData/attribute/'+desc_keyword+'_'+articles[desc_keyword].replace(' ','_').replace(':','-')+'.csv', 'r', encoding = 'utf-8')
        lines = file.readlines()
        file.close()
        for l in lines:
            tempkv = (l.replace('\n','')).split('\t') 
            defdesc[tempkv[0]].append(tempkv[1])        
    else:
        defdesc['Category'].append(categories[desc_keyword])    
    return defdesc

def output_description(desc_description):
    table = []
    for k,v in desc_description.items():
        if k != 'image':
            html_row = []
            #html_row.append( html.Td([  ]) )
            html_row.append(html.Td([ 
                    k 
                    ],style=dict(width='90px')))
            values = []
            for d in v:
                if d in articles.keys():
                    values.append(articles[d].replace('_',' '))
                    values.append(html.Br())
            html_row.append(html.Td(
                    values
                    #'\n'.join([articles[d] for d in dic[1] if d in articles.keys()])
                    ))
            #html_row.append( html.Td([  ]) )
            table.append(html.Tr(html_row))
    return table


def get_image(img_description):
    if len(img_description['image'])>0:
        soup = BeautifulSoup(urllib.request.urlopen('http://www.tolkiengateway.net/wiki/'+img_description['image'][0].replace(' ','_')))
        return 'http://www.tolkiengateway.net'+soup.find(id="file").find_all('a')[0].get('href')
    return 'http://www.tolkiengateway.net/w/skins/common/images/newlogo.gif'

def network_3d_plot_single(keywords):
    '''
    get the nodes between nodes, vElements are neighbors
    '''
    sgc = sg.copy()
    #print(sgc)
    
    vElements = []
    vKeywords = []
    vNodelinks = []
    vAttributes = []
    for keyword in keywords:
        vKeywords.append(keyword)
        # add category keywords
        if keyword in categories.keys():
            sgc.vs.find(name=keyword)['size'] = 35
            sgc.vs.find(name=keyword)['color'] = '#414387'
        # add article keywords
        elif keyword in articles.keys(): # if the keyword is an article  
            '''
            change size and group
            '''
            sgc.vs.find(name=keyword)['size'] = 40
            #sgc.vs.find(name=keyword)['group'] = 7
            sgc.vs.find(name=keyword)['color'] = 'yellow'
            '''
            get attribute
            '''
            file = open('../CleanData/attribute/'+keyword+'_'+articles[keyword].replace(' ','_').replace(':','-')+'.csv', 'r', encoding = 'utf-8')
            defdesc = defaultdict(list)
            lines = file.readlines()
            file.close()
            for l in lines:
                tempkv = (l.replace('\n','')).split('\t') # attributeName, nodeID
                # if attribute in dataset
                if tempkv[0] in allAttribute.keys(): 
                    defdesc[tempkv[0]].append(tempkv[1])
            for key,value in defdesc.items():
                '''
                add attribute label
                '''
                if key != 'image':
                    sgc.add_vertex(name = keyword+key, label = key, size = 15, color = '#ca6224', group = 1, symbol = 'diamond-open') 
                    sgc.add_edge(source=keyword,target=keyword+key,weight=1,color='black')
                    vAttributes.append(keyword+key)
                    for v in value:
                        vAttributes.append(v)
                        sgc.add_edge(source=keyword+key,target=v,weight=1,color='black')
                        if v not in keywords:
                            sgc.vs.find(name=v)['color'] = '#ca6224'
            '''
            get node links
            '''
            file = open('../CleanData/link/'+keyword+'_'+articles[keyword].replace(' ','_').replace(':','-')+'.csv', 'r', encoding = 'utf-8')
            lines = file.readlines()
            file.close()
            for l in lines:
                tempkv = (l.replace('\n','')).split('\t')  # get a keyword
                # if linked with another article
                if tempkv[0] in articles.keys():
                    #print("hello")
                    sgc.add_edge(source=keyword,target=tempkv[0],weight=1,color='black')
                    #sgc.vs[tempkv[0]]['group'] = 2
                    vNodelinks.append(tempkv[0])
                    '''
                    tkv = sgc.neighbors(sgc.vs.find(name=tempkv[0])) #find its neighbors
                    for nodelink in tkv:
                        nodelink_name = sgc.vs[nodelink]['name']
                        if nodelink_name in articles.keys():
                            sgc.vs[nodelink]['group'] = 2 # set the keyword's group to 3 -- articles
                        #elif nodelink_name in categories.keys():
                            #nodelink_group = 4 # set the neighvor's group to 4 -- categories
                        vNodelinks.append(nodelink_name) # add this to the vNodelinks
                    '''
        # find keyword's neighbors
        tTT = sgc.neighbors(sgc.vs.find(name=keyword))
        for element in tTT:
            element_name = sgc.vs[element]['name']
            if element_name in articles.keys() and element_name not in keywords and element_name not in vAttributes:
                sgc.vs[element]['color'] = '#68afe2' # set the neighvor's group to 2 -- articles
            elif element_name in categories.keys():
                sgc.vs[element]['color'] = '#9cd668' # set the neighvor's group to 3 -- categories
            vElements.append(element_name) 
    
    subNode = list(set(vElements+vKeywords+vNodelinks+vAttributes))
    
    # get search history (add enhancing)
    user_search = open('../CleanData/user_search.csv','r', encoding = 'utf-8')
    search_history = Counter([u.replace('\n','') for u in user_search.readlines()])
    # add user search history info
    for each in subNode:
        sgc.vs.find(name=each)['label'] += '<br>click: ' + str(search_history[each])
        if sgc.vs.find(name=each)['size'] < 35: # maxsize = 35
            sgc.vs.find(name=each)['size'] += search_history[each]*0.1 # add the click times*10%
                        
    return sgc.subgraph(subNode, implementation="auto")                

def desc_fuzzy(keywords):
    return ''
         
def network_3d_plot_fuzzy(keywords):
    return ''

def network_3d_plot(keywords, search_type):    
    
    sub = igraph.Graph()
    #print (sub)
    # keywords is a list, and search_type is a str
    if search_type == 'single':
        sub = network_3d_plot_single(keywords)
        
    elif search_type == 'fuzzy':
        sub = network_3d_plot_fuzzy(keywords)
    #print (sub)
    layt=sub.layout('kk', dim=3) 
    N = sub.vcount()
    Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
    Yn=[layt[k][1] for k in range(N)]# y-coordinates
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in sub.get_edgelist():
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]  
        Ze+=[layt[e[0]][2],layt[e[1]][2], None] 
        
    trace1=go.Scatter3d(
               x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )
    trace2=go.Scatter3d(
               x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               #name='articles',
               marker=dict(symbol=sub.vs['symbol'],
                             size=sub.vs['size'],
                             #sizeref = 45,
                             #reversescale = True,
                             #sizemode = 'diameter',
                             colorscale='Viridis',
                             color=sub.vs['color'],
                             line=dict(color='rgb(125,125,125)', width=1)
                             ),
               customdata=sub.vs['name'],
               text=sub.vs['label'],
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
        #title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
        width=700,
        height=500,
        #font=dict( family = 'Raleway' ),
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
            #aspectmode='cube'
        ),
        clickmode='event+select',      
        #autosize=True, 
        mapbox=dict(zoom=6),
        margin=dict(pad=0,b=0,l=0,r=0,t=0),
        hovermode='closest',
        )
    data=[trace1, trace2]
    #plot(fig,filename='E:/5.Karen/SilmPy/SilmPy/SilmMain/my-graph.html',output_type='div')
    return go.Figure(data=data, layout=layout)

SILM_KEYWORD = '4490'
FIGURE = network_3d_plot([SILM_KEYWORD],'single')
SILM_DESCRIPTION = get_description(SILM_KEYWORD)
SILM_IMG = get_image(SILM_DESCRIPTION)
'''  
BACKGROUND = 'rgb(230, 230, 230)'

COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"],
                [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(54,50,153)"] ]
'''
   
app.layout = html.Div([
    # Title with introduction
    html.Div([
            html.H2('Knowledge Graph',
                    style={
                        'position': 'relative',
                        #'top': '20px',
                        #'right': '200px',
                        'margin-left': '20px',
                        'font-family': 'Dosis',
                        'display': 'inline',
                        'font-size': '5rem',
                        'color': '#1e4b6b',
                        'float': 'right'
                    }),
            html.H2('Q & A System',
                    style={
                        'position': 'relative',
                        'top': '30px',
                        #'right': '37px',
                        'font-family': 'Dosis',
                        'display': 'inline',
                        'font-size': '6.0rem',
                        'color': '#182b4a',
                        'float': 'right'
                    }),
    ], className='Title-name-first', style={'position': 'relative', 'float': 'right', 'width': '100%'}),
    html.Div([
                html.P('''Input a KEYWORD or a SENTENCE in the search bar.\r\n
                       CHOOSE either KEYWORD SEARCH or FUZZY QUERY.\r\n
                       Click the VERTEX that you want to get the closer look in the knowledge graph.
                       ''')
            ], style={'position': 'relative','float': 'left','margin-top': '20px','width':'40%','font-size': '1.5rem','font-family': 'Open Sans','color': '#dadada'}),
            
    html.Div([
            html.H2('of Tolkien Gateway',
                    style={
                        'position': 'relative',
                        #'top': '-50px',
                        #'right': '10px',
                        'font-family': 'Dosis',
                        'display': 'inline',
                        'font-size': '5.2rem',
                        'color': '#005a98',
                        'float': 'right',
                        #'margin-left': '100px',
                        'margin-top': '70px'
                    }),
            ], 
            className='Title-name-second', 
            style={'position': 'relative', 'width': '55%', 'float': 'right'}
        ),
    
    html.Div([
            
            dcc.Dropdown(id='silm-dropdown',
                        multi=True,
                        value=[ SILM_KEYWORD ],
                        options=[{'label': unidecode.unidecode(articles[i].replace("_"," "))+' (Article)', 'value': i} for i in articles.keys()]+[{'label': unidecode.unidecode(categories[i].replace("_"," ")) +' (Category)', 'value': i} for i in categories.keys()],
                        ),
            dcc.Input(id='silm-input', 
                      type='hidden', 
                      placeholder='Please input a sentence...', 
                      value='', spellCheck=True,
                      style={'width':'100%'})
            ], id='silm-dropdown-outer', className='Intro-search', style={'width': '95%', 'margin':'20px','height':'40px','margin-top': '300px'} ),
            
    # Row 2: Hover Panel and Graph

    html.Div([
        html.Div([

            html.Img(id='silm-img',
                     src=SILM_IMG,  
                     style=dict(width='150px')),

            html.Br(),
            
            html.A(articles[SILM_KEYWORD],
                  id='silm-name',
                  href="http://www.tolkiengateway.net/wiki/"+articles[SILM_KEYWORD],
                  target="_blank",
                  style=dict(fontSize='2rem')),
            
            #html.P(id='silm-desc'),
           
            html.Table(output_description(SILM_DESCRIPTION),
                  id='silm-desc',
                  style=dict( fontSize='1.2rem' ))
            
        ], id='infobox', style={'float':'right','margin-top': '60px','height':'430px', 'overflow-y': 'scroll','width':'300px'} ),

        html.Div([

            dcc.RadioItems(
                id = 'silm-radio',
                options=[
                    dict( label='Keyword Search', value='single' ),
                    dict( label='Fuzzy Search', value='fuzzy' )
                ],
                labelStyle = dict(display='inline', margin='20px'),
                value='single'
            ),

            dcc.Graph(id='3d-network',
                      style=dict(width='700px'),
                      #clickData=dict( points=[dict(pointNumber=0)] ),
                      figure=network_3d_plot([SILM_KEYWORD], 'single'),
                      config={'scrollZoom':True}
                      ),
        ], className='knowledge-graph', style=dict(textAlign='center')),


    ], className='main-graph'),

    html.Div([
        #html.Table( make_dash_table( [STARTING_DRUG] ), id='table-element' )
    ])

], className='container', style={ 
               #'width': '90%',
               'min-width':'750px',
               'width':'85%',
               'position': 'relative',
               'background-repeat': 'no-repeat',
               'background-image': 'url(https://lh3.googleusercontent.com/uIkj4tOOjdYMzIeTrb-1wAIM4o94EMjjBeUVQe_Nq5fatXv0US1twdIcCdW4h443_HWg8_SPPyXFMQlLUtWc-1R_euGGCa9at94UIDxfI-sb9C6AfQdXiufiB7ulrl_L-vmTt_DF6imChrt67G9jp9N0a_tgAxs-XYsp0UPZmvXMkTcg2tOMJRSw4xm8HyiZ2kqoP2uRPl8cqYJZa_247bOAdhD6KWpCVFd_ugfMonZZeS5ItO6jz-OSwAbdVkt857gmnBlUwoB9kA_j_BbPS8_248xURDldvOv3H1LW56zGatqcV_Z1gvmg6DDgkyOZHdy3ukTAPmCXxLhSquGX3jM8l267YHOrjeWAcDL8a3pgXLePqzafOzPoRANxVW0Y4BMhhzPcTUJ2TGIp_B2QVj_QUhrPOP_jAbsxDadqyXORqSvm9VOhPsNznH-1IEH5ov1kBJRDnbRMW5wwh46UTWpCPjPi-oBu5GnzdikmI7-3rgs-H5o_sdJyRYnLEwyMhbulD0BxN1nF3bK38RADiI8UFKeAgVmoURTcptIMNMM0-QuIUWQf2qjq0ScpOiA3CYuwBkzSS4x1j5_tJx4qTGqUbV-5hGC5_74mTgo=w1366-h625)'})


@app.callback(
    Output('silm-dropdown-outer', 'children'),
    [Input('silm-radio', 'value')])
def change_radio(search_type):
    if search_type == 'single':
        return [dcc.Dropdown(id='silm-dropdown',
                             multi=True,
                             value=SILM_CACHE,
                             options=[{'label': unidecode.unidecode(articles[i].replace("_"," "))+' (Article)', 'value': i} for i in articles.keys()]+[{'label': unidecode.unidecode(categories[i].replace("_"," ")) +' (Category)', 'value': i} for i in categories.keys()]),
                dcc.Input(id='silm-input', type='search', placeholder='Please input a sentence...', value='', spellCheck=True,style={'display':'none'})]
    elif search_type == 'fuzzy' : #fuzzy
        return [dcc.Dropdown(id='silm-dropdown',
                             multi=True,
                             value=SILM_CACHE,
                             style={'display':'none'},
                             options=[{'label': unidecode.unidecode(articles[i].replace("_"," "))+' (Article)', 'value': i} for i in articles.keys()]+[{'label': unidecode.unidecode(categories[i].replace("_"," ")) +' (Category)', 'value': i} for i in categories.keys()]),
                dcc.Input(id='silm-input', type='search', placeholder='Please input a sentence...', value='', spellCheck=True,style={'width':'100%'})]
    

'''
When update the value in silm-dropdown, update table name
'''
@app.callback(
    Output('silm-name', 'children'),
    [Input('silm-dropdown', 'value')],
    [State('silm-radio', 'value')])
def update_name(silm_dropdown_value, search_type):
    SILM_CACHE.clear()
    for s in silm_dropdown_value:
        SILM_CACHE.append(s)
    if len(silm_dropdown_value) == 0:
        dash.exceptions.PreventUpdate()
    elif search_type == "single" and silm_dropdown_value[-1] in articles.keys():
        return articles[silm_dropdown_value[-1]]
    elif search_type == "single" and silm_dropdown_value[-1] in categories.keys():
        return  categories[silm_dropdown_value[-1]]
'''
When update the value in silm-dropdown, update table name href
'''
@app.callback(
     Output('silm-name', 'href'),
    [Input('silm-dropdown', 'value')],
    [State('silm-radio', 'value')])
def update_href(silm_dropdown_value, search_type):
    SILM_CACHE.clear()
    for s in silm_dropdown_value:
        SILM_CACHE.append(s)
    if len(silm_dropdown_value) == 0:
        dash.exceptions.PreventUpdate()
    elif search_type == "single" and silm_dropdown_value[-1] in articles.keys():
        return "http://www.tolkiengateway.net/wiki/"+articles[silm_dropdown_value[-1]]
    elif search_type == "single" and silm_dropdown_value[-1] in categories.keys():
        return 'http://www.tolkiengateway.net/w/skins/common/images/newlogo.gif'
'''
When update the value in silm-dropdown, update table img
'''
@app.callback(
     Output('silm-img', 'src'),
    [Input('silm-dropdown', 'value')],
    [State('silm-radio', 'value')])
def update_img(silm_dropdown_value, search_type):
    SILM_CACHE.clear()
    for s in silm_dropdown_value:
        SILM_CACHE.append(s)
    if len(silm_dropdown_value) == 0:
        dash.exceptions.PreventUpdate()
    elif search_type == "single" and silm_dropdown_value[-1] in articles.keys():
        return get_image(get_description(silm_dropdown_value[-1]))
    elif search_type == "single" and silm_dropdown_value[-1] in categories.keys():
        return get_image(get_description(silm_dropdown_value[-1]))
'''
When update the value in silm-dropdown, update network + table desc
'''
@app.callback(
    [Output('silm-desc', 'children'),
     Output('3d-network', 'figure')],
    [Input('silm-dropdown', 'value'),
     Input('silm-input', 'n_submit')],
    [State('silm-radio', 'value'),
     State('silm-input', 'value')])
def update_network(silm_dropdown_value, ns, search_type, input_sentence):
    SILM_CACHE.clear()
    for s in silm_dropdown_value:
        SILM_CACHE.append(s)
    if len(silm_dropdown_value) == 0:
        dash.exceptions.PreventUpdate()
    elif search_type == "single" and silm_dropdown_value[-1] in articles.keys():
        return output_description(get_description(silm_dropdown_value[-1])), network_3d_plot( silm_dropdown_value, search_type )
    elif search_type == "single" and silm_dropdown_value[-1] in categories.keys():
        return output_description(get_description(silm_dropdown_value[-1])), network_3d_plot( silm_dropdown_value, search_type )
    elif search_type == "fuzzy":
        keywords = understand_sentence(input_sentence)
        return desc_fuzzy(keywords), network_3d_plot_fuzzy(keywords)


@app.callback(
    Output('silm-dropdown', 'value'),
    [Input('3d-network', 'clickData'),
     Input('silm-radio', 'value')],
     [State('silm-dropdown', 'value')])
def click_vertex(clickData, search_type, silm_dropdown_value):
    SILM_CACHE.clear()
    for s in silm_dropdown_value:
        SILM_CACHE.append(s)
    #if search_type == "single" and hasattr(clickData, 'keys'):
    if hasattr(clickData, 'keys'):
        if 'points' in clickData.keys():
            if 'customdata' in clickData['points'][0]:
                click_node = clickData['points'][0]['customdata']
                user_search = open('../CleanData/user_search.csv','a', encoding = 'utf-8')
                user_search.write(click_node+'\n')
                user_search.close()
                if click_node.isdigit() and click_node not in silm_dropdown_value:
                    return silm_dropdown_value + [click_node]
                else:
                    return silm_dropdown_value
            else:
                return silm_dropdown_value
        else:
            return silm_dropdown_value
    else: 
        return silm_dropdown_value


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server()
