import csv
import json
import time
import re
import yaml
import irsdk

# ir = irsdk.IRSDK()
# ir.startup()
## >> use this to get fields for session, weekend, setup and telemetry 

ibt = irsdk.IBT()

file_path = 'C:\\path\\to\\file.ibt'

## still need to extract filename from filepath
## then perform car, track, date, time extraction

filename = 'porsche911cup_lagunaseca 2021-01-31 23-15-52.ibt'

# split filename by '_' to get car and a substring for track, date, time
car_split = re.split('_',filename)
car = car_split[0]

# use the second element of car_split for track, date, time
track_date_time_split = re.split(' ', car_split[1])
track = track_date_time_split[0]
date = track_date_time_split[1]
time = re.split('\.[^\.]+$',track_date_time_split[2])[0]

# car, track, date, time are now variables to be added to the df below
# which can then be used later for partitioning, comparisons and analytics

ibt.open(file_path) # longterm is to provide path as cli parameter when calling an executable



# for partitioning by car, track, date - need to parse the ibt filename and use the pieces as fields in data frame
# below need get all fields
# loop thru each field and get_all()
# add each as column to pandas data.frame
# write pandas to csv

df = pd.DataFrame()
all_fields = ibt.var_headers_names

for field_iterator, field in enumerate(all_fields):
    this_field = field
    print(this_field)
    df[this_field] = ibt.get_all(this_field)

df.to_csv('path/to/output.csv')

#### Pseudo-code
# get all Fields for one of the separate sections below
# df = pd.DataFrame()
# all_fields = ir_all_sessioninfo_fields # this can be done one time and written to iracing-fields.yaml
# do this once, using pyyaml write to file, then read in yaml - this also facilitates human-readable review and augmentation
# for field_iterator in all_fields:
#    this_field = all_fields[field_iterator]
#    print(this field)
#    df[this_field] = ibt.get_all(this_field)
# df.to_csv(path/to/session-data.csv) # or could be json depending on structure and needs

# break out into 4 (maybe more) separate outputs according to type of data
# SessionInfo
# WeekendInfo
# SessionTelemetry
# SessionSetup

