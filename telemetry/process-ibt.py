import csv
import json
import time
import irsdk

# ir = irsdk.IRSDK()
# ir.startup()

ir = irsdk.IBT()
ir.open('C:\\path\\to\\file.ibt')
ir.get(1,'Speed')
ir.var_headers_names()
ir.get(1,'Lat')
ir.get(1,'Lon')

# below need get all fields
# loop thru each field and get_all()
# add each as column to pandas data.frame
# write pandas to csv

# break out into 4 (maybe more) separate outputs according to type of data
# SessionInfo
# WeekendInfo
# SessionTelemetry
# SessionSetup

