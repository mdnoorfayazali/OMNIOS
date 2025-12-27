import logging
import sys

def setup_logger(name: str):
    """
    Configures and returns a logger instance.
    Logs to console (stdout).
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
