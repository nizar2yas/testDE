from apache_beam.options.pipeline_options import PipelineOptions

class CustomPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--data_folder_path',
            type=str,
            help='Path to the input CSV file',
            required=True
        )
        parser.add_argument(
            '--output_folder_path',
            type=str,
            help='Path to the output folder',
            required=True
        )
