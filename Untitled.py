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


output('94k50hp',10,'Ceramic')


# In[4]:


output('60k50hp',10,'Ceramic').to_dict()


# In[5]:


#UKCountries = FF.create_table(output('60k50hp',10,'Ceramic'))
#pyo.iplot(UKCountries)


# In[6]:



sojae_list1=['AL5052', 'Bronze',
       'CarbonFiber', 'Glass', 'Inconel600', 'Invar',
       'MildSteel_nA36', 'Plexiglass', 'Rubber',
       'SteelAR400', 'StainlessSteel304', 'StainlessSteel',
       'Ti', 'TungstenCarbide']
sojae_list2=['Ceramic', 'Marble', 'Quartz']
sojae_list=sojae_list1+sojae_list2
op_start=[{'label' : a, 'value': a} for a in sojae_list ]
op_start


# In[7]:



thick_list1=[5,10,20,30,50,100]
thick_dic1=[{'label' : str(a)+'mm','value': str(a)} for a in thick_list1]
thick_list2=[4,8,10,12,20]
thick_dic2=[{'label' : str(a)+'mm','value': str(a)} for a in thick_list2]
thick_dic1


# In[8]:


thick_dic3=[
                    {'label': '5', 'value': '5'},
                    {'label': '10', 'value': '10'},
                    {'label': '20', 'value': '20'},
                    {'label': '30', 'value': '30'},
                    {'label': '50', 'value': '50'},
                    {'label': '100', 'value': '100'}
                ]
thick_dic3


# In[9]:


type(thick_dic1),type(thick_dic3),len(thick_dic1),len(thick_dic3)


# In[10]:


(thick_dic1[0].keys()),(thick_dic3[0].keys())


# In[11]:


thick_dic1[0].keys()==thick_dic3[0].keys()


# In[67]:


model_list=['60k50hp','94k50hp','94k100hp']
model_label_list=['UltraJet is','HyperJet is','HyperJet id']
model_dic=[{'label' : model_label_list[a], 'value':model_list[a] } for a in range(0,3)]
model_dic


# In[ ]:





# In[24]:


df1=output('60k50hp',10,'Ceramic')
df2=output('94k50hp',10,'Ceramic')

df3=pd.concat([df1,df2],axis=1)
df3=df3.iloc[:,[0,1,3]]
df3.columns=['Quality','hi1','hi2']
df3


# In[25]:





# In[70]:


app = dash.Dash()



df_start=output('60k50hp',10,'Ceramic').to_dict()

app.layout = html.Div([html.Div([html.H1('Flow waterjet cutting feed rate calculator')]),
    html.Div([
        html.Div([
                html.H3('소재 :  ')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='sojae-dropdown',
                    options=op_start,
                    placeholder="선택하세요",
                    value='Glass')],
                style={'width':'11%','display':'inline-block'}

                )]),
    html.Div([
        html.Div([
                html.H3('두께 :   ')],style={'display':'inline-block','margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='thick-dropdown',
                    options=thick_dic1
                
            )],
                style={'width':'10%','display':'inline-block'}

                )]),
                      

    html.Div([
        html.Div([
                html.H3('모델1 :  ')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='model-dropdown',
                    options=model_dic,
                    placeholder="선택하세요")],
                style={'width':'10%','display':'inline-block'},
            

                ),
        html.Div([
                html.H3('모델2 :  ')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                dcc.Dropdown(
                    id='model-dropdown2',
                    options=model_dic,
                    placeholder="선택하세요")],
                style={'width':'10%','display':'inline-block'},
            

                )        
            ]),     
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
             
                       
    html.Div([
        html.Div([
                html.H4('사양')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H3('사양1',id='spec_1')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H4('사양')],style={'display':'inline-block', 'margin-right': '15px'}),        
        html.Div([
                html.H3('사양2',id='spec_2')],style={'display':'inline-block', 'margin-right': '15px'})
      
            ]) ,
    html.Div([
        html.Div([
                html.H4('노즐 in')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H3('',id='nozle_1')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H4('노즐 in')],style={'display':'inline-block', 'margin-right': '15px'}),        
        html.Div([
                html.H3('',id='nozle_2')],style={'display':'inline-block', 'margin-right': '15px'})
      
            ]) ,
    html.Div([
        html.Div([
                html.H4('오리피스 mm')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H3('',id='op_1')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H4('오리피스 mm')],style={'display':'inline-block', 'margin-right': '15px'}),        
        html.Div([
                html.H3('',id='op_2')],style={'display':'inline-block', 'margin-right': '15px'})
      
            ]) ,   
    html.Div([
        html.Div([
                html.H4('작동 압력 psi')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H3('',id='psi_1')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H4('작동 압력 psi')],style={'display':'inline-block', 'margin-right': '15px'}),        
        html.Div([
                html.H3('',id='psi_2')],style={'display':'inline-block', 'margin-right': '15px'})
      
            ]) ,
    html.Div([
        html.Div([
                html.H4('연마재 g/min')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H3('',id='gmin_1')],style={'display':'inline-block', 'margin-right': '15px'}),
        html.Div([
                html.H4('연마재 g/min')],style={'display':'inline-block', 'margin-right': '15px'}),        
        html.Div([
                html.H3('',id='gmin_2')],style={'display':'inline-block', 'margin-right': '15px'})
      
            ]) ,                       
    html.Div([
                html.H5('[단위 mm/min]')],style={'display':'inline-block', 'margin-left': '10%'}),

    html.Div([html.Div(id="update-table")]),                         
                    
                       

    
    ])


