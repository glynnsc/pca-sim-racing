"""
methods
"""

import awswrangler as wr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def getTelemetrySummaryStatsTotals():
    sel = "select * from telemetry_summary_stats_totals"
    df = wr.athena.read_sql_query(sel, database='iracing', ctas_approach=False)
    
    return df


def getiRacingTelemetryData(session_track, session_car, session_date):
    sel = "select lap, lapdist, lapdistpct, \
    lapcurrentlaptime, lapdeltatobestlap,lapdeltatooptimallap,\
    lapdeltatosessionbestlap, lapdeltatosessionoptimallap,\
    lapdeltatooptimallap_dd, lapdeltatosessionoptimallap_dd,\
    lat, lon, speed,  \
    gear, throttle, brake, rpm, steeringwheelangle, \
    round(atan2(velocityy,abs(velocityx))*100,2) as slip_angle, \
    yaw, pitch, roll, velocityx, velocityy, velocityz, vertaccel, lataccel, longaccel \
    from telemetry_raw \
    where sesssion__track = '" + session_track + "' and\
    session__car = '" + session_car + "' and\
    session__date = '" + session_date + "'"
    
    df = wr.athena.read_sql_query(sel, database='iracing', ctas_approach=False)
    
    return df

def getModalityStdDev(session_telemtry_dataframe, modality, round_decimals = 0):
    # method assumes standard telemetry raw features from iRacing
    # and that lapdist is the feature name to groupby
    
    # get unique lapdist and modality
    mod_df = pd.DataFrame({'lapdist':session_telemtry_dataframe['lapdist'].round(),
                             'modality':session_telemtry_dataframe[modality]})
    mod_df_sort = mod_df.sort_values(by=['lapdist'])
    mod_df_sort = mod_df_sort.drop_duplicates()
    # print(mod_df_sort.head())
    
    mod_df_sort['avg'] = mod_df_sort.groupby(['lapdist']).modality.transform(np.mean)
    mod_df_sort['std'] = mod_df_sort.groupby(['lapdist']).modality.transform('std')
    mod_df_sort = mod_df_sort.round(round_decimals)
    # print(mod_df_sort.head())
    mod_df_sort = mod_df_sort[{'lapdist','avg','std'}].drop_duplicates()
    # print(mod_df_sort.head())
    
    return mod_df_sort

def getSessionVarianceTraceFromTelemetryDataFrame(df, modality, round_decimals=0):
  ######## 
  ######## this is applied for summarizing telemetry_dataframe 
  ########
    modality_df = getModalityStdDev(df,modality,round_decimals)
    yupper = modality_df['avg'] + modality_df['std']
    ylower = modality_df['avg'] - modality_df['std']
    
    upper_trace = go.Scatter(
            name= 'Upper',
            x = modality_df['lapdist'],
            y = yupper,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        )
        
    lower_trace = go.Scatter(
            name='Lower Bound',
            x=modality_df['lapdist'],
            y=ylower,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        )
    
    return [upper_trace, lower_trace]


def getBestLap(session_telemetry):
    laptimes = session_telemetry.groupby('lap').agg({'lapcurrentlaptime' : ['max'], 'lapdist' : ['max']})
    laptimes.drop([0],inplace=True)
    laptimes.columns = ['laptime', 'lapdist']
    laptimes = laptimes.reset_index()
    lapdist = laptimes.agg({'lapdist' : [np.mean, 'std']})
    lapdist_threshold = {'lower': lapdist.lapdist['mean'] - lapdist.lapdist['std'], 
                         'upper': lapdist.lapdist['mean'] + lapdist.lapdist['std']}
    laptimes2 = laptimes[(laptimes['lapdist']>=lapdist_threshold['lower']) & 
                        (laptimes['lapdist']<=lapdist_threshold['upper'])]
    bestlap = laptimes2[laptimes2.laptime==laptimes2.laptime.min()]
    return bestlap

def getiRacingTelemetryLapdistAvgStd(session_track, session_car, session_date):
    sel = "select * from telemetry_lapdist_avg_stdev \
    where sesssion__track = '" + session_track + "' and \
    session__car = '" + session_car + "' and \
    session__date = '" + session_date + "'"
    #print(sel)
    df = wr.athena.read_sql_query(sel, database='iracing', ctas_approach=False)
    
    return df

