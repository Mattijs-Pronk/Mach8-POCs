# main.py
import os
import json
import pandas as pd
import datetime
import traceback # Voor debugging

# Eigen modules
from config import API_URL, LLM_AVAILABLE, OUTPUT_FILENAME
from persona_data import persona_data_store
from api_handler import get_recommendations_from_api
from llm_analyzer import generate_llm_analysis
from ragas_helpers import extract_user_input_for_ragas, format_ragas_answer, format_ragas_contexts
from reporting import save_evaluation_results, create_evaluation_record

# RAGAS en Datasets
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# --- KIES HIER DE PERSONA VOOR DE HUIDIGE RUN ---
SELECTED_PERSONA_ID = "student_webdev_docker_budget"
# SELECTED_PERSONA_ID = "professional_datascience_heavy_performance"
# SELECTED_PERSONA_ID = "freelance_webdev_docker_mobility"

def run_evaluation_for_persona(persona_id):
    if persona_id not in persona_data_store:
        print(f"FOUT: Persona ID '{persona_id}' niet gevonden in persona_data_store. Script stopt voor deze persona.")
        return

    current_persona_config = persona_data_store[persona_id]
    current_api_payload = current_persona_config["api_payload"]
    ground_truth_ragas = current_persona_config["ground_truth_text"]

    print(f"--- START TEST VOOR PERSONA: '{persona_id}' ---")

    # 1. Haal gebruikersinput voor RAGAS
    gesprek_input_voor_ragas = extract_user_input_for_ragas(current_api_payload.get('conversation'))

    # 2. Haal aanbevelingen van API
    api_response_data = get_recommendations_from_api(API_URL, current_api_payload)

    aanbevelingen_lijst = None
    if api_response_data:
        if isinstance(api_response_data, list):
            aanbevelingen_lijst = api_response_data
        elif isinstance(api_response_data, dict) and 'recommendations' in api_response_data and isinstance(api_response_data['recommendations'], list):
            aanbevelingen_lijst = api_response_data['recommendations']
        elif isinstance(api_response_data, dict): # Fallback als 'recommendations' key mist
            potential_list = [v for v in api_response_data.values() if isinstance(v, list)]
            if potential_list and all(isinstance(item, dict) and ('product' in item or 'name' in item) for item in potential_list[0]): # Check of het product-achtige dicts zijn
                 aanbevelingen_lijst = potential_list[0]
                 print("INFO: 'recommendations' key niet gevonden, maar een geschikte lijst met producten wel.")
            else:
                print(f"API response is dict, maar key 'recommendations' niet gevonden of geen duidelijke lijst van aanbevelingen gedetecteerd.")
    else:
        print("Kon geen data ophalen van de API of API response was None.")

    if not aanbevelingen_lijst or not isinstance(aanbevelingen_lijst, list) or not aanbevelingen_lijst:
        print(f"Aanbevelingen lijst is leeg of niet correct geformatteerd voor persona '{persona_id}'. RAGAS evaluatie wordt overgeslagen.")
        if aanbevelingen_lijst is not None: print(f"Ontvangen aanbevelingen_lijst (eerste 2 items indien beschikbaar): {aanbevelingen_lijst[:2]}...")
        print(f"--- EINDE TEST VOOR PERSONA: '{persona_id}' (GEFAALD BIJ API RESPONSE) ---")
        return

    try:
        # 3. Prepare RAGAS data
        answer_ragas = format_ragas_answer(aanbevelingen_lijst)
        contexts_ragas = format_ragas_contexts(aanbevelingen_lijst)

        if not contexts_ragas or answer_ragas == "Kon geen productnamen extraheren.":
            print("Geen valide contexten en/of antwoord (productnamen) kunnen genereren. RAGAS evaluatie wordt overgeslagen.")
            print(f"--- EINDE TEST VOOR PERSONA: '{persona_id}' (GEFAALD BIJ RAGAS DATA PREP) ---")
            return

        # 4. RAGAS Evaluatie
        dataset_dict = {"question": [gesprek_input_voor_ragas], "answer": [answer_ragas], "contexts": [contexts_ragas], "ground_truth": [ground_truth_ragas]}
        dataset = Dataset.from_dict(dataset_dict)
        
        metrics_to_use = [faithfulness, answer_relevancy, context_precision, context_recall]
        
        # De 'evaluate' functie kan direct met de OpenAI client omgaan als LLM_AVAILABLE is True
        # of zonder als het niet nodig is voor de metrics (of als RAGAS fallback intern heeft).
        # RAGAS configureert intern de LLM als die nodig is voor een metric.
        result = evaluate(dataset, metrics=metrics_to_use)
        
        df_results_current_run = result.to_pandas()
        
        # Scores extractie logica
        ragas_scores_dict = {}
        # Probeer eerst direct uit het result object (nieuwere RAGAS versies)
        if hasattr(result, 'scores') and isinstance(result.scores, dict):
            ragas_scores_dict = result.scores
        # Fallback naar dictionary-achtig resultaat (oudere RAGAS versies)
        elif isinstance(result, dict) and all(m.name in result and isinstance(result[m.name], (float, int, type(None))) for m in metrics_to_use):
            ragas_scores_dict = {k: (v if v is not None else float('nan')) for k,v in result.items() if k in [m.name for m in metrics_to_use]}

        # Aanvullende score extractie uit DataFrame als vorige methoden faalden of incompleet waren
        if not df_results_current_run.empty:
            score_column_names = [metric.name for metric in metrics_to_use]
            try: 
                existing_score_cols = [col for col in score_column_names if col in df_results_current_run.columns]
                if existing_score_cols:
                    scores_series = df_results_current_run.iloc[0][existing_score_cols]
                    for col_name, score_val in scores_series.to_dict().items():
                        # Vul alleen als de key mist of de waarde NaN is
                        if col_name not in ragas_scores_dict or pd.isna(ragas_scores_dict.get(col_name)):
                            ragas_scores_dict[col_name] = score_val if not pd.isna(score_val) else float('nan')
            except KeyError as e: 
                print(f"Waarschuwing: KeyError bij RAGAS scores uit DataFrame halen. Fout: {e}")
            except IndexError:
                 print(f"Waarschuwing: RAGAS DataFrame df_results_current_run is leeg. Kon geen scores extraheren.")
        
        # Zorg dat alle metrics een (NaN) entry hebben
        for metric in metrics_to_use:
            if metric.name not in ragas_scores_dict:
                ragas_scores_dict[metric.name] = float('nan')

        if all(pd.isna(v) for v in ragas_scores_dict.values()):
             print("KRITISCHE WAARSCHUWING: Kon RAGAS scores op geen enkele manier vullen. Controleer RAGAS output en data.")

        # 5. LLM Analyse (als beschikbaar)
        parsed_llm_analysis_dict = generate_llm_analysis(
            ragas_scores_dict, 
            gesprek_input_voor_ragas, 
            ground_truth_ragas, 
            contexts_ragas, 
            answer_ragas
        )

        # 6. Resultaten opslaan
        current_timestamp_iso = datetime.datetime.now().isoformat()
        
        # Haal waarden uit DataFrame als die er zijn, anders uit de variabelen
        user_input_val = df_results_current_run.iloc[0].get("question", gesprek_input_voor_ragas) if not df_results_current_run.empty else gesprek_input_voor_ragas
        response_val = df_results_current_run.iloc[0].get("answer", answer_ragas) if not df_results_current_run.empty else answer_ragas
        reference_val = df_results_current_run.iloc[0].get("ground_truth", ground_truth_ragas) if not df_results_current_run.empty else ground_truth_ragas
        retrieved_contexts_val = df_results_current_run.iloc[0].get("contexts", contexts_ragas) if not df_results_current_run.empty else contexts_ragas


        final_record = create_evaluation_record(
            timestamp=current_timestamp_iso,
            persona_id=persona_id,
            user_input=user_input_val,
            response=response_val,
            reference=reference_val,
            ragas_scores_dict=ragas_scores_dict,
            llm_metric_explanations=parsed_llm_analysis_dict,
            retrieved_contexts=retrieved_contexts_val,
            metrics_objects=metrics_to_use
        )
        save_evaluation_results(OUTPUT_FILENAME, final_record)
        print(f"Scores voor deze run ({persona_id}): {ragas_scores_dict}")

    except TypeError as te:
        print(f"TypeError TIJDENS verwerken van RAGAS data voor persona '{persona_id}': {te}")
        traceback.print_exc()
    except Exception as e:
        print(f"Algemene fout TIJDENS RAGAS evaluatie voor persona '{persona_id}': {e}")
        traceback.print_exc()

    print(f"\n--- EINDE TEST VOOR PERSONA: '{persona_id}' ---")


if __name__ == "__main__":
    # Je kunt hier een lijst van persona's specificeren om te testen
    # persona_ids_to_test = ["student_webdev_docker_budget", "professional_datascience_heavy_performance"]
    persona_ids_to_test = [SELECTED_PERSONA_ID] # Of alleen de geselecteerde
    
    if SELECTED_PERSONA_ID not in persona_data_store.keys() and SELECTED_PERSONA_ID not in persona_ids_to_test :
        print(f"Geselecteerde persona '{SELECTED_PERSONA_ID}' is niet bekend. Voeg toe aan persona_data.py of kies een bestaande.")
    
    for pid in persona_ids_to_test:
        run_evaluation_for_persona(pid)
    
    print("\nAlle gespecificeerde persona evaluaties voltooid.")