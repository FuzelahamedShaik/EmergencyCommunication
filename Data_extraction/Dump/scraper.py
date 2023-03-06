from bs4 import BeautifulSoup
import requests, json, lxml, re
import pandas as pd


def bs4_scrape_google_play_store_search_apps(
    query: str, filter_by: str = "apps", country: str = "US"
):
    params = {
        "q": query,     
        "gl": country,  
        "c": filter_by  
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
    }

    html = requests.get("https://play.google.com/store/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")

    apps_data = []

    for app in soup.select("[jscontroller=tKHFxf]"):
        title = app.select_one(".DdYX5").text
        company = app.select_one(".wMUdtb").text
        app_icon = app.select_one(".j2FCNc img")["srcset"]

        try:
            thumbnail = app.select_one(".Shbxxd img")["srcset"]
        except:
            thumbnail = app.select_one(".Vc0mnc img")["src"]

        app_link = f'https://play.google.com{app.select_one(".Si6A0c.Gy4nib")["href"]}'
        app_id = app.select_one("a")["href"].split("id=")[1]
        
        try:
            rating = re.search(r"\d{1}\.\d{1}", app.select_one(".ubGTjb div")["aria-label"]).group()
        except:
            rating = None
        
        
        apps_data.append({
            "title": title,
            "app_link": app_link,
            "company": company,
            "rating": float(rating) if rating else rating, 
            "app_id": app_id,
            "thumbnail": thumbnail,
            "icon": app_icon
        })   

    app_name = [apps_data[i]['title'] for i in range(len(apps_data)-1)]
    app_link = [apps_data[i]['app_link'] for i in range(len(apps_data)-1)]
    app_rating = [apps_data[i]['rating'] for i in range(len(apps_data)-1)]

    df = pd.DataFrame()
    df['app_name'] = app_name
    df['app_link'] = app_link
    df['app_rating'] = app_rating

    df.to_csv('app_data.csv',index=False,header=['app_name','app_link','app_rating'])

    #print(json.dumps(apps_data, indent=2, ensure_ascii=False))

bs4_scrape_google_play_store_search_apps(query="emergency apps", filter_by="apps", country="FI")