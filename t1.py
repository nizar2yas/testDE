import json
from collections import defaultdict

# Load the JSON data
medication_data = [
    {"name": "DIPHENHYDRAMINE", "clinical_trials": [[{"clinical_trials": {"title": "Use of Diphenhydramine as an Adjunctive Sedative for Colonoscopy in Patients Chronically on Opioids", "date": "1 January 2020", "journal": "Journal of emergency nursing"}}, {"clinical_trials": {"title": "Phase 2 Study IV QUZYTTIR™ (Cetirizine Hydrochloride Injection) vs V Diphenhydramine", "date": "1 January 2020", "journal": "Journal of emergency nursing"}}, {"clinical_trials": {"title": "Feasibility of a Randomized Controlled Clinical Trial Comparing the Use of Cetirizine to Replace Diphenhydramine in the Prevention of Reactions Related to Paclitaxel", "date": "1 January 2020", "journal": "Journal of emergency nursing"}}]], "pubMed": [[{"pubmed": {"title": "A 44-year-old man with erythema of the face diphenhydramine, neck, and chest, weakness, and palpitations", "date": "01/01/2019", "journal": "Journal of emergency nursing"}}, {"pubmed": {"title": "An evaluation of benadryl, pyribenzamine, and other so-called diphenhydramine antihistaminic drugs in the treatment of allergy.", "date": "01/01/2019", "journal": "Journal of emergency nursing"}}, {"pubmed": {"title": "Diphenhydramine hydrochloride helps symptoms of ciguatera fish poisoning.", "date": "02/01/2019", "journal": "The Journal of pediatrics"}}]]},
    {"name": "TETRACYCLINE", "clinical_trials": [], "pubMed": [[{"pubmed": {"title": "Tetracycline Resistance Patterns of Lactobacillus buchneri Group Strains.", "date": "01/01/2020", "journal": "Journal of food protection"}}, {"pubmed": {"title": "Appositional Tetracycline bone formation rates in the Beagle.", "date": "02/01/2020", "journal": "American journal of veterinary research"}}, {"pubmed": {"title": "Rapid reacquisition of contextual fear following extinction in mice: effects of amount of extinction, tetracycline acute ethanol withdrawal, and ethanol intoxication.", "date": "2020-01-01", "journal": "Psychopharmacology"}}]]},
    {"name": "ETHANOL", "clinical_trials": [], "pubMed": [[{"pubmed": {"title": "Rapid reacquisition of contextual fear following extinction in mice: effects of amount of extinction, tetracycline acute ethanol withdrawal, and ethanol intoxication.", "date": "2020-01-01", "journal": "Psychopharmacology"}}]]},
    {"name": "EPINEPHRINE", "clinical_trials": [[{"clinical_trials": {"title": "Tranexamic Acid Versus Epinephrine During Exploratory Tympanotomy", "date": "27 April 2020", "journal": "Journal of emergency nursingÃJournal of emergency nursing\xc3(28"}}]], "pubMed": [[{"pubmed": {"title": "The High Cost of Epinephrine Autoinjectors and Possible Alternatives.", "date": "01/02/2020", "journal": "The journal of allergy and clinical immunology. In practice"}}, {"pubmed": {"title": "Time to epinephrine treatment is associated with the risk of mortality in children who achieve sustained ROSC after traumatic out-of-hospital cardiac arrest.", "date": "01/03/2020", "journal": "The journal of allergy and clinical immunology. In practice"}}]]},
    {"name": "BETAMETHASONE", "clinical_trials": [[{"clinical_trials": {"title": "Preemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or ÃPreemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or \xc3±Preemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or \xc3\xb1 Laminectomy", "date": "1 January 2020", "journal": "Hôpitaux Universitaires de Genève"}}]], "pubMed": []}
]

# Part 1: Find the journal with the most unique medication mentions
journal_medications = defaultdict(set)

for med in medication_data:
    med_name = med["name"]
    # Check PubMed journals
    for pub_list in med.get("pubMed", []):
        for pub_entry in pub_list:
            journal = pub_entry["pubmed"]["journal"]
            journal_medications[journal].add(med_name)
    # Check Clinical Trials journals
    for trial_list in med.get("clinical_trials", []):
        for trial_entry in trial_list:
            journal = trial_entry["clinical_trials"]["journal"]
            journal_medications[journal].add(med_name)

# Find the journal with the most unique medications
most_cited_journal = max(journal_medications, key=lambda j: len(journal_medications[j]))
print("Journal with most unique medication mentions:", most_cited_journal)

# Part 2: Find medications mentioned in the same PubMed journals but not in Clinical Trials
med_in_pubmed_only = defaultdict(set)

for med in medication_data:
    med_name = med["name"]
    pubmed_journals = set()
    clinical_journals = set()

    # Collect PubMed journals for the current medication
    for pub_list in med.get("pubMed", []):
        for pub_entry in pub_list:
            pubmed_journals.add(pub_entry["pubmed"]["journal"])

    # Collect Clinical Trials journals for the current medication
    for trial_list in med.get("clinical_trials", []):
        for trial_entry in trial_list:
            clinical_journals.add(trial_entry["clinical_trials"]["journal"])

    # Get journals unique to PubMed
    unique_pubmed_journals = pubmed_journals - clinical_journals

    for journal in unique_pubmed_journals:
        med_in_pubmed_only[journal].add(med_name)

print("\nMedications mentioned in the same PubMed journals but not in Clinical Trials:")
for journal, meds in med_in_pubmed_only.items():
    print(f"Journal: {journal}, Medications: {', '.join(meds)}")
