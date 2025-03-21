from qdrant_client import models, QdrantClient
import json
from qdrant_client.models import PointStruct, VectorParams, Distance
import json
import openai
import secrets

# OpenAI client initialization
openai_client = openai.Client(
    api_key=secrets.OPENAI_API_KEY
)

system_prompt_generate_global_template = """
You have a list of products within the same category. Your task is to generate a **single global template** that represents the most crucial and common features of these products.  

### Instructions:  
- Analyze all products and extract the most **relevant and important** features.
- For each feature, assign a **tier** based on general categories without being overly specific. For example, the **CPU** could be categorized as "Low", "Medium", or "High" based on its performance level; similarly, **Operating System** might be categorized as "Windows", "Linux", or "MacOS". 
  - The **tier** should reflect the general level of the feature across the product range, not individual products.
  - The **tier** should always use categories such as ["Low", "Medium", "High"] based on the general feature level across all products.
- For each feature:
  - **Feature Name** (e.g., "Battery Life")
  - **Tier Options**: Provide a list of tiers such as ["Low", "Medium", "High"].
  - **Explanation**: Briefly explain why this feature matters in this product category.
Ensure that this is a **single unified template** summarizing the category, **not** individual product templates.

### Output Format Example:
{
  "Category": "Laptops",
  "Price": "399",
  "PriceIndication": "Affordable",
  "features": [
        {
            "featureName": "Battery Life",
            "tierOptions": ["Short", "Average", "Long"],
            "explanation": "Long battery life is crucial for professionals and students who need portability without frequent charging."
        },
        {
            "featureName": "CPU Performance",
            "tierOptions": ["Low", "Medium", "High"],
            "explanation": "A powerful processor ensures smooth performance for multitasking and demanding applications."
        },
        {
            "featureName": "Operating System",
            "tierOptions": ["Windows", "Linux", "MacOS"],
            "explanation": "An operating system offers a user interface and enhances the overall user experience."
        }
    ]
}

### Additional Rules:  
- **Prioritize essential features** based on how frequently they appear and their impact on the user experience.  
- Be **concise and precise** in explanations.  
- Avoid product-specific details; focus on the **category as a whole**.
- The system should automatically identify the most common levels of each feature, ensuring the tiers are relevant to the overall product range and not to individual products.
"""

system_prompt_generate_global_template2 = """
You have a comprehensive list of products within a given category. Your task is to generate a single, global, and versatile template that captures every crucial feature shared by these products—both common and additional attributes—regardless of product category (e.g., electronics, clothing, vehicles, etc.).

### Instructions:
- **Analyze all products** in the category and extract both:
  - **Primary features**: Core aspects that fundamentally define the product (e.g., functionality, design, material).
  - **Secondary features**: Additional aspects that enhance the product's appeal (e.g., special features, user convenience, aesthetics).
- **Ensure comprehensive coverage** by including both physical attributes (e.g., size, weight, material type, build quality, design style) and functional attributes (e.g., performance, durability, comfort, energy efficiency, usability).
- **Include all identified features** and, for each feature, specify whether it is primary or secondary.
- **Sort the features**: Arrange the features so that the most relevant (primary) features are listed first, followed by the secondary features.
- The template should be flexible and applicable to any product category by allowing customization of the "Category" field and feature list. If a specific attribute does not apply to a given category, it may be omitted or replaced.

### Feature Structuring:
For each feature, assign a **tier** based on a structured scale relevant to that feature:
- **Default tier**: Use ["Low", "Medium", "High"] for performance or capacity-based features.
- **Alternative tiers** when appropriate:
  - For size-related features → ["Small", "Medium", "Large"]
  - For build quality or material type → ["Basic", "Standard", "Premium"]
  - For weight → ["Light", "Moderate", "Heavy"]
  - For specialized features such as operating systems, engine types, or style → use the specific categories relevant to the product (e.g., ["Gasoline", "Hybrid", "Electric"] for cars or ["Casual", "Formal", "Sport"] for clothing).

Each feature entry should follow this **EXACT** format:
  - **Feature Name**: A concise title (e.g., "Performance", "Material", "Engine Power", "Fabric Type", "Design").
  - **Tier Options**: A list of one-word levels.
  - **Explanation**: A brief statement on why this feature is significant for the product category.

---

### Output Format Example (Generic):

```json
{
  "Category": "<CategoryName>",
  "PriceRange": "Mixed",
  "features": [
    {
      "featureName": "Performance",
      "tierOptions": ["Low", "Medium", "High"],
      "explanation": "Indicates overall efficiency and user experience."
    },
    {
      "featureName": "Build Quality",
      "tierOptions": ["Basic", "Standard", "Premium"],
      "explanation": "Reflects durability and material quality."
    },
    {
      "featureName": "Size/Portability",
      "tierOptions": ["Small", "Medium", "Large"],
      "explanation": "Affects ease of transport and suitability for various uses."
    }
  ]
}

Deliver the output in a **structured format** that is easy to process.
"""


