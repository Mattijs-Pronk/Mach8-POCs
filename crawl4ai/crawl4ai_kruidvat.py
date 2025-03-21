import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )
    
    schema = {
        "name": "Links",
        "baseSelector": "div.tile__product-slide-product-name",
        "fields": [
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ],
        "base_url": "https://www.kruidvat.nl/garnier"
    }
    extraction = JsonCssExtractionStrategy(schema)

    run_config = CrawlerRunConfig(
        extraction_strategy=extraction,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        all_links = []
        page = 0

        while True:
            current_url = f"https://www.kruidvat.nl/search?q=garnier&text=garnier&searchType=manual&page={page}&size=100&sort=score"
            result = await crawler.arun(url=current_url, config=run_config)

            if result.success:
                for link in result.links["internal"]:
                    if link['href'].startswith(schema["base_url"]):
                        all_links.append(link['href'])

                next_page_url = f"https://www.kruidvat.nl/search?q=garnier&text=garnier&searchType=manual&page={page + 1}&size=100&sort=score"
                if next_page_url not in [link['href'] for link in result.links["internal"]]:
                    break
                page += 1
            else:
                with open("output_kruidvat.txt", "w") as f:
                    f.write(f"Crawl failed: {result.error_message}\n")
                return

        with open("output_kruidvat.txt", "w") as f:
            for link in all_links:
                f.write(f"{link}\n")

if __name__ == "__main__":
    asyncio.run(main())