def getSessionModalityVarianceTrace(session_stats_df, modality, round_decimals=0):
    
    # Separate query of Athena View provides session_stats_df
    # session_stats_df contains avg and std for all modalities
    # grouped by session_date, session_track, session_car, and round_lapdist 
    # the session_stats_df serves all modalities
    # returns list with 3 traces for each modality, [upperbound, average, lowerbound]
    # Upper_Bound and LowerBound provide session variance shading
    # Average provides line for session average
    
    modality_clms = sorted(list(session_stats_df.filter(like=modality).columns),key=str.lower)
    modality_df = pd.DataFrame({'lapdist':session_stats_df['round_lapdist'],
                                'avg':session_stats_df[modality_clms[0]],
                                'std':session_stats_df[modality_clms[1]]})
    
    x = modality_df['lapdist']
    yupper = modality_df['avg'] + modality_df['std']
    ylower = modality_df['avg'] - modality_df['std']
    
    rolling_window = 25
    yavg = modality_df['avg'].rolling(rolling_window).mean()
    
    upper_trace = go.Scatter(
            name= 'Upper Bound',
            x = x,
            y = yupper.round(round_decimals),
            mode='lines',
            line=dict(width=0),
            showlegend=False
        )
        
    lower_trace = go.Scatter(
            name='Lower Bound',
            x=x,
            y=ylower.round(round_decimals),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.2)',
            fill='tonexty',
            showlegend=False
        )
    
    average_trace = go.Scatter(
            name='Average',
            x=x,
            y=yavg.round(round_decimals),
            marker=dict(color="#444"),
            line=dict(width=1),
            mode='lines',
            showlegend=False
        )
    
    return [upper_trace, lower_trace, average_trace]

def getTelemetryDataFigure(session_telemetry_df, session_avg_std_df, session_view_title):
    # generate background shading for telemetry modality variances
    
    point_size = 2 # line thickness
    vis_mode = 'lines' # lines much more performant than 'markers' for viz
    
    d_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_dt', round_decimals=4)
    dd_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_ddt', round_decimals=4)
    speed_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_speed', round_decimals=0)
    slip_angle_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_slip_angle', round_decimals=2)
    steering_angle_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_steer', round_decimals=2)
    throttle_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_throttle', round_decimals=2)
    brake_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_brake', round_decimals=2)
    rpm_traces = getSessionModalityVarianceTrace(session_avg_std_df, '_rpm', round_decimals=0)

    # initiate plot and add background variance shading
    telemetry_view = make_subplots(rows=10, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.01
                )

    # add background variance and average traces
    for i in range(len(d_traces)):
        telemetry_view.add_trace(dd_traces[i],row=2,col=1)
        telemetry_view.add_trace(speed_traces[i],row=3,col=1)
        telemetry_view.add_trace(throttle_traces[i],row=4,col=1)
        telemetry_view.add_trace(brake_traces[i],row=5,col=1)
        telemetry_view.add_trace(slip_angle_traces[i],row=6,col=1)
        telemetry_view.add_trace(steering_angle_traces[i],row=7,col=1)
        telemetry_view.add_trace(rpm_traces[i],row=8,col=1)

    # identify best lap in this session
    bestlap = getBestLap(session_telemetry_df).lap

    # isolate the bestlap
    one_lap_df = session_telemetry_df.loc[session_telemetry_df['lap'].isin(bestlap)]

    # sort and clean up bestlap data for good viz
    one_lap_df = one_lap_df.sort_values(by=['lapdist'])
    
    # fill forward makes for better gear shift trace by 
    # replacing 0s with forward fill from previous gear
    one_lap_df.replace({'gear':0}, np.nan, inplace=True)
    one_lap_df['gear'] = one_lap_df['gear'].fillna(method='ffill')
    
    # add traces to telemetry.view
    telemetry_view.add_trace(d_traces[2],row=1,col=1) # the avg line, shading makes noisy viz
    
    # add bestlap delta from optimal; delta is cumulative difference for this lap
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['lapdeltatooptimallap'], name='delta-t',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=1,col=1)
    # add bestlap delta-delta from optimal; delta-delta is rate of change at each lapdist
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['lapdeltatosessionoptimallap_dd'], name='delta-delta-t',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=2, col=1)
    # add bestlap speed
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['speed'], name='speed',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=3, col=1)
    # add bestlap throttle
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['throttle'], name='throttle',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=4, col=1)
    # add bestlap brake
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['brake'], name='brake',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=5, col=1)
    # add bestlap calculated slip_angle
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['slip_angle'], name='slip_angle',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=6, col=1)
    # # add bestlap steering angle
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['steeringwheelangle'], name='steering angle',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=7, col=1)
    # add bestlap rpm
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['rpm'],name='rpm',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=8, col=1)
    # add bestlap gear
    telemetry_view.add_trace(go.Scatter(x=one_lap_df['lapdist'], y=one_lap_df['gear'],name='gear',
                         mode=vis_mode,marker=dict(size=point_size)),
                  row=9, col=1)
    
    # update view with height, width and title
    telemetry_view.update_layout(height=800, width=900,
                  title_text=session_view_title)
    
    #################
    ## TBD ##########
    ## section here to perhaps
    ## to add the peaks and highlight most
    ## variable corners
    ## also consider separating this out as
    ## as a separate module to augment the fig
    ## generated from this method
    ## - might be beneficial as toggle on/off feature
    ## - also consider toggle on/off for variance shading
    #################
    
    return telemetry_view
