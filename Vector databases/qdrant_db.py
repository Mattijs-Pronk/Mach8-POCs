# docker pull qdrant/qdrant
# docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

from qdrant_client import models, QdrantClient
import json
from qdrant_client.models import PointStruct, VectorParams, Distance
import openai
import secrets

client = QdrantClient(url="http://localhost:6333")

openai_client = openai.Client(
    api_key=secrets.OPENAI_API_KEY
)

collection_name = "gpt-collection-laptops3"
embedding_model = "text-embedding-3-small"

# Extract products from the JSON file
# with open('output.json', 'r', encoding='utf-8') as file:
#     products = json.load(file)

# # Create semantic descriptions for embedding
# texts = []
# for product in products:
#     description = f"""
#     Dit is een {product['brand']} laptop die {product.get('Recommended_usage', 'geschikt voor verschillende taken')} is.
#     De laptop heeft een beoordeling van {product['rating']} en kost {product['price']}.
    
#     Prestaties en Hardware:
#     - Processor: {product['processor_name']} {product.get('processor_number', '')}
#     - Geheugen: {product['internal_ram_memory']}
#     - Grafische kaart: {product['graphics_card_chipset']}
#     - Opslag: {product.get('total_storage_capacity', '')} {product.get('storage_type', '')}
    
#     Gebruikerservaring:
#     - Scherm: {product['screen_diagonal']} {product['screen_resolution']}
#     - Batterijduur: {product.get('battery_capacity', 'Niet gespecificeerd')}
#     - Bouwkwaliteit: {product.get('build_quality', 'Standaard')}
#     - Prestatie niveau: {product.get('speed_class', 'Standaard')}
#     - Gewicht: {product.get('weight', 'Niet gespecificeerd')}
    
#     Connectiviteit en Kenmerken:
#     - USB-poorten: {product.get('amount_of_usb_connections', '')} {product.get('usb_type', '')}
#     - Camera: {product.get('camera_resolution', '')}
#     - Audio: {product.get('amount_of_speakers', '')} luidsprekers
#     """
#     texts.append(description)

result = openai_client.embeddings.create(input=texts, model=embedding_model)

points = [
    PointStruct(
        id=idx,
        vector=data.embedding,
        payload=product,
    )
    for idx, (data, product) in enumerate(zip(result.data, products))
]

try:
    client.create_collection(
        collection_name,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )
except Exception as e:
    print(f"Collection might already exist: {e}")

client.upsert(collection_name, points)


