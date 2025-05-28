# llm_analyzer.py
from config import CLIENT_OPENAI, LLM_AVAILABLE
from ragas.metrics import ( # Importeer RAGAS metrics hier als ze direct nodig zijn voor .name property
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

def parse_llm_metric_analysis(llm_output_string):
    parsed_analysis = {}
    lines = llm_output_string.strip().split('\n')
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            metric_name_raw = parts[0].strip()
            explanation = parts[1].strip()
            
            # Gebruik de .name property van de RAGAS metric objecten
            if metric_name_raw == "Faithfulness": key_name = faithfulness.name + "_explanation"
            elif metric_name_raw == "Answer Relevancy": key_name = answer_relevancy.name + "_explanation"
            elif metric_name_raw == "Context Precision": key_name = context_precision.name + "_explanation"
            elif metric_name_raw == "Context Recall": key_name = context_recall.name + "_explanation"
            else: 
                key_name = metric_name_raw.lower().replace(" ", "_") + "_explanation"
            parsed_analysis[key_name] = explanation
            
    for metric_obj in [faithfulness, answer_relevancy, context_precision, context_recall]:
        key_to_check = metric_obj.name + "_explanation"
        if key_to_check not in parsed_analysis:
            parsed_analysis[key_to_check] = "LLM heeft geen specifieke verklaring gegeven voor deze metric."
            
    return parsed_analysis

def generate_llm_analysis(ragas_scores, user_input, reference_gt, retrieved_contexts_str_list, recommended_product_names_str):
    if not LLM_AVAILABLE or CLIENT_OPENAI is None:
        fallback_analysis = {}
        # Gebruik de .name property van de RAGAS metric objecten
        for metric_obj in [faithfulness, answer_relevancy, context_precision, context_recall]:
            key = metric_obj.name + "_explanation"
            score = ragas_scores.get(metric_obj.name, 1.0) 
            if metric_obj.name == faithfulness.name:
                fallback_analysis[key] = f"Faithfulness: {'Hoog (score > 0.5).' if score > 0.5 else 'Laag (score <= 0.5), kern van antwoord mogelijk niet direct ondersteund in context.'}"
            elif metric_obj.name == answer_relevancy.name:
                fallback_analysis[key] = f"Answer Relevancy: {'Relevant (score > 0.7).' if score > 0.7 else 'Minder relevant (score <= 0.7), mismatch specs vs vraag.'}"
            elif metric_obj.name == context_precision.name:
                fallback_analysis[key] = f"Context Precision: {'Precies (score > 0.7).' if score > 0.7 else 'Minder precies (score <= 0.7), context bevat mogelijk ruis.'}"
            elif metric_obj.name == context_recall.name:
                fallback_analysis[key] = f"Context Recall: {'Volledig (score > 0.6).' if score > 0.6 else 'Onvolledig (score <= 0.6), context mist mogelijk ideale criteria.'}"
        return {"llm_not_available_fallback": True, **fallback_analysis}

    contexts_for_prompt = "\n\nDetails van Aanbevolen Producten (Retrieved Contexts):\n"
    if not retrieved_contexts_str_list:
        contexts_for_prompt += "Er zijn geen productdetails (retrieved contexts) beschikbaar voor analyse.\n"
    else:
        for i, ctx_str in enumerate(retrieved_contexts_str_list):
            contexts_for_prompt += f"\n--- Product Context {i+1} ---\n{ctx_str}\n--- Einde Product Context {i+1} ---\n"

    prompt = f"""
    Je taak is om RAGAS scores voor een laptopaanbeveling KORT en BONDIG te verklaren.
    Vergelijk 'Details van Aanbevolen Producten' met 'Ideale Specificaties' en 'Gebruikersvraag'.
    Geef per RAGAS metric een verklaring van MAXIMAAL ÉÉN ZIN. Focus op de kernreden.
    Als info in 'Details van Aanbevolen Producten' staat, ga ervan uit dat die beschikbaar is.

    Gebruikersvraag:
    "{user_input}"

    Ideale Specificaties (Reference Ground Truth):
    "{reference_gt}"

    {contexts_for_prompt}

    RAGAS Scores (0.0-1.0, hoger is beter):
    - Faithfulness: {ragas_scores.get(faithfulness.name, float('nan')):.2f}
    - Answer Relevancy: {ragas_scores.get(answer_relevancy.name, float('nan')):.2f}
    - Context Precision: {ragas_scores.get(context_precision.name, float('nan')):.2f}
    - Context Recall: {ragas_scores.get(context_recall.name, float('nan')):.2f}

    Instructies voor output (MAXIMAAL ÉÉN zin per metric, beginnend met de metric naam):
    Faithfulness: Kernreden waarom de claim in het antwoord wel/niet volledig feitelijk ondersteund wordt door de productdetails.
    Answer Relevancy: Kernreden waarom de producten wel/niet goed aansluiten bij de gebruikersvraag (noem 1-2 kernspecificaties).
    Context Precision: Kernreden waarom de productdetails wel/niet to-the-point zijn voor de gebruikersvraag (noem eventueel type ruis).
    Context Recall: Kernreden waarom de productdetails wel/niet de belangrijkste ideale specificaties dekken (noem 1-2 belangrijkste missende/afwijkende criteria als score < 1.0).

    Output Formaat (exact aanhouden, elke metric op een nieuwe regel):
    Faithfulness: [Jouw verklaring]
    Answer Relevancy: [Jouw verklaring]
    Context Precision: [Jouw verklaring]
    Context Recall: [Jouw verklaring]
    """
    try:
        chat_completion = CLIENT_OPENAI.chat.completions.create(
            messages=[
                {"role": "system", "content": "Je bent een AI-analist die RAGAS scores uitlegt. Je output is extreem beknopt (maximaal één zin per metric) en volgt het gevraagde formaat."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o", 
            temperature=0.0,
            max_tokens=300
        )
        llm_output_string = chat_completion.choices[0].message.content.strip()
        parsed_llm_analysis = parse_llm_metric_analysis(llm_output_string)
        return parsed_llm_analysis
    except Exception as e:
        print(f"Fout tijdens genereren beknopte LLM-analyse: {e}")
        return {"error_generating_analysis": f"Fout bij genereren automatische analyse per metric: {str(e)}"}