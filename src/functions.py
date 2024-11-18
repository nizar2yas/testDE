from utils import get_distinct_journal, get_journals_for_drug, get_mentioned_drugs_in_jornals


def get_journal_with_most_distinct_medications(data):
    drugs_journals = {}
    for drugs in data['result']:
        name = drugs['name']
        clinical_trials_journals = get_distinct_journal(
            drugs['clinical_trials'])
        pub_med_journal = get_distinct_journal(drugs['pubMed'])
        drugs_journals[name] = clinical_trials_journals.union(pub_med_journal)
    return max(drugs_journals, key=lambda k: len(drugs_journals[k]))


def get_related_medications(data, drug):
    journals = get_journals_for_drug(data['result'], drug)

    if journals:
        clinical_trials_journals = get_distinct_journal( journals['clinical_trials'])
        pub_med_journal = get_distinct_journal(journals['pubMed'])
        only_pub_med = pub_med_journal - clinical_trials_journals
        drugs = get_mentioned_drugs_in_jornals(data['result'],only_pub_med).remove(drug)
    return drugs
