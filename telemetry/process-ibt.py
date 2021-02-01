import csv
import json
import time
import yaml
import irsdk

# ir = irsdk.IRSDK()
# ir.startup()
## >> use this to get fields for session, weekend, setup and telemetry 

ibt = irsdk.IBT()
ibt.open('C:\\path\\to\\file.ibt')
ibt.get(1,'Speed')
ibt.var_headers_names()
ibt.get(1,'Lat')
ibt.get(1,'Lon')

# below need get all fields
# loop thru each field and get_all()
# add each as column to pandas data.frame
# write pandas to csv

#### Pseudo-code
# get all Fields for one of the separate sections below
# all_fields = ir_all_sessioninfo_fields # this can be done one time and written to iracing-fields.yaml
# do this once, using pyyaml write to file, then read in yaml - this also facilitates human-readable review and augmentation
# for field_iterator in all_fields:
#    this_field = all_fields[field_iterator]
#    print(this field)
#    df[this_field] = ir.get_all(this_field)
# df.to_csv(path/to/session-data.csv) # or could be json depending on structure and needs

# break out into 4 (maybe more) separate outputs according to type of data
# SessionInfo
# WeekendInfo
# SessionTelemetry
# SessionSetup

