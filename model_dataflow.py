from __future__ import annotations

import logging
import platform

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


def run(beam_args: list[str] | None = None) -> None:
    beam_options = PipelineOptions(beam_args, save_main_session=True)
    pipeline = beam.Pipeline(options=beam_options)
    (
        pipeline
        | "Create data" >> beam.Create(["Hello", "World!", platform.platform()])
        | "Print" >> beam.Map(logging.info)
    )
    pipeline.run()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()