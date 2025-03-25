import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib

# Load environment variables from .env file
load_dotenv(".env")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# URL of the Amazon product page to track
URL = ("https://www.amazon.com/Quencher-FlowState-Stainless-Insulated-Smoothie/dp/B0CRMZHDG8/"
       "?_encoding=UTF8&pd_rd_w=QxUjE&content-id=amzn1.sym.f2128ffe-3407-4a64-95b5-696504f68ca1&pf_rd_p=f2128ffe-3407-4a64-95b5-696504f68ca1&pf_rd_r="
       "9MFE2VYDVB94ACVNA2BP&pd_rd_wg=hgIxS&pd_rd_r=12cbfd8a-9b5e-4853-ae65-b61132715ae7&ref_=pd_hp_d_btf_crs_zg_bs_1055398&th=1")

# HTTP headers to mimic a request from a specific browser
http_headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.51 Safari/537.36",
}

# Make an HTTP GET request to the specified URL with the provided headers
response = requests.get(URL, headers=http_headers)
website_html = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(website_html, "html.parser")

# Extract the product price and convert it to a float
price = float(soup.find(name="span", class_="a-offscreen").getText()[1:])

# Extract and clean up the product name
product_name = " ".join(
    soup.find(name="span", class_="a-size-large product-title-word-break", id="productTitle").getText().split())

# Check if the price is below the threshold and send an email alert if it is
if price < 30.00:
    with smtplib.SMTP("smtp.outlook.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject: Alert: Amazon Price Tracker\n\n{product_name}\nis now ${price}.\n\n{URL}",
        )