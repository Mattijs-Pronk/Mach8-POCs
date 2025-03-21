import openai
import sqlite3
import secrets

# Stel je OpenAI API-sleutel in
openai_client = openai.Client(
    api_key=secrets.OPENAI_API_KEY
)

# Functie om de SQL-query te genereren op basis van de gebruikersvraag
def generate_sql_query(prompt):
    formatted_prompt = f"""
    Je krijgt een gebruikersvraag over het zoeken naar een laptop. 
    Je taak is om een veilige en efficiënte SQL-query te genereren die laptops zoekt op basis van relevante eigenschappen zoals:
    - Schermgrootte (screen_diagonal)
    - Opslagcapaciteit (total_storage_capacity)
    - Prijs (price)
    - Merk (brand)
    - GPU (graphics_card_chipset)
    - CPU (processor_name)
    - RAM (internal_ram_memory)
    - Ververssnelheid (refresh_rate)
    - Bedoeld voor (Recommended_usage)

    **Belangrijk:** 
    - Zorg ervoor dat de gegenereerde SQL-query correct werkt voor numerieke waarden.
    - Converteer de waarden correct (bijv. "512GB" → 512, "17 inch" → 17).
    - Gebruik alleen de relevante filters die uit de gebruikersvraag komen.
    - **Voor Recommended_usage:**  
        - Gebruik `LOWER(Recommended_usage) LIKE '%<zoekterm>%'` zodat het werkt bij verschillende schrijfwijzen.
        - Indien meerdere zoektermen worden genoemd, combineer met `OR`.
    - Voeg een ORDER BY toe als de gebruiker een voorkeur aangeeft (bijv. goedkoopste eerst).
    - **Geef alleen de SQL-query terug, zonder uitleg of extra tekst.**

    Gebruikersvraag:
    "{prompt}"
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Je bent een SQL-expert. Geef alleen een geldige SQL-query terug, zonder uitleg."},
            {"role": "user", "content": formatted_prompt}
        ],
        max_tokens=100,
        temperature=0.3
    )

    sql_query = response.choices[0].message.content.strip()
    sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
    return sql_query


prompt = "Ik zoek een laptop voor video editing."

# Verkrijg de SQL-query van OpenAI
generated_sql_query = generate_sql_query(prompt)
print("Gegenereerde SQL-query:", generated_sql_query)

# Verbinden met de SQLite database
conn = sqlite3.connect('coolblueDatabase.db')
cursor = conn.cursor()

# Voer de gegenereerde SQL-query uit
cursor.execute(generated_sql_query)

# Haal de resultaten op
results = cursor.fetchall()

# Toon de resultaten (alleen de gewenste kolommen)
if results:
    for row in results:
        # Zorg ervoor dat we alleen de gewenste kolommen loggen
        name = row[:1]
        print(f"name: {name}")
else:
    print("Geen laptops gevonden die voldoen aan de criteria.")

# Sluit de verbinding
conn.close()
