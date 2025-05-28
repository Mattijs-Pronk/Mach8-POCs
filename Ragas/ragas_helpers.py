# ragas_helpers.py

def extract_user_input_for_ragas(conversation_data):
    """Extraheert de input van de gebruiker uit de conversatiedata."""
    if isinstance(conversation_data, str):
        user_parts = []
        for line in conversation_data.strip().split('\n'):
            if line.lower().startswith("user:"):
                user_parts.append(line[len("user:"):].strip())
        if user_parts:
            return " ".join(user_parts)
        else:
            print("Waarschuwing: Kon geen 'user:' prefix vinden in de string conversatie. Gebruik de volledige string voor RAGAS question.")
            return conversation_data
    elif isinstance(conversation_data, list):
        user_conversation_history = [turn['content'] for turn in conversation_data if turn['role'] == 'user']
        return " ".join(user_conversation_history)
    else:
        print(f"Onverwacht type of ontbrekende 'conversation' data: {type(conversation_data)}. Kan RAGAS question niet bepalen.")
        return "Gebruikersinput niet beschikbaar."

def format_ragas_answer(aanbevelingen_lijst):
    """Formatteert de RAGAS 'answer' string op basis van productnamen."""
    answer_ragas_list = []
    for p_item_wrapper in aanbevelingen_lijst:
        p_item = None
        if isinstance(p_item_wrapper, dict) and 'product' in p_item_wrapper and isinstance(p_item_wrapper['product'], dict):
            p_item = p_item_wrapper['product']
        elif isinstance(p_item_wrapper, dict) and 'name' in p_item_wrapper:
            p_item = p_item_wrapper
        if p_item and 'name' in p_item:
            answer_ragas_list.append(p_item['name'])

    if answer_ragas_list:
        product_names_only = ", ".join(answer_ragas_list)
        return f"{product_names_only}. Deze modellen bieden een krachtige basis voor web development en het draaien van Docker, dankzij specificaties zoals minimaal 16GB RAM en moderne Intel Core processors."
    else:
        print("Kon geen productnamen extraheren voor RAGAS answer.")
        return "Kon geen productnamen extraheren."

def format_ragas_contexts(aanbevelingen_lijst):
    """Formatteert de RAGAS 'contexts' lijst op basis van productdetails."""
    contexts_ragas = []
    for rec_item_wrapper in aanbevelingen_lijst:
        prod = None
        if isinstance(rec_item_wrapper, dict) and 'product' in rec_item_wrapper and isinstance(rec_item_wrapper['product'], dict):
            prod = rec_item_wrapper['product']
        elif isinstance(rec_item_wrapper, dict) and 'name' in rec_item_wrapper:
            prod = rec_item_wrapper
        if not prod: continue

        feature_strings = []
        for feat in prod.get('features', []):
            f_name = feat.get('featureName', 'N/A')
            f_tier = feat.get('tier', 'N/A')
            f_expl = feat.get('explanation', 'N/A')
            feature_strings.append(f"{f_name}: {f_tier} ({f_expl})")
        contexts_ragas.append(f"Product: {prod.get('name', 'N/A')}. Prijs: {prod.get('price', 'N/A')}. Categorie: {prod.get('category', 'N/A')}. Features: {'; '.join(feature_strings)}")
    return contexts_ragas