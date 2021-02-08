import os
import csv
import json
import time
import ntpath
import re
import yaml
import irsdk
import pandas as pd

# process filepath to get car, track, date, time
full_path = 'C:/Users/User/Documents/iRacing/telemetry/car track date time.ibt'
filename = ntpath.basename(full_path)
filename = re.split('\.[^\.]+$',filename)[0].replace(' ','_')

# split filename by '_' to get car and a substring for track, date, time
filename_split = re.split('_',filename)
car = filename_split[0]
track = filename_split[1]
date = filename_split[2]
time = filename_split[3]

# instantiate irsdk and open file
ibt = irsdk.IBT()
ibt.open(full_path)

# create the dataframe
df = pd.DataFrame()

# get all ibt headers
all_headers = ibt.var_headers_names

## loop over headers
for header_iterator, value in enumerate(all_headers):
    this_header = value
    print(this_header)
    df[this_header] = ibt.get_all(this_header)

# add date, time, track, car, parsed from filename above
df['telemetry_log_start_time'] = time
df['telemetry_log_date'] = date
df['telemetry_track'] = track
df['telemetry_car'] = car

# write output in suitable json format for aws glue
outdirectory = 'C:/Users/User/Documents/folder/'
outpath = os.path.join(outdirectory,str(filename+'.json'))
ibt2json = df.to_json(orient='records').replace('[','').replace(']','').replace('},{','}\n{')
jsonfile = open(outpath, "w")
jsonfile.write(ibt2json)
jsonfile.close()

####################
## END
####################

## code to limit fields to those relevant for analysis
# f = open('/home/glynnsc/play/lapwise/dat/ibt-headers.txt')
# txt_file = [line.rstrip('\n') for line in f]
i# bt_headers = pd.Series(txt_file)

# analytics headers
# analytics_filter = ibt_headers[ibt_headers.str.contains('##')].str.replace(' ##.+$','')
# analytics_filter = analytics_filter.str.replace(' (.+)$','')

# boolean list of headers in analytics
# needs additional work, but basics are here
# analytics_boolean = all_headers.isin(analytics_filtered)
# analytics_headers = all_headers.loc[analytics_boolean]

# since text file contains additional text, 
# output needs to be trimmed/cleaned to match header format

#############
# break out into 4 (maybe more) separate outputs according to type of data
# SessionInfo
# WeekendInfo
# SessionTelemetry
# SessionSetup

# the setup, session and weekend details are not in ibt file
# get car setup details
# if car_setup:
#    setup = json.dumps(ir['CarSetup']) # creates a python dict

# get session details
# if ir['SessionInfo']:
#    session = json.dumps(ir['SessionInfo'])

# weekend details
# if ir['WeekendInfo']:
#    weekend = json.dumps(ir['WeekendInfo']) 
