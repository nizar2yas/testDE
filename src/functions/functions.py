from ..utils.utils import get_distinct_journals, load_json_file, extract_related_drugs
from collections import defaultdict
import argparse


def get_journal_with_most_distinct_medications(data):
    """Finds the journal with the most distinct medication mentions."""
    journal_medications = defaultdict(set)
    for drugs_data in data:
        drug_name = drugs_data['name']
        for journal in get_distinct_journals(drugs_data['clinical_trials'] + drugs_data['pubMed']):
            journal_medications[journal].add(drug_name)

    # return max(journal_medications, key=lambda k: len(journal_medications[k]), default=None)
    return max(journal_medications, key=journal_medications.get, default=None)



def get_related_medications(data, drug_name):
    """Finds medications mentioned in the same PubMed journals as the target drug, but not in Clinical Trials."""

    drug_data = next((item for item in data if item['name'] == drug_name), None)
    if not drug_data:
        return None
    
    clinical_trials_journals = get_distinct_journals( drug_data['clinical_trials'])
    pubmed_journals = get_distinct_journals(drug_data['pubMed'])

    exclusive_pubmed_journals = pubmed_journals - clinical_trials_journals

    return extract_related_drugs(data, drug_name, exclusive_pubmed_journals)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help = "drugs data file path",  required=True)
    parser.add_argument("-d", "--drug_name", help = "Drug name to search for", required=True)
    args = parser.parse_args()

    data = load_json_file(args.input_path)['result']
    most_cited_journal = get_journal_with_most_distinct_medications(
        data)
    related_medications = get_related_medications(data, args.drug_name)
    print(f"Journal with the most distinct medications: {most_cited_journal}")
    print(f"Related medications: {related_medications}")
