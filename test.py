import unittest
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from apache_beam.testing.test_stream import TestStream
from apache_beam import Create, DoFn, ParDo, GroupByKey, Map
import json
import src.MentionsExtractor as me
from src.utils import FormatOutput
# Assuming MentionsExtractor and FormatOutput are defined as shown above


class TestPipeline(unittest.TestCase):

    def test_mentions_extractor(self):
        input_data = [
            '1,"Drug A and Drug B",2023-10-01,"Journal A"',
            '2,"Drug C study",2024-01-15,"Journal B"',
            '3,"A research on Drug B",2024-05-20,"Journal C"'
        ]
        drugs = ['Drug A', 'Drug B', 'Drug C']
        expected_output = [
            ('Drug A', {
                'clinical_trials': {
                    'title': 'Drug A and Drug B',
                    'date': '2023-10-01',
                    'journal': 'Journal A'
                }
            }),
            ('Drug B', {
                'clinical_trials': {
                    'title': 'Drug A and Drug B',
                    'date': '2023-10-01',
                    'journal': 'Journal A'
                }
            }),
            ('Drug C', {
                'clinical_trials': {
                    'title': 'Drug C study',
                    'date': '2024-01-15',
                    'journal': 'Journal B'
                }
            }),
            ('Drug B', {
                'clinical_trials': {
                    'title': 'A research on Drug B',
                    'date': '2024-05-20',
                    'journal': 'Journal C'
                }
            })
        ]

        with TestPipeline() as p:
            input_collection = p | 'Create Input' >> Create(input_data)
            output = (input_collection
                      | 'Apply MentionsExtractor' >> ParDo(me.MentionsExtractor('clinical_trials'), drugs=drugs))
            assert_that(output, equal_to(expected_output))

    def test_format_output(self):
        input_data = [
            ('Drug A', {'clinical_trials': [{'title': 'Study on Drug A', 'date': '2023-05-10', 'journal': 'Journal A'}],
                        'pubmed': []}),
            ('Drug B', {'clinical_trials': [],
                        'pubmed': [{'title': 'PubMed on Drug B', 'date': '2024-03-12', 'journal': 'Journal B'}]})
        ]
        expected_output = [
            json.dumps({
                'name': 'Drug A',
                'clinical_trials': [{'title': 'Study on Drug A', 'date': '2023-05-10', 'journal': 'Journal A'}],
                'pubMed': []
            }),
            json.dumps({
                'name': 'Drug B',
                'clinical_trials': [],
                'pubMed': [{'title': 'PubMed on Drug B', 'date': '2024-03-12', 'journal': 'Journal B'}]
            })
        ]

        with TestPipeline() as p:
            input_collection = p | 'Create Input for FormatOutput' >> Create(
                input_data)
            output = (input_collection
                      | 'Apply FormatOutput' >> ParDo(FormatOutput())
                      | 'Convert to JSON' >> Map(lambda x: json.dumps(x)))
            assert_that(output, equal_to(expected_output))


if __name__ == '__main__':
    unittest.main()
