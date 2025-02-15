import scrapy
import csv
import json
import os

class MetadataSpider(scrapy.Spider):
    name = "metadata_spider"

    # Default starting URL
    default_url = 'https://www.bbc.com/'

    custom_settings = {
        'FEEDS': {
            'C://Users//ADMIN//Desktop//test_scrapy//net_data.csv': {
                'format': 'csv',
                'fields': ['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 
                           'Request Headers', 'Response Headers', 'Content Length', 'User Agent', 
                           'Redirected URLs', 'Encoding', 'Cookies'],
            },
        }
    }

    def __init__(self, url=None, *args, **kwargs):
        """
        Initialize the spider with a starting URL.
        :param url: The URL to scrape, passed as a parameter.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = [url] if url else [self.default_url]

        # Check if the CSV file exists, if not, create it with headers
        file_path = 'C://Users//ADMIN//Desktop//test_scrapy//net_data.csv'
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth', 'IP Address', 
                                 'Request Headers', 'Response Headers', 'Content Length', 
                                 'User Agent', 'Redirected URLs', 'Encoding', 'Cookies'])

    def parse(self, response):
        # Extract metadata
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

        # Write to CSV
        file_path = 'C://Users//ADMIN//Desktop//test_scrapy//net_data.csv'
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(metadata.values())

        self.logger.info(f"Successfully processed {response.url}")

        # Follow pagination links (if any)
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
