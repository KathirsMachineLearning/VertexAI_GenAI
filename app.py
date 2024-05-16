import argparse
import yaml

from gcp.vertex_ai import VertexAIHandler
from gcp.gcs import GCSHandler
from gcp.big_query import BigQueryHandler
from google.cloud.bigquery import SchemaField

from model.data_preprocessing.data_preprocessing import DataPreprocessor
from model.prompt_engineering.prompt_engineering import PromptEngineer
from model.data_post_processing.data_postprocessing import PostProcessor


class App:

    def __init__(self, app_config_path='./config.yaml'):
        with open(app_config_path) as f:
            self.config = yaml.safe_load(f)

    def run_predictions(self):  

        print("Prediction Process has started successfully.")

        gcs_handler = GCSHandler(self.config['gcp']['project_id'])
        gcs_handler.download_file(self.config['model']['input_bucket']['bucket_name'], self.config['model']['input_bucket']['bucket_input_path'], self.config['model']['preprocessing']['data_path'])

        # Initialize data preprocessor
        data_preprocessor = DataPreprocessor()
        # Preprocess data
        preprocessed_data = data_preprocessor.preprocess_data(self.config['model']['preprocessing']['data_path'])
        texts = preprocessed_data['Text'].tolist()

        prompt_engineering_text = PromptEngineer()
        prompt = prompt_engineering_text.prompt_engineering()
        print(f"prompt text: {prompt}")

        # Initialize an empty list to store sentiments
        sentiments = []

        vertex_ai_handler = VertexAIHandler(self.config['gcp']['project_id'], self.config['gcp']['region_name'])
        # Predict sentiment for each text.     
        sentiments = vertex_ai_handler.predict_text_generation_models(self.config['model']['model_name'], prompt, texts)

        # Add the sentiments as a new column to the preprocessed data
        preprocessed_data['Sentiment'] = sentiments

        # Initialize post processor
        post_processor = PostProcessor()

        # Save predictions to CSV
        post_processor.save_predictions_to_csv(preprocessed_data, self.config['model']['postprocessing']['output_path'])
        
        
        gcs_handler.upload_file(self.config['model']['postprocessing']['output_path'], self.config['model']['output_bucket']['bucket_name'],self.config['model']['output_bucket']['bucket_output_path'])
        
        print("Prediction Process has ended successfully.")

    def run_data_engineering(self):
        print("Data Engineering Process has started successfully.")
        
    def run(self, task):
        if task == 'predictions':
            self.run_predictions()
        # Add more elif conditions for other tasks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use Case Pipeline")
    parser.add_argument("--task", type=str, choices=["predictions"], default="predictions", help="Specify the task to execute")
    args = parser.parse_args()

    app = App()
    app.run(args.task)
