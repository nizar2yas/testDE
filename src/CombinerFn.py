import apache_beam as beam
from utils import extract_data_from_nested_list

class CombinerFn(beam.CombineFn):

    def create_accumulator(self):
        return []

    def add_input(self, accumulator, input):
        drug_name, data = input
        # Extract and flatten data if needed
        clinical_trials = extract_data_from_nested_list(data,"clinical_trials")
        pub_med = extract_data_from_nested_list(data,"pubmed")
        
        output = {
            'name': drug_name,
            'clinical_trials': clinical_trials,
            'pubMed': pub_med
        }
        accumulator.append(output)
        return accumulator

    def merge_accumulators(self, accumulators):
        return [x for accumulator in accumulators for x in accumulator]

    def extract_output(self, accumulator):
        return {"result":accumulator}