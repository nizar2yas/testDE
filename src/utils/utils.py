import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_data_from_nested_list(data, field):
    """Extracts data from a nested list based on the provided field.
    Handles potential missing 'field' keys gracefully.

    Args:
        data (dict): A dictionary potentially containing the nested list.
        field (str): The key corresponding to the desired nested list.

    Returns:
        list: A flattened list containing the extracted data.
    """
    logger.debug("Extracting data from nested list for field: %s", field)
    result = [
        pub.get(field)
        for sublist in data.get(field, [])
        for pub in sublist if pub.get(field) is not None
    ]
    logger.debug("Extracted data: %s", result)
    return result


def load_json_file(file_path):
    """Loads JSON data from a file, handling potential errors.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data or None if an error occurred.
        Prints an error message if the file is not found.
    """
    logger.info("Loading JSON file: %s", file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        logger.error("Input file %s not found", file_path)
        raise ValueError(f"Error: Input file '{file_path}' not found.") from e
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON format in %s", file_path)
        raise ValueError(f"Error: Invalid JSON format in '{file_path}'.") from e


def get_distinct_journals(journals):
    """Extracts distinct journal names from a list of publications.

    Args:
        publications (list): A list of publication dictionaries.

    Returns:
        set: A set of distinct journal names.
    """

    logger.debug("Getting distinct journals from: %s", journals)
    distinct_journals = {pub.get('journal') for pub in journals if pub.get('journal')}
    logger.debug("Distinct journals: %s",distinct_journals)
    return distinct_journals


def extract_related_drugs(data, drug_name, exclusive_pubmed_journals):
    """Identifies related drugs based on shared PubMed journals.

    Args:
        data (list): A list of drug data dictionaries.
        drug_name (str): The name of the target drug.
        exclusive_pubmed_journals (set): A set of PubMed journals unique to the target drug.

    Returns:
        set: A set of related drug names.
    """
    logger.info("Extracting related drugs for %s based on exclusive journals: %s", drug_name, exclusive_pubmed_journals)

    related_medications = set()
    for other_drug_data in data:
        if other_drug_data['name'] != drug_name:
            other_drug_pubmed_journals = get_distinct_journals(other_drug_data['pubMed'])
            if other_drug_pubmed_journals.intersection(exclusive_pubmed_journals):
                related_medications.add(other_drug_data['name'])
                logger.debug("Found related drug: %s",other_drug_data['name'])


    logger.info("Related medications found: %s", related_medications)
    return related_medications