@app.callback(Output('spec_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_output_div1(n_clicks,input_value):
    if input_value==None:
        return None
    return input_value
@app.callback(Output('spec_2', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown2', 'value')])
def update_output_div2(n_clicks,input_value):
    if input_value==None:
        return None
    return input_value


@app.callback(Output('nozle_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_nozle_div1(n_clicks,input_value):
    print(input_value)
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '1.02'
        elif input_value=='94k50hp':
            return '0.89'
        if input_value=='94k100hp':
            return '1.02'        
    
@app.callback(Output('nozle_2', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown2', 'value')])
def update_nozle_div2(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '1.02'
        elif input_value=='94k50hp':
            return '0.89'
        if input_value=='94k100hp':
            return '1.02'      


        
@app.callback(Output('op_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_op_div1(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '0.33'
        elif input_value=='94k50hp':
            return '0.25'
        if input_value=='94k100hp':
            return '0.38'        
    
@app.callback(Output('op_2', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown2', 'value')])
def update_op_div2(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '0.33'
        elif input_value=='94k50hp':
            return '0.25'
        if input_value=='94k100hp':
            return '0.38'  
        
@app.callback(Output('psi_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_psi_div1(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '55,000'
        elif input_value=='94k50hp':
            return '87,000'
        if input_value=='94k100hp':
            return '87,000'        
    
@app.callback(Output('psi_2', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown2', 'value')])
def update_psi_div2(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '55,000'
        elif input_value=='94k50hp':
            return '87,000'
        if input_value=='94k100hp':
            return '87,000'    
        
 
@app.callback(Output('gmin_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_gmin_div1(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '400'
        elif input_value=='94k50hp':
            return '400'
        if input_value=='94k100hp':
            return '500'        
    
@app.callback(Output('gmin_2', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown2', 'value')])
def update_gmin_div2(n_clicks,input_value):
    if input_value==None:
        return None
    else:
        if input_value=='60k50hp':
            return '400'
        elif input_value=='94k50hp':
            return '400'
        if input_value=='94k100hp':
            return '500'        

@app.callback(Output('thick-dropdown', 'options'),
              [Input('sojae-dropdown', 'value')])
def update_figure(value):
    if value in sojae_list1:
        print(value)
        return thick_dic1
    elif value in sojae_list2:
        return thick_dic2
    else:
        return None

@app.callback(Output('update-table', "children"),
              Input('submit-button-state', 'n_clicks'),
              State('sojae-dropdown', 'value'),
              State('thick-dropdown', 'value'),
              State('model-dropdown', 'value'),
              State('model-dropdown2', 'value'))
        
def update_output(n_clicks, sojae, thick,model1,model2):
    if (thick==None)&(model1==None):
        return None
    else:
        df1=output(model1,int(thick),sojae)
        df2=output(model2,int(thick),sojae)

        df3=pd.concat([df1,df2],axis=1)
        df3=df3.iloc[:,[0,1,3]]
        df3.columns=['Quality',model1,model2]

        return html.Div(
            [
                dash_table.DataTable(




                    data=df3.to_dict("rows"),
                    columns=[{"id": x, "name": x} for x in df3.columns],
                )
            ],style={'width':'10%'}
    )


'''
@app.callback(Output('update-table2', "children"),
              Input('submit-button-state', 'n_clicks'),
              State('sojae-dropdown', 'value'),
              State('thick-dropdown', 'value'),
              State('model-dropdown2', 'value'))
        
def update_output2(n_clicks, sojae, thick,model ):
    if (thick==None)&(model==None):
        return None
    return html.Div(
        [
            dash_table.DataTable(
                data=output(model,int(thick),sojae).to_dict("rows"),
                columns=[{"id": x, "name": x} for x in output(model,int(thick),sojae).columns],
            )
        ],style={'width':'10%'}
    )
'''
username = 'Hanmool' # your username
api_key = 'MpUhAi8DD94aZ7z4aMol' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)




if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=5050)


# In[ ]:




