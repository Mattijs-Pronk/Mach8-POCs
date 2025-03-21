import asyncio
import json
import os
import xml.etree.ElementTree as ET
import aiohttp
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from houseSchema import houseSchemaDTO
from laptopSchema import laptopSchemaDTO
from bookSchema import bookSchemaDTO
from filmSchema import filmSchemaDTO

SITEMAP_PATH = "arrowfilms_films.xml"

# Select the appropriate DTO based on the source
SELECTED_DTO = filmSchemaDTO

def fetch_sitemap_urls_from_file():
    try:
        with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
            xml_data = f.read()
            root = ET.fromstring(xml_data)

            # Define the XML namespace
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # Extract all <loc> elements
            loc_elements = root.findall(".//ns:loc", namespace)

            urls = [url.text for url in loc_elements]
            return urls

    except FileNotFoundError:
        print(f"❌ Error: The file '{SITEMAP_PATH}' was not found. Download the sitemap manually.")
        return []
    except ET.ParseError as e:
        print(f"❌ Error parsing XML: {e}")
        return []

# Function to save the last processed URL to a file
def save_last_processed_url(url):
    with open('last_processed_url.txt', 'w') as f:
        f.write(url)

# Function to load the last processed URL from a file
def load_last_processed_url():
    if os.path.exists('last_processed_url.txt'):
        with open('last_processed_url.txt', 'r') as f:
            return f.read().strip()
    return None

# Function to check if the URL is accessible (status code 200)
async def is_url_accessible(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
                else:
                    print(f"❌ URL not accessible (status code {response.status}): {url}")
                    return False
    except Exception as e:
        print(f"❌ Error accessing {url}: {e}")
        return False

async def scrape_data(urls):
    last_processed_url = load_last_processed_url()
    processed_urls = set()
    total_urls = len(urls)
    processed_count = 0

    # Determine the last processed index
    if last_processed_url and last_processed_url in urls:
        processed_count = urls.index(last_processed_url) + 1
    else:
        processed_count = 0  # Start fresh if no previous record

    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )

    extraction = JsonCssExtractionStrategy(SELECTED_DTO)

    run_config = CrawlerRunConfig(
        extraction_strategy=extraction,
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["nav", "footer", "header"],
        exclude_external_links=True,
        remove_forms=True,
        stream=True,
    )

    async with AsyncWebCrawler() as crawler:
        for url in urls:
            if url in processed_urls or (last_processed_url and url <= last_processed_url):
                continue

            processed_urls.add(url)

            # Check if the URL is accessible before trying to scrape
            if not await is_url_accessible(url):
                continue  # Skip the URL if it's not accessible

            try:
                result = await crawler.arun(url=url, config=run_config)
                data = json.loads(result.extracted_content)

                for item in data:
                    item["url"] = url
                    with open('scraped_data.json', 'a', encoding='utf-8') as f:
                        if f.tell() > 0:
                            f.write(",\n")
                        json.dump(item, f, ensure_ascii=False, indent=4)

                save_last_processed_url(url)

                processed_count += 1
                print(f"{processed_count}/{total_urls} items processed")
            except Exception as e:
                # Handle the error (e.g., skip the URL and log it)
                print(f"❌ Failed to process {url}: {e}")
            
            await asyncio.sleep(1)  # Prevent excessive requests

async def main():
    product_urls = fetch_sitemap_urls_from_file()

    if not product_urls:
        print("❌ No URLs found in the sitemap.")
        return
    
    product_urls.sort()

    await scrape_data(product_urls)

    print("Scraping completed.")

if __name__ == "__main__":
    asyncio.run(main())
