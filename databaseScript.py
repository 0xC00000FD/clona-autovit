import urllib.request
from serpapi import GoogleSearch
import json

def serpapi_get_google_images(queries):
    image_results = []
    
    for query in queries:
        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            "api_key": "1300c9dea4ff8ff04e5d19d44b208c5e3307e28c63df62f4f5e2cb014d3e3c5f",                 # https://serpapi.com/manage-api-key
            # other query parameters: hl (lang), gl (country), etc  
        }
    
        search = GoogleSearch(params)         # where data extraction happens

        print(1)
        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary
    
            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if image["original"] not in image_results:
                        image_results.append(image["original"])
                        break
                
                # update to the next page
                params["ijn"] += 1
                break
            else:
                print(results["error"])
                images_is_present = False
    
    # -----------------------
    # Downloading images

    for index, image in enumerate(results["images_results"], start=1):
        print(f"Downloading {index} image...")
        
        opener=urllib.request.build_opener()
        opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(image["original"], f"./img/{image["title"]}.jpg")

    print(json.dumps(image_results, indent=2))
    print(len(image_results))
 
carsJson = json.load(open("./brandMasini.json"))

searchQueries = []
for car in carsJson:
    for model in car["models"]:
        searchQueries.append(f"{car["brand"]} {model}")
    
serpapi_get_google_images(searchQueries)