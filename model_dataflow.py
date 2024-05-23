from __future__ import annotations

import logging
import platform
import os
from app import App  # Ensure this module exists and is accessible
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


# Define a custom DoFn to list files and folders
class ListFilesAndFoldersDoFn(beam.DoFn):
    def process(self, element):
        current_directory = os.getcwd()
        items = os.listdir(current_directory)
        logging.info(f"Current directory: {current_directory}")
        for item in items:
            logging.info(f"Item: {item}")
        yield element


# Define a custom DoFn to perform predictions
class PredictionsDoFn(beam.DoFn):
    def __init__(self, app_instance):
        self.app_instance = app_instance

    def process(self, element):
        # Assuming app_instance has a method called run_predictions that processes data
        logging.info("Starting predictions...")
        self.app_instance.run_predictions()
        logging.info("Predictions completed.")
        yield element


def run(beam_args: list[str] | None = None) -> None:
    app_instance = App()  # Make sure the App class and its methods are correctly defined in the app module
    beam_options = PipelineOptions(beam_args, save_main_session=True)
    pipeline = beam.Pipeline(options=beam_options)
    (
        pipeline
        | "Create data" >> beam.Create(["Data Flow!", platform.platform()])
        | "Print" >> beam.Map(logging.info)
        | "List files and folders" >> beam.ParDo(ListFilesAndFoldersDoFn())
        | "Make predictions" >> beam.ParDo(PredictionsDoFn(app_instance))
    )
    pipeline.run()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
