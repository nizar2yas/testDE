import json

def extract_data_from_nested_list(data, field):
    return [
            pub.get(field) 
            for sublist in data.get(field, []) 
            for pub in sublist if pub.get(field) is not None
        ]


def load_medication_data(file_path):
    """Loads medication data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_distinct_journal(journals):
    result = set()
    for journal in journals:
        result.add(journal.get('journal'))
    return result

def get_journals_for_drug(data,drug):
    for item in data:
        if item['name']== drug:
            return item

def get_mentioned_drugs_in_jornals(data,journals):
    drugs=set()
    for item in data:
        drug =item['name']
        for journal in item['pubMed']:
            if journal['journal'] in journals:
                drugs.add(drug)
                break
    return drugs