def generate_search_criteria(user_query):
    prompt = f"""
    Je krijgt een gebruikersvraag over het zoeken naar een laptop. Je taak is om de zoekopdracht om te zetten naar een geformatteerde zoekopdracht met duidelijk gedefinieerde criteria zoals bijvoorbeeld schermgrootte, opslagcapaciteit en batterijduur. 

    Geef de criteria zoals "17 inch scherm", "512 GB opslag" en eventuele andere relevante kenmerken, gebaseerd op de vraag. Geef ALLEEN kenmerken van de gebruikersvraag.

    Gebruikersvraag:
    "{user_query}"
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Je bent een expert in het analyseren van laptop zoekopdrachten en het omzetten naar specifieke criteria."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5
    )
    
    # Haal het geformatteerde resultaat op
    formatted_search_query = response.choices[0].message.content.strip()
    return formatted_search_query

# Example user query
# user_query = "Ik ben op zoek naar een laptop met een 17 inch scherm en 1 TB opslag, de batterij moet 15 uur of meer mee gaan"
# user_query = "Opslag: 512 GB, Batterijduur: 15 uur, Scherm: 15 inch, kost: 700 euro"
# user_query = "Ik heb een laptop nodig voor dagelijkse taken zoals e-mail en documenten. Ik ben veel onderweg, dus ik heb een uitstekende batterijduur nodig."
# user_query = "Ik ben opzoek naar een gaming laptop die ongeveer 1000 euro kost"
user_query = "Ik ben opzoek naar een laptop met een groot scherm en veel opslag"


# search_criteria = generate_search_criteria(user_query)
# print('search_criteria', search_criteria)

search_result = client.search(
    collection_name=collection_name,
    query_vector=openai_client.embeddings.create(
        input=[user_query],
        model=embedding_model,
    )
    .data[0]
    .embedding,
    limit=3
)

print("\nBest matches for your query:")
for hit in search_result:
    print(f"\nMatch score: {hit.score:.4f}")
    print(f"Model: {hit.payload.get('name')}")
    print(f"Usage: {hit.payload.get('Recommended_usage', 'Not specified')}")
    print(f"Battery: {hit.payload.get('battery_capacity', 'Not specified')}")
    print(f"Price: {hit.payload.get('price')}")
    print(f"screen_diagonal: {hit.payload.get('screen_diagonal', 'Not specified')}")
    print(f"total_storage_capacity: {hit.payload.get('total_storage_capacity', 'Not specified')}")
    
    
    
    
    
    
    
    
# docker pull qdrant/qdrant
# docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

# from qdrant_client import models, QdrantClient
# import json
# from qdrant_client.models import PointStruct, VectorParams, Distance
# import openai

# # Verbind met Qdrant client
# client = QdrantClient(url="http://localhost:6333")

# openai_client = openai.Client(
#     api_key=secrets.OPENAI_API_KEY
# )

# collection_name = "gpt-collection-laptops2"
# embedding_model = "text-embedding-3-small"

# # Laad je laptopdata uit een JSON-bestand
# with open('output.json', 'r', encoding='utf-8') as file:
#     products = json.load(file)

# # Maak een lijst van tekstbeschrijvingen voor de laptops met ALLE beschikbare data
# texts = [
#     f"Name: {product['name']}, Rating: {product['rating']}, Price: {product['price']}, "
#     f"URL: {product['url']}, Article Number: {product['articlenumber']}, Manufacturer Code: {product['manufacturercode']}, "
#     f"Brand: {product['brand']}, Warranty: {product['warranty']}, Handling of Defects: {product['handling_of_your_defect']}, "
#     f"Screen: {product['screen_diagonal']}, RAM: {product['internal_ram_memory']}, "
#     f"Graphics: {product['graphics_card_chipset']}, Processor: {product['processor_name']} {product['processor_number']}, "
#     f"Storage: {product['total_storage_capacity']}, Battery Life: {product['battery_capacity']}, "
#     f"Operating System: {product['operating_system']}, Color: {product['color']}, Material: {product['material']}, "
#     f"Weight: {product['weight']}, Bluetooth Version: {product['bluetooth_version']}, "
#     f"Keyboard Layout: {product['keyboard_layout']}, Speakers: {product['amount_of_speakers']}, "
#     f"Camera: {product['camera_resolution']}, USB Ports: {product['amount_of_usb_connections']}, "
#     f"Screen Resolution: {product['screen_resolution']}, Refresh Rate: {product['refresh_rate']}, "
#     f"USB Type: {product['usb_type']}, Storage Type: {product['storage_type']}, "
#     f"GPU: {product['gpu_chipset']}, GPU Type: {product['gpu_type']}, "
#     f"Security: {product['security_class']}, RAM Slots: {product['ram_slots']}, "
#     f"Extra Software: {product['extra_software']}"
#     for product in products
# ]

# Genereer embeddings voor de laptops
# result = openai_client.embeddings.create(input=texts, model=embedding_model)

# client.create_collection(
#     collection_name,
#     vectors_config=VectorParams(
#         size=1536,
#         distance=Distance.COSINE,
#     ),
# )

# # Voeg de laptops toe aan Qdrant
# points = [
#     PointStruct(
#         id=idx,
#         vector=data.embedding,
#         payload={
#             "name": product["name"],
#             "price": product["price"],
#             "rating": product["rating"],
#             "url": product["url"],
#             "articlenumber": product["articlenumber"],
#             "brand": product["brand"],
#             "warranty": product["warranty"],
#             "screen_diagonal": product["screen_diagonal"],
#             "internal_ram_memory": product["internal_ram_memory"],
#             "graphics_card_chipset": product["graphics_card_chipset"],
#             "processor_name": product["processor_name"],
#             "processor_number": product["processor_number"],
#             "total_storage_capacity": product["total_storage_capacity"],
#             "battery_capacity": product["battery_capacity"],
#             "operating_system": product["operating_system"],
#             "color": product["color"],
#             "material": product["material"],
#             "weight": product["weight"],
#             "bluetooth_version": product["bluetooth_version"],
#             "keyboard_layout": product["keyboard_layout"],
#             "amount_of_speakers": product["amount_of_speakers"],
#             "camera_resolution": product["camera_resolution"],
#             "amount_of_usb_connections": product["amount_of_usb_connections"],
#             "screen_resolution": product["screen_resolution"],
#             "refresh_rate": product["refresh_rate"],
#             "usb_type": product["usb_type"],
#             "storage_type": product["storage_type"],
#             "gpu_chipset": product["gpu_chipset"],
#             "gpu_type": product["gpu_type"],
#             "security_class": product["security_class"],
#             "ram_slots": product["ram_slots"],
#             "extra_software": product["extra_software"]
#         },
#     )
#     for idx, (data, product) in enumerate(zip(result.data, products))
# ]

# client.upsert(collection_name, points)

# result = client.search(
#     collection_name=collection_name,
#     query_vector=openai_client.embeddings.create(
#         input=[
#             f"Name: None, Rating: None, Price: None, "
#             f"URL: None, Article Number: None, Manufacturer Code: None, "
#             f"Brand: None, Warranty: None, Handling of Defects: None, "
#             f"Screen: None, RAM: None, "
#             f"Graphics: None, Processor: None None, "
#             f"Storage: None, Battery Life: 18 uur, "
#             f"Operating System: None, Color: None, Material: None, "
#             f"Weight: None, Bluetooth Version: None, "
#             f"Keyboard Layout: None, Speakers: None, "
#             f"Camera: None, USB Ports: None, "
#             f"Screen Resolution: None, Refresh Rate: None, "
#             f"USB Type: None, Storage Type: None, "
#             f"GPU: None, GPU Type: None, "
#             f"Security: None, RAM Slots: None, "
#             f"Extra Software: None"],
#         model=embedding_model,
#     )
#     .data[0]
#     .embedding,
#     limit=4
# )

# # Resultaten tonen
# for hit in result:
#     print(f"Score: {hit.score}, name: {hit.payload.get('name')}")