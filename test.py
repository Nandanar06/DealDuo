import argparse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

def scrape_etsy(search_query):
    # Set Firefox WebDriver options
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument('--headless')  # Optional: Run headless for faster scraping
    
    # Initialize Firefox WebDriver with options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    
    # Construct the Etsy search URL
    url = f"https://www.etsy.com/in-en/search?q={search_query}&ref=search_bar"
    
    # Open the URL
    driver.get(url)
    
    # Wait for the page to fully load (you may need to adjust the timeout)
    driver.implicitly_wait(100)
    
    # Get the page source
    page_source = driver.page_source
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    
    while not soup:
        driver.implicitly_wait(5000)
    
        # Get the page source
        page_source = driver.page_source
    
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
    
    # Extract product information from the HTML
    products = []
    for item in soup.select(".listing-link.wt-display-inline-block"):
        name = item.select_one(".wt-text-captian.v2-listing-card__title.wt-text-truncate").text.strip()
        price = item.select_one(".wt-text-title-01.lc-price").text.strip()
        link = item["href"]
        products.append({"name": name, "price": price, "link": link, "retailer": "Etsy"})
    
    # Close the WebDriver
    # driver.quit()
    
    return products

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Etsy using Selenium.')
    parser.add_argument('query', metavar='query', type=str, nargs=1,
                        help='the search query to scrape on Etsy')
    args = parser.parse_args()
    
    search_query = args.query[0]
    print(scrape_etsy(search_query))
