import apache_beam as beam
from ..utils.utils import extract_data_from_nested_list
import logging


class CombinerFn(beam.CombineFn):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_accumulator(self):
        self.logger.debug("Creating accumulator")
        return []

    def add_input(self, accumulator, input):
        drug_name, data = input
        self.logger.debug("Construct journals for drug: %s", drug_name)
        # Extract and flatten data if needed
        clinical_trials = extract_data_from_nested_list(
            data, "clinical_trials")
        pub_med = extract_data_from_nested_list(data, "pubmed")

        output = {
            'name': drug_name,
            'clinical_trials': clinical_trials,
            'pubMed': pub_med
        }
        accumulator.append(output)
        self.logger.debug("Accumulator updated: %s", accumulator)
        return accumulator

    def merge_accumulators(self, accumulators):
        merged_accumulator = [
            x for accumulator in accumulators for x in accumulator]
        self.logger.debug("Merged accumulators: %s", merged_accumulator)
        return merged_accumulator

    def extract_output(self, accumulator):
        self.logger.debug("Extracting output: %s", accumulator)
        return {"result": accumulator}
