import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

# Step 1: Get the sitemap URL from robots.txt
print("Fetching robots.txt...")
robots_url = "http://127.0.0.1:5500/robots.txt"  # Change this to the actual domain
headers = {"User-Agent": "Mozilla/5.0"}

sitemap_urls = []  # Initialize sitemap_urls here

# Retry logic for fetching robots.txt
max_retries = 3
for attempt in range(max_retries):
    try:
        robots_response = requests.get(robots_url, headers=headers, timeout=30)  # Increased timeout

        if robots_response.status_code == 200:
            print("Successfully fetched robots.txt.")
            for line in robots_response.text.split("\n"):
                if line.lower().startswith("sitemap:"):
                    sitemap_url = line.split(": ")[1].strip()
                    sitemap_urls.append(sitemap_url)
            print(f"Found {len(sitemap_urls)} sitemap URLs.")
            break  # Exit the loop if successful
        else:
            print(f"Failed to fetch robots.txt with status code: {robots_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching robots.txt: {e}")
        if attempt < max_retries - 1:  # If not the last attempt, wait before retrying
            print("Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying

# Step 2: Fetch all product URLs from the sitemap(s)
if sitemap_urls:  # Check if sitemap_urls is not empty
    product_urls = []

    for sitemap_url in sitemap_urls:
        print(f"Fetching sitemap: {sitemap_url}...")
        try:
            response = requests.get(sitemap_url, headers=headers, timeout=30)  # Increased timeout
            if response.status_code == 200:
                print(f"Successfully fetched sitemap: {sitemap_url}.")
                # Parse XML to extract URLs
                root = ET.fromstring(response.text)
                urls_in_sitemap = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
                print(f"Processing sitemap: {sitemap_url} - Found {len(urls_in_sitemap)} URLs.")
                for url in urls_in_sitemap:
                    loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
                    product_urls.append(loc)
            else:
                print(f"Failed to fetch sitemap: {sitemap_url} with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching sitemap: {sitemap_url} - {e}")

    # Step 3: Save URLs to a file
    print("Saving product URLs to file...")
    with open("product_urls.txt", "w") as f:
        for url in product_urls:
            f.write(url + "\n")

    print(f"Total product URLs indexed: {len(product_urls)}")
else:
    print("No sitemap URLs found. Exiting.")
