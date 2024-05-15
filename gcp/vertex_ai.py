from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel
import concurrent.futures
import vertexai
import os

class VertexAIHandler:

    def __init__(self, project_id, region, credentials_path=None):
        """
        Initialize the Vertex AI handler with the GCP project ID, region, and optional credentials path.

        :param project_id: The ID of your GCP project.
        :param region: The region where the model is deployed.
        :param credentials_path: Path to the service account key file.
        """
        self.project_id = project_id
        self.region = region
        self.credentials_path = credentials_path
        self.client = self._create_client()

    def _create_client(self):
        """
        Create a Vertex AI API client.

        :return: A client object for accessing Vertex AI.
        """
        if self.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            vertexai.init(project=self.project_id, location=self.region)
        else:
            vertexai.init(project=self.project_id, location=self.region)
        return aiplatform.gapic.PredictionServiceClient()
    
    def predict_text_generation_models(self, model_name, prompt, texts, max_output_tokens=300, temperature=0.9, top_k=40):
        """
        Make sentiment prediction requests to the specified model in Vertex AI.

        :param model_name: The name of the model to use for prediction.
        :param text: List of prompts for the model.
        :param max_output_tokens: Maximum number of tokens in the output.
        :param temperature: Sampling temperature for the output.
        :param top_k: Number of top tokens to consider in the output.
        :return: List of responses from the model.
        """
        # Load model
        generation_model = TextGenerationModel.from_pretrained(model_name)

        # Define a function to predict text generation for a single prompt
        def predict_single(text):
            response = generation_model.predict(
                prompt=f"{prompt}: {text}",
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_k=top_k,
            )
            return response.text

        # Use ThreadPoolExecutor for parallel execution
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks for each text
            futures = [executor.submit(predict_single, text) for text in texts]

            # Retrieve results as they become available
            responses = [future.result() for future in concurrent.futures.as_completed(futures)]

        return responses

