import os
import json
import asyncio
from typing import List
from pydantic import BaseModel, Field, HttpUrl
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import secrets

class Product(BaseModel):
    url: HttpUrl

class KnowledgeGraph(BaseModel):
    products: List[Product]

async def main():
    llm_strategy = LLMExtractionStrategy(
        provider="openai/gpt-4o-mini",
        api_token=secrets.OPENAI_API_KEY,
        schema=KnowledgeGraph.model_json_schema(),
        extraction_type="schema",
        instruction="Extract the exact product page URLs from this website, nothing else. Do not include duplicate or broken links.",
        chunk_token_threshold=1200,
        overlap_rate=0.1,
        apply_chunking=True,
        input_format="html",
        extra_args={"temperature": 0.0},
        verbose=True,
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        check_robots_txt=True,
        pdf=False,
        screenshot=False,
    )

    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # result = await crawler.arun(url="http://127.0.0.1:5500/index.html", config=crawl_config)
        result = await crawler.arun(url="https://www.kruidvat.nl/search?q=garnier&text=garnier&searchType=manual", config=crawl_config)
        if result.success:
            
            articles = json.loads(result.extracted_content)
            # print(articles)
            extracted_urls = [item["url"] for item in articles if "url" in item and item["url"]]


            # Filter out None values (invalid URLs)
            product_links = [url for url in extracted_urls if url]

            # Save to JSON
            with open("product_links.json", "w") as f:
                json.dump(product_links, f, indent=4)

        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
