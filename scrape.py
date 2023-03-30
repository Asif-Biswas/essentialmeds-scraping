"""
This script scrapes the list of essential medicines from the WHO website.
Drug Should have the following attributes in Json File Format.
Name
Active Ingredient  ( I will explain this when Json file is done)
EML section
Age
ATC code
Formulation
    - formulation 1
    - formulation 2
    - so on
Indications
    - first choise
    - second choise
    - so on
Tags
    - first tag
    - second tag
    - so on

JSON File Format:
{
    "name": "Drug Name",
    "active_ingredient": "Active Ingredient",
    "age": "Age",
    "atc_code": "ATC Code",
    "sections": [
        {
            "name": "EML Section Name",
            "formulation": [
                "formulation 1",
                "formulation 2",
                "so on"
            ],
            "indications": [
                "first choise",
                "second choise",
                "so on"
            ]
        },
        {
            "name": "EML Section Name",
            "formulation": [
                "formulation 1",
                "formulation 2",
                "so on"
            ],
            "indications": [
                "first choise",
                "second choise",
                "so on"
            ]
        }
    ],
    "tags": [
        "first tag",
        "second tag",
        "so on"
    ]
}
"""

import requests
from bs4 import BeautifulSoup
import json
import re

# URL to scrape
url = "https://list.essentialmeds.org/?section=&indication=&year=&age=adult&sex="

# selector path: #container > div > div.medicines-list-container

# get the HTML
r = requests.get(url)
html = r.text

# parse the HTML
msoup = BeautifulSoup(html, "html.parser")

# get the container
container = msoup.select("#container > div > div.medicines-list-container")
# get all li elements of ol inside container
lis = container[0].select("ol > li")

# loop through all li elements
# in the li tag, there is a h5 tag with class "medicine-name" and there is a <a> tag inside it. get the link

# save this data to a json file
with open("data_adult2.json", "w") as f:
    for li in lis:
        link = li.select("h5 > a")[0]["href"]
        soup = BeautifulSoup(requests.get(link).text, "html.parser")
        # get the div with class "medicine-title"
        title = soup.select(".medicine-title")[0].text
        name = title.strip()
        age = 'adult'
        # get the div with class "header-data"
        header_data = soup.select(".header-data")[0]
        # get the first <a> tag inside header_data
        atc_code = header_data.select("a")[0]
        if 'www.whocc.no/atc_ddd_index' in atc_code['href']:
            atc_code = atc_code.text.strip()
        else:
            atc_code = ''

        json_format = {
            "name": name,
            "active_ingredient": "",
            "age": age,
            "atc_code": atc_code,
            "sections": [],
            "tags": []
        }
        
        print(name, atc_code)

        # get the div with class "section-container"
        sections = soup.select(".section-container")
        
        # loop through all sections
        for section in sections:
            section_format = {
                "name": "",
                "formulations": [],
                "indications": []
            }
            # get the div with class "section-name"
            section_name = section.select(".section-name")[0].text.strip()
            section_format["name"] = section_name
            # get the div with class "formulations"
            formulations = section.select(".formulations")
            if formulations:
                formulations = formulations[0]
                # get all <li> tags inside formulations
                formulations = formulations.select("li")
                # loop through all <li> tags
                for formulation in formulations:
                    # get the text inside <li> tag
                    formulation = formulation.text.strip()
                    if ";" in formulation:
                        formulation = formulation.split(";")
                        before_clone = formulation[0].split(":")[0]
                        is_first = True
                        for f1 in formulation:
                            if is_first:
                                is_first = False
                                f1 = f1.strip()
                                # append it to the json_format
                                section_format["formulations"].append(f1)
                            else:
                                f1 = f1.strip()
                                # append it to the json_format
                                section_format["formulations"].append(before_clone + ": " + f1)
                    else:
                        # append it to the json_format
                        section_format["formulations"].append(formulation)

            # get the div with class "antibiotic-choices"
            indications = section.select(".antibiotic-choices")
            if len(indications) > 0:
                for indication in indications:
                    indication_format = {
                        "name": "",
                        "choices": []
                    }
                    # get the <h6> tag inside indications
                    indication_name = indication.select("h6")[0].text.strip()
                    indication_format["name"] = indication_name
                    # select all <span> tags inside indication which has no class
                    spans = indication.select("span:not([class])")
                    for span in spans:
                        choise_format = {
                            "name": "",
                            "combination": ""
                        }
                        # check if the span child element has a class "combination-medicine"
                        if span.select(".combination-medicine"):
                            # get the text inside span
                            choise_format["combination"] = span.select(".combination-medicine")[0].text.strip()
                            choise_format["combination"] = re.sub(r'\s+', ' ', choise_format["combination"])

                        choise_format["name"] = span.select(".indication-text")[0].text.strip()
                        indication_format["choices"].append(choise_format)
                    section_format["indications"].append(indication_format)
            else:
                indication_text = section.select(".indication-text")
                if len(indication_text) > 0:
                    for indication in indication_text:
                        section_format["indications"].append(indication.text.strip())
            json_format["sections"].append(section_format)

        # add the json_format to the json file
        f.write(json.dumps(json_format, indent=4))
        f.write(",")
        f.write("\n")



                    

