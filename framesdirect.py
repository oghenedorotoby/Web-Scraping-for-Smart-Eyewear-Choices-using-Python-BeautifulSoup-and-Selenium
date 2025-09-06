import csv
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Step 1 - Configuration and Data Fetching
# Setup Selenium and WebDriver
print("Setting up webdriver...")
chrome_option = Options()
chrome_option.add_argument('--headless')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
)
print("done setting up..")

# Install the chrome driver (This is a one time thing)
print("Installing Chrome WD")
service = Service(ChromeDriverManager().install())
print("Final Setup")
driver = webdriver.Chrome(service=service, options=chrome_option)
print("Done")

# Make connection and get URL content
url = "https://www.framesdirect.com/eyeglasses/"
print(f"Visting {url} page")
driver.get(url)

# Further instruction: wait for JS to load the files
try:
    print("Waiting for product tiles to load")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'fd-cat'))
    )
    print("Done...Proceed to parse the data")
except (TimeoutError, Exception) as e:
    print(f"Error waiting for {url}: {e}")
    driver.quit()
    print("Closed")

# Step 2 - Data Parsing and Extraction
# Get page source and parse using BeautifulSoup
content = driver.page_source
page = BeautifulSoup(content, 'html.parser')

def normalize_price(text):
    """Convert a price string like '$299.00' into a float (299.0)."""
    if not text:
        return None
    # Extract numbers (with decimals) from the text
    match = re.search(r"\d+(\.\d+)?", text.replace(",", ""))  # handles $1,299.50
    return float(match.group()) if match else None

def clean_text(tag):
    """Return text from a tag, or None if missing/empty."""
    if tag:
        text = tag.get_text(strip=True)
        return text if text else None
    return None

# Temporary storage for the extracted data
frames_data = []

# Locate all product holder and extract the data for each product.
product_holders = page.find_all("div", class_='prod-holder')
print(f"Found {len(product_holders)} products")

for holder in product_holders:
    product_info = holder.find('div', class_='prod-title')

    if product_info:
        brand_tag = product_info.find('div', class_='catalog-name')
        brand = brand_tag.text if brand_tag else None # product brand

        name_tag = product_info.find('div', class_='product_name')
        name = name_tag.text if name_tag else None

        # for price
        price_cnt = holder.find('div', class_='prod-bot')
        if price_cnt:
            # Former Price
            former_price_tag = price_cnt.find('div', class_='prod-catalog-retail-price')
            former_price_raw = clean_text(former_price_tag)
            former_price = normalize_price(former_price_raw)
            # Current Price
            current_price_tag = price_cnt.find('div', class_='prod-aslowas')
            current_price_raw = clean_text(current_price_tag)
            current_price = normalize_price(current_price_raw)
        else:
            former_price = current_price = None
    else:
        brand = name = former_price = current_price = None 
        # Automatically applies missing value, if the product info is not available.
    
    brand_tag = holder.find('div', class_='catalog-name')
    price_cnt = holder.find('div', class_='prod-bot')

    if not brand_tag or not price_cnt:
     continue  # skip ads or invalid entries
 
    discount_tag = holder.find('div', class_='frame-discount')
    discount = clean_text(discount_tag)

            
    data = {
        'Brand': brand,
        'Product_Name': name,
        'Former_Price': former_price,
        'Current_Price': current_price,
        'Discount': discount
    }
    # Append data to the list
    frames_data.append(data)

# Step 3 - Data Storage and Finalization
# Save to CSV file
column_name = frames_data[0].keys() # get the column names
with open('framesdirect_data.csv', mode='w', newline='', encoding='utf-8') as csv_file: # open up the file with context manager
    dict_writer = csv.DictWriter(csv_file, fieldnames=column_name)
    dict_writer.writeheader()
    dict_writer.writerows(frames_data)
print(f"Saved {len(frames_data)} records to CSV")

# Save to JSON file
with open("framesdirect.json", mode='w') as json_file:
    json.dump(frames_data, json_file, indent=4)
print(f"Saved {len(frames_data)} records to JSON")

# close the browser
driver.quit()
print("End of Web Extraction")