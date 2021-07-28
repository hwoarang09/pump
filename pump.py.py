#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas as pd
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import datetime
import chart_studio.plotly as py
import chart_studio
import os
import dash_table

import plotly.figure_factory as FF
#plotly.offline doesn't push your charts to the clouds
import plotly.offline as pyo
#allows us to create the Data and Figure objects
from plotly.graph_objs import *
#plotly.plotly pushes your charts to the cloud  
import chart_studio.plotly as py

#pandas is a data analysis library
import pandas as pd
from pandas import DataFrame


# In[2]:




def output(model,thick,columns):
    df_60k50hp_1=pd.read_csv('60k50hp_1.csv',encoding='euc-kr')

    df_94k50hp_1=pd.read_csv('94k50hp_1.csv',encoding='euc-kr')
    df_94k100hp_1=pd.read_csv('94k100hp_1.csv',encoding='euc-kr')

    df_60k50hp_2=pd.read_csv('60k50hp_2.csv')
    df_94k50hp_2=pd.read_csv('94k50hp_2.csv')
    df_94k100hp_2=pd.read_csv('94k100hp_2.csv')

    columns_list=['Thick', 'Quality', 'AL5052', 'Bronze',
           'CarbonFiber', 'Glass', 'Inconel600', 'Invar',
           'MildSteel_nA36', 'Plexiglass', 'Rubber',
           'SteelAR400', 'StainlessSteel304', 'StainlessSteel',
           'Ti', 'TungstenCarbide', 'Unnamed: 16']
    df_60k50hp_1.columns=columns_list
    df_94k50hp_1.columns=columns_list
    df_94k100hp_1.columns=columns_list 
    df=pd.DataFrame([])
    if columns in ['Ceramic', 'Marble', 'Quartz']:
        if model=='60k50hp':
            df=df_60k50hp_2
        if model=='94k50hp':
            df=df_94k50hp_2
        if model=='94k100hp':
            df=df_94k100hp_2            
    else:
        if model=='60k50hp':
            df=df_60k50hp_1
        if model=='94k50hp':
            df=df_94k50hp_1
        if model=='94k100hp':
            df=df_94k100hp_1   
    return df[(df.Thick==(thick))][['Quality',columns]]


# In[3]:


output('60k50hp',12,'Ceramic')


# In[9]:


output('60k50hp',10,'Ceramic').to_dict()


# In[4]:


UKCountries = FF.create_table(output('60k50hp',10,'Ceramic'))
pyo.iplot(UKCountries)


# In[5]:



sojae_list1=['AL5052', 'Bronze',
       'CarbonFiber', 'Glass', 'Inconel600', 'Invar',
       'MildSteel_nA36', 'Plexiglass', 'Rubber',
       'SteelAR400', 'StainlessSteel304', 'StainlessSteel',
       'Ti', 'TungstenCarbide']
sojae_list2=['Ceramic', 'Marble', 'Quartz']
sojae_list=sojae_list1+sojae_list2
op_start=[{'label' : a, 'value': a} for a in sojae_list ]


# In[6]:


thick_list1=[5,10,20,30,50,100]
thick_dic1=[{'label' : a, 'value':a } for a in thick_list1]
thick_list2=[4,8,10,12,20]
thick_dic2=[{'label' : a, 'value':a } for a in thick_list2]


# In[20]:


model_list=['60k50hp','94k50hp','94k100hp']
model_dic=[{'label' : a, 'value':a } for a in model_list]


# In[30]:


output('60k50hp',10,'Ceramic')


# In[43]:


app = dash.Dash()



df_start=output('60k50hp',10,'Ceramic').to_dict()

app.layout = html.Div([html.Div([html.H1('Flow pump')]),
    html.Div([
        html.Div([
                html.H3('소재 :  ')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='sojae-dropdown',
                    options=op_start,
                    value='Bronze')],
                style={'width':'10%','display':'inline-block'}

                )]),
    html.Div([
        html.Div([
                html.H3('두께 :   ')],style={'display':'inline-block','margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='thick-dropdown',
                    options=thick_dic1,
                    value='5')],
                style={'width':'10%','display':'inline-block'}

                )]),

    html.Div([
        html.Div([
                html.H3('모델 :  ')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='model-dropdown',
                    options=model_dic,
                    value='60k50hp')],
                style={'width':'10%','display':'inline-block'},
            

                ),
        html.Div([
                html.H3('모델 :  ')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='model-dropdown2',
                    options=model_dic,
                    value='60k50hp')],
                style={'width':'10%','display':'inline-block'},
            

                )        
            ]),                       
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    
    html.Div([html.Div(id="update-table")],style={'display' : 'inline-block'}),
    html.Div([html.Div(id="update-table2")],style={'display' : 'inline-block'})                       
])






@app.callback(Output('thick-dropdown', 'options'),
              [Input('sojae-dropdown', 'value')])
def update_figure(value):
    if value in sojae_list1:
        print(value)
        return thick_dic1
    elif value in sojae_list2:
        return thick_dic2

@app.callback(Output('update-table', "children"),
              Input('submit-button-state', 'n_clicks'),
              State('sojae-dropdown', 'value'),
              State('thick-dropdown', 'value'),
              State('model-dropdown', 'value'))
        
def update_output(n_clicks, sojae, thick,model ):
    print('model, thick, sojae',model,thick,sojae, type(thick))
    print(output(model,int(thick),sojae).to_dict('records'))
    return html.Div(
        [
            dash_table.DataTable(
                data=output(model,int(thick),sojae).to_dict("rows"),
                columns=[{"id": x, "name": x} for x in output(model,int(thick),sojae).columns],
            )
        ],style={'width':'10%'}
    )



@app.callback(Output('update-table2', "children"),
              Input('submit-button-state', 'n_clicks'),
              State('sojae-dropdown', 'value'),
              State('thick-dropdown', 'value'),
              State('model-dropdown2', 'value'))
        
def update_output2(n_clicks, sojae, thick,model ):
    print('model, thick, sojae',model,thick,sojae, type(thick))
    print(output(model,int(thick),sojae).to_dict('records'))
    return html.Div(
        [
            dash_table.DataTable(
                data=output(model,int(thick),sojae).to_dict("rows"),
                columns=[{"id": x, "name": x} for x in output(model,int(thick),sojae).columns],
            )
        ],style={'width':'10%'}
    )
        
username = 'Hanmool' # your username
api_key = 'MpUhAi8DD94aZ7z4aMol' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)




if __name__ == '__main__':
    app.run_server()


# In[ ]:




