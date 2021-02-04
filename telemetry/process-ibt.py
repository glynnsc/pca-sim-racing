import os
import csv
import json
import time
import ntpath
import re
import yaml
import irsdk
import pandas as pd

#ir = irsdk.IRSDK()
#ir.startup()

# process filepath to get car, track, date, time
## still need to extract filename from filepath
## then perform car, track, date, time extraction

full_path = 'C:\\Users\\Glynn\\Documents\\iRacing\\telemetry\\porsche911cup_lagunaseca 2021-01-21 21-54-11.ibt'
# full_path = 'C:\\Users\\Glynn\\Documents\\iRacing\\telemetry\\porsche911cup_lagunaseca 2021-01-31 23-15-52.ibt'
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
outdirectory = 'C:/Users/Glynn/Documents/play/ibt2json-data/'
outpath = os.path.join(outdirectory,str(filename+'.json'))
ibt2json = df.to_json(orient='records').replace('[','').replace(']','').replace('},{','}\n{')
jsonfile = open(outpath, "w")
jsonfile.write(ibt2json)
jsonfile.close()

####################
## END
####################
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
