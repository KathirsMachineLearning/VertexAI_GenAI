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
        big_query_handler = BigQueryHandler(project_id=self.config['gcp']['project_id'], credentials_path='./credentials.json')
        # tables = big_query_handler.list_tables("fraud")
        # schema = big_query_handler.get_table_schema("fraud", "fraud")
        # print(schema)
        #new_column = SchemaField('V123', 'FLOAT', 'NULLABLE')
        # big_query_handler.add_columns_to_table("fraud", "fraud", [new_column])
        #big_query_handler.create_dataset("testbigquerydatasetcreation")
        #big_query_handler.delete_dataset("testbigquerydatasetcreation")
        #big_query_handler.create_table("fraud","test_fraud", [new_column])
        # rows = [
        #             {"V123": "1.0"},
        #             {"V123": "2.0"},
        #             # Add more rows as needed
        #         ]
        #big_query_handler.insert_rows_to_table("fraud", "test_fraud", rows)
        #df = big_query_handler.read_table("fraud", "test_fraud")
        #print(df)

        # import pandas as pd

        # # Read CSV file into a Pandas DataFrame
        # df = pd.read_csv('./Life_Expectancy_Data_short.csv')        
        # # Specify dataset and table references
        # dataset_ref = big_query_handler.client.dataset('fraud')
        # table_ref = dataset_ref.table('test_fraud')

        # # Write DataFrame to BigQuery table
        # big_query_handler.write_dataframe_to_table(dataframe=df, dataset_id=dataset_ref.dataset_id, table_id=table_ref.table_id, if_exists='replace')


if __name__ == "__main__":
    app = App()
    app.run()
