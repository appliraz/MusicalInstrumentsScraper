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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.98);")
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
    product_element_class = "grid row"
    product_name_tag = "h3"
    product_name_class = "title text-center"
    product_price_tag = "span"
    product_price_class = "price center-price-in-grid text-center"
    product_second_price_tag = "span"
    product_second_price_class = "price center-price-in-grid text-center center_price"
    #product_third_price_tag = "span"
    #product_third_price_class = "price center-price-in-grid text-center center_price PriceChecked"
    # Extract the data
    items = soup.find_all(product_element_tag, class_=product_element_class)
    print(str(len(items)))
    data = []
    for item in items:
        base_url = "https://www.music-center.co.il"
        try:
            #get the link
            try:
                link = base_url + item.find("a")['href'][2:]
                print(link)
            except Exception as e:
                print(e)
                link = "no link"
            #get the model/name
            try:
                title = item.find(product_name_tag, class_=product_name_class).text.strip()
            except Exception as e:
                print(e)
                title = "no title"
            #get the price
            try:
                price = item.find(product_price_tag, class_=product_price_class).contents[2]
                price = price.replace(",", "").replace(" ", "").replace("₪", "") #clean the price
            except Exception as e:
                print(e)
                try:
                    price = item.find(product_second_price_tag, class_=product_second_price_class).contents[2]
                    price = price.replace(",", "").replace(" ", "").replace("₪", "")
                except Exception as e:
                    print(e)
                    #price = item.find(product_third_price_tag, class_=product_third_price_class).text.strip()
                    price = "no price"
            data.append((link, title, price))
            print(title)
        except Exception as e:
            print(e)
            continue
    """
    # Save the data to a CSV file
    with open('data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
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
        # csvwriter.writerow("title", "price")
       # csvwriter.writerows(data)
    """
    # Close the webdriver
    driver.quit()

    return data

#scrap_music_center("https://www.music-center.co.il/89647-%D7%9E%D7%92%D7%91%D7%A8%D7%99%D7%9D-%D7%95%D7%A8%D7%9E%D7%A7%D7%95%D7%9C%D7%99%D7%9D-%D7%9C%D7%92%D7%99%D7%98%D7%A8%D7%94")