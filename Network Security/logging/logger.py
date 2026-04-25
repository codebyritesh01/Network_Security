# logging module is used to record messages from your program while it runs.
# These messages help in debugging errors, tracking execution flow,
# and monitoring what happens inside the project.

import logging
import os

# Correct import is datetime 
from datetime import datetime  


# Create log file name using current date and time
# Example: 04_26_2026_14_30_55.log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Create path for logs folder
# os.getcwd() gives current working directory
# Example: C:/project/logs
logs_path = os.path.join(os.getcwd(), "logs")


# Create logs folder if it does not exist
# exist_ok=True prevents error if folder already exists
os.makedirs(logs_path, exist_ok=True)


# Full path of log file inside logs folder
# Example: C:/project/logs/04_26_2026_14_30_55.log
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


# Configure logging settings
logging.basicConfig(
    
    # Save logs in this file
    filename=LOG_FILE_PATH,
    
    # Format of each log message
    # asctime  = current date/time
    # lineno   = line number where log was called
    # name     = module name
    # levelname = INFO / ERROR / WARNING
    # message  = actual message
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    
    # Minimum level to save
    # INFO means INFO, WARNING, ERROR, CRITICAL will be saved
    level=logging.INFO
)