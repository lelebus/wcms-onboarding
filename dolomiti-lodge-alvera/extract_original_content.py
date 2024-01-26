from bs4 import BeautifulSoup
import csv

# load content
content = BeautifulSoup(open("original-content.html"))

# iterate over top level divs
# iterate over tab-menu-content divs.tab-content
# for each, extract a wine name, winery, and wine price
class Wine:
    def __init__(self, name, info, vintage, price):
        self.name = name
        self.info = info
        self.vintage = vintage
        self.price = price

    def get_name(self):
        return self.name
    
    def get_info(self):
        return self.info

    def get_vintage(self):
        return self.vintage

    def get_price(self):
        return self.price

    def __str__(self):
        return self.name + " " + self.info + " " + self.price

wines = []
categories = content.find_all("div", {"class": "first-level-container"})
for category in categories:
    wines_in_category = category.find_all("div", {"class": "dish-row"})
    for wine in wines_in_category:
        name = wine.find("div", {"class": "dish-name"}).text.strip()
        info = wine.find("div", {"class": "ingredienti-elenco"})
        if info is None:
            info = ""
        else:
            info = info.text.strip()

        vintage = wine.find("span", {"class": "dish-year"})
        if vintage is None:
            vintage = ""
        else:
            # replace in name
            name = name.replace(vintage.text, "").strip()
            vintage = vintage.text.replace("-", "").strip()

        price = wine.find("div", {"class": "dish-price"}).text.replace("€","").replace(",","").strip()
        wines.append(Wine(name, info, vintage, price))

print(len(wines))


# write to csv
with open("v1-cleaned.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name", "vintage", "price"])
    for wine in wines:
        writer.writerow([wine.get_name() + " " + wine.get_info(), wine.get_vintage(), wine.get_price()])