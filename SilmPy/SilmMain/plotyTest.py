# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:22:42 2019

@author: xingg
"""
import dash
import igraph as ig
import json
import urllib.request
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash('Silm-Graph-Search')
server = app.server

data = []
urlData = "https://raw.githubusercontent.com/plotly/datasets/master/miserables.json"
webURL = urllib.request.urlopen(urlData)
readData = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
data = json.loads(readData.decode(encoding))

print (data.keys())
N=len(data['nodes'])
print (N)
L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)
print (data['nodes'][0])
labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])
    
layt=G.layout('kk', dim=3) 

print (layt[5])


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
        ],    )

data=[trace1, trace2]
fig=go.Figure(data=data, layout=layout)

#print (plot(fig,filename='my-graph.html',output_type='div'))

app.layout = html.Div([
        
        dcc.Graph(id='3d-network',
                      style=dict(width='700px'),
                      #clickData=dict( points=[dict(pointNumber=0)] ),
                      figure=fig
                      ),
        ], className='knowledge-graph', style=dict(textAlign='center'))


if __name__ == '__main__':
    app.run_server()