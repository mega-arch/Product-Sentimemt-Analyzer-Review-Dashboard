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
    
    for i in range(5):
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i/4});")
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
                print(f"Found price: ₹{price}")
                break

    rating = "0"
    rating_selectors = [
        'div._3LWZlK',
        'div._2d4LTz',
        '.XQDdHH',
        'div._3lS5K4',
        '[class*="rating"]',
        'div._2d4LTz._1mR1Nw',
        'div._3LWZlK._1D-8OL'
    ]
    for selector in rating_selectors:
        element = soup.select_one(selector)
        if element and element.get_text(strip=True):
            rating_text = element.get_text(strip=True)
            if re.match(r'^\d+(\.\d+)?$', rating_text) and 0 < float(rating_text) <= 5:
                rating = f"{rating_text}★"
                break

    total_ratings = "0"
    total_reviews = "0"
    
    # METHOD 1: Look for ALL possible rating-review containers
    rating_review_selectors = [
        'span._2_R_DZ',
        'div._3UAT2v',
        'div._1e6HeN',
        'div.row._2afbiS',
        'div._2p6lqe',
        'div._3Ay6Sb',
        'div._1dqRvU',
        'div._16Jk6d',
        'div._1Gn1Td',
        'div._3_L3jD',
        'span._13vcmD',
        'div.col._2wzgFH',
        'div._1rc-Qu',
        'div._1YokD2._3Mn1Gg'
    ]
    
    for selector in rating_review_selectors:
        elements = soup.select(selector)
        for element in elements:
            text = element.get_text(strip=True)
            print(f"Checking container: {text}")
            
            # Look for "X,X Ratings & X,X Reviews" pattern
            match = re.search(r'([\d,]+)\s*Ratings?\s*&\s*([\d,]+)\s*Reviews?', text)
            if match:
                total_ratings = match.group(1).replace(',', '')
                total_reviews = match.group(2).replace(',', '')
                print(f"Found in container: {total_ratings} ratings, {total_reviews} reviews")
                break
            
            # Look for just ratings
            ratings_match = re.search(r'([\d,]+)\s*Ratings?', text)
            if ratings_match:
                total_ratings = ratings_match.group(1).replace(',', '')
                print(f"Found ratings in container: {total_ratings}")
                
                # Try to find reviews in the same container
                reviews_match = re.search(r'([\d,]+)\s*Reviews?', text)
                if reviews_match:
                    total_reviews = reviews_match.group(1).replace(',', '')
                    print(f"Found reviews in container: {total_reviews}")
                break
        
        if total_ratings != "0":
            break
    
    # METHOD 2: If still not found, look for any text containing "Ratings" or "Reviews"
    if total_ratings == "0":
        # Find all elements that contain "Ratings" or "Reviews"
        ratings_elements = soup.find_all(string=re.compile(r'Ratings?|Reviews?', re.IGNORECASE))
        for element in ratings_elements:
            if element.parent:
                parent_text = element.parent.get_text(strip=True)
                print(f"Found ratings/reviews text: {parent_text}")
                
                # Look for patterns in this text
                match = re.search(r'([\d,]+)\s*Ratings?\s*&\s*([\d,]+)\s*Reviews?', parent_text)
                if match:
                    total_ratings = match.group(1).replace(',', '')
                    total_reviews = match.group(2).replace(',', '')
                    print(f"Found in text: {total_ratings} ratings, {total_reviews} reviews")
                    break
                
                ratings_match = re.search(r'([\d,]+)\s*Ratings?', parent_text)
                if ratings_match:
                    total_ratings = ratings_match.group(1).replace(',', '')
                    print(f"Found ratings in text: {total_ratings}")
                    
                    reviews_match = re.search(r'([\d,]+)\s*Reviews?', parent_text)
                    if reviews_match:
                        total_reviews = reviews_match.group(1).replace(',', '')
                        print(f"Found reviews in text: {total_reviews}")
                    break
    
    # METHOD 3: Look for numbers near the rating stars
    if total_ratings == "0" and rating != "0":
        # Find rating element and look around it
        rating_element = soup.select_one('div._3LWZlK, div._2d4LTz, [class*="rating"]')
        if rating_element:
            # Check parent
            parent = rating_element.parent
            if parent:
                parent_text = parent.get_text()
                ratings_match = re.search(r'([\d,]+)\s*Ratings?', parent_text)
                if ratings_match:
                    total_ratings = ratings_match.group(1).replace(',', '')
                    print(f"Found ratings near rating: {total_ratings}")
            
            # Check siblings
            if total_ratings == "0":
                for sibling in rating_element.find_next_siblings():
                    sibling_text = sibling.get_text()
                    ratings_match = re.search(r'([\d,]+)\s*Ratings?', sibling_text)
                    if ratings_match:
                        total_ratings = ratings_match.group(1).replace(',', '')
                        print(f"Found ratings in sibling: {total_ratings}")
                        break
    
    # METHOD 4: Final comprehensive search in page text
    if total_ratings == "0":
        page_text = soup.get_text()
        
        # Look for all instances of "Ratings" with numbers
        all_ratings_matches = re.findall(r'(\d{1,3}(?:,\d{3})*)\s*Ratings?', page_text)
        for match in all_ratings_matches:
            rating_num = match.replace(',', '')
            if rating_num.isdigit():
                rating_int = int(rating_num)
                # Reasonable range for ratings
                if 1 <= rating_int <= 100000:
                    total_ratings = rating_num
                    print(f"Found ratings in page: {total_ratings}")
                    break
    
    if total_reviews == "0":
        page_text = soup.get_text()
        all_reviews_matches = re.findall(r'(\d{1,3}(?:,\d{3})*)\s*Reviews?', page_text)
        for match in all_reviews_matches:
            review_num = match.replace(',', '')
            if review_num.isdigit():
                review_int = int(review_num)
                if 1 <= review_int <= 100000:
                    total_reviews = review_num
                    print(f"Found reviews in page: {total_reviews}")
                    break

    # If still 0, the product might genuinely have no ratings/reviews
    if total_ratings == "0" and total_reviews == "0":
        print("Product appears to have no ratings and reviews")

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
    'Laptop': 'https://www.flipkart.com/search?q=laptops&page=1',
    'Mobile': 'https://www.flipkart.com/search?q=mobiles&page=1', 
    'Tablet': 'https://www.flipkart.com/search?q=tablets&page=1',
    'Headphones': 'https://www.flipkart.com/search?q=headphones&page=1',
    'Smartwatch': 'https://www.flipkart.com/search?q=smartwatch&page=1',
    'Camera': 'https://www.flipkart.com/search?q=camera&page=1',
    'Television': 'https://www.flipkart.com/search?q=television&page=1',
    'Printer': 'https://www.flipkart.com/search?q=printer&page=1',
    'Speaker': 'https://www.flipkart.com/search?q=speaker&page=1',
    'Gaming': 'https://www.flipkart.com/search?q=gaming%20laptop&page=1',
    'Refrigerator': 'https://www.flipkart.com/search?q=refrigerator&page=1',
    'Washing_Machine': 'https://www.flipkart.com/search?q=washing%20machine&page=1'
}

max_products_per_category = 25

for category_name, category_url in categories.items():
    print(f"\n=== Processing {category_name} ===")
    product_links = get_product_links(category_url, max_products_per_category)
    
    pages_to_try = 3
    current_page = 2
    while len(product_links) < max_products_per_category and current_page <= pages_to_try:
        print(f"Only found {len(product_links)} products, trying page {current_page}...")
        next_page_url = category_url.replace('page=1', f'page={current_page}')
        additional_links = get_product_links(next_page_url, max_products_per_category - len(product_links))
        product_links.extend(additional_links)
        current_page += 1
    
    for i, link in enumerate(product_links):
        print(f"\n--- {category_name} - Product {i+1}/{len(product_links)} ---")
        try:
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
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping product {i+1}: {e}")
            continue

print(f"\nScraping completed! Total products: {len(all_data)}")
print(f"Expected: {len(categories) * max_products_per_category} products")
save_to_csv(all_data)
driver.quit()
print("Scraping finished!")