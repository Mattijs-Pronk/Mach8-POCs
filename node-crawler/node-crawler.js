import Crawler from "crawler";
import fs from "fs";
import { url } from "inspector";

const config = {
    maxConnections: 10,
    delay: 1000,
    timeout: 30000,
    
    // urlsToAdd: ["https://www.mach8.io/"],
    urlsToAdd: ["https://www.etos.nl/aanbiedingen/"],
};

// Function to validate URLs
const isValidUrl = (url) => {
    const pattern = new RegExp('^(https?:\\/\\/)?'+
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])?)\\.)+([a-z]{2,}|[a-z\\d-]{2,})|' +
        'localhost|' +
        '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|' +
        '\\[?[a-fA-F0-9]*:[a-fA-F0-9:]+\\]?)' +
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' +
        '(\\?[;&a-z\\d%_.~+=-]*)?' +
        '(\\#[-a-z\\d_]*)?$','i');
    return !!pattern.test(url);
};

// Delay function for rate limiting
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Function to write URLs to a file
const writeUrlsToFile = (urls) => {
    fs.appendFileSync('found_urls.txt', urls.join('\n') + '\n');
};

// Function to handle the crawling process
const handleCrawl = async (error, res, done) => {
    if (error) {
        const url = res && res.request ? res.request.uri.href : 'unknown URL';
        console.error(`Error crawling ${url}:`, error);
        if (res && res.statusCode) {
            console.error(`HTTP Status Code: ${res.statusCode}`);
        }
    } else {
        const dom = res.$;
        console.log(dom("title").text());

        const baseUrl = "https://www.etos.nl";
        const links = dom(".product-grid__tile a").map((index, element) => {
            let url = dom(element).attr("href");
            if (url && !url.startsWith("http")) {
                url = baseUrl + url;
            }
            return isValidUrl(url) ? url : null;
        }).get();

        const uniqueUrls = new Set(links.filter(url => url));

        writeUrlsToFile(Array.from(uniqueUrls));

        uniqueUrls.forEach(url => {
            console.log(`Found URL: ${url}`);
        });
    }
    done();
};

// Crawler configuration
const crawler = new Crawler({
    maxConnections: config.maxConnections,
    timeout: config.timeout,
    skipDuplicates: true,
    userAgents: [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
    ],
    callback: handleCrawl,
});

// Function to add URLs with rate limiting
const addUrls = async (urls) => {
    for (const url of urls) {
        if (isValidUrl(url)) {
            crawler.add(url);
            await delay(config.delay);
        } else {
            console.error(`Invalid URL: ${url}`);
        }
    }
};

addUrls(config.urlsToAdd);
