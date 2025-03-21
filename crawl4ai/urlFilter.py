import json

# Load the JSON file
with open("input.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Filter items where title contains "Garnier" (case insensitive), only if title exists
filtered_data = [item for item in data if item.get("title") and "garnier" in item["title"].lower()]

# Save the filtered results to a new JSON file
with open("filtered_output.json", "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

print(f"Filtered {len(filtered_data)} items and saved to 'filtered_output.json'.")
