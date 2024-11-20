import apache_beam as beam
import csv
import logging

# Class for extracting mentions from a CSV line
class MentionsExtractor(beam.DoFn):
    def __init__(self, field_name):
        self.field_name = field_name
        self.logger = logging.getLogger(__name__)

    def process(self, element, drugs, ):
        id_, title, date, journal = next(csv.reader(
            [element], delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True))
        self.logger.debug("Processing element: %s", element)
        for drug_name in drugs:
            self.logger.debug("Checking drug: {drug_name}")
            if drug_name.lower() in title.lower():
                output_element = (drug_name, {
                    self.field_name: {
                        'title': title.strip('"'),
                        'date': date,
                        'journal': journal
                    }
                })
                self.logger.debug("Yielding mention: %s", output_element)
            else:
                output_element = (drug_name, {self.field_name: None})
                self.logger.debug("No mention found, yielding: %s", output_element)
            yield output_element
