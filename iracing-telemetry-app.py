
#import sys
#sys.path.append("./telemetry")
from telemetry import iracing_methods as helpers
# import iracing_methods
import awswrangler as wr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_html_components as html
#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
#PLOTLY_LOGO = "http://pngimg.com/uploads/octopus/octopus_PNG31.png"

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.2/css/bootstrap.min.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# def getTelemetrySummaryStatsTotals():
#     sel = "select * from telemetry_summary_stats_totals"
#     df = wr.athena.read_sql_query(sel, database='iracing', ctas_approach=False)
    
#     return df

#### Overall Stats for Cards
total_stats = helpers.getTelemetrySummaryStatsTotals()

total_cars = total_stats['total'][total_stats['category']=='cars'].values[0]
total_tracks = total_stats['total'][total_stats['category']=='tracks'].values[0]
total_days = total_stats['total'][total_stats['category']=='days'].values[0]
total_laps = total_stats['total'][total_stats['category']=='laps'].values[0]
total_hours = total_stats['total'][total_stats['category']=='seat_time'].values[0]     

cars_card = [
    dbc.CardHeader("Cars"),
    dbc.CardBody(
        [
            html.H5(str(total_cars), className="card-title"),
        ]
    ),
]

tracks_card = [
    dbc.CardHeader("Tracks"),
    dbc.CardBody(
        [
            html.H5(str(total_tracks), className="card-title"),
        ]
    ),
]


# activity_trend_fig = px.bar(stats_df, x='Date',y='miles_per_hour',
#                     barmode='group',height=200
#                     ).update_layout(
#                         template='plotly_dark',
#                         plot_bgcolor= 'rgba(0, 0, 0, 0)',
#                         paper_bgcolor= 'rgba(0, 0, 0, 0)',
#                         )
                        



#### Construct the Row of KPI cards
row_1 = dbc.Row(
     [
         dbc.Col(dbc.Card(cars_card, color="dark", inverse=True)),
         dbc.Col(dbc.Card(tracks_card, color="dark", inverse=True))
#         dbc.Col(dbc.Card(speed_card, color="dark", inverse=True)),
#         dbc.Col(dbc.Card(climb_card, color="dark", inverse=True)),
     ],
     className="mb-4",
)
# row_2 = dbc.Row(
#     [
#         dbc.Col(dbc.Card(distance_card_fig, color="dark")),
#         dbc.Col(dbc.Card(speed_card_fig, color="dark", inverse=True)),
#         #dbc.Col(dbc.Card(duration_card_fig, color="dark")),
        
#     ],
#     className="mb-4",
# )

#### Construct cards for graphs
#### also look at plotly indicators

####
app.layout = html.Div(children=[
    html.Nav(children='SimRacing',style={'backgroundColor':'#4a494a'}),
    html.Hr(),
    html.Div([row_1]),
    html.Br(),
#     html.Div([row_2]),
#     html.Div([
#         dcc.Graph(
#             id='speed-graph',
#             figure=speed_fig
#           ),
            
#         dcc.Graph(
#             id='duration-graph',
#             figure=duration_fig
#         )],
#         style={'width':'49%', 'height':'100px','float':'left', 'display':'inline-block'}
#     ),
#   generate_table(stats_df)
])
    
if __name__ == '__main__':
    app.run_server(debug=True)

#### Construct Dahsboard Cards 
# cars_card = [
#     dbc.CardHeader("Cars"),
#     dbc.CardBody(
#         [
#             html.H5("Total: "+ str(distance_total) + " Miles", className="card-title"),
#             html.H5("Average: "+ str(distance_average) + " Miles", className="card-title"),
#         ]
#     ),
# ]

# duration_card = [
#     dbc.CardHeader("Tracks"),
#     dbc.CardBody(
#         [
#             html.H5("Total: " + str(duration_total) + " Minutes", className="card-title"),
#             html.H5("Average: "+ str(duration_average) + " Minutes", className="card-title"),
#         ]
#     ),
# ]


# putting fig in a card
# speed_card_fig = [
#     dbc.CardBody(
#             [
#                 dcc.Graph(
#                     id='speed_card_fig_id',
#                     figure=speed_fig
#                 )
#             ]
#         )
#     ]
