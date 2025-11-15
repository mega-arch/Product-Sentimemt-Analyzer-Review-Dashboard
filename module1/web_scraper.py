from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import re

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def close_popup():
    try:
        close_btn = driver.find_element(By.CSS_SELECTOR, "button._2KpZ6l._2doB4z")
        close_btn.click()
        time.sleep(1)
    except:
        pass

def get_product_links(category_url, max_products=25):
    print(f"Getting products from: {category_url}")
    driver.get(category_url)
    time.sleep(4)
    close_popup()
    product_links = []
    for i in range(3):
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i/2});")
        time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_links = soup.find_all('a', href=True)
    for link in all_links:
        if len(product_links) >= max_products:
            break
        href = link['href']
        if '/p/' in href and '?pid=' in href:
            full_url = "https://www.flipkart.com" + href if not href.startswith('http') else href
            if full_url not in product_links:
                product_links.append(full_url)
    print(f"Total product links found: {len(product_links)}")
    return product_links[:max_products]

def extract_product_info(product_url):
    print(f"Extracting from: {product_url[:80]}...")
    driver.get(product_url)
    time.sleep(4)
    close_popup()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f"Page title: {driver.title[:50]}...")
    name = "Not Found"
    name_selectors = [
        'span.B_NuCI',
        'h1.yhB1nd',
        'span.VU-ZEz',
        'h1._2NKhZn',
        '.product-title',
        'h1'
    ]
    for selector in name_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            name = element.get_text(strip=True)
            break
    price = "0"
    price_selectors = [
        'div._30jeq3._16Jk6d',
        'div._30jeq3',
        'div._1vC4OE._3qQ9m1',
        'div._25b18c',
        '.dyC4hf',
        '[class*="price"]',
        'div.Nx9bqj',
        'div.CxhGGb',
        'div._3I9_wc',
        'div._3iZgFn',
        'div._2p6lqe'
    ]
    for selector in price_selectors:
        element = soup.select_one(selector)
        if element:
            price_text = element.get_text(strip=True)
            price_digits = ''.join(filter(str.isdigit, price_text))
            if price_digits and len(price_digits) >= 3:
                price = price_digits
                print(f"Found price with selector {selector}: ₹{price}")
                break
    if price == "0":
        page_text = soup.get_text()
        price_patterns = [
            r'₹\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'Rs\.\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'INR\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'price.*?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'₹(\d+(?:,\d+)*)'
        ]
        for pattern in price_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                for match in matches:
                    price_digits = ''.join(filter(str.isdigit, str(match)))
                    if price_digits and len(price_digits) >= 3:
                        price = price_digits
                        print(f"Found price with regex: ₹{price}")
                        break
                if price != "0":
                    break
    if price == "0":
        rupee_elements = soup.find_all(text=re.compile('₹'))
        for element in rupee_elements:
            parent = element.parent
            if parent:
                text = parent.get_text(strip=True)
                price_match = re.search(r'₹\s*(\d{1,3}(?:,\d{3})*)', text)
                if price_match:
                    price_digits = ''.join(filter(str.isdigit, price_match.group(1)))
                    if price_digits and len(price_digits) >= 3:
                        price = price_digits
                        print(f"Found price with ₹ symbol: ₹{price}")
                        break
    rating = "0"
    rating_selectors = [
        'div._3LWZlK',
        'div._2d4LTz',
        '.XQDdHH',
        'div._3lS5K4',
        '[class*="rating"]'
    ]
    for selector in rating_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            rating_text = element.get_text(strip=True)
            if re.match(r'^\d+(\.\d+)?$', rating_text) and 0 < float(rating_text) <= 5:
                rating = rating_text
                break
    total_ratings = "0"
    total_reviews = "0"
    review_patterns = [
        r'(\d+\.?\d*)\s*-\s*([\d,]+)\s*reviews',
        r'(\d+\.?\d*)\s*&\s*([\d,]+)\s*reviews',
        r'([\d,]+)\s*Ratings\s*&\s*([\d,]+)\s*Reviews',
        r'([\d,]+)\s*ratings'
    ]
    page_text = soup.get_text()
    for pattern in review_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        if matches:
            if pattern == r'(\d+\.?\d*)\s*-\s*([\d,]+)\s*reviews':
                rating_match = matches[0][0]
                reviews_match = matches[0][1]
                total_reviews = ''.join(filter(str.isdigit, reviews_match))
                ratings_pattern = r'([\d,]+)\s*ratings'
                ratings_matches = re.findall(ratings_pattern, page_text, re.IGNORECASE)
                if ratings_matches:
                    total_ratings = ''.join(filter(str.isdigit, ratings_matches[0]))
                else:
                    total_ratings = total_reviews
                break
            elif pattern == r'([\d,]+)\s*Ratings\s*&\s*([\d,]+)\s*Reviews':
                total_ratings = ''.join(filter(str.isdigit, matches[0][0]))
                total_reviews = ''.join(filter(str.isdigit, matches[0][1]))
                break
            else:
                if len(matches[0]) >= 1:
                    total_ratings = ''.join(filter(str.isdigit, str(matches[0][0])))
                if len(matches[0]) >= 2:
                    total_reviews = ''.join(filter(str.isdigit, str(matches[0][1])))
                break
    if total_ratings == "0" and total_reviews == "0":
        rating_review_selectors = [
            'span._2_R_DZ',
            'div._2p6lqe',
            '.row._2afbiS',
            'div._3_L3jD',
            'span._13vcmD'
        ]
        for selector in rating_review_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if ' - ' in text and 'reviews' in text.lower():
                    parts = text.split(' - ')
                    if len(parts) > 1:
                        reviews_part = parts[1]
                        total_reviews = ''.join(filter(str.isdigit, reviews_part))
                        total_ratings = total_reviews
                elif 'Ratings' in text and 'Reviews' in text:
                    if '&' in text:
                        parts = text.split('&')
                        if len(parts) >= 1 and 'Ratings' in parts[0]:
                            total_ratings = ''.join(filter(str.isdigit, parts[0]))
                        if len(parts) >= 2 and 'Reviews' in parts[1]:
                            total_reviews = ''.join(filter(str.isdigit, parts[1]))
                elif 'Ratings' in text:
                    total_ratings = ''.join(filter(str.isdigit, text))
                elif 'Reviews' in text:
                    total_reviews = ''.join(filter(str.isdigit, text))
                break
    discount = "0%"
    discount_selectors = [
        'div._3Ay6Sb span',
        'div._3I9_wc',
        '.VGWI6T',
        '.UkUFwK',
        '[class*="discount"]'
    ]
    for selector in discount_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            discount_text = element.get_text(strip=True)
            if '%' in discount_text or 'off' in discount_text.lower():
                discount = discount_text
                break
    print("EXTRACTED DATA:")
    print(f"Name: {name[:50]}...")
    print(f"Price: ₹{price}")
    print(f"Rating: {rating}")
    print(f"Ratings Count: {total_ratings}")
    print(f"Reviews Count: {total_reviews}")
    print(f"Discount: {discount}")
    print("------------------------------------------------------------")
    return {
        'Product_Name': name,
        'Price': price,
        'Discount': discount,
        'Rating': rating,
        'Total_Ratings': total_ratings,
        'Total_Reviews': total_reviews,
        'Product_URL': product_url
    }

