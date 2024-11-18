import json

def load_medication_data(file_path):
    """Loads medication data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_journal_with_most_distinct_medications(medication_data):
    """Finds the journal that mentions the highest number of distinct medications."""
    journal_medications = {}

    for med in medication_data:
        name = med['name']
        all_journals = set()

        # Collect journal names from clinical trials
        for trial_list in med.get('clinical_trials', []):
            for trial in trial_list:
                journal = trial['clinical_trials']['journal']
                all_journals.add(journal)

        # Collect journal names from PubMed
        for pub_list in med.get('pubMed', []):
            for pub in pub_list:
                journal = pub['pubmed']['journal']
                all_journals.add(journal)

        for journal in all_journals:
            if journal not in journal_medications:
                journal_medications[journal] = set()
            journal_medications[journal].add(name)

    # Find the journal with the most distinct medications
    max_journal = max(journal_medications, key=lambda k: len(journal_medications[k]))
    return max_journal, len(journal_medications[max_journal])

def get_related_medications(medication_data, target_medication):
    """Finds medications mentioned in the same journals as the target_medication in PubMed, 
    but not in Clinical Trials."""
    pubmed_journals = set()
    clinical_trial_journals = set()

    # Identify journals for the target medication
    for med in medication_data:
        if med['name'].lower() == target_medication.lower():
            # Collect PubMed journals
            for pub_list in med.get('pubMed', []):
                for pub in pub_list:
                    pubmed_journals.add(pub['pubmed']['journal'])
            
            # Collect Clinical Trials journals
            for trial_list in med.get('clinical_trials', []):
                for trial in trial_list:
                    clinical_trial_journals.add(trial['clinical_trials']['journal'])
            break

    # Find journals exclusive to PubMed
    exclusive_pubmed_journals = pubmed_journals - clinical_trial_journals

    # Find medications mentioned in those exclusive PubMed journals
    related_medications = set()
    for med in medication_data:
        if med['name'].lower() != target_medication.lower():
            for pub_list in med.get('pubMed', []):
                for pub in pub_list:
                    if pub['pubmed']['journal'] in exclusive_pubmed_journals:
                        related_medications.add(med['name'])

    return related_medications

# Load the medication data
# file_path = 'output.json'
# medication_data = load_medication_data(file_path)

# # Find the journal with the most distinct medications
# journal, count = get_journal_with_most_distinct_medications(medication_data)
# print(f"Journal with the most distinct medications: {journal} ({count} medications)")

# # User input for the second function
# target_medication = input("Enter the name of the medication: ")
# related_meds = get_related_medications(medication_data, target_medication)
# print(f"Medications mentioned in the same journals as {target_medication} in PubMed but not in Clinical Trials:")
# print(related_meds)
