from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import socket

urls = [
    "http://example.com",
    "http://quotes.toscrape.com",
    "http://httpbin.org/get"
]

def fetch_metadata_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce bot detection
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    start_time = time.time()
    driver.get(url)
    end_time = time.time()

    metadata = {
        "url": url,
        "status_code": driver.execute_script("return document.readyState"),  # Check page load status
        "response_time": round(end_time - start_time, 4),
        "content_length": len(driver.page_source),
        "ip_address": socket.gethostbyname(url.split("//")[1].split("/")[0])
    }

    print(metadata)
    driver.quit()
    return metadata

# Fetch metadata using Selenium
data = [fetch_metadata_selenium(url) for url in urls]
