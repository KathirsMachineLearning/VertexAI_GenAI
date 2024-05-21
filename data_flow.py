import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners.dataflow.options.pipeline_options import SetupOptions
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
    region=region
)

# Set the SDK container image
setup_options = options.view_as(SetupOptions)
setup_options.sdk_container_image = docker_image

# Create your pipeline using the options
p = beam.Pipeline(options=options)

# Define a simple DoFn that runs the command to execute app.py
class RunApp(beam.DoFn):
    def process(self, element):
        # This will run app.py within the Docker container
        result = subprocess.run(['python', 'app.py'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error executing app.py: {result.stderr}")
        else:
            print(f"app.py output: {result.stdout}")
        yield element

# Define your pipeline
(p 
 | "Create data" >> beam.Create([1])  # This is your input data
 | "Run app.py" >> beam.ParDo(RunApp())  # This DoFn will run the app.py script
)

# Run the pipeline
result = p.run()
result.wait_until_finish()
