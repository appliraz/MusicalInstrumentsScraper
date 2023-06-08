import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import Workbook, load_workbook
import csv

def getNextUrl(url, page):
    base_url = url
    page_url = "page/"
    query_url = ""
    if (i := base_url.find("?"))!=-1:
        base_url = url[:i]
        query_url = url[i:]
    url = base_url + page_url + str(page) + query_url
    return url

def scrap(url):
    base_url = url
    page = 1
    url = getNextUrl(base_url, page)
    r = requests.get(url)
    #product_element_class = "product type-product post-12854 status-publish first instock product_cat-78 product_cat-24 product_cat-77 has-post-thumbnail sale shipping-taxable purchasable product-type-simple"
    #product_element_tag = "li"
    product_element_class = "woocommerce-LoopProduct-link woocommerce-loop-product__link"
    product_element_tag = "a"
    data = []
    nextloop = True
    while r.status_code != 404 and nextloop:
        try:
            soup = BeautifulSoup(r.text, "html.parser")
            products = soup.find_all(product_element_tag, class_ = product_element_class)
            pages = soup.find_all('a', class_ = "next page-numbers")
            if not pages:
                nextloop = False
        except Exception as e:
            print(e)
            break
        for product in products:
            try:
                if product.has_attr('href'):
                    link = product['href']
                    print(link)
            except Exception as e:
                print(e)
                link = "no link"
            try:
                model = product.find('h2').text.strip()
                print(f"model is {model}")
            except Exception as e:
                print(e)
                model = "no model"
            try:
                price = product.find('ins').find('bdi').text.strip().replace("₪","").replace(",","")
                print(f"price is {price}")
            except Exception as e:
                print(e)
                price = "no price"
            data.append((link, model, price))
        page += 1
        url = getNextUrl(base_url, page)
        print(url)
        try:
            r = requests.get(url)
        except Exception as e:
            print(e)
    return data

    """
    final_data = []
    
    for link, model, price in data:
        if price == "no price":
            price = getPriceFromKleyWebPage(link).replace(" ", "")
        final_data.append((link, model, price))
    
    # Save the data to a CSV file
    with open('data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow("title", "price")
        csvwriter.writerows(data)





url = "https://diez.co.il/product-category/%d7%a4%d7%a1%d7%a0%d7%aa%d7%a8%d7%99%d7%9d/%d7%a4%d7%a1%d7%a0%d7%aa%d7%a8-%d7%90%d7%a7%d7%95%d7%a1%d7%98%d7%99-%d7%97%d7%93%d7%a9/"
getProducts(url)
    
    """