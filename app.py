import dash
from dash import dash_table, html, dcc

#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go



####################################################################################################################
## Wrangle the data
####################################################################################################################

#data_path = 'https://raw.githubusercontent.com/fpontejos/ifood-team13/main/data/food_recipes.csv'
#data_path2 = 'data/food_recipes.csv'

data_path = 'data/'

pct_data = pd.read_csv(data_path + 'renewables_percent_timeseries.csv')
pct_data = pct_data.sort_values(by='Country')

country_codes = [i for i in pct_data['Country Code'].unique()]
ts_years = [str(i) for i in range(2004, 2021)]

percent_timeseries = pct_data.loc[pct_data['SIEC Code']=='RA000']\
                              .reset_index(drop=True)
percent_timeseries_tot = pct_data.loc[pct_data['SIEC Code']=='TOTAL']\
                                 .reset_index(drop=True)

for yi in ts_years:
    percent_timeseries[yi] = round((100*percent_timeseries[yi] / percent_timeseries_tot[yi]), 2)

######################################################Functions##############################################################



######################################################Interactive Components############################################

dropdown_cc = dcc.Dropdown(
       id='cc_drop',
       options=country_codes,
       multi=True
   )

slider_years = dcc.Slider(
       id='slider_years',
       value=2020,
       marks={str(i): '{}'.format(str(i)) for i in
              ts_years},
       step=1
   )

######## 


##################################################APP###################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div(className='hero-bg'),

        html.Div([
            html.H1('EU Renewable Energy Directive'),
            html.P("Some text here")
        ],className='hero-title is-marginless'),
        
    ], 
    className='row hero'),

    html.Div([
        html.Div([
            html.H2(["Top Performing Countries: ",html.Span(id='title_top_year')]),
            html.Div([
                html.Div([], id='top_eu_1', className='col top_eu'),
                html.Div([], id='top_eu_2', className='col top_eu'),
                html.Div([], id='top_eu_3', className='col top_eu')
            ],className='row'),
            html.Div([
                html.Div([], id='top_not_1', className='col-4 top_eu'),
                html.Div([], id='top_not_2', className='col-4 top_eu'),
                html.Div([
                    html.P("Some notes", className='small')
                ], className='col-4 top_eu placeholder'),
            ],className='row')
            ],
            className='col-7 top_perf_container'),
        html.Div([
            html.P("")
            ],
            className='col placeholder'),
    ],
    className='row'),


    html.H2('Placeholder h2'),
    dropdown_cc, 

    #prop options display
    html.Div([
        html.Label('Placeholder Div'),
        html.Div(id='placeholder_title',className='holder')
    ], className=''),

    html.Div([
        html.Label('Placeholder Div'),
        html.Div([
            slider_years
        ],
        className='holder')
    ], className=''),
    ],
    
    className="container card outer")



######################################################Callbacks#########################################################




@app.callback(
    Output('placeholder_title', 'children'),
    Output('title_top_year', 'children'),
    Output('top_eu_1', 'children'),
    Output('top_eu_2', 'children'),
    Output('top_eu_3', 'children'),
    Output('top_not_1', 'children'),
    Output('top_not_2', 'children'),
    Input('slider_years', 'value'),
    
)
def getTopPerforming(year_value):
    print('foooo')
    print(year_value)

    perf_by_year = percent_timeseries.loc[:,['Country', str(year_value), 'Country Code']].sort_values(by=str(year_value), ascending=False).reset_index(drop=True)
    
    top_res_return = []

    for ti in range(5):
        f_ = "url('assets/flags/" + str.lower(perf_by_year.iloc[ti,2]) + ".svg')"
        top_res_return.append([
            html.Div([
                html.Div(className='country_flag', id="top_flag_"+perf_by_year.iloc[ti,2],
                        style={"background-image": f_}
                ),
                html.H4(perf_by_year.iloc[ti,0]),
                html.H5(str(perf_by_year.iloc[ti,1])+" %")
            ], className='top_perf'
            )
            ])

    return [year_value,
        year_value, 
        top_res_return[0], 
        top_res_return[1], 
        top_res_return[2], 
        top_res_return[3], 
        top_res_return[4], 
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
