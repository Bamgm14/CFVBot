import requests as r
from bs4 import BeautifulSoup

def getWikiaCategory(url):
    dataList = []
    data = r.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    soup = BeautifulSoup(data.text, 'html.parser')
    #print(dataList)
    #print(soup.prettify())
    #print(soup.find_all("a"))
    for x in soup.find_all("a"):
        try:
            #print(x)
            #print(x['class'], x['class'] == ['category-page__member-link'])
            if x['class'] == ['category-page__member-link']:
                #print(x['href'])
                #print(x['href'].removeprefix('/wiki/'))
                name = x['href'].removeprefix('/wiki/')
                if ("Card_Gallery:" not in name and "Category:" not in name and "Cardfight_Pack" not in name 
                    and "(ZERO)" not in name and "Set_Gallery:" not in name and "User:" not in name
                    and "List of" not in name and "User blog:" not in name):
                    dataList.append(name)
                #print(name)
            if x['class'] == ['category-page__pagination-next', 'wds-button', 'wds-is-secondary']:
                #print(x['href'])
                dataList += getWikiaCategory(x['href'])
        except:
            pass
    return dataList