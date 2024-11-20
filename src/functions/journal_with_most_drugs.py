from ..utils.utils import get_distinct_journals, load_json_file 
from collections import defaultdict
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_journal_with_most_distinct_drugs(data):
    """Finds the journal with the most distinct medication mentions."""
    logging.info("Starting to find the journal with the most distinct medications.")

    journal_medications = defaultdict(set)
    for drugs_data in data:
        drug_name = drugs_data['name']
        logging.debug("Processing drug :%s",drug_name)
        for journal in get_distinct_journals(drugs_data['clinical_trials'] + drugs_data['pubMed']):
            journal_medications[journal].add(drug_name)
            logging.debug("Adding %s to %s",drug_name,journal)


    jouranl_with_max_drugs = max(journal_medications, key=journal_medications.get, default=None)
    logging.info("Journal with the most distinct medications: %s",jouranl_with_max_drugs)
    return jouranl_with_max_drugs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="drugs data file path", required=True)
    parser.add_argument("-d", "--drug_name", help="Drug name to search for", required=True)
    args = parser.parse_args()

    drug_journal_data = load_json_file(args.input_path)
    most_cited_journal = get_journal_with_most_distinct_drugs(drug_journal_data['result'])
    print(f"Journal with the most distinct medications: {most_cited_journal}")
