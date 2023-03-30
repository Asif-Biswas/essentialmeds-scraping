
import requests
from bs4 import BeautifulSoup
import json
import re

# URL to scrape
url = "https://list.essentialmeds.org/?section=&indication=&year=&age=newborn&sex="

# get the HTML
r = requests.get(url)
html = r.text

# parse the HTML
msoup = BeautifulSoup(html, "html.parser")

# get the container
container = msoup.select("#container > div > div.medicines-list-container")
# get all li elements of ol inside container
lis = container[0].select("ol > li")

# save this data to a json file
with open("group_data_newborn.json", "w") as f:
    for li in lis:
        data_format = {
            "name": "",
            "group": ""
        }
        link = li.select("h5 > a")[0]["href"]
        soup = BeautifulSoup(requests.get(link).text, "html.parser")
        # get the div with class "medicine-title"
        title = soup.select(".medicine-title")[0].text
        name = title.strip()
        data_format["name"] = name
        # get the <a> tag with class "antibiotic-group"
        group = soup.select(".antibiotic-group")
        if len(group) > 0:
            href = group[0]["href"]
            group = href.split("/")[-1]
            print(name, group)
            data_format["group"] = group.lower()
        
            json.dump(data_format, f, indent=4)



