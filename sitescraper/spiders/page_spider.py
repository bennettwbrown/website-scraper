import scrapy
from datetime import datetime
import os
import logging
from urllib.parse import urlparse


def get_base_domain(url):
    """Extract the domain and top-level domain from the URL, excluding subdomains."""
    parsed_uri = urlparse(url)
    domain_parts = parsed_uri.netloc.split(".")
    # Keep only the domain and top-level domain (e.g., example.com)
    domain = ".".join(domain_parts[-2:])
    return domain


class PageSpider(scrapy.Spider):
    name = "page_spider"

    def __init__(self, url_list=None, directory=None, *args, **kwargs):
        super(PageSpider, self).__init__(*args, **kwargs)
        self.start_urls = url_list.split(",") if url_list else []
        self.directory = directory
        self.date = datetime.now().strftime("%d_%m_%Y")
        self.files = {}

    def start_requests(self):
        for url in self.start_urls:
            print("start urls scrape", url)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        base_domain = get_base_domain(response.url)
        filename = os.path.join(self.directory, f"{base_domain}_{self.date}.txt")
        if base_domain not in self.files:
            self.files[base_domain] = open(filename, "a")

        file = self.files[base_domain]
        text_elements = response.xpath(
            "//h1/text() | //h2/text() | //h3/text() | //p/text()"
        ).getall()
        page_text = " ".join(text_elements).strip()
        logging.info(f"Crawled URL: {response.url} with status: {response.status}")

        file.write(f"URL: {response.url}\n{page_text}\n\n")

    def close(self, reason):
        for file in self.files.values():
            file.close()

    def closed(self, reason):
        self.log(f"Spider closed due to: {reason}")
