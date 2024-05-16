import time
from google.cloud import dataflow_v1beta3 as dataflow
from google.api_core.exceptions import NotFound
import datetime


class DataflowHandler:
    def __init__(self, project_id, credentials_path=None):
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.client = self._create_client()

    def _create_client(self):
        if self.credentials_path:
            return dataflow.JobsV1Beta3Client.from_service_account_json(
                self.credentials_path
            )
        else:
            return dataflow.JobsV1Beta3Client()

    def create_job_from_template(
        self,
        template_name,
        parameters,
        location=None,
        job_id=None,
        wait_until_finished=False,
        max_wait_time=None,
        teardown_policy=None,
        on_success_handler=None,
        on_error_handler=None,
        additional_experiments=None,
        additional_job_labels=None,
        kms_key_name=None,
        service_account_email=None,
        network=None,
        subnetwork=None,
        zone=None,
        enable_streaming_engine=None,
        ip_configuration=None,
        use_public_ips=None,
        max_workers=None,
        disk_size_gb=None,
        machine_type=None,
        num_workers=None,
        worker_region=None,
        worker_zone=None,
        autoscaling_algorithm=None,
        max_num_workers=None,
        network_tags=None,
        service_account=None,
        delegate_to=None,
        labels=None,
        environment=None,
        retries=None,
        timeout=None,
        metadata=None,
    ):
        template = f"projects/{self.project_id}/locations/{location}/templates/{template_name}"
        request = {
            "jobName": job_id,
            "parameters": parameters,
            "environment": environment,
            "location": location,
            "requestId": job_id,
            "projectId": self.project_id,
            "gcsPath": template,
        }
        response = self.client.create_job_from_template(request=request)
        return response

    def create_job(
        self, name, steps, environment=None, retries=None, timeout=None, metadata=None
    ):
        job = {
            "name": name,
            "steps": steps,
            "environment": environment,
            "location": "us-central1",  # Default location
            "projectId": self.project_id,
        }
        response = self.client.create_job(projectId=self.project_id, body=job)
        return response

    def get_job(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        response = self.client.get_job(name=job_name)
        return response

    def cancel_job(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        request = {"name": job_name}
        response = self.client.cancel_job(request=request)
        return response

    def is_job_done(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        response = self.client.get_job(name=job_name)
        return response.state == dataflow.JobState.JOB_STATE_DONE
    
    def wait_for_done(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        while True:
            job = self.client.get_job(name=job_name)
            if job.state in [
                dataflow.JobState.JOB_STATE_DONE,
                dataflow.JobState.JOB_STATE_FAILED,
            ]:
                return job.state
            time.sleep(10)  # Adjust the sleep interval as needed

    def list_jobs(
        self, project_id=None, location=None, filter=None, retries=None, timeout=None
    ):
        location = f"projects/{self.project_id}/locations/{location}"
        response = self.client.list_jobs(parent=location)
        jobs = [job for job in response]
        return jobs

    def delete_job(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        try:
            self.client.delete_job(name=job_name)
        except NotFound:
            print(f"Job '{job_id}' not found.")
    
    def get_job_metrics(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        try:
            job_metrics = self.client.get_job_metrics(name=job_name)
            return job_metrics
        except NotFound:
            print(f"Job '{job_id}' not found.")
            return None

    def get_job_messages(
        self, job_id, location=None, retries=None, timeout=None, metadata=None
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        try:
            job_messages = self.client.get_job_messages(name=job_name)
            return job_messages
        except NotFound:
            print(f"Job '{job_id}' not found.")
            return None

    def template_to_parameters(
        self, template_name, location=None, project_id=None, retries=None, timeout=None, metadata=None
    ):
        try:
            template_spec = {
                "projectId": project_id or self.project_id,
                "location": location,
                "gcsPath": template_name,
            }
            templates_client = dataflow_v1beta3.TemplatesServiceClient()
            response = templates_client.get_template_parameters(
                template_spec, retries=retries, timeout=timeout, metadata=metadata
            )
            return response.parameters
        except NotFound:
            print(f"Template '{template_name}' not found.")
            return None

    def stage_job(
        self,
        job_id,
        location=None,
        project_id=None,
        retries=None,
        timeout=None,
        metadata=None,
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        try:
            request = dataflow_v1beta3.StageJobRequest(
                job_name=job_name,
                location=location,
                project_id=project_id or self.project_id,
            )
            response = self.client.stage_job(
                request=request, retries=retries, timeout=timeout, metadata=metadata
            )
            return response
        except NotFound:
            print(f"Job '{job_id}' not found.")
            return None

    def update_job(
        self,
        job_id,
        location=None,
        project_id=None,
        retries=None,
        timeout=None,
        metadata=None,
    ):
        job_name = f"projects/{self.project_id}/locations/{location}/jobs/{job_id}"
        try:
            request = dataflow_v1beta3.UpdateJobRequest(
                job_name=job_name,
                location=location,
                project_id=project_id or self.project_id,
            )
            response = self.client.update_job(
                request=request, retries=retries, timeout=timeout, metadata=metadata
            )
            return response
        except NotFound:
            print(f"Job '{job_id}' not found.")
            return None