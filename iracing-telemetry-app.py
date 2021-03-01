from telemetry import iracing_methods as helpers
import awswrangler as wr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_html_components as html

#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
#PLOTLY_LOGO = "http://pngimg.com/uploads/octopus/octopus_PNG31.png"
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.2/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

#### Overall Stats for Cards
total_stats = helpers.getTelemetrySummaryStatsTotals()
total_cars = total_stats['total'][total_stats['category']=='cars'].values[0]
total_tracks = total_stats['total'][total_stats['category']=='tracks'].values[0]
total_days = total_stats['total'][total_stats['category']=='days'].values[0]
total_sessions = total_stats['total'][total_stats['category']=='sessionstarts'].values[0]
total_hours = total_stats['total'][total_stats['category']=='seat_time'].values[0]
total_laps = total_stats['total'][total_stats['category']=='laps'].values[0]
total_incidents = 337 # get this when the total_stats query is refactored

trackcarlap_stats = helpers.getTrackCarLapSummaryStats()
trackcarlap_stats.rename(columns={
    "sesssion__track": "Track", "session__car": "Car",
    "minlap": "Min","avglap": "Average",
    "maxlap": "Max","stdevlap": "Variance","covlap": "Consistency"
    },inplace=True)
trackcarlap_stats = trackcarlap_stats.round({'Min': 4, 'Average': 4, 
'Max': 4, 'Variance': 4, 'Consistency': 4})

lapcount_by_date = helpers.getLapCountbyDate()
lapcount_fig = px.bar(lapcount_by_date, x='session__date', y='Lap_Count', title='Lap Activity')


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

laps_card = [
    dbc.CardHeader("Laps"),
    dbc.CardBody(
        [
            html.H5(str(total_laps), className="card-title"),
        ]
    ),
]

activity_card = [
    dbc.CardHeader("Activity"),
    dbc.CardBody(
        [
            html.H5("Days: " + str(total_days) +
            "  Sessions: " + str(total_sessions),
            className="card-title"),
            ]
    ),
]

hours_card = [
    dbc.CardHeader("Seat Time"),
    dbc.CardBody(
        [
            html.H5(str(round(total_hours/60,2)), className="card-title"),
        ]
    ),
]

incidents_card = [
    dbc.CardHeader("Incidents"),
    dbc.CardBody(
        [
            html.H5(str(total_incidents), className="card-title"),
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
         dbc.Col(dbc.Card(tracks_card, color="dark", inverse=True)),
         dbc.Col(dbc.Card(laps_card, color="dark", inverse=True))
     ],
     className="mb-4",
)

row_2 = dbc.Row(
     [
         dbc.Col(dbc.Card(activity_card, color="dark",inverse=True)),
         dbc.Col(dbc.Card(hours_card, color="dark", inverse=True)),
         dbc.Col(dbc.Card(incidents_card, color="dark", inverse=True))
        
     ],
     className="mb-4",
 )

#### Layout the dashboard
app.layout = html.Div(children=[
    html.Nav(children='SimRacing',style={'height': '50px', 'backgroundColor':'#483D8B'}),
    html.Hr(),
    html.Div([row_1]),
    html.Br(),
    html.Div([row_2]),
    html.Div([
        dcc.Graph(figure=lapcount_fig)
        ]),
    html.Div([
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in trackcarlap_stats.columns],
    data=trackcarlap_stats.to_dict('records'),
    style_cell=dict(textAlign='left'),
    style_header=dict(backgroundColor="paleturquoise"),
    )])
    ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
