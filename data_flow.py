import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import subprocess

project_id = "exploregcp-422706"
region = "us-central1"
staging_location = "gs://testdataflows/staging"
temp_location = "gs://testdataflows/temp"
job_name = "dataflow-docker-python"
docker_image = 'gcr.io/exploregcp-422706/csa'

# Create pipeline options
options = PipelineOptions(
    project=project_id,
    runner="DataflowRunner",
    job_name=job_name,
    temp_location=temp_location,
    staging_location=staging_location,
    region=region,
    sdk_container_image=docker_image,
)

# Create your pipeline using the options
p = beam.Pipeline(options=options)

# Define a simple DoFn that prints the input element and runs the command
class RunCommandAndPrintElement(beam.DoFn):
    def process(self, element):
        print(element)
        subprocess.run(['python3', 'app.py', '--task=predictions'], check=True)

# Define your pipeline
(p
 | "Create data" >> beam.Create([1, 2, 3, 4, 5])  # This is your input data
 | "Run command and print data" >> beam.ParDo(RunCommandAndPrintElement())  # This DoFn will run the command and print each element of the input data
)

# Run the pipeline
result = p.run()
result.wait_until_finish()
