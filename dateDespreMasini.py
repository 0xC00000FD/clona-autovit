import json
from bs4 import BeautifulSoup
import requests

carsJson = json.load(open("./brandMasini.json"))

brands = {}
searchQueries = []
for car in carsJson:
    masini = {}
    for model in car["models"]:
        results = requests.get(f"https://www.auto-data.net/ro/results?search={car["brand"] + "%20" + model}")
        
        parser = BeautifulSoup(results.text)
        div = parser.find("div", class_=["down", "down", "2"])
        
        try:
            link = list(div.children)[0].get("href")
            
            results = requests.get("https://www.auto-data.net" + link)
            parser = BeautifulSoup(results.text)
            
            table = parser.find("table", class_=["cardetailsout", "car2"])
            dateMasina = {}
            
            
            for tr in table.findChildren("tr"):
                if not tr.has_attr('class'):
                    print(tr)
                    
                    caption = list(tr.children)[0].text
                    
                    try:
                        value = list(tr.children)[1][1].text
                        dateMasina.update({caption: value})
                    except:
                        try:
                            value = list(tr.children)[1].text
                            dateMasina.update({caption: value})
                        except:
                            value=""     
        except:
            print("sarim peste")
        else:
            masini.update({model: dateMasina})
    
    brands.update({car["brand"]: masini})
    
with open("./bazaDeDate.json", "w+") as f:
    f.write(json.dumps(brands, ensure_ascii=False))