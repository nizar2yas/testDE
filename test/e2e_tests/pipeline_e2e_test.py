import unittest
import json
import os
from src.pipeline import  CustomPipelineOptions
from src.pipeline.main import run

# Constants for input file names (used in the pipeline)
DRUGS_FILE = "drugs.csv"
CLINICAL_TRIALS_FILE = "clinical_trials.csv"
PUBMED_FILE = "pubmed.csv"
OUTPUT_FILE = "output.json"

class TestPipeline(unittest.TestCase):

    def test_pipeline_e2e(self):
        # Create test data
        test_data_dir = "test_data"
        os.makedirs(test_data_dir, exist_ok=True)

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
        pipeline_options = CustomPipelineOptions.CustomPipelineOptions(['--data_folder_path', test_data_dir, '--output_folder_path', test_output_dir])

         # Use TestPipeline for unit testing
            # Import and run your pipeline function here.  Adjust the import path if necessary
        run(pipeline_options)  # Pass pipeline_options to your run function


        # Construct expected output
        expected_output = {
            "result": [
                {
                    "name": "drug_a",
                    "clinical_trials": [
                        {"title": "Clinical trial of drug_a", "date": "2023-10-26", "journal": "Journal A"}
                    ],
                    "pubMed": [
                        {"title": "drug_a mentioned in pubmed", "date": "2023-10-27", "journal": "Journal B"}
                    ]
                },
                {
                    "name": "drug_b",
                    "clinical_trials": [],
                    "pubMed": []
                }
            ]
        }

        # Read the output file and compare with expected output
        output_file_path = os.path.join(test_output_dir, OUTPUT_FILE)

        # Assert output file exists
        self.assertTrue(os.path.exists(output_file_path))

        with open(output_file_path, 'r') as f:
            output_data_str = f.read()
            # Because WriteToText creates sharded files even with an empty template,
            # make sure to only parse valid JSON, ignoring empty lines.
            valid_json_lines = [line for line in output_data_str.splitlines() if line.strip()]
            output_data = json.loads(valid_json_lines[0])  # Convert back to JSON to compare
            
        self.assertDictEqual(output_data, expected_output)

        # Clean up test data and output after the test (Optional)
        os.remove(os.path.join(test_data_dir, DRUGS_FILE))
        os.remove(os.path.join(test_data_dir, CLINICAL_TRIALS_FILE))
        os.remove(os.path.join(test_data_dir, PUBMED_FILE))
        for filename in os.listdir(test_output_dir): # Clean up all sharded files
            os.remove(os.path.join(test_output_dir, filename))
        os.rmdir(test_data_dir)
        os.rmdir(test_output_dir)

if __name__ == '__main__':
    unittest.main()