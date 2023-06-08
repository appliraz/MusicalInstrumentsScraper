import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import Workbook, load_workbook
import csv

def getSoup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def getPriceAsText(url):
    soup = getSoup(url)
    price = soup.find(id="oldprice")
    pricetext = price.get_text(strip=True)
    last = len(pricetext)-1
    pricetext = pricetext[:last]
    return pricetext

def getPriceAsInt(url):
    return int(getPriceAsText(url))

def getProductName(url):
    soup = getSoup(url)
    name = soup.find('h2')
    nametext = name.get_text(strip=True)
    return nametext

def getProductNameFromSoup(soup):
    name = soup.find('h2')
    nametext = name.get_text(strip=True)
    return nametext

def getProductsPricesFromSoup(soup, pricetype):
    oldprice = soup.find_all(id=pricetype)
    pricetext = oldprice.get_text(strip=True)
    if not pricetext:
        return ""
    last = len(pricetext)-1
    pricetext = pricetext[:last]
    return pricetext

def stripName(name):
    nametext = name.get_text(strip=True)
    return nametext

def stripPrice(price):
    pricetext = price.get_text(strip=True)
    if not pricetext:
        return ""
    last = len(pricetext)-1
    pricetext = pricetext[:last]
    return pricetext

def getPriceFromProduct(product):
    try:
        price = product.find('div', class_="saleprice").contents[0]
    except Exception as e:
        print(e)
        price = "no"
    price = price.replace(" ", "")
    try:
        int(price)
    except Exception as e:
        print(e)
        try:
            price = product.find('div', class_="oldprice").contents[0]
        except Exception as e:
            price = "no price"
    return price.replace(" ", "")

def getPriceFromKleyWebPage(url):
    soup = getSoup(url)
    price = getPriceFromProduct(soup)
    return price

def scrap(url):
    base_url = "https://www.kley-zemer.co.il/"
    if url.find("?")!= -1:
        end_page = "&bscrp="
    else:
        end_page = "?bscrp="
    og_url = url
    page = 1
    url = og_url + end_page + str(page)
    soup = getSoup(url)
    products = soup.find_all('div', class_="border_item")
    data = []
    while len(products)>0:
        print(f"loop with page {page} there are {len(products)} products ")
        for product in products:
            link = product.find('a')
            if link.has_attr('href'):
                print("link exists")
                link = base_url + link['href']
                print(link)
            model = product.find('h2').text.strip()
            price = getPriceFromProduct(product)
            data.append((link, model, price))
        page += 1
        url = og_url + end_page + str(page)
        soup = getSoup(url)
        products = soup.find_all('div', class_="border_item")
        

    final_data = []
    for link, model, price in data:
        if price == "no price":
            price = getPriceFromKleyWebPage(link).replace(" ", "")
            last = price.length-2
            price = price[:last]
        
        #clean up the price from empty spaces
        to_replace = []
        for p in price:
            print(f"order of char {p} is {ord(p)}")
            if ord(p)==160:
                to_replace.append(p)
        for p in to_replace:
            price = price.replace(p, "")
        final_data.append((link, model, price))
    return final_data

    """
    # Save the data to a CSV file
    with open('data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow("title", "price")
        csvwriter.writerows(final_data)
    """


"""
url = "https://www.kley-zemer.co.il/%D7%A4%D7%A1%D7%A0%D7%AA%D7%A8%D7%99%D7%9D-%D7%93%D7%99%D7%92%D7%99%D7%98%D7%9C%D7%99%D7%99%D7%9D-%D7%A0%D7%99%D7%99%D7%97%D7%99%D7%9D-%D7%A7%D7%9C%D7%91%D7%99%D7%A0%D7%95%D7%91%D7%94"
scrap(url)
"""