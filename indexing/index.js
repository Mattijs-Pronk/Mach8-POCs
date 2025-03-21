const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function fetchSitemap() {
    const sitemapUrl = 'https://www.trekpleister.nl/sitemap.xml';
    try {
        const response = await axios.get(sitemapUrl);
        return response.data;
    } catch (error) {
        console.error('Error fetching sitemap:', error);
    }
}

async function parseSitemap(sitemapXml) {
    const $ = cheerio.load(sitemapXml, { xmlMode: true });
    const urls = [];
    $('sitemap loc').each((i, elem) => {
        urls.push($(elem).text());
    });
    return urls;
}

async function indexWebsite() {
    const sitemapXml = await fetchSitemap();
    const urls = await parseSitemap(sitemapXml);
    
    // Write the URLs to a JSON file
    fs.writeFileSync('indexed_urls.json', JSON.stringify(urls, null, 2), 'utf-8');
    console.log('Indexed URLs written to indexed_urls.json');

    console.log(`Starting to index ${urls.length} URLs...`);

    for (const [index, url] of urls.entries()) {
        console.log(`Indexing (${index + 1}/${urls.length}): ${url}`);
        // Here you can add more logic to fetch and index each page
    }

    console.log('Indexing complete.');
}

indexWebsite();
