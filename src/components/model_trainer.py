import os
import sys
from dataclasses import dataclass

# Choices here are arbitrary for the purposes of this tutorial
from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging # Custom logging format
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_filepath = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, train_array, test_array):
        try:
            logging.info("Initiating model training")
            # TODO: Don't hardcode the format like this
            x_train, y_train, x_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )


            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Nearest Neighbors": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "CatboostingClassifier": CatBoostRegressor(),
                "Adaboost Classifier": AdaBoostRegressor()
            }
            # TODO: Add a hyperparameters config that can be passed to utils.evaluate_models here
        
            model_report:dict = evaluate_models(
                x_train = x_train,
                y_train = y_train,
                x_test = x_test,
                y_test = y_test,
                models = models
            )
            best_r2_score = max(sorted(model_report.values()))
            best_r2_score_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_r2_score)
            ]
            best_r2_score_model = models[best_r2_score_model_name]


            if best_r2_score < 0.6:
                raise CustomException("No model performed greater than 60%")
            logging.info("Models evaluated")


            # Does this save the model's name, or the weights?
            save_object(
                file_path=self.model_trainer_config.trained_model_filepath,
                obj=best_r2_score_model
            )

            # TODO: No need to reevaluate scores? Not sure how much that matters
            predicted = best_r2_score_model.predict(x_test)
            logging.info("Best model discovered: " + str(best_r2_score_model_name))
            r2 = r2_score(y_test, predicted)

            return r2

        except Exception as e:
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    from src.components.data_ingestion import DataIngestion, DataIngestionConfig
    # TODO This import is technically a chained import, and might cause weird race conditions
    from src.components.data_transformation import DataTransformationConfig, DataTransformation

    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    trans = DataTransformation()
    train_arr, test_arr, _ = trans.initiate_data_transformation(train_data, test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_training(train_arr, test_arr, ))

