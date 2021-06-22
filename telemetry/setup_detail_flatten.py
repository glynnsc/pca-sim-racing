import json
import pandas as pd

from itertools import chain, starmap

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
    
# remove beginning and ending single quotes if needed
# to comply with standard json

# fiepath
#json_file = '/path/to/setup_detail.json'
#csv_file = '/path/to/setup_detail.csv'

# read file
with open(json_file, 'r') as myfile:
    content = myfile.read()

content = content.replace("'","\"")

# parse file
data = json.loads(content)

df = pd.Series(flatten_json_iterative_solution(data)).to_frame()
# print(df)
df.to_csv(csv_file, index=True)
####
