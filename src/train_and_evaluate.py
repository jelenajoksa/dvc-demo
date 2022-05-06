# load train and test files
# train algotithm
# save the metrics and params


# load the train and test
# train algo
# save the metrices, params
import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import read_params
import argparse
import joblib
import json


# function that will calculate metrics of our algorithm
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config["split_data"]["test_path"]
    train_data_path = config["split_data"]["train_path"]
    random_state = config["base"]["random_state"]
    # directory we are going to save our model in:
    model_dir = config["model_dir"]

    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]
    # we are doing this target in this way so every time csv file (data is changed),dvc repro will pick it up
    target = [config["base"]["target_col"]]

    # we need train data path:
    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]
    # same as y just without tha last column
    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    lr = ElasticNet(
        alpha=alpha,
        l1_ratio=l1_ratio,
        random_state=random_state)
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    ######################################################################
    # last is to add scores and params after we added report folder, params and scores json files inside and updated scores in dvc.yaml

    scores_file = config['reports']['scores']
    params_file = config['reports']['params']

    with open(scores_file, 'w') as f:
        # we create dictionary to store our scores/metrics
        scores = {
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }
        # we are now dumping this dictionary into scores file
        # indent = 4 means that the output will be organized properly, read the big comment below
        json.dump(scores, f, indent=4)

    with open(params_file, 'w') as f:
        # we create dictionary to store our parameters
        params = {
            'alpha': alpha,
            'l1_ratio': l1_ratio
        }

        '''Using the json.dump() method of Python json module, we can write prettyprinted JSON into the file.
        The json.dump() method provides the following parameters to pretty-print JSON data.
        The indent parameter specifies the spaces that are used at the beginning of a line. 
        We can use the indent parameter of json.dump() to specify the indentation value. 
        By default, when you write JSON data into a file, Python doesn’t use indentations and writes all data on a single line, which is not readable. '''
        json.dump(params, f, indent=4)

    ######################################################################

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(lr, model_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
