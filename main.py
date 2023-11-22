import subprocess
from urllib.parse import urlparse
from gooey import Gooey, GooeyParser
import os
from datetime import datetime
import logging

APPLICATION_NAME = "website crawler"

logging.getLogger("scrapy").setLevel(logging.INFO)


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
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
    if not parsed.netloc:
        url = url.replace(parsed.path, "www." + parsed.path)
    return url


def run_spider(url, index, directory):
    url = correct_url(url)
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

    for index, url in enumerate(urls):
        # Pass the save_folder as the third argument
        run_spider(url.strip(), index, save_folder)
        print(f"Spider has finished running for {url}!")

    # Inform users about the file location
    print(f"Files are saved in {save_folder}")

    # Open the save folder if the user requested it
    if args.open_folder:
        if os.name == "nt":  # Windows
            os.startfile(save_folder)
        elif os.name == "posix":  # macOS, Linux
            subprocess.run(["open", save_folder])


if __name__ == "__main__":
    main()
