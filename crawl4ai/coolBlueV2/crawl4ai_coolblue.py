import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import json
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from laptopSchema import laptopSchemaDTO

SITEMAP_URL = "https://www.coolblue.nl/sitemap/nl_nl/products/17632_laptops.xml"

# Fetch URLs from sitemap
async def fetch_sitemap_urls(sitemap_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(sitemap_url) as response:
            if response.status == 200:
                xml_data = await response.text()
                try:
                    root = ET.fromstring(xml_data)
                    return list({url.text for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")})
                except ET.ParseError as e:
                    print(f"Error parsing XML: {e}")
                    return []
            else:
                print(f"Failed to fetch sitemap: {response.status}")
                return []

# Save the last processed URL to a file
def save_last_processed_url(url):
    with open('last_processed_url.txt', 'w') as f:
        f.write(url)

# Load the last processed URL from a file
def load_last_processed_url():
    if os.path.exists('last_processed_url.txt'):
        with open('last_processed_url.txt', 'r') as f:
            return f.read().strip()
    return None

# Read the existing data from the laptop_data.json file
def read_existing_data(filepath='laptop_data.json'):
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r') as f:
        return [json.loads(line.strip()) for line in f.readlines()]

# Check if a product with the same URL already exists
def is_duplicate(data, filepath='laptop_data.json'):
    existing_data = read_existing_data(filepath)
    existing_urls = {item['url'] for item in existing_data}
    
    for item in data:
        if item['url'] in existing_urls:
            return True  # Duplicate found
    return False

# Main scraping function
async def scrape_laptop_data(urls):
    last_processed_url = load_last_processed_url()

    total_urls = len(urls)
    processed_count = 0  # Initialize processed count

    processed_urls = set()

    if last_processed_url:
        for url in urls:
            if last_processed_url and last_processed_url in urls:
                processed_count = urls.index(last_processed_url) + 1
            else:
                processed_count = 0  # Start fresh if no previous record found

    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )

    extraction = JsonCssExtractionStrategy(laptopSchemaDTO)

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

            result = await crawler.arun(url=url, config=run_config)
            data = json.loads(result.extracted_content)

            for item in data:
                item["url"] = url

            # Only append if not duplicate
            for item in data:
                # Check if the item is a duplicate before writing
                if not is_duplicate([item]):
                    with open('laptop_data.json', 'a') as f:
                        json.dump(item, f)
                        f.write('\n')

            save_last_processed_url(url)

            processed_count += 1
            print(f"{processed_count}/{total_urls} products processed")

            # Introduce a delay after each insert
            await asyncio.sleep(1)

# Main entry point
async def main():
    product_urls = await fetch_sitemap_urls(SITEMAP_URL)

    if not product_urls:
        print("No URLs found in the sitemap.")
        return

    product_urls.sort()

    await scrape_laptop_data(product_urls)

    print("Scraping completed.")

if __name__ == "__main__":
    asyncio.run(main())
