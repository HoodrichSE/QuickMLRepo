import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Class to contain initialization configs for ingestion
# This can be moved to a configs dir or class once we collect more config classes
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', "train.csv")
    test_data_path: str=os.path.join('artifacts', "test.csv")
    raw_data_path: str=os.path.join('artifacts', "uningested_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    # This could be our function to read data from a stream or database.
    # Here, we read from a local file for now, so we can lay out the project sensibly.
    # Returns filepaths to train and test datasets.
    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion method")
        try:
            
            df=pd.read_csv('notebook\data\students.csv')
            logging.info("Read the CSV as dataframe.")

            # Create data directories if they don't exist, then save
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=41)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Data ingestion completed.")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("CSV read failed.")
            raise CustomException(e,sys)

# Testing
if __name__ == "__main__":
    logging.info("Data ingestion test __main__ entered.")
    ingester = DataIngestion()
    ingester.initiate_data_ingestion()
    logging.info("Data ingestion test completed.")