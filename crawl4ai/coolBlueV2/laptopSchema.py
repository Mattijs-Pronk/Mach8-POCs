laptopSchemaDTO = {
    "name": "Laptops",
    "baseSelector": ".product-page",
    "fields": [
        {
            "name": "name",
            "selector": ".js-product-name",
            "type": "text"
        },
        {
            "name": "rating",
            "selector": ".review-rating__reviews",
            "type": "text"
        },
        {
            "name": "price",
            "selector": ".sales-price__current",
            "type": "text"
        },
        # artikedingen
        {
            "name": "product_specifications",
            "selector": ".section--2.product-specs--skeleton.js-specifications-content",
            "type": "text"
        }
        
    ]
}