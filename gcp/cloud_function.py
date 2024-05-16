from google.cloud import functions_v1

class CloudFunctionHandler:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = functions_v1.CloudFunctionsServiceClient()

    def create_function(self, name, runtime, entry_point, trigger, source_archive_url=None, source_archive_bucket=None, source_archive_object=None, trigger_resource=None, service_account_email=None, network=None, max_instances=None, min_instances=None, vpc_connector=None, vpc_connector_egress_settings=None, available_memory_mb=None, timeout=None, kms_key_name=None, environment_variables=None, labels=None, build_environment=None, build_worker_pool=None, build_name=None, description=None, update_on_deploy=None, region=None, project=None, retries=None, metadata=None):
        location = f"projects/{self.project_id}/locations/{region}"
        parent = f"projects/{self.project_id}/locations/{region}"
        function = {
            "name": f"projects/{self.project_id}/locations/{region}/functions/{name}",
            "description": description,
            "entry_point": entry_point,
            "runtime": runtime,
            "trigger": trigger,
            "source_archive_url": source_archive_url,
            "source_archive_bucket": source_archive_bucket,
            "source_archive_object": source_archive_object,
            "environment_variables": environment_variables,
            "service_account_email": service_account_email,
            "network": network,
            "max_instances": max_instances,
            "min_instances": min_instances,
            "vpc_connector": vpc_connector,
            "vpc_connector_egress_settings": vpc_connector_egress_settings,
            "available_memory_mb": available_memory_mb,
            "timeout": timeout,
            "kms_key_name": kms_key_name,
            "labels": labels,
            "build_environment": build_environment,
            "build_worker_pool": build_worker_pool,
            "build_name": build_name,
            "update_on_deploy": update_on_deploy,
        }
        response = self.client.create_function(
            parent=parent, function=function, retry=retries, timeout=timeout, metadata=metadata
        )
        return response

    def create_function_from_zip(self, name, runtime, entry_point, zip_path, trigger, source_archive_url=None, source_archive_bucket=None, source_archive_object=None, trigger_resource=None, service_account_email=None, network=None, max_instances=None, min_instances=None, vpc_connector=None, vpc_connector_egress_settings=None, available_memory_mb=None, timeout=None, kms_key_name=None, environment_variables=None, labels=None, build_environment=None, build_worker_pool=None, build_name=None, description=None, update_on_deploy=None, region=None, project=None, retries=None, metadata=None):
        location = f"projects/{self.project_id}/locations/{region}"
        parent = f"projects/{self.project_id}/locations/{region}"
        function = {
            "name": f"projects/{self.project_id}/locations/{region}/functions/{name}",
            "description": description,
            "entry_point": entry_point,
            "runtime": runtime,
            "trigger": trigger,
            "source_archive_url": source_archive_url,
            "source_archive_bucket": source_archive_bucket,
            "source_archive_object": source_archive_object,
            "environment_variables": environment_variables,
            "service_account_email": service_account_email,
            "network": network,
            "max_instances": max_instances,
            "min_instances": min_instances,
            "vpc_connector": vpc_connector,
            "vpc_connector_egress_settings": vpc_connector_egress_settings,
            "available_memory_mb": available_memory_mb,
            "timeout": timeout,
            "kms_key_name": kms_key_name,
            "labels": labels,
            "build_environment": build_environment,
            "build_worker_pool": build_worker_pool,
            "build_name": build_name,
            "update_on_deploy": update_on_deploy,
        }
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
        response = self.client.create_function(
            parent=parent, function=function, source_archive_content=zip_content, retry=retries, timeout=timeout, metadata=metadata
        )
        return response

    def get_function(self, name, region=None, project=None, retry=None, timeout=None, metadata=None):
        """
        Retrieves information about a specific Cloud Function.

        Args:
            name (str): The name of the Cloud Function.
            region (str): The region where the Cloud Function is deployed.
            project (str): The ID of the GCP project.
            client: A client object used to make requests to the Cloud Functions API.
            retries (Optional[int]): The number of retries for the request.
            timeout (Optional[float]): The timeout duration for the request in seconds.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata headers for the request.

        Returns:
            google.cloud.functions_v1.types.CloudFunction: The Cloud Function resource.

        Raises:
            google.api_core.exceptions.NotFound: If the Cloud Function is not found.
            google.api_core.exceptions.GoogleAPICallError: If the API request fails.
        """
        if project is None:
            project = self.project_id

        function_name = f"projects/{project}/locations/{region}/functions/{name}"
        function = self.client.get_function(name=function_name, retry=retry, timeout=timeout, metadata=metadata)

        return function

    def delete_function(self, name, region=None, project=None, retry=None, timeout=None, metadata=None):
        """
        Deletes a Cloud Function.

        Args:
            name (str): The name of the Cloud Function.
            region (str): The region where the Cloud Function is deployed.
            project (str): The ID of the GCP project.
            client: A client object used to make requests to the Cloud Functions API.
            retries (Optional[int]): The number of retries for the request.
            timeout (Optional[float]): The timeout duration for the request in seconds.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata headers for the request.

        Raises:
            google.api_core.exceptions.NotFound: If the Cloud Function is not found.
            google.api_core.exceptions.GoogleAPICallError: If the API request fails.
        """
        if project is None:
            project = self.project_id

        function_name = f"projects/{project}/locations/{region}/functions/{name}"
        request = functions_v1.DeleteFunctionRequest(name=function_name)

        self.client.delete_function(request=request, retry=retry, timeout=timeout, metadata=metadata)

        print(f"Cloud Function {name} deleted successfully.")
    
    def update_function(self, name, runtime=None, entry_point=None, trigger=None, source_archive_url=None,
                        source_archive_bucket=None, source_archive_object=None, trigger_resource=None,
                        service_account_email=None, network=None, max_instances=None, min_instances=None,
                        vpc_connector=None, vpc_connector_egress_settings=None, available_memory_mb=None,
                        timeout=None, kms_key_name=None, environment_variables=None, labels=None,
                        build_environment=None, build_worker_pool=None, build_name=None, description=None,
                        update_on_deploy=None, region=None, project=None,retry=None,
                        metadata=None):
        """
        Updates an existing Cloud Function.

        Args:
            name (str): The name of the Cloud Function to update.
            runtime (str): The runtime of the Cloud Function.
            entry_point (str): The entry point of the Cloud Function.
            trigger (str): The trigger type of the Cloud Function.
            source_archive_url (str): The URL of the source archive for the Cloud Function.
            source_archive_bucket (str): The name of the bucket containing the source archive.
            source_archive_object (str): The name of the source archive object.
            trigger_resource (str): The resource associated with the trigger.
            service_account_email (str): The service account email associated with the Cloud Function.
            network (str): The network configuration for the Cloud Function.
            max_instances (int): The maximum number of instances for the Cloud Function.
            min_instances (int): The minimum number of instances for the Cloud Function.
            vpc_connector (str): The VPC connector for the Cloud Function.
            vpc_connector_egress_settings (str): The egress settings for the VPC connector.
            available_memory_mb (int): The available memory in MB for the Cloud Function.
            timeout (str): The timeout duration for the Cloud Function.
            kms_key_name (str): The KMS key name for the Cloud Function.
            environment_variables (Dict[str, str]): The environment variables for the Cloud Function.
            labels (Dict[str, str]): The labels for the Cloud Function.
            build_environment (str): The build environment for the Cloud Function.
            build_worker_pool (str): The build worker pool for the Cloud Function.
            build_name (str): The build name for the Cloud Function.
            description (str): The description for the Cloud Function.
            update_on_deploy (bool): Whether to update on deploy for the Cloud Function.
            region (str): The region where the Cloud Function is deployed.
            project (str): The ID of the GCP project.
            client: A client object used to make requests to the Cloud Functions API.
            retries (Optional[int]): The number of retries for the request.
            timeout (Optional[float]): The timeout duration for the request in seconds.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata headers for the request.

        Returns:
            google.cloud.functions_v1.CloudFunction: The updated Cloud Function.

        Raises:
            google.api_core.exceptions.NotFound: If the Cloud Function is not found.
            google.api_core.exceptions.GoogleAPICallError: If the API request fails.
        """
        if project is None:
            project = self.project_id

        function_name = f"projects/{project}/locations/{region}/functions/{name}"
        request = functions_v1.UpdateFunctionRequest(
            name=function_name,
            function=functions_v1.CloudFunction(
                runtime=runtime,
                entry_point=entry_point,
                trigger=trigger,
                source_archive_url=source_archive_url,
                source_archive_bucket=source_archive_bucket,
                source_archive_object=source_archive_object,
                trigger_resource=trigger_resource,
                service_account_email=service_account_email,
                network=network,
                max_instances=max_instances,
                min_instances=min_instances,
                vpc_connector=vpc_connector,
                vpc_connector_egress_settings=vpc_connector_egress_settings,
                available_memory_mb=available_memory_mb,
                timeout=timeout,
                kms_key_name=kms_key_name,
                environment_variables=environment_variables,
                labels=labels,
                build_environment=build_environment,
                build_worker_pool=build_worker_pool,
                build_name=build_name,
                description=description,
                update_on_deploy=update_on_deploy
            )
        )

        return self.client.update_function(request=request, retry=retry, timeout=timeout, metadata=metadata)

    def call_function(self, name, data=None, region=None, project=None, retry=None, timeout=None,
                      metadata=None):
        """
        Calls a Cloud Function.

        Args:
            name (str): The name of the Cloud Function.
            data (str): The data to be passed to the Cloud Function.
            region (str): The region where the Cloud Function is deployed.
            project (str): The ID of the GCP project.
            client: A client object used to make requests to the Cloud Functions API.
            retries (Optional[int]): The number of retries for the request.
            timeout (Optional[float]): The timeout duration for the request in seconds.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata headers for the request.

        Returns:
            google.cloud.functions_v1.CallFunctionResponse: The response from the Cloud Function.

        Raises:
            google.api_core.exceptions.NotFound: If the Cloud Function is not found.
            google.api_core.exceptions.GoogleAPICallError: If the API request fails.
        """
        if project is None:
            project = self.project_id

        function_name = f"projects/{project}/locations/{region}/functions/{name}"
        request = functions_v1.CallFunctionRequest(
            name=function_name,
            data=data
        )

        return self.client.call_function(request=request, retry=retry, timeout=timeout, metadata=metadata)