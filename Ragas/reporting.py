# reporting.py
import json
import os
import datetime
import pandas as pd # Voor pd.isna en allow_nan

def save_evaluation_results(filename, record_to_add):
    """Laadt bestaande resultaten, voegt de nieuwe run toe, en slaat alles op."""
    all_runs_details_records = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f_details:
                all_runs_details_records = json.load(f_details)
            if not isinstance(all_runs_details_records, list):
                all_runs_details_records = [all_runs_details_records] if all_runs_details_records else []
        except json.JSONDecodeError:
            print(f"Waarschuwing: {filename} bevat ongeldige JSON. Start met een lege lijst.")
            all_runs_details_records = []
    
    all_runs_details_records.append(record_to_add)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f_details:
            json.dump(all_runs_details_records, f_details, indent=4, ensure_ascii=False, allow_nan=True)
        print(f"Resultaten succesvol opgeslagen in {filename}")
    except Exception as e:
        print(f"Fout bij het opslaan van resultaten naar {filename}: {e}")

def create_evaluation_record(
    timestamp, persona_id, user_input, response, reference,
    ragas_scores_dict, llm_metric_explanations, retrieved_contexts,
    metrics_objects # [faithfulness, answer_relevancy, ...]
    ):
    """Stelt het record samen dat wordt opgeslagen in JSON."""
    record = {
        "timestamp": timestamp,
        "persona_id": persona_id,
        "user_input": user_input,
        "response": response,
        "reference": reference,
        "llm_metric_explanations": llm_metric_explanations,
        "retrieved_contexts": retrieved_contexts
    }
    for metric in metrics_objects:
        record[metric.name] = ragas_scores_dict.get(metric.name)
    return record