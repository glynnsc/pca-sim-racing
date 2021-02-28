import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import plotly.express as px
import pandas as pd
import awswrangler as wr
import calplot

#######
# sel = "select * from sensorlog_sumstats_view"
# stats_df = wr.athena.read_sql_query(sel, database="telemetry", ctas_approach=False)

###
sel = "select * from sensorlog_sumstats_view"
stats_df = wr.athena.read_sql_query(sel, database="telemetry", ctas_approach=False)

stats_df.rename(columns = {'log_time':'Date'}, inplace = True)
stats_df['Date'] = pd.to_datetime(stats_df['Date'], format='%Y-%m-%d')

def createCalendarDataFrame(start='2000-01-01', end='2050-12-31'):
    date_df = pd.DataFrame({"Date": pd.date_range(start, end)})
    date_df["Year"] = date_df.Date.dt.year
    date_df["Month"] = date_df.Date.dt.month_name()
    date_df["Week"] = date_df.Date.dt.isocalendar().week
    date_df["Day"] = date_df.Date.dt.day_name()
    return date_df
    
calendar_df = createCalendarDataFrame(start='2020-01-01', end='2020-12-31')
stint_calendar_df = pd.merge(calendar_df,stats_df, how="outer", on=["Date"])
stint_calendar_series = pd.Series(stint_calendar_df['miles'].values,index=stint_calendar_df['Date'])


#######
# this needs to be rebuilt using dash_table.DataTable
def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
#PLOTLY_LOGO = "http://pngimg.com/uploads/octopus/octopus_PNG31.png"

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.2/css/bootstrap.min.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

#### Overall Stats for Cards
duration_total = stats_df['duration'].sum()
duration_average = stats_df['duration'].mean().round(0)
distance_total = stats_df['miles'].sum().round(0)
distance_average = stats_df['miles'].mean().round(0)
climb_total = stats_df['climb_feet'].sum()
climb_average = stats_df['climb_feet'].mean().round(0)
average_speed = stats_df['miles_per_hour'].mean().round(0)
maximum_speed = stats_df['miles_per_hour'].max()
#### Figures
#calendar_fig = calplot.calplot(stint_calendar_series)

speed_fig = px.bar(stats_df, x='Date',y='miles_per_hour',
                    barmode='group',height=200
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        )
                        
duration_fig = px.bar(stats_df, x='Date',y='duration',
                    barmode='group',height=200
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        )
                        
distance_fig = px.bar(stats_df, x='Date',y='miles',
                    barmode='group',height=200
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        )


#### Construct Card Content
distance_card = [
    dbc.CardHeader("Distance"),
    dbc.CardBody(
        [
            html.H5("Total: "+ str(distance_total) + " Miles", className="card-title"),
            html.H5("Average: "+ str(distance_average) + " Miles", className="card-title"),
        ]
    ),
]

duration_card = [
    dbc.CardHeader("Duration"),
    dbc.CardBody(
        [
            html.H5("Total: " + str(duration_total) + " Minutes", className="card-title"),
            html.H5("Average: "+ str(duration_average) + " Minutes", className="card-title"),
        ]
    ),
]

climb_card = [
    dbc.CardHeader("Climb"),
    dbc.CardBody(
        [
            html.H5("Total: " + str(climb_total) + " Feet", className="card-title"),
            html.H5("Average: " + str(climb_average) + " Feet", className="card-title"),
        ]
    ),
]

speed_card = [
    dbc.CardHeader("Speed"),
    dbc.CardBody(
        [
            html.H5("Max: " + str(maximum_speed) + " MPH", className="card-title"),
            html.H5("Average: " + str(average_speed) + " MPH", className="card-title"),
        ]
    ),
]

speed_card_fig = [
    dbc.CardBody(
            [
                dcc.Graph(
                    id='speed_card_fig_id',
                    figure=speed_fig
                )
            ]
        )
    ]

duration_card_fig = [
    dbc.CardBody(
            [
                dcc.Graph(
                    id='duration_card_fig_id',
                    figure=duration_fig
                )
            ]
        )
    ]

distance_card_fig = [
    dbc.CardBody(
            [
                dcc.Graph(
                    id='distance_card_fig_id',
                    figure=distance_fig
                )
            ]
        )
    ]

#### Construct the Row of KPI cards
row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(distance_card, color="dark", inverse=True)),
        dbc.Col(dbc.Card(duration_card, color="dark", inverse=True)),
        dbc.Col(dbc.Card(speed_card, color="dark", inverse=True)),
        dbc.Col(dbc.Card(climb_card, color="dark", inverse=True)),
    ],
    className="mb-4",
)
row_2 = dbc.Row(
    [
        dbc.Col(dbc.Card(distance_card_fig, color="dark")),
        dbc.Col(dbc.Card(speed_card_fig, color="dark", inverse=True)),
        #dbc.Col(dbc.Card(duration_card_fig, color="dark")),
        
    ],
    className="mb-4",
)

#### Construct cards for graphs
#### also look at plotly indicators

####
app.layout = html.Div(children=[
    html.Nav(children='BillyGoat',style={'backgroundColor':'#4a494a'}),
    html.Hr(),
    html.Div([row_1]),
    html.Br(),
    html.Div([row_2]),
    html.Div([
        dcc.Graph(
            id='speed-graph',
            figure=speed_fig
           ),
            
        dcc.Graph(
            id='duration-graph',
            figure=duration_fig
        )],
        style={'width':'49%', 'height':'100px','float':'left', 'display':'inline-block'}
    ),
   generate_table(stats_df)
])
    
if __name__ == '__main__':
    app.run_server(debug=True)
