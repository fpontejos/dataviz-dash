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
    'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap',
    'https://fonts.googleapis.com/css2?family=Roboto:wght@400;900&display=swap',
    'https://fonts.googleapis.com/css2?family=Overlock:wght@900&display=swap'
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

country_names = sorted([i for i in pct_data['Country'].unique()])

ts_years = [str(i) for i in range(2004, 2021)]

percent_timeseries = pct_data.loc[pct_data['SIEC Code']=='RA000']\
                              .reset_index(drop=True)
percent_timeseries_tot = pct_data.loc[pct_data['SIEC Code']=='TOTAL']\
                                 .reset_index(drop=True)


gdp_data = pd.read_csv(data_path2 + 'gdp_data.csv')
gdp_data.loc[gdp_data['Country']=='Czechia','Country'] = 'Czech Republic'

for yi in ts_years:
    percent_timeseries[yi] = round((100*percent_timeseries[yi] / percent_timeseries_tot[yi]), 2)


rs_data = pd.read_csv(data_path2 + 'renewable_sources_2020.csv')
rs_data.loc[rs_data['Country']=='Czechia','Country'] = 'Czech Republic'

#print(rs_data.columns)
rs_data.replace(np.nan, '', inplace=True)
rs_country_names = country_names #[i for i in rs_data['Country'].unique()]

######################################################Functions##############################################################


def get_color_bins(color):
    
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
app.title = "Renewables on the Rise: a Look at Energy Sources in Europe"
app._favicon = ('logo-preto.png')

server = app.server


app.layout = html.Div([


    html.Div([

    ########## Hero Row ##########

    html.Div([
        html.Div(className='hero-bg'),

        html.Div([
            html.Div([
                html.H1(['Renewables on the Rise:', html.Br(), 'a Look at Energy Sources in Europe']),
                html.P(["""In light of the current geopolitical issues and long term social 
                        and environmental trends affecting our generation, 
                        we wanted to focus on the topic of the current state and direction 
                        of the European energy mix. """]),
                html.P([ "We wanted to answer the question: ",
                        html.Em("How much of Europe’s energy comes from renewable sources?")])
            ],className='hero-title is-marginless'),

        ], className='col-8'),
        html.Div([

        ], className='col'),

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
                html.P("""
                The EU has established a Renewable Energy Directive, 
                which is a policy promoting the use of renewable energy sources among EU countries. 
                In particular, it set a target of having 20% of its energy needs to be sourced from renewable energy 
                by the year 2020. 
                """),
                html.P(html.Em("Which countries have met this goal?")),
                html.P("The year can be changed using the slider below."),
                html.Div([
                    dcc.Graph(id='top_bar'),
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
                    html.H4("Distribution of All Sources of Energy (2020)"),
                    html.P(html.Em("What are the different energy sources being used?")),

                    html.Div([
                        dcc.Graph(id='sunburst_sources', style={'width': '95%', 'margin': '0 auto'}),

                    ], className='sunburst_container'
                    ),
                ]),
                ],
                className='col-6'),
            html.Div([
                html.Div([
                        html.H4(["GDP Per Capita and Percentage of Energy From Renewables: ", html.Br(), html.Span(id='country_selection')]),
                        html.P(html.Em("Do countries with higher GDP per capita have a higher percentage of renewables used?")),
                        dcc.Graph(id='gdp_pct_ts', style={'margin': '0'}),
                        

                        html.H4(["Percentage of Energy From Renewables Over Time: ", html.Span(id='country_selection2')]),
                        html.P(html.Em("Are European countries moving towards increased renewables use?")),
                        dcc.Graph(id='pct_ts', style={'margin': '0'}),
                        

                ], ),
                ],
                className='col ranking_container'),


        ],
        className='row'),

    ], className='card'),

    ################### References ###################
    html.Div([
        html.Div([
            html.Div([
                html.H5("NOVA IMS"),
                html.Ul(
                    [
                    html.Li(["Miriam Hadidi Pereira ", html.Em("20210644")]),
                    html.Li(["Beatriz Peres ", html.Em("20210910")]),
                    html.Li(["Farina Pontejos ", html.Em("20210649")]),

                    ]
                )
            ], className='col-4 authors'),

            html.Div([
                html.H5("Data Sources"),
                html.Ul(
                    [
                    html.Li(["Calculation of overall target - details. (2022, February 1). Retrieved April 4, 2022, from ",
                            html.A("https://ec.europa.eu/eurostat/web/products-datasets/-/nrg_ind_cotd", href="https://ec.europa.eu/eurostat/web/products-datasets/-/nrg_ind_cotd")]),
                    html.Li(["Energy flow - Sankey diagram data. (2022, January 3). Retrieved April 4, 2022, from ", 
                            html.A("https://ec.europa.eu/eurostat/web/products-datasets/-/nrg_bal_sd", href="https://ec.europa.eu/eurostat/web/products-datasets/-/nrg_bal_sd", )]),
                    html.Li(["GDP and main components (output, expenditure and income). (2022, April 12). Retrieved April 12, 2022, from ",
                            html.A("https://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp", href="https://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp" )]),
                    ]),
                html.H5("Assets Used"),
                html.Ul([
                    html.Li([html.A("Europe GeoJSON", href="https://github.com/leakyMirror/map-of-europe" )]),
                    html.Li([html.A("Vector illustration", href="https://www.freepik.com/free-vector/landing-page-web-template-ecological-company_5083829.htm" )]),

                    ]
                )
            ], className='col sources')
        ], className='row'),    
    ], className='card'),











], className='outer container')





