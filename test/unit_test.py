import unittest
import apache_beam as beam
from apache_beam.testing.util import assert_that, equal_to
from apache_beam.testing.test_pipeline import TestPipeline
from src.pipeline import MentionsExtractor, CombinerFn
import os
import json
from apache_beam.options.pipeline_options import PipelineOptions

DRUGS_FILE = "drugs.csv"
CLINICAL_TRIALS_FILE = "clinical_trials.csv"
PUBMED_FILE = "pubmed.csv"
OUTPUT_FILE = "output.json"

class TestMentionsExtractor(unittest.TestCase):


    def test_pipeline_e2e(self):
        from src.pipeline import CustomPipelineOptions as opt
        # Create test data
        test_data_dir = "test_data"
        os.makedirs(test_data_dir, exist_ok=True)  # Ensure directory exists

        with open(os.path.join(test_data_dir, DRUGS_FILE), "w") as f:
            f.write("id,drug\n")
            f.write("1,drug_a\n")
            f.write("2,drug_b\n")

        with open(os.path.join(test_data_dir, CLINICAL_TRIALS_FILE), "w") as f:
            f.write("id,title,date,journal\n")
            f.write("1,\"Clinical trial of drug_a\",2023-10-26,Journal A\n")

        with open(os.path.join(test_data_dir, PUBMED_FILE), "w") as f:
            f.write("id,title,date,journal\n")
            f.write("1,\"drug_a mentioned in pubmed\",2023-10-27,Journal B\n")

        # Create a temporary directory for output
        test_output_dir = "test_output"
        os.makedirs(test_output_dir, exist_ok=True)

        # Create and configure pipeline options
        options = opt.CustomPipelineOptions(
            ['--data_folder_path', test_data_dir, '--output_folder_path', test_output_dir])

        # Run the pipeline
        self.run(options)

        # Verify the output
        output_file_path = os.path.join(test_output_dir, OUTPUT_FILE)
        with open(output_file_path, 'r') as f:
            output_data_str = f.read()

        output_data = json.loads(output_data_str)
        expected_output = {
            "result": [
                {
                    "name": "drug_a",
                    "clinical_trials": [
                        {"title": "Clinical trial of drug_a",
                            "date": "2023-10-26", "journal": "Journal A"}
                    ],
                    "pubMed": [
                         {"title": "drug_a mentioned in pubmed",
                             "date": "2023-10-27", "journal": "Journal B"}
                    ]
                },
                {
                    "name": "drug_b",
                    "clinical_trials": [],
                    "pubMed": []
                }
            ]
        }

        self.assertDictEqual(output_data, expected_output)

        # Clean up test data and output after the test
        # (Optional:  Comment out during debugging)
        os.remove(os.path.join(test_data_dir, DRUGS_FILE))
        os.remove(os.path.join(test_data_dir, CLINICAL_TRIALS_FILE))
        os.remove(os.path.join(test_data_dir, PUBMED_FILE))
        os.remove(output_file_path)
        os.rmdir(test_data_dir)
        os.rmdir(test_output_dir)
    
    def test_mentionsextractor(self):
        with TestPipeline() as p:
            drugs = p | "Create drugs" >> beam.Create(["drug_a"])
            drug_list = beam.pvalue.AsList(drugs)
            input_data = '1,\"Clinical trial of drug_a\",2023-10-26,Journal A'
            expected_output = [("drug_a", {'clinical_trials': {'title': 'Clinical trial of drug_a', 'date': '2023-10-26', 'journal': 'Journal A'}})]
            
            results = (p | "create input" >> beam.Create([input_data])
                        | "Extract mentions" >> beam.ParDo(MentionsExtractor.MentionsExtractor('clinical_trials'), drugs=drug_list))
            assert_that(results, equal_to(expected_output))

    # def test_combinerfn(self):
    #     with TestPipeline() as p:
    #         input_data = [('drug_a', {'clinical_trials': [[{'clinical_trials':{'title': 'Clinical trial of drug_a', 'date': '2023-10-26', 'journal': 'Journal A'}}]], 'pubmed': []}),
    #                       ('drug_c', {'clinical_trials': [[]], 'pubmed': []}),
    #                       ('drug_b', {'pubmed': [[{'pubmed':{'title': 'drug_b in pubmed', 'date': '2023-10-27', 'journal': 'Journal B'}}]], 'clinical_trials': []})]
    #         expected_output = [{'name': 'drug_a', 'clinical_trials': [{'title': 'Clinical trial of drug_a', 'date': '2023-10-26', 'journal': 'Journal A'}], 'pubMed': []}, {'name': 'drug_c', 'clinical_trials': [],'pubMed': []},{'name': 'drug_b', 'clinical_trials': [], 'pubMed': [{'title': 'drug_b in pubmed', 'date': '2023-10-27', 'journal': 'Journal B'}]}]

    #         results = (p | "Create input" >> beam.Create(input_data)
    #                    | "Combine" >> beam.CombineGlobally(CombinerFn.CombinerFn()))
    #         assert_that(results, equal_to([{"result":expected_output}]))


if __name__ == '__main__':
    unittest.main()
