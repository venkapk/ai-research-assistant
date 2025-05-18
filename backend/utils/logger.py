import logging
import os

# Fetch environment variables
app_name = os.getenv("APP_NAME", "AI-Research-Tool")
log_level = os.getenv("LOG_LEVEL", "DEBUG")

def get_logger() -> logging.Logger:
    """
    Initializes and returns a configured logger for the application.

    Environment Variables:
        - APP_NAME (str, optional): Name of the application, defaults to 'AI-Research-Tool'.
        - LOG_LEVEL (str, optional): Logging level, defaults to 'DEBUG'.

    Logging Setup:
        - Adds a stream handler for console output.
        - Adds a file handler to write logs to a file named after the app.
        - Ensures handlers are not duplicated if logger is reused.

    Returns:
        logging.Logger: A logger instance configured with handlers and formatters.
    """
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.DEBUG))

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s: %(levelname)s %(name)s - %(message)s')

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler
        file_handler = logging.FileHandler(f'{app_name.lower()}.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
