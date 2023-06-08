from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time


def scrap(url):
    # Initialize the webdriver
    driver = webdriver.Chrome()

    # Go to the website
    driver.get(url)

    # Get the current height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll to the bottom of the page
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.88);")
        # Wait for the page to load
        time.sleep(5)
        # Get the new height of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        # If the page height hasn't changed, we've reached the end of the page
        if new_height == last_height:
            break
        last_height = new_height

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #define the data types
    product_element_tag = "div"
    product_element_class = "product product_item"
    product_name_tag = "span"
    product_name_class = "prod_title block"
    product_price_tag = "ins"
    #product_price_class = "price center-price-in-grid text-center"
    product_second_price_tag = "bdi"
    #product_second_price_class = "woocommerce-Price-amount amount"
    #product_third_price_tag = "span"
    #product_third_price_class = "price center-price-in-grid text-center center_price PriceChecked"
    # Extract the data
    items = soup.find_all(product_element_tag, class_=product_element_class)
    data = []
    for item in items:
        try:
            #get link
            try:
                link = item.find("a", class_="prod_inner block")['href']
                print(link)
            except Exception as e:
                print(e)
                link = "no link"
            #get name
            try:
                title = item.find(product_name_tag, class_=product_name_class).text.strip()
            except Exception as e:
                print(e)
                title = "no name"
            #get price
            try:
                price = item.find(product_price_tag).find("bdi").text.strip()
                price = price.replace(",", "").replace(" ", "").replace("₪", "") #clean the price
            except Exception as e:
                print(e)
                try:
                    #second try
                    price = item.find(product_second_price_tag).text.strip()
                    price = price.replace(",", "").replace(" ", "").replace("₪", "")
                except Exception as e:
                    print(e)
                    price = "no price"
            #get stock
            try:
                stock = item.find("span", class_ = "prod-tag tag--out-of-stock").text.strip()
            except Exception as e:
                print(e)
                stock = ""
            #add to list
            data.append((link, title, price, stock))
            print(title)
        except Exception as e:
            print(e)
            continue
    # Save the data to a CSV file
    with open('data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow("title", "price")
        csvwriter.writerows(data)

    # Close the webdriver
    driver.quit()

    return data

#scrap_avi("https://www.avigil.co.il/product-category/%d7%92%d7%99%d7%98%d7%a8%d7%95%d7%aa/%d7%92%d7%99%d7%98%d7%a8%d7%95%d7%aa-%d7%90%d7%a7%d7%95%d7%a1%d7%98%d7%99%d7%95%d7%aa/%d7%92%d7%99%d7%98%d7%a8%d7%95%d7%aa-%d7%90%d7%a7%d7%95%d7%a1%d7%98%d7%99%d7%95%d7%aa-yamaha/")