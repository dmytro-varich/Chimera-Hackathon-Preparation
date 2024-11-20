import requests
from bs4 import BeautifulSoup

target_url = "https://www.scrapingcourse.com/javascript-rendering"

def scraper(url):
    response = requests.get(url)

    if response.status_code != 200:
        return f"status failed with {response.status_code}"
    else: 
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup.prettify())

# print(scraper(target_url))

# pip3 install selenium
from selenium import webdriver

# instantiate options for Chrome
options = webdriver.ChromeOptions()

# run the browser in headless mode
options.add_argument("--headless=new")

# instantiate Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

# URL of the web page to scrape
url = "https://www.scrapingcourse.com/javascript-rendering"

# open the specified URL in the browser
driver.get(url)

# print the page source
# print(driver.page_source)

# close the browser
driver.quit()



