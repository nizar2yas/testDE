import json


def extract_data_from_nested_list(data, field):
    """Extracts data from a nested list based on the provided field.
    Handles potential missing 'field' keys gracefully.

    Args:
        data (dict): A dictionary potentially containing the nested list.
        field (str): The key corresponding to the desired nested list.

    Returns:
        list: A flattened list containing the extracted data.
    """
    return [
        pub.get(field)
        for sublist in data.get(field, [])
        for pub in sublist if pub.get(field) is not None
    ]


def load_json_file(file_path):
    """Loads JSON data from a file, handling potential errors.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data or None if an error occurred.
        Prints an error message if the file is not found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        return None


def get_distinct_journals(journals):
    """Extracts distinct journal names from a list of publications.

    Args:
        publications (list): A list of publication dictionaries.

    Returns:
        set: A set of distinct journal names.
    """
    return {pub.get('journal') for pub in journals if pub.get('journal')}


def extract_related_drugs(data, drug_name, exclusive_pubmed_journals):
    """Identifies related drugs based on shared PubMed journals.

    Args:
        data (list): A list of drug data dictionaries.
        drug_name (str): The name of the target drug.
        exclusive_pubmed_journals (set): A set of PubMed journals unique to the target drug.

    Returns:
        set: A set of related drug names.
    """
    related_medications = set()
    for other_drug_data in data:
        if other_drug_data['name'] != drug_name:
            other_drug_pubmed_journals = get_distinct_journals( other_drug_data['pubMed'])
            if other_drug_pubmed_journals.intersection(exclusive_pubmed_journals):
                related_medications.add(other_drug_data['name'])
    return related_medications