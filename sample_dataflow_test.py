from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners import DataflowRunner
import apache_beam as beam

# Replace with your project ID, region, and bucket
project_id = "exploregcp-422706"
region = "us-central1"
staging_location = "gs://testdataflows/staging"
temp_location = "gs://testdataflows/temp"
job_name = "dataflow-sample-python"

# Set up the pipeline options
options = PipelineOptions(
    project=project_id,
    runner="DataflowRunner",
    job_name=job_name,
    temp_location=temp_location,
    staging_location=staging_location,
    region=region,
)

# Define the pipeline
def run():
    with beam.Pipeline(options=options) as p:
        lines = p | 'ReadFromText' >> beam.io.ReadFromText('gs://testdataflows/test/input.txt')
        counts = (
            lines
            | 'Split' >> (beam.FlatMap(lambda x: x.split(' '))
                          .with_output_types(str))
            | 'PairWithOne' >> beam.Map(lambda x: (x, 1))
            | 'GroupAndSum' >> beam.CombinePerKey(sum)
        )
        counts | 'WriteToText' >> beam.io.WriteToText('gs://testdataflows/output.txt')

# Run the pipeline
if __name__ == "__main__":
    run()
