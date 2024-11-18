import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import csv

class MentionsExtractor(beam.DoFn):
    def __init__(self, field_name):
        self.field_name = field_name

    def process(self, element, drugs):
        id_, title, date, journal = next(csv.reader(
            [element], delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
        for drug_name in drugs:
            if drug_name.lower() in title.lower():
                yield (drug_name, {
                    self.field_name: {
                        'title': title.strip('"'),
                        'date': date,
                        'journal': journal
                    }
                })


class FormatOutput(beam.DoFn):
    def process(self, element):
        drug_name, data = element
        output = {
            'name': drug_name,
            'clinical_trials': data.get('clinical_trials', []),
            'pubMed': data.get('pubmed', [])
        }
        yield output
# Function to run the pipeline


def run():
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        # Read drugs.csv to extract the list of drug names
        drugs = (p
                 | 'Read drugs.csv' >> beam.io.ReadFromText('src/data/drugs.csv', skip_header_lines=1)
                 | 'Extract drug names' >> beam.Map(lambda line: line.split(',')[1]))

        drug_list = beam.pvalue.AsList(drugs)

        # Read and extract mentions from clinical_trials.csv
        clinical_trials = (p
                           | 'Read clinical_trials.csv' >> beam.io.ReadFromText('src/data/clinical_trials.csv', skip_header_lines=1)
                           | 'Extract clinical mentions' >> beam.ParDo(MentionsExtractor('clinical_trials'), drugs=drug_list)
                           | 'Group clinical trials by drug' >> beam.GroupByKey())

        # Read and extract mentions from pubmed.csv
        pubmed = (p
                  | 'Read pubmed.csv' >> beam.io.ReadFromText('src/data/pubmed.csv', skip_header_lines=1)
                  | 'Extract pubmed mentions' >> beam.ParDo(MentionsExtractor('pubmed'), drugs=drug_list)
                  | 'Group pubmed by drug' >> beam.GroupByKey())

        # Combine and format the output
        combined_results = ({'clinical_trials': clinical_trials, 'pubmed': pubmed}
                            | 'CoGroup results' >> beam.CoGroupByKey()
                            | 'Format output' >> beam.ParDo(FormatOutput())
                            | 'Convert to JSON' >> beam.Map(lambda x: json.dumps(x))
                            | 'Write to JSON' >> beam.io.WriteToText('output.json', shard_name_template=''))


if __name__ == '__main__':
    run()