######################################################Callbacks#########################################################



@app.callback(
    Output('country_selection', 'children'),
    Output('country_selection2', 'children'),
    Output('sunburst_sources', 'figure'),
    Output('gdp_pct_ts', 'figure'),
    Output('pct_ts', 'figure'),

    Input(dropdown_cc, 'value')
)
def getSelectedCountry(country):
    so_ = rs_data.loc[(rs_data['Country']==country) &( rs_data['Sunburst_Parent']=='Other Renewable')].sum()['Consumption in KTOE']
    
    s_ = rs_data.loc[(rs_data['Country']==country),['Sunburst_SIEC','Sunburst_Parent','Consumption in KTOE', 'Renewable']]

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

    sun_layout = go.Layout(
        #height=300,
        paper_bgcolor=colors[1],
        )

    fig_sun = go.Figure(
        go.Sunburst(
            labels=s_labels,
            parents=s_parents,
            values=s_values,
            branchvalues="total",
            insidetextorientation='radial',
            marker=dict(colors=sun_colors)
        ),
        layout=sun_layout
    )
    fig_sun.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    ###################### GDP vs PCT ######################

    gdp_layout = go.Layout(
        height=300,
        paper_bgcolor=colors[1],
        plot_bgcolor='#eef6f6',
        )
    #Add traces
    fig_gdp = go.Figure(layout=gdp_layout)

    pct_ts_layout = go.Layout(
        height=300,
        paper_bgcolor=colors[1],
        plot_bgcolor='#eef6f6',
        yaxis_title="Percentage Renewables",
        xaxis =  {'showgrid': False},
        yaxis = {'showgrid': False}
        )
    
    fig_pct_ts = go.Figure(layout=pct_ts_layout)

    ###################### Add Traces ######################


    for c_ in country_names:
        gdp_x = gdp_data.loc[gdp_data['Country']==c_, ts_years].T.iloc[:,0]
        gdp_y = percent_timeseries.loc[percent_timeseries['Country']==c_, ['2020']].T.iloc[:,0]
        pct_y = percent_timeseries.loc[percent_timeseries['Country']==c_, ts_years].T.iloc[:,0]
        if c_ != country:
            fig_gdp.add_trace(go.Scatter(x=gdp_x, y=gdp_y,
                    #text=ts_years,
                    mode='markers',
                    name=c_,
                    opacity=.25,
                    marker=dict(color='#333333')
                    #visible='legendonly'
                    ))
            fig_gdp.update_traces(showlegend=False)

            fig_pct_ts.add_trace(go.Scatter(
                x=ts_years,
                y=pct_y, 
                mode='lines',
                name=c_,
                    opacity=.05,
                    marker=dict(color='#575757')
            ))
            fig_pct_ts.update_traces(showlegend=False)


        if c_ == country:
            fig_gdp.add_trace(go.Scatter(x=gdp_x, y=gdp_y,
                    text=[c_],
                    mode='lines+markers+text',
                    name=c_,
                    marker=dict(color='#0c7c59'),
                    textposition="middle right"

                    #marker=dict(color=sun_colors[0])

                    ))
            fig_pct_ts.add_trace(go.Scatter(
                x=ts_years,
                y=pct_y, 
                mode='lines',
                name=c_,
                marker=dict(color='#0c7c59'),
            ))



    fig_gdp.update_layout(
        xaxis_title="GDP Per Capita in Euros",
        yaxis_title="Percentage Renewables",
        
    )

    fig_gdp.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig_gdp.update_yaxes(range=[0,100])

    fig_pct_ts.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig_pct_ts.update_yaxes(range=[0,100])

    ###################### PCT Time Series ######################

    


    return [country, country, fig_sun, fig_gdp, fig_pct_ts]


@app.callback(
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
                    plot_bgcolor='#eef6f6',
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
                  mapbox_zoom=2.5, mapbox_center = {"lat": 53, "lon": 5}, paper_bgcolor=colors[1])
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_traces(hovertemplate="%{location}: %{customdata}")




    return [
        fig_bar,
        fig_map
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
