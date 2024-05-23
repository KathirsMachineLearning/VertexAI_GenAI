FROM apache/beam_python3.10_sdk:2.56.0 AS beam_python
FROM python:3.10-slim

WORKDIR /pipeline

# Set the entrypoint to Apache Beam SDK worker launcher.
COPY --from=beam_python /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]

# Install the requirements.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip check

COPY . .