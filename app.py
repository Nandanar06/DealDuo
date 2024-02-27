from flask import Flask, jsonify, request, render_template
from bs4 import BeautifulSoup
import requests
import os
# import threading
# from twisted.internet import reactor
# from twisted.python import log
# from twisted.web.server import Site
# from twisted.web.wsgi import WSGIResource
# from autobahn.twisted.resource import WSGIRootResource
# from waitress import serve
# Set the environment variable
# os.environ['PYPPETEER_CHROMIUM_REVISION'] = '1263111'


from requests_html import HTMLSession
app = Flask(__name__)

# Function to scrape eBay
def scrape_ebay(search_query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = []
    for item in soup.select(".s-item"):
        img = item.select_one(".s-item__wrapper image-treatement")
        name = item.select_one(".s-item__title").text.strip()
        price = item.select_one(".s-item__price").text.strip()
        link = item.select_one(".s-item__link")["href"]
        products.append({"name": name, "price": price, "link": link, "retailer": "eBay", "img": img})
    
    return products

# Function to scrape Etsy
def scrape_etsy(search_query):
    session = HTMLSession()
    url = f"https://www.etsy.com/in-en/search?q={search_query}&ref=search_bar"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = session.get(url,  headers=headers)
    response.html.render() 
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = []
    for item in soup.select(".listing-link.wt-display-inline-block"):
        name = item.select_one(".wt-text-captian.v2-listing-card__title.wt-text-truncate").text.strip()
        price = item.select_one(".wt-text-title-01.lc-price").text.strip()
        link = item["href"]
        products.append({"name": name, "price": price, "link": link, "retailer": "Etsy"})
    
    return products



# Route to render the index.html template
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle product search
@app.route("/search", methods=["POST"])
def search():
    search_query = request.json.get("query", "").strip()
    if not search_query:
        return jsonify({"error": "Please provide a valid search query."}), 400

    ebay_products = scrape_ebay(search_query)
    all_products = jsonify(ebay_products)
    print(all_products)
    return all_products


# Run the Flask application
if __name__ == "__main__":
        app.run(debug=True)
        