def save_to_csv(data, filename='flipkart_products.csv'):
    keys = ['Product_ID', 'Category', 'Product_Name', 'Rating', 'Total_Ratings',
            'Total_Reviews', 'Price', 'Discount', 'Product_URL']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data saved to {filename} with {len(data)} rows")

print("Starting Flipkart Scraper...")
all_data = []
product_id = 1

categories = {
    'Laptop': 'https://www.flipkart.com/search?q=laptops',
    'Mobile': 'https://www.flipkart.com/search?q=mobiles',
    'Tablet': 'https://www.flipkart.com/search?q=tablets'
}

max_products_per_category = 17

for category_name, category_url in categories.items():
    print(f"\n=== Processing {category_name} ===")
    product_links = get_product_links(category_url, max_products_per_category)
    for i, link in enumerate(product_links):
        print(f"\n--- Product {i+1}/{len(product_links)} ---")
        product_info = extract_product_info(link)
        all_data.append({
            'Product_ID': product_id,
            'Category': category_name,
            'Product_Name': product_info['Product_Name'],
            'Rating': product_info['Rating'],
            'Total_Ratings': product_info['Total_Ratings'],
            'Total_Reviews': product_info['Total_Reviews'],
            'Price': product_info['Price'],
            'Discount': product_info['Discount'],
            'Product_URL': product_info['Product_URL']
        })
        product_id += 1
        time.sleep(2)

print(f"\nScraping completed! Total products: {product_id-1}")
save_to_csv(all_data)
driver.quit()
print("Scraping finished!")
