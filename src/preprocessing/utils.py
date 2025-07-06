import json

def load_json(file_path):
    """Load JSON from file and pop '_meta' key if exists.
    parameters:
        file_path (str): The path to the JSON file to be loaded.
    Returns:
        dict: The loaded JSON data without the meta data.
        dict: The extracted meta data, if it exists.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    meta = data.pop("_meta", None)
    return data, meta

def save_json(data, file_path):
    """Save JSON data to file with pretty formatting.
    Parameters:
        data (dict): The JSON data to be saved.
        file_path (str): The path to the output JSON file will be saved."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



