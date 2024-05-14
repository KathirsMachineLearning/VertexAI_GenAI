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

    def run(self):  

        # Initialize data preprocessor
        data_preprocessor = DataPreprocessor()
        # Preprocess data
        preprocessed_data = data_preprocessor.preprocess_data(self.config['model']['preprocessing']['data_path'])
        texts = preprocessed_data['Text'].tolist()

        

        prompt_engineering_text = PromptEngineer()
        prompt = prompt_engineering_text.prompt_engineering()
        print(prompt)
        
        # Initialize an empty list to store sentiments
        sentiments = []

        vertex_ai_handler = VertexAIHandler(self.config['gcp']['project_id'], self.config['gcp']['region_name'], self.config['gcp']['credentials_path'])
        # Predict sentiment for each text.     
        sentiments = vertex_ai_handler.predict_text_generation_models(self.config['model']['model_name'], prompt, texts)

        # Add the sentiments as a new column to the preprocessed data
        preprocessed_data['Sentiment'] = sentiments

        # Initialize post processor
        post_processor = PostProcessor()

        # Save predictions to CSV
        post_processor.save_predictions_to_csv(preprocessed_data, self.config['model']['postprocessing']['output_path'])


if __name__ == "__main__":
    app = App()
    app.run()
