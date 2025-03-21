bookSchemaDTO = {
    "name": "Books",
    "baseSelector": "#MainContent",
    "fields": [
        {
            "name": "summary",
            "selector": "#shopify-section-template--23719700922641__product_accordion_summary_66E94L .panel",
            "type": "text"
        },
        {
            "name": "price",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Price')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "sku",
            "selector": ".additional-info-table tr:has(td:first-child:contains('SKU')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "isbn_13",
            "selector": ".additional-info-table tr:has(td:first-child:contains('ISBN 13')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "isbn_10",
            "selector": ".additional-info-table tr:has(td:first-child:contains('ISBN 10')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "title",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Title')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "author",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Author')) td a",
            "type": "text"
        },
        {
            "name": "condition",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Condition')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "binding_type",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Binding Type')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "publisher",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Publisher')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "year_published",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Year published')) td:nth-of-type(2)",
            "type": "text"
        },
        {
            "name": "number_of_pages",
            "selector": ".additional-info-table tr:has(td:first-child:contains('Number of pages')) td:nth-of-type(2)",
            "type": "text"
        }
    ]
}

