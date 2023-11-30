import subprocess
from urllib.parse import urlparse
from gooey import Gooey, GooeyParser
import os
from datetime import datetime
import logging

APPLICATION_NAME = "Copy Harvester"
# Copy Combine.
logging.getLogger("scrapy").setLevel(logging.INFO)


# TODO -  ALLOW ONLY ONE URL FOR SITEMAP TO BE SCRAPPED. AND TO PROVIDE FEEDBACK


def create_today_directory():
    # Define the base output directory
    output_dir = "output"

    # Ensure the base output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get today's date in the format dd-mm-yyyy
    today = datetime.now().strftime("%d-%m-%Y")
    # Create the directory name as a sub-directory within /output/
    directory_name = os.path.join(output_dir, today)

    # Check if the directory exists
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory created: {directory_name}")
    else:
        print(f"Directory already exists: {directory_name}")

    return directory_name


def correct_url(url):
    """Correct the URL if necessary"""
    try:
        parsed = urlparse(url, "http")
        if not parsed.netloc:
            # If the netloc is missing, assume the path is the netloc
            # This handles cases like 'example.com'
            parsed = parsed._replace(netloc=parsed.path, path="")
        if not parsed.scheme:
            # Default to http if the scheme is missing
            parsed = parsed._replace(scheme="http")

        corrected_url = parsed.geturl()
        return corrected_url
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None


def run_page_spider(url, directory):
    """
    Function to handle scraping of multiple URLs.
    urls: A list of URLs.
    directory: The directory where the scraped data will be saved.
    """
    print("run page spider ", url)
    print(type(url))
    url = correct_url(url)
    if url is None:
        print("Invalid URL provided.")
        return

    command = f"scrapy crawl page_spider -a url_list='{url}' -a directory={directory}"
    print("Command:", command)  # Debugging print statement
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


def run_sitemap_spider(url, index, directory):
    url = correct_url(url)
    print(type(url))
    if url is None:
        print("Invalid URL provided.")
        return
    # Update the command to save output to different files based on the URL index
    command = f"scrapy crawl sitemap_spider -a url={url} -a directory={directory}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


@Gooey(
    program_name=APPLICATION_NAME,
    terminal_font_family="Consolas",
    terminal_font_size=12,
)
def main():
    parser = GooeyParser(description="Enter URLs to crawl")

    # parser.add_argument(
    #     "--scrape_method",
    #     help="Choose the scraping method",
    #     choices=["Sitemap", "Specific URL"],
    #     default="Sitemap",
    # )
    parser.add_argument(
        "URLs", help="Enter URLs separated by commas", widget="Textarea"
    )
    parser.add_argument(
        "--open_folder",
        action="store_true",
        help="Open the folder where files are saved after completion",
    )

    args = parser.parse_args()
    urls = args.URLs.split(",")

    # Create today's directory and save its path
    save_folder = create_today_directory()
    print("URLS TO PASS  ", urls)
    for index, url in enumerate(urls):
        url = url.strip()
        # if args.scrape_method == "Sitemap":
        # run_sitemap_spider(url, index, save_folder)
        # elif args.scrape_method == "Specific URL":
        run_page_spider(url, save_folder)
        print(f"Spider has finished running for {url}!")


if __name__ == "__main__":
    main()
