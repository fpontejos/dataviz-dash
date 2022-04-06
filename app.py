import dash
from dash import dash_table, html, dcc

#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.fftpack import cc_diff



####################################################################################################################
## Wrangle the data
####################################################################################################################

data_path2 = 'https://raw.githubusercontent.com/fpontejos/dataviz-dash/main/data/'
data_path = 'data/'

colors = ['#363537', '#fcfcfc', '#bee9e8', '#62b6cb', '#1b4965', '#ffef84', '#c3d37a', '#86b66f', '#0c7c59']


pct_data = pd.read_csv(data_path2 + 'renewables_percent_timeseries.csv')
pct_data = pct_data.sort_values(by='Country')

country_codes = [i for i in pct_data['Country Code'].unique()]
country_names = [i for i in pct_data['Country'].unique()]

ts_years = [str(i) for i in range(2004, 2021)]

percent_timeseries = pct_data.loc[pct_data['SIEC Code']=='RA000']\
                              .reset_index(drop=True)
percent_timeseries_tot = pct_data.loc[pct_data['SIEC Code']=='TOTAL']\
                                 .reset_index(drop=True)

for yi in ts_years:
    percent_timeseries[yi] = round((100*percent_timeseries[yi] / percent_timeseries_tot[yi]), 2)


rs_data = pd.read_csv(data_path + 'renewable_sources_2020.csv')
#print(rs_data.columns)
rs_country_names = [i for i in rs_data['Country'].unique()]

######################################################Functions##############################################################



######################################################Interactive Components############################################

dropdown_cc = dcc.Dropdown(
       id='cc_drop',
       options=rs_country_names,
       multi=False,
       value='Austria'
   )

slider_years = dcc.Slider(
       id='slider_years',
       value=2020,
       min=2004,
       max=2020,
       marks={str(i): '{}'.format(str(i)) for i in
              ts_years},
       step=5,
       tooltip={"placement": "top", "always_visible": True}
   )


######## 


##################################################APP###################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([


    html.Div([

    ########## Hero Row ##########

    html.Div([
        html.Div(className='hero-bg'),

        html.Div([
            html.H1('EU Renewable Energy Directive'),
            html.P("Some text here")
        ],className='hero-title is-marginless'),
        
    ], 
    className='row hero'),


     ########## First Row ##########
    html.Div([
        html.Div([
            html.H2(["Top Performing Countries: ",html.Span(id='title_top_year')]),
            html.Div([
                html.Div([], id='top_eu_1', className='col top_eu'),
                html.Div([], id='top_eu_2', className='col top_eu'),
                html.Div([], id='top_eu_3', className='col top_eu'),
                html.Div([], id='top_not_1', className='col top_eu'),
                html.Div([], id='top_not_2', className='col top_eu'),

            ],className='row top_eu_row'),
            html.Div([
                #html.Div([], id='top_not_1', className='col top_eu'),
                #html.Div([], id='top_not_2', className='col top_eu'),
                #html.Div([
                #    html.P("Some notes", className='small')
                #], className='col top_eu placeholder'),
            ],className='row')
            ],
            className='col top_perf_container'),
        html.Div([
            html.Div([
                html.P("Some text here anbout the sliders")
            ], className="notes"),
            ],
            className='col toprow_container'),
    ],
    className='row'),

     ########## Slider Row ##########

    html.Div([
        html.Div([slider_years],className='col holder'),
    ], className='row'),
        



    ########## Second Row ##########
    html.Div([
        html.Div([
            html.H3("Performance of All Countries: "),
            html.Div([
                dcc.Graph(id='top_bar', style={'width': '95%', 'margin': '0 auto'}),
                #html.Div([], id='top_bar', className='placeholder'),
            ],className='row'),
            ],
            className='col ranking_container'),
        html.Div([
            html.H3("Choropleth map? Or Scatter vs GDP"),
            ],
            className='col'),
    ],
    className='row'),


    ], className='card'),





    ########## Third Row ##########
    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Country Selector"),
                    html.Div([
                        dropdown_cc
                    ], id='country_selector'),
                ]),
                html.Div([
                    html.H3("Placeholder for Sunburst "),
                    html.Div([
                    
                    ], className='placeholder'),
                ]),
                ],
                className='col'),
            html.Div([
                html.H3(["Sources of Available Renewable Energy: ", html.Span(id='country_selection')]),
                html.Div([
                    html.Div([
                        html.Div([], id='wind_value', className='energy-value'),
                        html.Div([
                            "Wind"
                        ], className='energy-label'),
                    ], className='energy-source', id='energy_wind'),
                    html.Div([
                        html.Div([], id='solar_value', className='energy-value'),
                        html.Div(["Solar"], className='energy-label'),
                    ], className='energy-source', id='energy_solar'),
                    html.Div([
                        html.Div([], id='geotherm_value', className='energy-value'),
                        html.Div(["Geotherm"], className='energy-label'),
                    ], className='energy-source', id='energy_geotherm'),
                    html.Div([
                        html.Div([], id='bio_value', className='energy-value'),
                        html.Div(["Biomass"], className='energy-label'),
                    ], className='energy-source', id='energy_bio'),
                    html.Div([
                        html.Div([], id='hydro_value', className='energy-value'),
                        html.Div(["Hydro"], className='energy-label'),
                    ], className='energy-source', id='energy_hydro'),
                    html.Div([
                        html.Div([], id='other_value', className='energy-value'),
                        html.Div(["Other"], className='energy-label'),
                    ], className='energy-source', id='energy_other'),
                ],
                className='row', id='energy_source_container'),
                ],
                className='col ranking_container'),
            
        ],
        className='row'),

    ], className='card'),











], className='outer container')





