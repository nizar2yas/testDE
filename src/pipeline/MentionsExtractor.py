import apache_beam as beam
import csv
# Class for extracting mentions from a CSV line
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
            else :
                yield (drug_name, {
                    self.field_name: None
                })
