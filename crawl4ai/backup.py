import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import json
from bs4 import BeautifulSoup

async def main():
    url = "https://www.kruidvat.nl/search?q=garnier&text=garnier&searchType=manual&page=0&size=200&sort=score"
    
    browser_conf = BrowserConfig(
        browser_type="chromium",
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        # Fetch the HTML content first
        page_content = await crawler.arun(url=url, config=None)
        
        if not page_content.success:
            print("Error fetching page:", page_content.error_message)
            return

        html = page_content.html  # Updated to access the correct attribute for HTML content
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Find all containers with at least one <a> tag
        link_containers = soup.find_all(lambda tag: tag.find("a", href=True))

        if not link_containers:
            print("No link-containing elements found.")
            return
        
        links_with_titles = []
        for container in link_containers:
            # Find the heading (h1, h2, h3) inside the same container
            heading_tag = container.find(["h1", "h2", "h3"])
            container_title = heading_tag.get_text(strip=True) if heading_tag else None
            
            # Extract all <a> tags with href inside the container
            links = container.find_all("a", href=True)
            for link in links:
                link_text = link.get_text(strip=True)  # Get <a> text
                
                # Use container heading as title, otherwise fallback to <a> text
                title = container_title if container_title else link_text
                url = link["href"]

                links_with_titles.append({"title": title, "url": url})

        # Remove duplicates while preserving structure (based on unique URLs)
        links_with_titles = list({v['url']: v for v in links_with_titles}.values())

        print("Extracted links with titles:", links_with_titles)

        # Write to JSON file
        with open('extracted_content.json', 'w') as json_file:
            json.dump(links_with_titles, json_file, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
