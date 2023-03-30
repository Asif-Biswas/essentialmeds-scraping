
        # get the div with class "formulations"
        formulations = soup.select(".formulations")
        if formulations:
            formulations = formulations[0]
            # get all <li> tags inside formulations
            formulations = formulations.select("li")
            # loop through all <li> tags
            for formulation in formulations:
                # get the text inside <li> tag
                formulation = formulation.text.strip()
                # append it to the json_format
                json_format["formulation"].append(formulation)

        # get the div with class "antibiotic-choices"
        indications = soup.select(".antibiotic-choices")
        if len(indications) > 0:
            for indication in indications:
                indication_format = {
                    "name": "",
                    "choices": []
                }
                # get the <h6> tag inside indications
                indication_name = indication.select("h6")[0].text.strip()
                print(indication_name)
                indication_format["name"] = indication_name
                # get all the span tags with class "indication-text"
                choices = indication.select(".indication-text")
                for choice in choices:
                    # get the text inside span tag
                    choice = choice.text.strip()
                    # append it to the json_format
                    indication_format["choices"].append(choice)
                json_format["indications"].append(indication_format)

        else:
            indications = soup.select(".indication-text")
            if len(indications) > 0:
                for indication in indications:
                    # get the text inside span tag
                    indication = indication.text.strip()
                    # append it to the json_format
                    json_format["indications"].append(indication)

        # add the json_format to the json file
        f.write(json.dumps(json_format, indent=4))
        f.write(",")
        f.write("\n")






# Load the JSON data from file
with open('data_all2.json', 'r') as f:
    data = json.load(f)

# Loop over the objects
for obj in data:
    if len(obj['formulation']):
        active_ingredient = []
        for formulation in obj['formulation']:
            active_ingredient.append(f"{obj['name']} + {formulation}")
        obj['active_ingredient'] = active_ingredient
    else:
        obj['active_ingredient'] = []
    

# Write the updated data back to the file
with open('data_all3.json', 'w') as f:
    json.dump(data, f, indent=4)
        




