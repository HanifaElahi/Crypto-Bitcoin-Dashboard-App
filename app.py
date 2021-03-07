import pandas as pd
import numpy as np
import plotly.express as px

import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

#------------------------------------------------------------------------------------------------------------------------------------------------


data = pd.read_csv("Historical_Data_for_Bitcoin.csv")
data = data.set_index('Date')


data['Open'] = data['Open'].str.replace(',','', regex=True)
data['High'] = data['High'].str.replace(',','', regex=True)
data['Low'] = data['Low'].str.replace(',','', regex=True)
data['Close'] = data['Close'].str.replace(',','', regex=True)
data['Volume'] = data['Volume'].str.replace(',','', regex=True)
data['Market Cap'] = data['Market Cap'].str.replace(',','', regex=True)


data['Open'] = data['Open'].str.replace('$','', regex=True)
data['High'] = data['High'].str.replace('$','', regex=True)
data['Low'] = data['Low'].str.replace('$','', regex=True)
data['Close'] = data['Close'].str.replace('$','', regex=True)
data['Volume'] = data['Volume'].str.replace('$','', regex=True)
data['Market Cap'] = data['Market Cap'].str.replace('$','', regex=True)
data.astype('float64')


data['Open'] = pd.to_numeric(data['Open'])
data['High'] = pd.to_numeric(data['High'])
data['Low'] = pd.to_numeric(data['Low'])
data['Close'] = pd.to_numeric(data['Close'])
data['Volume'] = pd.to_numeric(data['Volume'])
data['Market Cap'] = pd.to_numeric(data['Market Cap'])

data.reset_index(inplace=True)

data['Date'] = pd.DatetimeIndex(data['Date']) 
data['Year']=data['Date'].dt.year

df = data[['Year','High','Open','Low','Close','Volume','Market Cap']]

dff = df.groupby(["Year"])[['High','Open','Low','Close','Volume','Market Cap']].mean()
#------------------------------------------------------------------------------------------------------------------------------------------------


app.layout = html.Div([

   

    html.H1('Bitcoin Hitorical Data', style={"textAlign": "center","color":"purple"}),

    html.Br(),
    html.Br(),


    dcc.Dropdown(
        id='linedropdown', 
        options=[{'label': x, 'value': x} for x in dff.columns],
        value = "Close", 
        disabled=False,                     
        multi=True,                        
        searchable=True,                    
        search_value='',                   
        placeholder='Select...',     
        clearable=True,                          
        style={'width':"100%",'color':'purple'},
    ),

    dcc.Graph(id='graph',figure = {}),
    
])

@app.callback(Output('graph', 'figure'),
              [Input('linedropdown', 'value')])


def display_value(option):
    df_filterd = dff[option]
    figure = px.line(df_filterd)
    return figure

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)