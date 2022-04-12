import dash
from dash import dash_table, html, dcc

#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd
import plotly.graph_objs as go


import urllib.request as urllib
import json



external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap',
    'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap'
]
####################################################################################################################
## Wrangle the data
####################################################################################################################

data_path = 'https://raw.githubusercontent.com/fpontejos/dataviz-dash/main/data/'
data_path2 = 'data/'

colors = ['#363537', '#fcfcfc', '#bee9e8', '#62b6cb', '#1b4965', '#ffef84', '#c3d37a', '#86b66f', '#0c7c59']

sun_colors = ['#1b4965', '#D4D6B9', '#4F486B', '#824670', '#6C6293', '#32213A', '#c3d37a', '#86b66f', '#0c7c59', '#D4D6B9', '#EEC643']

pct_data = pd.read_csv(data_path2 + 'renewables_percent_timeseries.csv')
pct_data = pct_data.sort_values(by='Country')

pct_data.loc[pct_data['Country']=='Czechia','Country'] = 'Czech Republic'

response = urllib.urlopen(data_path + "europe.geojson")
europe_json = json.loads(response.read())

country_codes = [i for i in pct_data['Country Code'].unique()]
country_names = [i for i in pct_data['Country'].unique()]

ts_years = [str(i) for i in range(2004, 2021)]

percent_timeseries = pct_data.loc[pct_data['SIEC Code']=='RA000']\
                              .reset_index(drop=True)
percent_timeseries_tot = pct_data.loc[pct_data['SIEC Code']=='TOTAL']\
                                 .reset_index(drop=True)

for yi in ts_years:
    percent_timeseries[yi] = round((100*percent_timeseries[yi] / percent_timeseries_tot[yi]), 2)


rs_data = pd.read_csv(data_path2 + 'renewable_sources_2020.csv')
#print(rs_data.columns)
rs_data.replace(np.nan, '', inplace=True)
rs_country_names = [i for i in rs_data['Country'].unique()]

######################################################Functions##############################################################


def get_color_bins(color):
    cmap = cm.get_cmap('viridis')
    if color > 80 :
        return 80
    elif color > 60 :
        return 60
    elif color > 40 :
        return 40
    elif color > 20 :
        return 20
    else:
        return 0
    
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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.config.serve_locally = True

server = app.server


