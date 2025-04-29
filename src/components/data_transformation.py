import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

# These class choices are rather arbitrary. Adjust according to need.
from sklearn.compose import ColumnTransformer # Pipeline for data manipulation
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging # Use our custom logging format
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

# Processes data
# TODO: Data format is hard coded. Make it abstract
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    # Constructs a pipeline for processing data
    def get_data_transformer_object(self):
        try:
            # TODO: read these column headers programatically
            numerical_columns = ["writing_score", "reading_score"] # Ignoring math_score because it's an output
            categorical_columns = [
                'gender', 
                'race_ethnicity', 
                'parental_level_of_education', 
                'lunch', 
                'test_preparation_course'
                ]
            
            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            logging.info("Numerical columns scaling completed.")

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy = "most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Categorical columns encoding and scaling completed.")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            logging.info("Preprocessor initialized.")

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Train and test data read.")


            # Separate outputs from inputs
            # TODO: Do this programatically
            numerical_columns = ["writing_score", "reading_score"] 
            target_column_name = "math_score" 

            train_inputs_df = train_df.drop(columns=[target_column_name], axis=1)
            train_target_df = train_df[target_column_name]

            test_inputs_df = test_df.drop(columns=[target_column_name], axis=1)
            test_target_df = test_df[target_column_name]
            

            logging.info("Preprocessing train and test dataframes.")
            
            preprocessing_obj = self.get_data_transformer_object() # ColumnTransformer

            # TODO: verify with_mean = False is appropriate
            input_feature_train_arr = preprocessing_obj.fit_transform(train_inputs_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(test_inputs_df)

            logging.info("Preprocessing complete.")


            # Return values in a c structure [preprocessed inputs, storage vector for outputs]
            train_arr = np.c_[
                # TODO: What are the shapes here?
                input_feature_train_arr, 
                np.array(train_target_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr,
                np.array(test_target_df)
            ]

            # Serialize to disk
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    from src.components.data_ingestion import DataIngestion, DataIngestionConfig

    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)