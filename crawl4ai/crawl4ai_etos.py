import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    # 1) Browser config: headless, bigger viewport, no proxy
    browser_conf = BrowserConfig(
        browser_type="chromium",
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )

    # 2) Example extraction strategy
    schema = {
        "name": "Links",
        "baseSelector": "div.tile__product-slide-product-name",
        "fields": [
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ],
        "base_url": "https://www.etos.nl/producten/garnier"
    }
    extraction = JsonCssExtractionStrategy(schema)

    # 3) Crawler run config: skip cache, use extraction
    run_conf = CrawlerRunConfig(
        extraction_strategy=extraction,
        cache_mode=CacheMode.BYPASS,
        # enable_rate_limiting=True,
        # rate_limit_config=RateLimitConfig(
        #     base_delay=(1.0, 3.0),
        #     max_delay=60.0,
        #     max_retries=3,
        #     rate_limit_codes=[429, 503]
        # )
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        all_links = []  # To store all product links

        current_url = "https://www.etos.nl/assortiment/garnier/?sz=9999"
        result = await crawler.arun(url=current_url, config=run_conf)

        if result.success:
            # Process links that fit the schema
            for link in result.links["internal"]:
                    if link['href'].startswith(schema["base_url"]):
                        all_links.append(link['href'])
        else:
            print("Error:", result.error_message)
            return  # Exit if there's an error

        # Write all collected links to the output file
        with open("etos_output.txt", "w") as f:
            for link in all_links:
                f.write(f"{link}\n")  # Write all collected URLs

if __name__ == "__main__":
    asyncio.run(main())