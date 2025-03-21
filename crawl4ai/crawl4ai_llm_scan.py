import openai
import asyncio
import json
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from collections import Counter
import secrets

# API Key and URLs
OPENAI_API_KEY = secrets.OPENAI_API_KEY
# BASE_URL = "http://127.0.0.1:5500/"
# SEARCH_URL = "http://127.0.0.1:5500/"
BASE_URL = "https://www.trekpleister.nl"
SEARCH_URL = "https://www.trekpleister.nl/beauty/make-up"

async def fetch_html(url):
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        viewport_width=1280,
        viewport_height=720
    )
    
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        return result.html

def find_repeating_container(soup):
    potential_containers = soup.find_all(['div', 'ul'])

    best_container = None
    max_similar_children = 0

    for container in potential_containers:
        # Get direct children that are HTML tags (ignore text nodes)
        children = [child for child in container.find_all(recursive=False) if child.name]
        if not children:
            continue

        # Count tag occurrences among children
        tags = [child.name for child in children]
        tag_counts = Counter(tags)
        most_common_tag, count = tag_counts.most_common(1)[0]

        # Select the container with the most repeated structure
        if count > max_similar_children and count > 2:  # Heuristic threshold
            max_similar_children = count
            best_container = container

    print(best_container.find_all(recursive=False)[:3])
    return best_container

def analyze_html_with_openai(html):
    openai.api_key = OPENAI_API_KEY

    prompt = f"""
    Given the following HTML snippet, identify the CSS selectors that would select:
    1. The product URL elements.
    2. The product name elements.

    The HTML contains a container that holds multiple products. Your task is to determine
    the correct selectors inside this container.

    Return response in JSON format exactly like this:
    {{
    "product_url_selector": "CSS Selector",
    "product_name_selector": "CSS Selector"
    }}

    HTML:
    {html[:3500]}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert in analyzing web structures."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing OpenAI response: {e}")
        return None

async def main():
    # Step 1: Fetch HTML from the search page
    html_content = await fetch_html(SEARCH_URL)
    soup = BeautifulSoup(html_content, "html.parser")

    # Step 2: Detect product list container dynamically
    product_container = find_repeating_container(soup)

    if not product_container:
        print("No repeating product container found.")
        return

    # Step 3: Use OpenAI to determine selectors inside the container
    selectors = analyze_html_with_openai(str(product_container))
    
    if not selectors:
        print("Failed to extract selectors from OpenAI.")
        return

    product_url_selector = selectors.get("product_url_selector")
    product_name_selector = selectors.get("product_name_selector")

    if not product_url_selector or not product_name_selector:
        print("OpenAI did not return valid selectors.")
        return

    # Step 4: Extract product links and names using AI-generated selectors
    product_links = [a["href"] for a in product_container.select(product_url_selector)]
    product_names = [element.get_text(strip=True) for element in product_container.select(product_name_selector)]

    products = [{"name": name, "url": f"{BASE_URL}{link}" if link.startswith("/") else link}
                for name, link in zip(product_names, product_links)]

    if not products:
        print("No product links found.")
        return

    # Step 5: Save results to JSON
    output_filename = "crawled_products.json"
    with open(output_filename, "w", encoding="utf-8") as outfile:
        json.dump(products, outfile, ensure_ascii=False, indent=4)
    print(f"Results written to {output_filename}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
