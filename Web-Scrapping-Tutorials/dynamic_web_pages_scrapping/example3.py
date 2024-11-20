from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scraper(driver):
    products = driver.find_elements(By.CLASS_NAME, "product-item")

    scraped_data = []

    for product in products:
        product_name = product.find_element(By.CLASS_NAME, "product-name")
        product_price = product.find_element(By.CLASS_NAME, "product-price")

        data = {
            "name": product_name.text if product_name else "",
            "price": product_price.text if product_price else "",
        }

        scraped_data.append(data)

    return scraped_data

# instantiate options for Chrome
options = webdriver.ChromeOptions()

# run the browser in headless mode
options.add_argument("--headless=new")

# instantiate Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

# open the specified URL in the browser
driver.get("https://www.scrapingcourse.com/infinite-scrolling")

# print(scraper(driver))

# get the previous height value
last_height = driver.execute_script("return document.body.scrollHeight")

product_data = []

while True:
    # scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # wait for the page to load
    time.sleep(2)

    # get the new height and compare it with the last height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        # extract data once all content has loaded
        product_data.extend(scraper(driver))
        break
    last_height = new_height

# print the scraped data after scrolling
print(product_data)

# close the browser
driver.quit()