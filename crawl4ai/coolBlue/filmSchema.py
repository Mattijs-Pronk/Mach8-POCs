filmSchemaDTO = {
    "name": "Films",
    "baseSelector": ".athenaProductPage_topRow",
    "fields": [
        {
            "name": "title",
            "selector": ".productName_title",
            "type": "text"
        },
        {
            "name": "price",
            "selector": ".productPrice_price",
            "type": "text"
        },
        {
            "name": "description",
            "selector": ".productDescription_synopsisContent",
            "type": "text"
        },
        {
            "name": "studio",
            "selector": ".productDescription_contentPropertyValue_studio li",
            "type": "text"
        },
        {
            "name": "run_time",
            "selector": ".productDescription_contentPropertyValue_RunTime li",
            "type": "text"
        },
        {
            "name": "certificate",
            "selector": ".productDescription_contentPropertyValue_certificate li",
            "type": "text"
        },
        {
            "name": "main_language",
            "selector": ".productDescription_contentPropertyValue_mainLanguage li",
            "type": "text"
        },
        {
            "name": "number_of_discs",
            "selector": ".productDescription_contentPropertyValue_numberDisks li",
            "type": "text"
        },
        {
            "name": "director",
            "selector": ".productDescription_contentPropertyValue_director li",
            "type": "text"
        },
        {
            "name": "dubbing_languages",
            "selector": ".productDescription_contentPropertyValue_dubbingLanguage li",
            "type": "text"
        },
        {
            "name": "subtitle_languages",
            "selector": ".productDescription_contentPropertyValue_subtitleLanguage li",
            "type": "text"
        },
        {
            "name": "theatrical_release_year",
            "selector": ".productDescription_contentPropertyValue_TheatricalReleaseYear li",
            "type": "text"
        },
        {
            "name": "region",
            "selector": ".productDescription_contentPropertyValue_region li",
            "type": "text"
        }
    ]
}
