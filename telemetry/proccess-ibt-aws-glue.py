###################################
# this code runs as a custom python script
# as part of an AWS Glue 2.0 ETL Job
# it produces a .json file with a schema that 
# is known by an AWS Glue Crawler.  The Glue
# Crawler makes the iRacing Telemetry data 
# available for interactive SQL analysis via AWS Athena
# AWS Glue Job config details:
### Name	process-ibt-aws-glue
### IAM role	glue-etl-s3-athena
### Type	Spark
### Glue version	2.0
### Python version	3
### ETL language	python
### Script location	s3://bucket/script/process-ibt-aws-glue.py
### Temporary directory	s3://bucket/temp
### Job bookmark	Disable
### Job metrics	Disable
### Continuous logging	Disable
### Server-side encryption	Disabled
### Python lib path	s3://bucket/awswrangler-2.3.0-py3-none-any.whl
### Jar lib path
### Other lib path
### Job parameters	
### --additional-python-modules boto3==1.17.3, pyarrow==2, awswrangler==2.4.0, pyirsdk==1.2.6, PyYAML==5.4.1
### Non-overrideable Job parameters	
### Connections	-
### Maximum capacity	10
### Worker type	G.1X
### Number of workers	10
### Job timeout (minutes)	2880
### Delay notification threshold (minutes)
### Tags	
#
##################################

import os
import csv
import json
import time
import ntpath
import re
import os
import irsdk
# import awswrangler as wr
# import getpass
import boto3
import pandas as pd

#################################
#######
## This part needs to be refactored to take filename from s3 file rather than hard-coded
inpath = 's3://bucket/folder/file.ibt'
outpath = 's3://bucket/folder/file.json'

filename = ntpath.basename(inpath)
filename = re.split('\.[^\.]+$',filename)[0].replace(' ','_')

# split filename by '_' to get car and a substring for track, date, time
filename_split = re.split('_',filename)
car = filename_split[0]
track = filename_split[1]
date = filename_split[2]
time = filename_split[3]
########
##################################

print('#1')

# download file to glue local storage
s3 = boto3.client('s3')
s3.download_file('bucket', 'folder/file.ibt', 'file.ibt')
print('#2 file transfer successful')

# instantiate irsdk and open file
ibt = irsdk.IBT()
ibt.open('file.ibt')
print('#3 ibt open')

# create the dataframe
df = pd.DataFrame()

# get all ibt headers
all_headers = ibt.var_headers_names
print('#4 have headers, starting extraction...')

## loop over headers
for header_iterator, value in enumerate(all_headers):
    this_header = value
    # print(this_header)
    df[this_header] = ibt.get_all(this_header)

# add date, time, track, car, parsed from filename above
df['session__starttime'] = time
df['session__date'] = date
df['sesssion__track'] = track
df['session__car'] = car

print('#5 extraction complete, writing data to s3')

# write output in suitable json format for aws glue crawler
ibt2json = df.to_json(orient='records').replace('[','').replace(']','').replace('},{','}\n{')

# write back to s3 
s3 = boto3.resource('s3')
s3.Object('bucket', 'folder/file.json').put(Body=ibt2json)

print('#6 write complete, job end')
###################################
