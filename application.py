# Copied from app.py, except without debug mode enabled
# TODO: Find another way to deploy to AWS

from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from src.pipeline.prediction_pipeline import CustomData, PredictionPipeline
from src.logger import logging


application = Flask(__name__) # Application entry point; must match EB's python.config

app = application

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Prediction call
@app.route('/predictdata', methods = ['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        # TODO: capture, validate, feature scaling
        data = CustomData(
            gender = request.form.get("gender"),
            race_ethnicity = request.form.get("race_ethnicity"),
            parental_level_of_education = request.form.get("parental_level_of_education"),
            lunch = request.form.get("lunch"),
            test_preparation_course = request.form.get("test_preparation_course"),
            reading_score = request.form.get("reading_score"),
            writing_score  = request.form.get("writing_score"),
            #math_score = request.form.get("math_score"),
        )
        
        pred_df = data.get_data_as_data_frame()
        logging.info("Data frame gathered.")
        logging.info(pred_df)

        prediction_pipeline = PredictionPipeline()
        results = prediction_pipeline.predict(pred_df)
        return render_template('home.html', results=results[0])
    else:
        # TODO: warning
        pass


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = False)