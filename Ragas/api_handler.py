# api_handler.py
import requests
import json
import re

def get_recommendations_from_api(api_url, payload):
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        response_text = response.text
        try:
            recommendations = json.loads(response_text)
        except json.JSONDecodeError:
            print("Directe JSON parse mislukt, probeer ObjectId cleaning...")
            clean_response_text = re.sub(r"new ObjectId\('([^']*)'\)", r'"\1"', response_text)
            recommendations = json.loads(clean_response_text)
            print("ObjectId cleaning succesvol.")
        return recommendations
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error bij het aanroepen van de API: {http_err}")
        if hasattr(response, 'content'): print(f"Response content: {response.content.decode(errors='ignore')[:500]}...")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Fout bij het aanroepen van de API: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Fout bij het parsen van de API JSON response: {e}")
        print(f"Ontvangen tekst (die faalde te parsen): {response_text[:500]}...")
        return None