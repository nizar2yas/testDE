import unittest
import apache_beam as beam
from apache_beam.testing.util import assert_that, equal_to
from apache_beam.testing.test_pipeline import TestPipeline
from src.pipeline import MentionsExtractor, CombinerFn

DRUGS_FILE = "drugs.csv"
CLINICAL_TRIALS_FILE = "clinical_trials.csv"
PUBMED_FILE = "pubmed.csv"
OUTPUT_FILE = "output.json"

class TestMentionsExtractor(unittest.TestCase):

    def test_mentionsextractor(self):
        with TestPipeline() as p:
            drugs = p | "Create drugs" >> beam.Create(["drug_a"])
            drug_list = beam.pvalue.AsList(drugs)
            input_data = '1,\"Clinical trial of drug_a\",2023-10-26,Journal A'
            expected_output = [("drug_a", {'clinical_trials': {'title': 'Clinical trial of drug_a', 'date': '2023-10-26', 'journal': 'Journal A'}})]
            
            results = (p | "create input" >> beam.Create([input_data])
                        | "Extract mentions" >> beam.ParDo(MentionsExtractor.MentionsExtractor('clinical_trials'), drugs=drug_list))
            assert_that(results, equal_to(expected_output))

    def test_combinerfn(self):
        with TestPipeline() as p:
            input_data = [('drug_a', {'clinical_trials': [[{'clinical_trials':{'title': 'Clinical trial of drug_a', 'date': '2023-10-26', 'journal': 'Journal A'}}]], 'pubmed': []}),
                          ('drug_c', {'clinical_trials': [[]], 'pubmed': []}),
                          ('drug_b', {'pubmed': [[{'pubmed':{'title': 'drug_b in pubmed', 'date': '2023-10-27', 'journal': 'Journal B'}}]], 'clinical_trials': []})]
            expected_output = [{'name': 'drug_a', 'clinical_trials': [{'title': 'Clinical trial of drug_a', 'date': '2023-10-26', 'journal': 'Journal A'}], 'pubMed': []}, {'name': 'drug_c', 'clinical_trials': [],'pubMed': []},{'name': 'drug_b', 'clinical_trials': [], 'pubMed': [{'title': 'drug_b in pubmed', 'date': '2023-10-27', 'journal': 'Journal B'}]}]

            results = (p | "Create input" >> beam.Create(input_data)
                       | "Combine" >> beam.CombineGlobally(CombinerFn.CombinerFn()))
            assert_that(results, equal_to([{"result":expected_output}]))


if __name__ == '__main__':
    unittest.main()
