import logging
from google.cloud import logging as gcp_logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging
import os

class GCPLoggingHandler:
    def __init__(self, credentials_path=None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Create a Google Cloud Logging client
        self.client = gcp_logging.Client()

        # Create a handler using the client
        self.handler = CloudLoggingHandler(self.client)

        # Set up logging with the handler
        setup_logging(self.handler)

    def get_logger(self, logger_name='default_logger', level=logging.DEBUG):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Check if the handler is already added to prevent duplicate handlers
        if not any(isinstance(h, CloudLoggingHandler) for h in logger.handlers):
            logger.addHandler(self.handler)
        
        return logger
