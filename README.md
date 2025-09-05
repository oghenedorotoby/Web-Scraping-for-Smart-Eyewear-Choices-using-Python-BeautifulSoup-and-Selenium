# Web-Scraping-for-Smart-Eyewear-Choices-using-Python-BeautifulSoup-and-Selenium
Automating Prescription Glasses Data Collection by extracting structured product data from ecommerce sites and creating clean data sets for decision making

# FramesDirect Eyeglasses Scraper
This repository contains a fully functional Python script (framesdirect.py) that scrapes eyeglasses products from [FramesDirect.com](https://www.framesdirect.com/eyeglasses/) using Selenium (for dynamic content) and BeautifulSoup (for parsing). It exports clean CSV and JSON files with the following fields for each product:

- Brand Name
- Product Name
- Original Price (numbers only)
- Current/Offer Price (numbers only)
-  Discount Percent (computed where applicable)

# Outputs:
#   data/framesdirect.csv
#   data/framesdirect.json

Challenges faced: I used the wrong class names when looking for product details, i had to go back to the websites and get the correct classes for the details i needed.
I also had challenges in removing the dollar sign from the prices for that i created a function to convert the price string into a float.
I also noticed in my output that some of the elements that had no value where returning blank instead of it being filled with a null so i also created a function to clean the text output by making sure all blanks were filled with null.
