from selenium import webdriver
from selenium.webdriver.common.by import By
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
        try:
            # Press load more button
            driver.find_element(By.CLASS_NAME, "btn.wd-load-more.wd-products-load-more.load-on-scroll").click()
            time.sleep(3)
        except Exception as e:
            print(e)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.70);")
        # Wait for the page to load
        time.sleep(4)
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
    product_element_class = "product-wrapper"
    product_name_tag = "h2"
    product_name_class = "product-title"
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
            #get name
            try:
                link_block = item.find(product_name_tag, class_=product_name_class)
                title = link_block.text.strip()
            except Exception as e:
                print(e)
                title = "no name"
            #get link
            try:
                link = link_block.find("a")['href']
                print(link)
            except Exception as e:
                print(e)
                link = "no link"
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
            """
            #get stock
            try:
                stock = item.find("span", class_ = "prod-tag tag--out-of-stock").text.strip()
            except Exception as e:
                print(e)
                stock = ""
             """
            #add to list
            data.append((link, title, price))
            print(title)
        except Exception as e:
            print(e)
            continue
    """
    # Save the data to a CSV file
    with open('data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow("title", "price")
        for element in data:
            try:
                csvwriter.writerow(element)
            except Exception as e:
                print(e)
                print(element)
                try:
                    link = element[0]
                    name = "error reading name"
                    price = "error reading price"
                    csvwriter.writerow((link, name, price))
                except Exception as e:
                    print(e)
                    continue
        #csvwriter.writerows(data)
    """
    # Close the webdriver
    driver.quit()

    return data

#scrap_wild("https://www.wildguitars.co.il/product-category/%D7%90%D7%A4%D7%A7%D7%98%D7%99%D7%9D/%D7%90%D7%A4%D7%A7%D7%98%D7%99%D7%9D-%D7%9C%D7%92%D7%99%D7%98%D7%A8%D7%94/")