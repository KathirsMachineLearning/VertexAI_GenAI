# BigQuery Operations

Below are the sample usage of methods available in the `BigQueryHandler` class for interacting with Google BigQuery.

### Initialization

```python
from big_query import BigQueryHandler

# Initialize BigQueryHandler
big_query_handler = BigQueryHandler(project_id='your_project_id', credentials_path='./credentials.json')
```

### Creating a Dataset

```python
# Create a new dataset in BigQuery
big_query_handler.create_dataset("test_bigquery_dataset")
```

### Deleting a Dataset

```python
# Delete a dataset from BigQuery
big_query_handler.delete_dataset("test_bigquery_dataset")
```

### Creating a Table

```python
# Define schema for the table
schema = [
    bigquery.SchemaField('column1', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('column2', 'INTEGER', mode='NULLABLE')
]

# Create a new table in a dataset
big_query_handler.create_table("your_dataset_id", "your_table_id", schema)
```

### Deleting a Table

```python
# Delete a table from a dataset
big_query_handler.delete_table("your_dataset_id", "your_table_id")
```

### Reading Data from a Table

```python
# Read data from a table and return as pandas DataFrame
df = big_query_handler.read_table("your_dataset_id", "your_table_id")
```

### Inserting Rows into a Table

```python
# Insert rows into a table
rows = [
    {"column1": "value1", "column2": 123},
    {"column1": "value2", "column2": 456},
    # Add more rows as needed
]
big_query_handler.insert_rows_to_table("your_dataset_id", "your_table_id", rows)
```

### Adding Columns to a Table

```python
from google.cloud import bigquery

# Define new columns to add
new_columns = [
    bigquery.SchemaField('new_column', 'STRING', mode='NULLABLE'),
    # Add more columns as needed
]

# Add columns to an existing table
big_query_handler.add_columns_to_table("your_dataset_id", "your_table_id", new_columns)
```

### Deleting Columns from a Table

```python
# Specify column names to delete
columns_to_delete = ["column1", "column2"]

# Delete columns from an existing table
big_query_handler.delete_columns_from_table("your_dataset_id", "your_table_id", columns_to_delete)
```

### Executing Any Query

```python
# Execute any SQL query on BigQuery
result = big_query_handler.execute_any_query("SELECT * FROM your_dataset_id.your_table_id")
```

### Getting Dataset and Table Details

```python
# Get a list of all datasets in BigQuery
datasets = big_query_handler.list_datasets()
print("Datasets:", datasets)

# Get a list of all tables in a dataset
tables = big_query_handler.list_tables("your_dataset_id")
print("Tables:", tables)

# Get the dataset details based on the dataset ID
dataset_details = big_query_handler.get_dataset_details("your_dataset_id")
print("Dataset Details:", dataset_details)

# Get the table details based on the dataset ID and table ID
table_details = big_query_handler.get_table_details("your_dataset_id", "your_table_id")
print("Table Details:", table_details)
```

### Getting Table Schema

```python
# Get the schema details of a table in BigQuery
schema = big_query_handler.get_table_schema("your_dataset_id", "your_table_id")
print("Table Schema:", schema)
```

This concludes the sample usage of methods available in the `BigQueryHandler` class for performing various operations in Google BigQuery.