######################################################Callbacks#########################################################

@app.callback(
    Output('country_selection', 'children'),
    Output('solar_value', 'children'),
    Input(dropdown_cc, 'value')
)
def getSelectedCountry(country):
    
    a = rs_data.loc[(rs_data['Country']==country)&(rs_data['SIEC Code']=='RA200'),'Consumption in KTOE']
    return [country,
            a]


@app.callback(
    Output('title_top_year', 'children'),
    Output('top_eu_1', 'children'),
    Output('top_eu_2', 'children'),
    Output('top_eu_3', 'children'),
    Output('top_not_1', 'children'),
    Output('top_not_2', 'children'),
    Output('top_bar', 'figure'),
    Input('slider_years', 'value'),
    
)
def getTopPerforming(year_value):

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

    fig_bar = go.Figure()
    sorted_bar = percent_timeseries.loc[:,['Country', str(year_value)]].sort_values(by=str(year_value), ascending=False)

    fig_bar.add_trace(dict(type='bar',
                     x=sorted_bar['Country'],
                     y=sorted_bar[str(year_value)],
                     name=str(year_value),
                     showlegend=False,
                     visible=True,
                     marker_color=colors[4],
                    )
               )
#
    fig_bar.update_layout(dict(title=dict(text='Percentage of consumption using renewables', x=.5),
                    yaxis=dict(range=[0,100]),
                    paper_bgcolor=colors[1],
                    plot_bgcolor='#e9f6f6',
                    margin=dict(r=10, t=50, l=10)

                  ))
    fig_bar.update_xaxes(tickangle=270)

    fig_bar.add_annotation(text="Year "+str(year_value),
                  xref="paper", yref="paper",
                  x=.99, y=.99, showarrow=False, 
                  font=dict(
                    color=colors[4],
                    size=20
                ))


    return [
        year_value, 
        top_res_return[0], 
        top_res_return[1], 
        top_res_return[2], 
        top_res_return[3], 
        top_res_return[4],
        #go.Figure(data=data_bar, layout=layout_bar)
        fig_bar
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
