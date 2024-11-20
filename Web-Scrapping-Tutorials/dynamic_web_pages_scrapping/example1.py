import requests
from bs4 import BeautifulSoup

target_url = "https://www.scrapingcourse.com/ajax/products"

def scraper(url):
    response = requests.get(url)

    if response.status_code != 200:
        return f"status failed with {response.status_code}"
    else:
        soup = BeautifulSoup(response.text, "html.parser")

        scraped_data = []

        products = soup.find_all("div", class_="product-item")

        for product in products:
            name_tag = product.find(class_="product-name")
            price_tag = product.find(class_="product-price")

            data = {
                "name": name_tag.text if name_tag else "", 
                "price": price_tag.text if price_tag else "", 
            }

            scraped_data.append(data)
        
        return scraped_data
    
# print(scraper(target_url))

offset_count = 0

product_data = []

for page in range(0, 15):
    requested_page_url = f"{target_url}?offset={offset_count}"

    collected_data = scraper(requested_page_url)

    product_data.extend(collected_data)

    offset_count += 10

print(product_data)