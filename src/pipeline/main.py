import apache_beam as beam
from src.pipeline import MentionsExtractor as me
from src.pipeline import CombinerFn as cFn
from src.pipeline import CustomPipelineOptions as options
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants for input file names
DRUGS_FILE = "drugs.csv"
CLINICAL_TRIALS_FILE = "clinical_trials.csv"
PUBMED_FILE = "pubmed.csv"
OUTPUT_FILE = "output.json"


def run(options):
    data_path = options.data_folder_path
    output_folder = options.output_folder_path

    logger.info("Starting pipeline with data_path: %s, output_folder: %s", data_path, output_folder)


    with beam.Pipeline(options=options) as p:
        logger.info("Pipeline started")

        # Read drugs.csv to extract the list of drug names
        drugs = (p
                 | f'Read {DRUGS_FILE}' >> beam.io.ReadFromText(f'{data_path}/{DRUGS_FILE}', skip_header_lines=1)
                 | 'Extract drug names' >> beam.Map(lambda line: line.split(',')[1]))

        drug_list = beam.pvalue.AsList(drugs)
        logger.info("Drug list created")

        # Read and extract mentions from clinical_trials.csv
        clinical_trials = (p
                           | f'Read {CLINICAL_TRIALS_FILE}' >> beam.io.ReadFromText(f'{data_path}/{CLINICAL_TRIALS_FILE}', skip_header_lines=1)
                           | 'Extract clinical mentions' >> beam.ParDo(me.MentionsExtractor('clinical_trials'), drugs=drug_list)
                           | 'Group clinical trials by drug' >> beam.GroupByKey())
        logger.info("Clinical trials processed")

        # Read and extract mentions from pubmed.csv
        pubmed = (p
                  | f'Read {PUBMED_FILE}' >> beam.io.ReadFromText(f'{data_path}/{PUBMED_FILE}', skip_header_lines=1)
                  | 'Extract pubmed mentions' >> beam.ParDo(me.MentionsExtractor('pubmed'), drugs=drug_list)
                  | 'Group pubmed by drug' >> beam.GroupByKey())
        logger.info("Pubmed data processed")

        # Combine and format the output
        ({'clinical_trials': clinical_trials, 'pubmed': pubmed}
         | 'CoGroup results' >> beam.CoGroupByKey()
         | 'Combine' >> beam.CombineGlobally(cFn.CombinerFn())
         | 'Convert to JSON' >> beam.Map(lambda x: json.dumps(x))
         | f'Write to {OUTPUT_FILE}' >> beam.io.WriteToText(f'{output_folder}/{OUTPUT_FILE}', shard_name_template=''))

        logger.info("Pipeline finished. Output written to %s/%s",output_folder, OUTPUT_FILE)


if __name__ == '__main__':
    logger.info("Starting main execution")

    pipeline_options = options.CustomPipelineOptions()
    run(pipeline_options)

    logger.info("Main execution finished")

