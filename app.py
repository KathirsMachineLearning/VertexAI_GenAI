import yaml
from gcp.gcs import GCSHandler
from gcp.big_query import BigQueryHandler
from google.cloud.bigquery import SchemaField


class App:

    def __init__(self, app_config_path='./config.yaml'):
        with open(app_config_path) as f:
            self.config = yaml.safe_load(f)

    def run(self):
        print("Entry Point")
       

if __name__ == "__main__":
    app = App()
    app.run()
