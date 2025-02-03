from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from file_manager import save_products


# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Initialize the WebDriver (replace 'chromedriver_path' with the path to your ChromeDriver)
service = Service(ChromeDriverManager().install())

def scrape_laptop_data(brand):

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL to scrape
    url = f"https://www.zoomit.ir/product/list/laptop/{brand}/"
    # Open the URL
    print('[LOG]: Loading the web page')
    driver.get(url)
    # List to store scraped data
    scraped_data = []
    # Click the "Load More" button five times
    for i in range(4):
        print(f'[LOG]: Initiating a lazy load {i+1}/4')
        try:
            # Locate the "Load More" button
            load_more_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="load-more"]')
            # Click the button
            load_more_button.click()
            # Wait for 5 seconds to allow new content to load
            time.sleep(5)
        except Exception as e:
            print(f"Error clicking 'Load More' button: {e}")
            break
    print('[LOG]: Lazy loading complete')
    # Find all laptop items
    laptop_items = driver.find_elements(By.CSS_SELECTOR, 'div.bg-card.shadow-main.relative.overflow-hidden.rounded-md')
    list_size = len(laptop_items)
    print(f'[LOG]: Length of the list of items retrived: {list_size}')
    # Loop through each laptop item
    for i in range(list_size):
        item = laptop_items[i]
        try:
            # Find the "data container" div
            data_container = None
            try:
                data_container = item.find_element(By.CSS_SELECTOR, 'div[style="width:unset"]')
            except:
                data_container = item.find_element(By.CSS_SELECTOR, 'div[style="width: unset;"]')
            # Extract display size (direct child of data_container)
            display_size_div = data_container.find_element(By.CSS_SELECTOR, 'div > div:nth-child(1)')
            display_size_span = display_size_div.find_element(By.CSS_SELECTOR, 'span:nth-child(2)')
            display_size = display_size_span.text.split()[0]  # Take the first part of the text

            # Extract CPU model (direct child of data_container)
            cpu_div = data_container.find_element(By.CSS_SELECTOR, 'div > div:nth-child(2)')
            cpu_span = cpu_div.find_element(By.CSS_SELECTOR, 'span:nth-child(2)')
            cpu_model = cpu_span.text.replace('اینتل', 'Intel')

            # Extract RAM and storage (direct child of data_container)
            ram_storage_div = data_container.find_element(By.CSS_SELECTOR, 'div > div:nth-child(3)')
            ram_span = ram_storage_div.find_element(By.CSS_SELECTOR, 'span:nth-child(2)')
            storage_span = ram_storage_div.find_element(By.CSS_SELECTOR, 'span:nth-child(3)')
            ram_capacity = ram_span.text.split()[0]
            storage_capacity = storage_span.text.replace('گیگابایت', 'GB').replace('ترابایت', 'TB')

            # Extract price
            price_element = item.find_element(By.CSS_SELECTOR, 'p > span[aria-label="قیمت"]')
            price = price_element.text

            # Append the data to the list
            scraped_data.append({
                'brand': brand,
                'display': float(display_size),
                'cpu': cpu_model,
                'ram': int(ram_capacity),
                'storage': storage_capacity,
                'price': int(price.replace(',', ''))
            })
            print(f'[LOG]: Processing items: {i+1}/{list_size}\r')
        except Exception as e:
            print(f"Error processing an item: {e}")

    print('[LOG]: Processing completed successfully')
    # Close the WebDriver
    driver.quit()
    print('[LOG]: Driver was closed gracefully')
    return scraped_data


def start_scraping():

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

    brands = ['asus', 'hp', 'msi', 'acer', 'lenovo']
    data = []
    for brand in brands:
        print(f'[LOG]: Scraping laptop data, {brand=}')
        data += scrape_laptop_data(brand)
        print(f'[LOG]: Scraping for laptop {brand=} successfully completed')
    print(f'[LOG]: Saving product data to file')
    save_products(pd.DataFrame(data))
    print(f'[LOG]: Product data saved successfully')
