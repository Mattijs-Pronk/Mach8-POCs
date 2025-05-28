# config.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
LLM_AVAILABLE = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLIENT_OPENAI = None # Gebruik hoofdletters voor globale constanten/configuraties

if OPENAI_API_KEY:
    try:
        CLIENT_OPENAI = OpenAI(api_key=OPENAI_API_KEY)
        LLM_AVAILABLE = True
        print("OpenAI client succesvol geïnitialiseerd.")
    except Exception as e:
        print(f"Waarschuwing: Kon OpenAI client niet initialiseren. LLM-analyse wordt overgeslagen of gebruikt fallback. Fout: {e}")
else:
    print("Waarschuwing: OPENAI_API_KEY niet gevonden in environment. LLM-analyse wordt overgeslagen of gebruikt fallback.")

# API URL
API_URL = "http://localhost:3000/api/products/recommend"
OUTPUT_FILENAME = "ragas_evaluation_details.json"