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
with open("adult_atc.json", "w") as f:
    for li in lis:
        link = li.select("h5 > a")[0]["href"]
        soup = BeautifulSoup(requests.get(link).text, "html.parser")
        # get the div with class "medicine-title"
        title = soup.select(".medicine-title")[0].text
        name = title.strip()
        json_format = {
            "name": name,
            "atc_codes": []
        }
        # get the div with class "header-data"
        header_data = soup.select(".header-data")[0]
        # get all the <a> tag inside header_data
        atc_code = header_data.select("a")
        if len(atc_code) > 0:
            for a in atc_code:
                # check if "atc_ddd_index" in href:
                href = a["href"]
                if "atc_ddd_index" in href:
                    # get the text of the <a> tag
                    atc_code = a.text
                    print(atc_code)
                    json_format["atc_codes"].append(atc_code)

        

        # add the json_format to the json file
        f.write(json.dumps(json_format, indent=4))
        f.write(",")
        f.write("\n")



                    

