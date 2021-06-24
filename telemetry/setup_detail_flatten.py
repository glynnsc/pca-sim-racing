import json
import pandas as pd
import csv
import time
import irsdk
from itertools import chain, starmap
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd-mm-YY H:M:S
datetime_string = now.strftime("%d-%m-%Y %H:%M:%S")
print("date and time =", datetime_string)

# iRacing needs to running and a server-session should be active before running this program
ir = irsdk.IRSDK()
ir.startup()

# instantiate the method for parsing the nested json setup configuration details
def flatten_json_iterative_solution(dictionary):
    """Flatten a nested json file"""

    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!
        
        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '_' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0 
            for value in parent_value:
                temp2 = parent_key + '_'+str(i) 
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value    

            
    # Keep iterating until the termination condition is satisfied
    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
           not any(isinstance(value, list) for value in dictionary.values()):
            break

    return dictionary
    

# get CarSetUp
# a setup should be applied prior to making this function call
car_setup = ir['CarSetup']
    if car_setup:
	setup = json.dumps(ir['CarSetup']) # creates a python dict
        car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
        if car_setup_tick != state.last_car_setup_tick:
            state.last_car_setup_tick = car_setup_tick
            print('car setup update count:', car_setup['UpdateCount'])

# remove beginning and ending single quotes if needed
# to comply with standard json

# if reading from a previously written setup.json file
# provide filepath
#json_file = '/path/to/setup_detail.json'

# csv output file
# still need to come up with and automated and robust convention for unique and meaningful names for setups
# currently not clear how to get the actual name of the setup as seen in iRacing Garage
# consider using combination of timestamps and script cli args

# combine filename with datetime_string variable from above
# something like this (iRacing is Windows only so path should reflect Windows style:
filepath = /Users/name/folder/
setup_name = 'active' # default, should be something like - rsr_spa_R1
#setup_detail_csv_filename = f"{filepath}/{setup_name}_setup_{datetime_string}.csv"

# hard-coded version as needed
#setup_detail_csv_filename = '/path/to/setup_detail.csv'

# read file
#with open(json_file, 'r') as myfile:
#    json_content = myfile.read()

# json_content = json_content.replace("'","\"")

# parse file if using file based approach
# car_setup = json.loads(json_content)

df = pd.Series(flatten_json_iterative_solution(car_setup)).to_frame()
# print(df)
df.to_csv(setup_detail_csv_filename, index=True)
####
