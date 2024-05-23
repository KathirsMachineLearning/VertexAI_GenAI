FROM ubuntu:focal

WORKDIR /pipeline

# Set the entrypoint to Apache Beam SDK worker launcher.
COPY --from=apache/beam_python3.8_sdk:2.56.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]

# Install Python with pip, dev tools, distutils, and a C++ compiler.
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl g++ python3-dev python3-distutils \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    # Install the requirements.
    && pip install --no-cache-dir -r requirements.txt \
    && pip check

# Copy the pipeline source files.
COPY . .
