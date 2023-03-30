"""
Get all the data of data_adult2.json, data_children2.json, data_newborn2.json and save to all_data.json
"""
import json

# Load the JSON data from file
with open('adult_atc.json', 'r') as f:
    data_adult = json.load(f)

with open('children_atc.json', 'r') as f:
    data_children = json.load(f)

with open('newborn_atc.json', 'r') as f:
    data_newborn = json.load(f)

data = data_adult + data_children + data_newborn

# Save the data to a JSON file
with open('all_atc.json', 'w') as f:
    json.dump(data, f, indent=4)

    


