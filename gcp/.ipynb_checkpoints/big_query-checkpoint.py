from google.cloud import bigquery
import pandas as pd

class BigQueryHandler:
    
    def __init__(self, project_id, credentials_path=None):
        """
        Initialize the BigQuery handler with the GCP project ID and credentials.

        :param project_id: The ID of your GCP project.
        :param credentials_path: Path to the service account key file.
        """
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.client = self._create_client()

    def _create_client(self):
        """
        Create a BigQuery client for connecting to BigQuery.

        :return: A client object for accessing BigQuery.
        """
        if self.credentials_path:
            return bigquery.Client.from_service_account_json(
                self.credentials_path,
                project=self.project_id
            )
        else:
            return bigquery.Client(project=self.project_id)

    def create_table(self, dataset_id, table_id, schema):
        """
        Create a new table in the specified dataset with the given schema.

        :param dataset_id: ID of the dataset.
        :param table_id: ID of the table to be created.
        :param schema: Schema of the table.
        """
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        self.client.create_table(table)

    def delete_table(self, dataset_id, table_id):
        """
        Delete a table from the specified dataset.

        :param dataset_id: ID of the dataset.
        :param table_id: ID of the table to be deleted.
        """
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        self.client.delete_table(table_ref)

    def read_table(self, dataset_id, table_id):
        """
        Read data from a BigQuery table and return as pandas DataFrame.

        :param dataset_id: ID of the dataset.
        :param table_id: ID of the table to read.
        :return: DataFrame containing the table data.
        """
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = self.client.get_table(table_ref)
        return self.client.list_rows(table).to_dataframe()

    def add_columns_to_table(self, dataset_id, table_id, columns):
        """
        Add columns to an existing BigQuery table.

        :param dataset_id: ID of the dataset.
        :param table_id: ID of the table to add columns to.
        :param columns: List of column definitions to add.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        new_schema = table.schema + columns
        table.schema = new_schema
        self.client.update_table(table, ["schema"])

    def delete_columns_from_table(self, dataset_id, table_id, column_names):
        """
        Delete columns from an existing BigQuery table.

        :param dataset_id: ID of the dataset.
        :param table_id: ID of the table to delete columns from.
        :param column_names: List of column names to delete.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        new_schema = [field for field in table.schema if field.name not in column_names]
        table.schema = new_schema
        self.client.update_table(table, ["schema"])

    def execute_any_query(self, query):
        """
        Execute any SQL query on BigQuery.

        :param query: SQL query to execute.
        :return: Result of the query execution.
        """
        return self.client.query(query).result()
       
    def create_dataset(self, dataset_id, region='us-central1'):
        """
        Create a new dataset in BigQuery.

        :param dataset_id: ID of the dataset to be created.
        :param region: Optional. Region where the dataset will be created (default: 'us-central1').
        """
        dataset_ref = self.client.dataset(dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = region

        # Check if the dataset already exists
        if self.client.get_dataset(dataset_ref):
            print(f"Dataset '{dataset_id}' already exists.")
            return

        # Create the dataset
        self.client.create_dataset(dataset)
        print(f"Dataset '{dataset_id}' created successfully in region '{region}'.")

    def list_datasets(self):
        """
        Get a list of all datasets in BigQuery.

        :return: A list of dataset IDs.
        """
        datasets = self.client.list_datasets()
        return [dataset.dataset_id for dataset in datasets]

    def list_tables(self, dataset_id):
        """
        Get a list of all tables in a dataset.

        :param dataset_id: ID of the dataset.
        :return: A list of table IDs.
        """
        dataset_ref = self.client.dataset(dataset_id)
        tables = self.client.list_tables(dataset_ref)
        return [table.table_id for table in tables]

    def get_dataset_details(self, dataset_id):
        """
        Get the dataset details based on the dataset name.

        :param dataset_id: ID of the dataset.
        :return: ID of the dataset.
        """
        datasets = self.client.list_datasets()
        for dataset in datasets:
            if dataset.dataset_id == dataset_id:
                return dataset_id
        return None

    def get_table_details(self, dataset_id, table_id):
        """
        Get the table details based on the table name and dataset ID.

        :param dataset_id: ID of the dataset.
        :param table_name: Name of the table.
        :return: ID of the table.
        """
        dataset_ref = self.client.dataset(dataset_id)
        tables = self.client.list_tables(dataset_ref)
        for table in tables:
            if table.table_id == table_id:
                return table_id
        return None

    def delete_dataset(self, dataset_id, delete_contents=False):
        """
        Delete a dataset from BigQuery.

        :param dataset_id: ID of the dataset to be deleted.
        :param delete_contents: Optional. If True, delete all tables in the dataset as well (default: False).
        """
        dataset_ref = self.client.dataset(dataset_id)

        # Check if the dataset exists
        dataset = self.client.get_dataset(dataset_ref)
        if dataset is None:
            print(f"Dataset '{dataset_id}' does not exist.")
            return

        # Delete the dataset
        self.client.delete_dataset(dataset_ref, delete_contents=delete_contents, not_found_ok=True)
        print(f"Dataset '{dataset_id}' deleted successfully.")

    def get_table_schema(self, dataset_id, table_id):
        """
        Get the schema details of a table in BigQuery.

        :param dataset_id: ID of the dataset containing the table.
        :param table_id: ID of the table.
        :return: Schema details of the table.
        """
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = self.client.get_table(table_ref)
        return table.schema

    def insert_rows_to_table(self, dataset_id, table_id, rows):
        """
        Insert rows into a BigQuery table.

        :param dataset_id: ID of the dataset.
        :param table_id: ID of the table.
        :param rows: List of rows to insert into the table. Each row should be a dictionary
                     where keys are column names and values are corresponding values.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)

        errors = self.client.insert_rows(table, rows)
        if errors:
            print(f"Errors occurred while inserting rows into table '{table_id}':")
            for error in errors:
                print(error)
        else:
            print(f"Rows inserted successfully into table '{table_id}'.")
