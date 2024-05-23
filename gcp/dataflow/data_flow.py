import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import os
import subprocess

# Define the GCP project settings
project_id = "exploregcp-422706"
region = "us-central1"
staging_location = "gs://testdataflows/staging"
temp_location = "gs://testdataflows/temp"
job_name = "dataflow-docker-python"
docker_image = 'gcr.io/exploregcp-422706/csa'

# Create pipeline options
options = PipelineOptions(
    project=project_id,
    runner="DirectRunner",
    job_name=job_name,
    temp_location=temp_location,
    staging_location=staging_location,
    region=region,
    sdk_container_image=docker_image,
)

    
#Define a custom DoFn to call the list_files_and_folders function
class ListFilesAndFoldersDoFn(beam.DoFn):

    def process(self, element):
        # List files and folders
        current_directory = os.getcwd()
        items = os.listdir(current_directory)
        # Print each item
        for item in items:
            print(item)
        # Yield the element for further processing if needed
        yield element

# Create your pipeline using the options
p = beam.Pipeline(options=options)

# Define your pipeline
(p 
 | "Create data" >> beam.Create([1])  # This creates a single element to trigger the DoFn
 | "List files and folders" >> beam.ParDo(ListFilesAndFoldersDoFn())  # This DoFn will list files and folders
)

# Run the pipeline
result = p.run()
result.wait_until_finish()
