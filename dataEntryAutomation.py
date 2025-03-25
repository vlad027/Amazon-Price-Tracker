from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# HTTP headers to mimic a request from a specific browser
http_headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.51 Safari/537.36",
}

# Load environment variables from .env file
load_dotenv(".env")
URL = os.getenv("URL")

# Make an HTTP GET request to the specified URL with the provided headers
response = requests.get(URL, headers=http_headers)
# Initialize the ChromeDriver service with the path to the ChromeDriver executable
service = Service("") # Enter the path to the ChromeDriver executable.
driver = webdriver.Chrome(service=service)
website_html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(website_html, "html.parser")
# Find the search results container in the parsed HTML
search_results = soup.find("div", {"id": "grid-search-results"})

# Function to extract links to individual property listings
def get_links():
    links_list = [a["href"] for a in search_results.find_all("a", tabindex="0")]
    for index in range(len(links_list)):
        if not links_list[index].startswith("http"):
            links_list[index] = 'https://www.zillow.com' + links_list[index]
    return links_list

# Function to extract addresses of the properties
def get_addresses():
    address_list = [address.getText() for address in search_results.find_all("a", tabindex="0") if address.getText()]
    return address_list

# Function to extract prices of the properties
def get_price():
    price_list = [price.getText()[:7] for price in soup.find_all("div", class_="list-card-price")]
    return price_list

# URL of the Google Form to fill out
GOOGLE_FORMS = os.getenv("GOOGLE_FORMS")
# Open the Google Form in the Chrome browser
driver.get(GOOGLE_FORMS)
sleep(3)

# Print the number of addresses found
print(len(get_addresses()))
# Iterate through the extracted data and fill out the Google Form
for fill_out in range(len(get_addresses())):
    # Find the input fields for address, price, and link
    property_address = driver.find_element(
        By.XPATH, value='//*[@aria-describedby = "i2 i3"]')
    property_price = driver.find_element(
        By.XPATH, value='//*[@aria-describedby = "i6 i7"]')
    property_link = driver.find_element(
        By.XPATH, value='//*[@aria-describedby = "i10 i11"]')

    # Fill in the input fields with the extracted data
    property_address.send_keys(get_addresses()[fill_out])
    property_price.send_keys(get_price()[fill_out])
    property_link.send_keys(get_links()[fill_out])
    # Click the submit button to submit the form
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()

    # Click the "Submit another response" link to reset the form for the next entry
    another_response = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_response.click()

# Close the browser
driver.quit()