app.layout = html.Div([


    html.Div([

    ########## Hero Row ##########

    html.Div([
        html.Div(className='hero-bg'),

        html.Div([
            html.H1('Sources of Energy in European Countries'),
            html.P("Where does it come from and where is it going?")
        ],className='hero-title is-marginless'),

    ],
    className='row hero'),


     ########## First Row ##########

    html.Div([

            html.Div([
                html.H3("Energy consumption"),
                html.P("Percentage of energy consumed derived from renewable sources."),
                dcc.Graph(id='eu_choro')
            ], className='col choro_container'),

            html.Div([

            html.Div([
                #html.H3("Countries' Performance"),
                html.Br(),
                html.P("Performance of each country over time. Year can be changed using the slider below."),
                html.Div([
                    dcc.Graph(id='top_bar', style={'width': '95%', 'margin': '0 auto'}),
                    #html.Div([], id='top_bar', className='placeholder'),
                ],className='row'),
                ],
            className='ranking_container'),


            ], className='col top_container'),



        ], className='row'),

            ########## Slider Row ##########

    html.Div([
        html.Div([slider_years],className='col holder'),
    ], className='row'),



    html.Div([

        html.Div([
            html.H2(["Top 5 Countries: xx",html.Span(id='title_top_year')]),
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


    ],
    className='row'),


    ########## Second Row ##########
    html.Div([


        html.Div([
            html.Div([
                html.P("Some text here about the sliders")
            ], className="notes"),
            ],
            className='col toprow_container'),

    ],
    className='row'),




    ], className='card'),





    ########## Third Row ##########
    html.Div([

        html.Div([
            html.Div([
                html.Div([
                        html.Div([
                            html.H3("Country Profile: ")
                            ], className="country_profile_label"),
                        html.Div([
                            dropdown_cc
                        ], id='country_selector', className="country_profile_selector"),
                    ], className="country_profile_title"),

            ], className='col-7'),
            html.Div(className='col'),
        ], className="row"),

        html.Div([
            html.Div([
                
                html.Div([
                    html.H4("Distribution of All Sources of Energy "),
                    html.Div([
                        dcc.Graph(id='sunburst_sources', style={'width': '95%', 'margin': '0 auto'}),

                    ], className='sunburst_container'
                    ),
                ]),
                ],
                className='col-7'),
            html.Div([
                html.H4(["Available Renewable Energy Sources in 2020: (KTOE) ", html.Span(id='country_selection')]),
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
    #Output('country_selection', 'children'),
    Output('solar_value', 'children'),
    Output('wind_value', 'children'),
    Output('hydro_value', 'children'),
    Output('geotherm_value', 'children'),
    Output('bio_value', 'children'),
    Output('other_value', 'children'),

    Output('sunburst_sources', 'figure'),
    Input(dropdown_cc, 'value')
)
def getSelectedCountry(country):
    so_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Other Renewable')].sum()['Consumption in KTOE']
    sb_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Biomass')].sum()['Consumption in KTOE']
    sh_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Hydro')].sum()['Consumption in KTOE']
    sg_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Geothermal')].sum()['Consumption in KTOE']
    sw_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Wind')].sum()['Consumption in KTOE']
    ss_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Solar')].sum()['Consumption in KTOE']
    
    s_ = rs_data.loc[(rs_data['Country']==country),['Sunburst_SIEC','Sunburst_Parent','Consumption in KTOE']]

    s_labels = np.append(s_['Sunburst_Parent'].unique(), s_['Sunburst_SIEC'].values)
    s_parents = np.append([ '' for _ in range(len(s_['Sunburst_Parent'].unique()))], s_['Sunburst_Parent'].values)
    s_values = np.append([s_.loc[s_['Sunburst_Parent'] == _ ]['Consumption in KTOE'].sum() for _ in s_['Sunburst_Parent'].unique()] ,
               s_['Consumption in KTOE'])



    s_ = rs_data.loc[(rs_data['Country']==country),['Sunburst_SIEC','Sunburst_Parent','Consumption in KTOE', 'Renewable']]
    #print(s_['Renewable'].unique())

    gparent = pd.DataFrame(s_.groupby(['Sunburst_Parent', 'Renewable']).size()).reset_index().drop(columns=[0])


    s_labels = s_['Renewable'].unique().tolist() + \
                            s_['Sunburst_Parent'].unique().tolist() + \
                            s_['Sunburst_SIEC'].values.tolist()

    s_parents = ['', ''] + \
                        [ gparent.loc[gparent['Sunburst_Parent']==_, 'Renewable'].values[0] for _ in (s_['Sunburst_Parent'].unique()) ] + \
                        s_['Sunburst_Parent'].values.tolist()


    s_values = [s_.loc[s_['Renewable'] == _ ]['Consumption in KTOE'].sum() for _ in s_['Renewable'].unique()] + \
                [s_.loc[s_['Sunburst_Parent'] == _ ]['Consumption in KTOE'].sum() for _ in s_['Sunburst_Parent'].unique()] + \
                s_['Consumption in KTOE'].tolist()


    fig_sun = go.Figure(
        go.Sunburst(
            labels=s_labels,
            parents=s_parents,
            values=s_values,
            branchvalues="total",
            insidetextorientation='radial',
            marker=dict(colors=sun_colors)

        )
    )
    fig_sun.update_layout(margin = dict(t=0, l=0, r=0, b=0))



    #fig_gdp = go.Figure()

    # Add traces
    #fig_gdp.add_trace(go.Scatter(x=random_x, y=random_y0,
    #                mode='markers',
    #                name='markers'))

    return [ #country,
            round(ss_),
            round(sw_),
            round(sh_),
            round(sg_),
            round(sb_),
            round(so_),
            fig_sun
            ]


@app.callback(
    Output('title_top_year', 'children'),
    Output('top_eu_1', 'children'),
    Output('top_eu_2', 'children'),
    Output('top_eu_3', 'children'),
    Output('top_not_1', 'children'),
    Output('top_not_2', 'children'),
    Output('top_bar', 'figure'),
    Output('eu_choro', 'figure'),
    Input('slider_years', 'value'),

)
def getTopPerforming(year_value):

    perf_by_year = percent_timeseries.loc[:,['Country', str(year_value), 'Country Code']].sort_values(by=str(year_value), ascending=False).reset_index(drop=True)
    df_ = percent_timeseries.loc[:,['Country', str(year_value)]]

    top_res_return = []

    for ti in range(5):
        f_ = "url('assets/flags/" + str.lower(perf_by_year.iloc[ti,2]) + ".svg')"
        top_res_return.append([
            html.Div([
                html.Div(className='country_flag', id="top_flag_"+perf_by_year.iloc[ti,2],
                        style={"background-image": f_}
                ),
                html.P(perf_by_year.iloc[ti,0]),
                html.P(str(perf_by_year.iloc[ti,1])+" %")
            ], className='top_perf'
            )
            ])

    fig_bar = go.Figure()
    sorted_bar = df_.sort_values(by=str(year_value), ascending=False)

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
    fig_bar.update_layout(dict(
                    yaxis=dict(range=[0,100]),
                    paper_bgcolor=colors[1],
                    plot_bgcolor='#e9f6f6',
                    margin=dict(r=10, t=0, l=10)

                  ))
    fig_bar.update_xaxes(tickangle=270)

    fig_bar.add_annotation(text="Year "+str(year_value),
                  xref="paper", yref="paper",
                  x=.99, y=.99, showarrow=False,
                  font=dict(
                    color=colors[4],
                    size=20
                ))

    ########################### Choropleth ###########################
    fig_map = go.Figure(go.Choroplethmapbox(geojson=europe_json,
                    locations=df_['Country'], z=df_[str(year_value)].apply(lambda x: get_color_bins(x)),
                    colorscale="Viridis", 
                    zmin=0, zmax=100,
                    customdata=df_[str(year_value)],
                    name='Percent From Renewables',
                    marker_opacity=0.5, marker_line_width=0,
                    featureidkey="properties.NAME"))
    fig_map.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=2.5, mapbox_center = {"lat": 53, "lon": 5})
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_traces(hovertemplate="%{location}: %{customdata}")




    return [
        year_value,
        top_res_return[0],
        top_res_return[1],
        top_res_return[2],
        top_res_return[3],
        top_res_return[4],
        #go.Figure(data=data_bar, layout=layout_bar)
        fig_bar,
        fig_map
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
