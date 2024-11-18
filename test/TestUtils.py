import unittest
from src.utils.utils import extract_data_from_nested_list, get_distinct_journals, extract_related_drugs

class TestUtils(unittest.TestCase):

    def test_extract_data_from_nested_list(self):
        data = {'field': [[{'field': 'value1', 'other': 'data1'}], [{'field': 'value2'}]]}
        expected = ['value1', 'value2']
        self.assertEqual(extract_data_from_nested_list(data, 'field'), expected)

        # Test with missing field
        data = {'other_field': []}
        self.assertEqual(extract_data_from_nested_list(data, 'field'), [])


        # Test with None values for 'field'
        data = {'field': [[{'field': None, 'other': 'data1'}], [{'other_key': 'value2'}]]}
        self.assertEqual(extract_data_from_nested_list(data, 'field'), [])


    def test_get_distinct_journals(self):
        journals = [
            {'journal': 'Journal 1'},
            {'journal': 'Journal 2'},
            {'journal': 'Journal 1'},  # Duplicate
            {'other': 'data'}, #missing journal key
            {'journal': None} # None journal value
        ]

        expected = {'Journal 1', 'Journal 2'}
        self.assertEqual(get_distinct_journals(journals), expected)

        # Test with empty input
        self.assertEqual(get_distinct_journals([]), set())

    def test_extract_related_drugs(self):
        data = [
            {'name': 'Drug A', 'pubMed': [{'journal': 'Journal 1'}, {'journal': 'Journal 2'}]},
            {'name': 'Drug B', 'pubMed': [{'journal': 'Journal 2'}, {'journal': 'Journal 3'}]},
            {'name': 'Drug C', 'pubMed': [{'journal': 'Journal 4'}]}
        ]
        exclusive_journals = {'Journal 2'}  # Unique to Drug A
        related_drugs = extract_related_drugs(data, 'Drug A', exclusive_journals)
        self.assertEqual(related_drugs, {'Drug B'})

        # Test when no other drug shares the exclusive journals
        exclusive_journals = {'Journal 1'}
        related_drugs = extract_related_drugs(data, 'Drug A', exclusive_journals)
        self.assertEqual(related_drugs, set())

        # Test with empty exclusive journals
        exclusive_journals = set()
        related_drugs = extract_related_drugs(data, 'Drug A', exclusive_journals)
        self.assertEqual(related_drugs, set())



if __name__ == '__main__':
    unittest.main()

