#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[4]:




def output(model,thick,columns):
    df_60k50hp_1=pd.read_csv('60k50hp_1.csv',encoding='euc-kr')

    df_94k50hp_1=pd.read_csv('94k50hp_1.csv',encoding='euc-kr')
    df_94k100hp_1=pd.read_csv('94k100hp_1.csv',encoding='euc-kr')

    df_60k50hp_2=pd.read_csv('60k50hp_2.csv')
    df_94k50hp_2=pd.read_csv('94k50hp_2.csv')
    df_94k100hp_2=pd.read_csv('94k100hp_2.csv')

    columns_list=['Thick', 'Quality', 'AL5052', 'Bronze',
           'CarbonFiber', 'Glass', 'Inconel600', 'Invar',
           'MildSteel A36', 'Plexiglass 아크릴', 'Rubber',
           'Steel AR400', 'Stainless Steel 304', 'Stainless Steel 316L',
           'Ti', 'Tungsten Carbide', 'Unnamed: 16']
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


# In[5]:



sojae_list1=['AL5052', 'Bronze',
       'CarbonFiber', 'Glass', 'Inconel600', 'Invar',
       'MildSteel_nA36', 'Plexiglass', 'Rubber',
       'SteelAR400', 'StainlessSteel304', 'StainlessSteel',
       'Ti', 'TungstenCarbide']
sojae_list2=['Ceramic', 'Marble', 'Quartz']
sojae_list=sojae_list1+sojae_list2
op_start=[{'label' : a, 'value': a} for a in sojae_list ]
op_start


# In[6]:



thick_list1=[5,10,20,30,50,100]
thick_dic1=[{'label' : str(a)+'mm','value': str(a)} for a in thick_list1]
thick_list2=[4,8,10,12,20]
thick_dic2=[{'label' : str(a)+'mm','value': str(a)} for a in thick_list2]
thick_dic1


# In[7]:


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


model_list=['60k50hp','94k50hp','94k100hp']
model_label_list=['UltraJet iS','HyperJet iS','HyperJet iD']
model_dic=[{'label' : model_label_list[a], 'value':model_list[a] } for a in range(0,3)]
model_dic


# In[10]:


def delete_comma(x):
    try:
        return round(float(x.replace(',','')),2)
    except:
        return round(float(x),2)
    
def to_str(x):
    x=str(x)
    
    if len(x.split('.')[1])==1:
        return x+'0'
    return x    


# In[11]:


app = dash.Dash()






df_start=output('60k50hp',10,'Ceramic').to_dict()

