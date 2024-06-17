import google.auth
from google.auth.transport.requests import Request
import google.auth.transport.requests
import google.auth.credentials
import requests
import json

# Load service account credentials
credentials, project = google.auth.load_credentials_from_file('path/to/your-service-account-file.json')

# Get the access token
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
token = credentials.token

# Set up variables
project_id = 'your-project-id'
location = 'your-composer-location'  # e.g., us-central1
composer_env_name = 'your-composer-env-name'
dag_id = 'dataflow_model_job'

# Define the endpoint URL
url = f'https://composer.googleapis.com/v1/projects/{project_id}/locations/{location}/environments/{composer_env_name}/dagRuns'

# Set up the headers with the token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
}

# Define the data payload
data = {
    'dag_run_id': f'manual__{datetime.utcnow().isoformat()}',
    'conf': {},  # Any configuration parameters you need to pass to the DAG
}

# Make the POST request to trigger the DAG
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check the response
if response.status_code == 200:
    print(f'Successfully triggered DAG {dag_id}')
else:
    print(f'Failed to trigger DAG {dag_id}: {response.text}')
