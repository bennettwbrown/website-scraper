import scrapy
from urllib.parse import urlparse
from datetime import datetime
from usp.tree import sitemap_tree_for_homepage
import os
import logging


def get_base_domain(url):
    """Extract the base domain from the URL"""
    parsed_uri = urlparse(url)
    domain = parsed_uri.netloc
    base_domain = domain.replace("www.", "").split(".")[0]
    return base_domain


def parse_sitemap(url):
    """takes base url and checks site map returning all urls in site map"""
    tree = sitemap_tree_for_homepage(url)
    all_urls = []
    for page in tree.all_pages():
        all_urls.append(page.url)
    return all_urls


class SitemapSpider(scrapy.Spider):
    name = "sitemap_spider"

    def __init__(self, url=None, directory=None, *args, **kwargs):
        super(SitemapSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.start_urls = [f"{url}/sitemap.xml"]
        self.base_domain = get_base_domain(url)  # Set base_domain before using it
        self.date = datetime.now().strftime("%d_%m_%Y")
        self.filename = os.path.join(directory, f"{self.base_domain}_{self.date}.txt")
        self.file = open(self.filename, "a")

    def start_requests(self):
        # Start requests by fetching URLs from the sitemap
        sitemap_urls = parse_sitemap(self.base_url)
        for url in sitemap_urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # Extract text from specific tags
        text_elements = response.xpath(
            "//h1/text() | //h2/text() | //h3/text() | //p/text()"
        ).getall()
        page_text = " ".join(text_elements).strip()
        logging.info(f"Crawled URL: {response.url} with status: {response.status}")
        # Write the text to the file
        self.file.write(f"\n{page_text}\n\n")

    def close(self, reason):
        # Close the file when the spider is closed
        self.file.close()

    # Override the closed method of the scrapy.Spider class
    def closed(self, reason):
        self.log(f"Spider closed due to: {reason}")
        self.log(
            f"Total URLs crawled: {self.crawler.stats.get_value('response_received_count')}"
        )
        self.log(
            f"Total Requests made: {self.crawler.stats.get_value('downloader/request_count')}"
        )
        # Other stats...
