import logging
import os
from datetime import datetime

# Creates filename using current time in easily-ordered format
LOGFILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
# Creates dir for storing logs in this location
logging_dir=os.path.join(os.getcwd(),"logs",LOGFILE)
# Allow creating files even if directory already exists
os.makedirs(logging_dir, exist_ok=True)

LOGFILEPATH = os.path.join(logging_dir,LOGFILE)

logging.basicConfig(
    filename = LOGFILEPATH,
    # using Python's time format variables: 
    # https://docs.python.org/3/library/time.html#time.strftime
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # sets the type of logs that these configs will be applied to
    level = logging.INFO,
)

# Sanity check
if __name__=="__main__":
    # Should create a logfile
    logging.info("Logging has started")
