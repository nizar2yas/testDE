import unittest
from unittest.mock import patch, mock_open
import json

# Sample data from output.json for testing purposes
sample_medication_data = [
    {
        "name": "DIPHENHYDRAMINE",
        "clinical_trials": [
            [{"clinical_trials": {"title": "Study on Diphenhydramine", "date": "2020-01-01", "journal": "Journal of emergency nursing"}}]
        ],
        "pubMed": [
            [{"pubmed": {"title": "Diphenhydramine for allergies", "date": "2019-01-01", "journal": "Journal of emergency nursing"}}]
        ]
    },
    {
        "name": "TETRACYCLINE",
        "clinical_trials": [],
        "pubMed": [
            [{"pubmed": {"title": "Tetracycline Resistance Study", "date": "2020-01-01", "journal": "Journal of food protection"}}]
        ]
    },
    {
        "name": "ETHANOL",
        "clinical_trials": [],
        "pubMed": [
            [{"pubmed": {"title": "Study on Ethanol effects", "date": "2020-01-01", "journal": "Journal of food protection"}}]
        ]
    }
]


# Importing functions from the original code
from t2 import get_journal_with_most_distinct_medications, get_related_medications

class TestMedicationFunctions(unittest.TestCase):

    def test_get_journal_with_most_distinct_medications(self):
        # Call the function
        result = get_journal_with_most_distinct_medications(sample_medication_data)
        
        # Verify the result
        self.assertEqual(result[0], 'Journal of emergency nursing', "Should return the journal mentioning the most distinct drugs.")

    def test_get_related_medications(self):
        # Test for 'TETRACYCLINE'
        result = get_related_medications(sample_medication_data, 'TETRACYCLINE')
        
        # Expected drugs mentioned by the same journals in PubMed but not Clinical Trials
        expected_result = {'ETHANOL'}
        
        # Verify the result
        self.assertEqual(result, expected_result, "Should return the set of related drugs.")

if __name__ == '__main__':
    unittest.main()
