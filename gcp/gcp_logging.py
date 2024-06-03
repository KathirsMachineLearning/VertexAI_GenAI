import os
import logging
from google.cloud import logging as gcp_logging
from google.cloud.logging.handlers import CloudLoggingHandler

class GCPLoggingHandler:
    def __init__(self, project_id, credentials_path=None, logger_name='default_logger', level=logging.DEBUG):
        """
        Initialize the GCP logging handler with the GCP project ID and credentials.

        :param project_id: The ID of your GCP project.
        :param credentials_path: Path to the service account key file (optional).
        :param logger_name: Name of the logger.
        :param level: Logging level.
        """
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.logger_name = logger_name
        self.level = level

        self.logger = self._create_logger()

    def _create_logger(self):
        """
        Create a logger for Google Cloud Logging.

        :return: A logger object configured for Google Cloud Logging.
        """
        if self.credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

        # Create a Google Cloud Logging client
        client = gcp_logging.Client(project=self.project_id)

        # Create a handler using the client
        handler = CloudLoggingHandler(client)

        # Get the logger
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.level)
        
        # Check if the handler is already added to prevent duplicate handlers
        if not any(isinstance(h, CloudLoggingHandler) for h in logger.handlers):
            logger.addHandler(handler)
        
        return logger

    def log_info(self, message):
        """
        Log an info level message.

        :param message: The message to log.
        """
        self.logger.info(message)
        print(message)

    def log_debug(self, message):
        """
        Log a debug level message.

        :param message: The message to log.
        """
        self.logger.debug(message)
        print(message)

    def log_warning(self, message):
        """
        Log a warning level message.

        :param message: The message to log.
        """
        self.logger.warning(message)
        print(message)

    def log_error(self, message):
        """
        Log an error level message.

        :param message: The message to log.
        """
        self.logger.error(message)
        print(message)

    def get_logger(self):
        """
        Get the logger instance.

        :return: The logger instance.
        """
        return self.logger