app.layout = html.Div([
    html.Div(html.Img(src=app.get_asset_url('FLOW.png'), style={'height':'20%', 'width':'40%'})),
    html.Div([
        
        html.Div([
                dcc.Dropdown(
                    id='sojae-dropdown',
                    options=op_start,
                    placeholder="선택하세요",
                    value='Glass')],
                style={'width':'40%','display':'inline-block'}

                )]),
    html.Div([
     
        html.Div([
                dcc.Dropdown(
                    id='thick-dropdown',
                    options=thick_dic1,
                    placeholder='두께 (Thick mm)'
                
            )],
                style={'width':'40%','display':'inline-block'}

                )]),
                      

    html.Div([
       
        html.Div([
                dcc.Dropdown(
                    id='model-dropdown',
                    options=model_dic,
                    value='60k50hp')],
                style={'width':'20%','display':'inline-block'},
            

                ),
       
        html.Div([
                dcc.Dropdown(
                    id='model-dropdown2',
                    options=model_dic,
                    placeholder="선택하세요")],
                style={'width':'20%','display':'inline-block'},
            

                )        
            ]),     
    
             
                       
    html.Div([
        html.Div([
                html.H6('사양')],style={'display':'inline-block', 'width':'20%','height':'5%','margin-right':'5%'}),
        html.Div([
                html.H5('사양1',id='spec_1')],style={'display':'inline-block','width':'20%','height':'5%','margin-right':'5%'}),
        html.Div([
                html.H6('사양')],style={'display':'inline-block','width':'20%','height':'5%','margin-right':'5%'}),        
        html.Div([
                html.H5('사양2',id='spec_2')],style={'display':'inline-block','height':'5%','width':'20%','margin-right':'5%'})
      
            ],style={'width':'40%','height':'20px'}) ,
    html.Div([
        html.Div([
                html.H6('노즐')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H5('',id='nozle_1')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H6('노즐')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),        
        html.Div([
                html.H5('',id='nozle_2')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'})
      
            ],style={'width':'40%','height':'20px'}) ,
    html.Div([
        html.Div([
                html.H6('오리피스')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H5('',id='op_1')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H6('오리피스')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),        
        html.Div([
                html.H5('',id='op_2')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'})
      
            ],style={'width':'40%','height':'20px'}) ,   
    html.Div([
        html.Div([
                html.H6('작동 압력')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H5('',id='psi_1')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H6('작동 압력')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),        
        html.Div([
                html.H5('',id='psi_2')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'})
      
            ],style={'width':'40%','height':'20px'}) ,
    html.Div([
        html.Div([
                html.H6('연마재')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H5('',id='gmin_1')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),
        html.Div([
                html.H6('연마재')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'}),        
        html.Div([
                html.H5('',id='gmin_2')],style={'display':'inline-block', 'width':'20%','margin-right':'5%'})
      
            ],style={'width':'40%','height':'20px','display':'inline-block'}),
                       
    html.Div([html.Button(id='submit-button-state', n_clicks=0, children='Submit')],style={'width':'40%','textAlign': 'center','padding-top':'3%'}),
    
    html.Div([
                html.H5('Linear cutting speed : mm/min')],style={'width':'40%','textAlign': 'center'}),

    html.Div([html.Div(id="update-table")])                    
                    
                       

    
    ])


@app.callback(Output('spec_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_output_div1(n_clicks,input_value):
    if (input_value==None)or(n_clicks==0):
        return None
    return input_value
@app.callback(Output('spec_2', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown2', 'value')])
def update_output_div2(n_clicks,input_value):
    if (input_value==None)or(n_clicks==0):
        return None
    return input_value


@app.callback(Output('nozle_1', 'children'),[Input('submit-button-state', 'n_clicks')],[State('model-dropdown', 'value')])
def update_nozle_div1(n_clicks,input_value):
    print(input_value)
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (input_value==None)or(n_clicks==0):
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
    if (thick==None)&(sojae==None):
        return None
    else:
        df1=output(model1,int(thick),sojae)
        df2=output(model2,int(thick),sojae)

        df3=pd.concat([df1,df2],axis=1)
        df3=df3.iloc[:,[0,1,3]]
        df3.columns=['Quality',model1,model2]        
        df3.iloc[:,2]=df3.iloc[:,2].apply(delete_comma)
        df3.iloc[:,1]=df3.iloc[:,1].apply(delete_comma)
        df3.iloc[:,1]=pd.to_numeric(df3.iloc[:,1])
        df3.iloc[:,2]=pd.to_numeric(df3.iloc[:,2])
        print((df3.iloc[:,2]==df3.iloc[:,1]).values)
        if model1==model2:
            list3=[0,0,0,0,0]
        else:
            list3=round((df3.iloc[:,2]-df3.iloc[:,1])/df3.iloc[:,1]*100,2)
        df3['speed %']=list3
        df3.iloc[:,1]=df3.iloc[:,1].apply(to_str)
        df3.iloc[:,2]=df3.iloc[:,2].apply(to_str)
        print(df3)        
        
        return html.Div(
            [
                dash_table.DataTable(




                    data=df3.to_dict("rows"),
                    columns=[{"id": x, "name": x} for x in df3.columns],
                )
            ],style={'width':'38%'}
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


# In[12]:



