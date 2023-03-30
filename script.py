"""
Get all the data of data_adult2.json, data_children2.json, data_newborn2.json and save to all_data.json
"""
import json

# Load the JSON data from file
with open('group_data2.json', 'r') as f:
    data_adult = json.load(f)

with open('group_data_children.json', 'r') as f:
    data_children = json.load(f)

with open('group_data_newborn.json', 'r') as f:
    data_newborn = json.load(f)

data = data_adult + data_children + data_newborn

# Save the data to a JSON file
with open('group.json', 'w') as f:
    json.dump(data, f, indent=4)

    