system_prompt_structure_data_from_generated_template = """
You will receive a **global template structure** for products within a specific category. Your task is to accurately apply this template to **each individual product** in the dataset.

### Processing Guidelines:
1. **Maintain Structure**: Fill in the global template for each product, ensuring correct field assignments.
2. **Ensure Relevance**: Assess each feature’s importance for the product and assign the appropriate **tier** based on its relative level in the product range (e.g., based on performance, size, functionality). The tier should be **automatically inferred** based on the features in the dataset, selecting the most appropriate option from the **tier options** in the global template.
3. **Select Tier from Options**: For each feature:
   - Review the **tier options** from the global template (e.g., ["Low", "Medium", "High"], ["Windows", "Linux", "MacOS"],["Short", "Average", "Long"]).
   - Based on the product's specifications, you **MUST** select the most appropriate tier, this can only be 1. This should reflect the feature's relative level in the product compared to the overall product range.
4. **Create Relevant Explanations**: For each feature, provide **clear, concise, and understandable explanations** using the **specific product details**. The explanation should directly reflect how the feature **adds value** to the product.
   - **Example**: For a product with a 10-hour battery life, you might write: "With its 10-hour battery life, this product allows for uninterrupted use throughout the day, ideal for users who need a reliable device for work or travel."
   - Ensure each explanation uses the **exact product details** (e.g., "10-hour battery", "high-definition display") to make the explanation relevant and tailored to that product.
   - Focus on the benefit of the feature in terms of **practical use** for the end user.
5. **Handle Irrelevant Features Flexibly**: If a feature is not applicable to a product, leave it blank or skip it.

### Input Data:
- **Global Template:**  
  {global_template}
  
- **Product Data:**  
  {product_data}

### Output Requirements:
For each product, provide a **fully populated version of the template** with:
- **Category**
- **Product name**
- **Price** (real price)
- **Price indication**: Determine this relative to the typical price range for the product's category. For example, a price of 300 should be interpreted as "Cheap" for a laptop but "Expensive" for a shirt.
- **Features** with the appropriate **tier** (selected from the options in the global template) and **explanation** for each feature. The tier should be **automatically inferred** based on the product data, not pre-defined.

Deliver the output in a **structured format** that is easy to process.
"""

# Functions to generate global template
def generate_global_template(products):
    response = openai_client.chat.completions.create(
        model="o1",
        # model="o3-mini",
        messages=[{"role": "system", "content": system_prompt_generate_global_template2 + "\nIMPORTANT: Respond ONLY with valid JSON. Do not include any other text."},
                  {"role": "user", "content": json.dumps(products, indent=2)}],
        max_completion_tokens=4500,
        response_format={"type": "json_object"},
    )
    
    content = response.choices[0].message.content.strip()
    return content

def generate_template_data_input(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    first_10_products = data[:10]

    global_template = generate_global_template(first_10_products)

    global_template_json = json.loads(global_template)

    with open(output_file, 'w') as outfile:
        json.dump(global_template_json, outfile, indent=2)

    print(f"Global template has been saved to {output_file}")

# Functions to generate structured data according to the generated global tempplate
def generate_structured_data(global_template, product_data):
    system_prompt = system_prompt_structure_data_from_generated_template.format(
        global_template=json.dumps(global_template, indent=2),
        product_data=json.dumps(product_data, indent=2)
    )
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        # model="o3-mini",
        messages=[{"role": "system", "content": system_prompt + "\nIMPORTANT: Respond ONLY with valid JSON. Do not include any other text."},
                  {"role": "user", "content": json.dumps(product_data, indent=2)}],
        # max_completion_tokens=3000,
        response_format={"type": "json_object"},
        temperature=0.2
    )
    
    content = response.choices[0].message.content.strip()

    return content

def process_products_for_structured_data(input_file, global_template_file, output_file):
    with open(global_template_file, 'r') as file:
        global_template = json.load(file)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            products2 = json.load(file)
            # Dit later weghalen om alles te verwerken
            products = products2[:5]
            # Dit later weghalen om alles te verwerken
            print(f"\nSuccessfully loaded {len(products)} products from {input_file}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {input_file}: {e}")
        return
    
    processed_products = []
    failed_products = []
    
    for i, product in enumerate(products, 1):
        if not product:
            print("Leeg product overgeslagen.")
            continue

        print(f"\n{'='*50}")
        print(f"Processing product {i}/{len(products)}: {product.get('name', 'Unnamed')}")
        
        try:
            structured_product = generate_structured_data(global_template, product)
            
            if structured_product:
                try:
                    structured_data = json.loads(structured_product)
                    processed_products.append(structured_data)
                    print(f"✓ Successfully processed and added product {i}")
                except json.JSONDecodeError as e:
                    print(f"✗ JSON parsing error for product {product.get('name', 'Unnamed')}")
                    print(f"Error details: {e}")
                    print(f"First 200 characters of problematic JSON: {structured_product[:200]}")
                    failed_products.append({"name": product.get('name'), "error": "JSON parsing error"})
            else:
                print(f"✗ No data extracted for {product.get('name', 'Unnamed')}")
                failed_products.append({"name": product.get('name'), "error": "No data extracted"})
        except Exception as e:
            print(f"✗ Unexpected error processing product {i}: {str(e)}")
            failed_products.append({"name": product.get('name'), "error": str(e)})

    print(f"\n{'='*50}")
    print(f"Processing Summary:")
    print(f"Total products attempted: {len(products)}")
    print(f"Successfully processed: {len(processed_products)}")
    print(f"Failed to process: {len(failed_products)}")
    
    if failed_products:
        print("\nFailed products:")
        for failed in failed_products:
            print(f"- {failed['name']}: {failed['error']}")

    # Write the processed data to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(processed_products, json_file, indent=2)
        print(f"\nSuccessfully saved processed data to {output_file}.")
    except IOError as e:
        print(f"Error saving to {output_file}: {e}")



# generate_template_data_input('input_full.json', 'generated_template_o1.json')
# process_products_for_structured_data('input_full.json', 'generated_template_o1.json', 'structured_data_output_o1template_gpt4o-mini.json.json')
