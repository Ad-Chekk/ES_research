import scrapy
import csv
import json
import os

class MetadataSpider(scrapy.Spider):
    name = "metadata_spider"

    # Default list of URLs to scrape
    start_urls = [
    # "https://www.bbc.com",
    # "https://www.cnn.com",
    # "https://timesofindia.indiatimes.com",
    # "https://www.theguardian.com/international",
    "https://www.amazon.com",  
    "https://www.flipkart.com",
    "https://www.ebay.com",
    "https://www.alibaba.com",
    "https://www.walmart.com",
    # "https://httpbin.org/get",
    # "https://www.wikipedia.org",
    # "https://jsonplaceholder.typicode.com/posts",
    # "http://example.com"
    ]

    # CSV file path
    file_path = 'C://Users//ADMIN//Desktop//test_scrapy//net_data.csv'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'ROBOTSTXT_OBEY': False,
    'DOWNLOAD_DELAY': 2,  # Wait 2 sec to reduce detection
    'DEFAULT_REQUEST_HEADERS': {
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    },
        'FEEDS': {
            file_path: {
                'format': 'csv',
                'fields': ['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 
                           'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 
                           'Redirected URLs', 'Encoding', 'Cookies'],
            },
        }
    }

    def __init__(self, urls=None, *args, **kwargs):
        """
        Initialize the spider with a list of URLs.
        :param urls: Comma-separated list of URLs passed as a parameter.
        """
        super().__init__(*args, **kwargs)

        # If URLs are passed via command line, use those instead of default
        if urls:
            self.start_urls = urls.split(',')

        # Ensure the CSV file exists with headers
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 
                                 'Request Headers', 'Response Headers', 'Content Length', 
                                 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'])

    def parse(self, response):
        """ Extract metadata and append to CSV """
        metadata = {
            "URL": response.url,
            "Status Code": response.status,
            "Response Time (s)": response.meta.get('download_latency', 'N/A'),
            "Content Length": len(response.body),
            "Depth": response.meta.get('depth', 0),
            "IP Address": response.meta.get("download_slot"),
            "Request Headers": json.dumps({k.decode(): v[0].decode() for k, v in response.request.headers.items()}),
            "Response Headers": json.dumps({k.decode(): v[0].decode() for k, v in response.headers.items()}),
            "User Agent": response.request.headers.get('User-Agent', b'N/A').decode(),
            "Redirected URLs": ', '.join(response.meta.get('redirect_urls', [])),
            "Encoding": response.encoding if response.encoding else 'N/A',
            "Cookies": json.dumps(response.headers.getlist('Set-Cookie')),
        }

        # Append to CSV
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(metadata.values())

        self.logger.info(f"Successfully processed {response.url}")
