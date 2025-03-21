import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

START_URL = "https://www.kruidvat.nl/"
DOMAIN = urlparse(START_URL).netloc
CRAWLED_URLS = set()
RESULTS = []

async def crawl_page(crawler, url):
    """Fetch, parse, and extract links from a given page."""
    if url in CRAWLED_URLS or DOMAIN not in urlparse(url).netloc:
        return
    
    print(f"Crawling: {url}")
    CRAWLED_URLS.add(url)

    page_content = await crawler.arun(url=url, config=None)
    
    if not page_content.success:
        print(f"Error fetching {url}: {page_content.error_message}")
        return

    html = page_content.html
    soup = BeautifulSoup(html, "html.parser")

    link_containers = soup.find_all(lambda tag: tag.find("a", href=True))
    for container in link_containers:
        heading_tag = container.find(["h1", "h2", "h3"])
        container_title = heading_tag.get_text(strip=True) if heading_tag else None
        
        for link in container.find_all("a", href=True):
            link_text = link.get_text(strip=True)
            full_url = urljoin(url, link["href"])
            title = container_title if container_title else link_text

            if full_url not in {item["url"] for item in RESULTS}:
                RESULTS.append({"title": title, "url": full_url})

    # Find and crawl more internal links
    new_links = {urljoin(url, a["href"]) for a in soup.find_all("a", href=True)}
    internal_links = {link for link in new_links if urlparse(link).netloc == DOMAIN}

    for link in internal_links:
        await crawl_page(crawler, link)



async def main():
    browser_conf = BrowserConfig(browser_type="chromium", headless=True)
    
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        await crawl_page(crawler, START_URL)

    with open("extracted_content.json", "w") as json_file:
        json.dump(RESULTS, json_file, indent=4)

    print(f"✅ Crawling complete! {len(RESULTS)} links saved.")

if __name__ == "__main__":
    asyncio.run(main())
