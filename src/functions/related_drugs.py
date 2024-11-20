from ..utils.utils import get_distinct_journals, load_json_file, extract_related_drugs
from collections import defaultdict
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_related_drugs(data, drug_name):
    """Finds medications mentioned in the same PubMed journals as the target drug, but not in Clinical Trials."""
    logging.info("Starting to search related medications for: %s",drug_name)

    drug_data = next((item for item in data if item['name'] == drug_name), None)
    if not drug_data:
        logging.warning("Drug %s not found in the dataset.",drug_name)
        return None
    
    clinical_trials_journals = get_distinct_journals(drug_data['clinical_trials'])
    pubmed_journals = get_distinct_journals(drug_data['pubMed'])

    exclusive_pubmed_journals = pubmed_journals - clinical_trials_journals
    logging.debug("Exclusive PubMed journals for %s: %s", drug_name, exclusive_pubmed_journals)

    related_medications = extract_related_drugs(data, drug_name, exclusive_pubmed_journals)
    logging.info("Related medications found: %s",related_medications)
    return related_medications



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="drugs data file path", required=True)
    parser.add_argument("-d", "--drug_name", help="Drug name to search for", required=True)
    args = parser.parse_args()

    drug_journal_data = load_json_file(args.input_path)
    drug_journal_data = drug_journal_data['result']
    related_medications = get_related_drugs(drug_journal_data, args.drug_name)
    print(f"Related medications: {related_medications}")
