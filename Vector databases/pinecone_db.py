# Import the Pinecone library
from pinecone import Pinecone
import time
import secrets

pc = Pinecone(api_key=secrets.OPENAI_API_KEY)

# Sample records with your product data
records = [
    {
        "_id": "rec1",
        "chunk_text": "The Acer Chromebook 315 (CB315-4H-C8T6) is priced at €349 with a rating of 9.7/10 from 34 reviews. It features a 15.6-inch Full HD (1080p) screen with an IPS panel and anti-reflective coating, powered by an Intel Celeron N4500 processor with a 2-core setup, 1.1 GHz base speed, and 2.8 GHz turbo speed. It has 4 GB RAM (1 x 4 GB) and 64 GB eMMC storage. The laptop is lightweight at 1.6 kg with dimensions of 36.64 cm (W), 24.42 cm (D), and 2 cm (H). Connectivity includes Bluetooth 5.0, 4 USB ports (2 x USB-A 3.0, 2 x USB-C 3.1), headphone jack, and support for USB-C DisplayPort Alternate Mode. The laptop lacks HDMI, DisplayPort, VGA, and Thunderbolt ports. It runs Google Chrome OS, supports multiple languages, and offers a 720p built-in camera. The battery lasts for 4.5 hours, and it includes TPM and a Kensington lock for security. Other features include a QWERTY keyboard (no backlight, numeric keypad, or mechanical keys), stereo speakers, and microphone. The security class is mid-range, and there are no additional software or fingerprint sensor features. The laptop comes with a 2-year warranty and allows free return of your old device via Coolblue.",
        "url": "https://www.coolblue.nl/product/911648/acer-chromebook-315-cb315-4h-c8t6.html"
    },
    {
        "_id": "rec2",
        "chunk_text": "The Acer Chromebook 314 (CB314-3H-C99X) is priced at €456 with a rating of 9.0/10 from 16 reviews. It features a 14-inch Full HD (1080p) screen with an IPS panel and anti-reflective coating, powered by an Intel Celeron N4500 processor with 2 cores, 1.1 GHz base speed, and 2.8 GHz turbo speed. The laptop includes 4 GB RAM (1 x 4 GB) and 64 GB eMMC storage. It weighs 1.45 kg and has dimensions of 32.64 cm (W), 22.5 cm (D), and 2 cm (H). For connectivity, it offers Bluetooth 5.0, 4 USB ports (2 x USB-A 3.0, 2 x USB-C 3.1), a headphone jack, and supports USB-C DisplayPort Alternate Mode. It lacks HDMI, DisplayPort, VGA, and Thunderbolt ports. Running on Google Chrome OS, it supports multiple languages and includes a 720p built-in camera. The battery lasts for up to 8 hours. Security features include TPM and a Kensington lock, but it doesn't have Windows Hello or a fingerprint sensor. The laptop has a QWERTY keyboard (no backlight, numeric keypad, or mechanical keys), 2 stereo speakers, and a microphone. The security class is mid-range, and there is no additional software. It comes with a 2-year warranty and offers free return of your old device via Coolblue.",
        "url": "https://www.coolblue.nl/product/911646/acer-chromebook-314-cb314-3h-c99x.html"
    },
    {
        "_id": "rec3",
        "chunk_text": "The Lenovo ThinkPad X1 Carbon Gen 9 is a high-performance laptop priced at €1,799, with a rating of 8.8/10 from 42 reviews. It comes with a 3-year warranty and defect handling via Lenovo. It also offers free return of your old device. The laptop features a 14-inch WQHD (2560x1600) touchscreen display with an IPS panel, matte finish, and a 90 Hz refresh rate. It’s powered by an Intel Core i7-1165G7 processor with 4 cores, 2.8 GHz base speed, and 4.7 GHz turbo speed, alongside 16 GB RAM (1 x 16 GB) and a 512 GB SSD for storage. The graphics are handled by Intel Iris Xe Graphics. It runs Windows 10 Pro and supports multiple languages. The device weighs just 1.1 kg and has dimensions of 31.2 cm (W), 22.4 cm (D), and 1.4 cm (H), with a carbon fiber build in a sleek black color. The laptop also features 4G connectivity, Bluetooth 5.1, and 3 USB ports (2 x USB-A 3.0, 1 x USB-C 3.2 with DisplayPort support). For video output, it has HDMI, DisplayPort, and Thunderbolt ports. The keyboard has a QWERTY layout with a numeric keypad, backlighting, and is stain-resistant. It also supports programmable keys. The laptop includes 4 speakers with Dolby Audio, a 720p HD webcam, and a microphone for communication. Security features include TPM, a Kensington lock, Windows Hello, and a fingerprint sensor. The battery life lasts up to 15 hours. Additionally, the laptop comes pre-installed with Microsoft Office 365.",
        "url": "https://www.lenovo.com/thinkpad-x1-carbon-gen-9"
    },
]

index_name = "dense-index"
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )

dense_index = pc.Index(index_name)

# Upsert the records into a namespace
dense_index.upsert_records("example-namespace", records)

# Define the query
query = "A laptop with the best battery life for long hours of usage"

# Search the dense index
results = dense_index.search(
    namespace="example-namespace",
    query={
        "top_k": 10,
        "inputs": {
            'text': query
        }
    }
)

# Print the results
for hit in results['result']['hits']:
    print(f"id: {hit['_id']}, score: {round(hit['_score'], 2)}, text: {hit['fields']['chunk_text']}, category: {hit['fields']['category']}")
