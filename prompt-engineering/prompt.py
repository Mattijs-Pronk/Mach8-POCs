import openai
import secrets

openai_client = openai.Client(
    api_key=secrets.OPENAI_API_KEY
)

chat_history = []

def vraag_aan_chatbot(gebruikersvraag):
    global chat_history

    # Voeg de nieuwe gebruikersvraag toe aan de geschiedenis
    chat_history.append({"role": "user", "content": gebruikersvraag})

    response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"""
"Voer een natuurlijk, rustig en informeel verkoopgesprek voor een webshop met diverse producten. De klant zoekt een product, en jij helpt bij het vinden van de beste optie. Stel telkens één vraag per bericht en vraag door tot je minstens vier relevante details hebt, zoals:

- Productcategorie en type (bijv. laptop, telefoon, koptelefoon)
- Gebruikstoepassing (bijv. gamen, werk, reizen, studie)
- Budget
- Gewenste kenmerken (bijv. formaat, batterijduur, duurzaamheid, merkvoorkeur)

Gebruik een informele en behulpzame toon. Zodra je genoeg informatie hebt, bied je maximaal drie opties aan met elk drie voordelen. Sluit af met een vraag of de klant nog extra wensen heeft."
        """},
        *chat_history
    ],
    max_tokens=300,
    temperature=0.6
)

    # Verkrijg het antwoord van de chatbot (aangepaste syntax voor nieuwe client)
    antwoord = response.choices[0].message.content

    # Voeg het antwoord toe aan de geschiedenis
    chat_history.append({"role": "assistant", "content": antwoord})

    return antwoord

# Test de chatbot
while True:
    vraag = input("Jij: ")
    if vraag.lower() in ["stop", "exit", "quit"]:
        print("Chatbot afgesloten.")
        break
    antwoord = vraag_aan_chatbot(vraag)
    print("\nChatbot: " + antwoord + "\n")
