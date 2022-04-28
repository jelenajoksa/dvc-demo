## read params
##process
##return the dataframe


#if some of these libraries are not in python by default you have to put it first into requirements file and do pip install
import os
import yaml
import pandas as pd
import argparse

#read file and return the dictionary
def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def get_data(config_path):
    config = read_params(config_path)
    #print(config)
    data_path = config['data_source']['s3_source']
    df = pd.read_csv(data_path, sep = ',', encoding = 'utf-8')
    #print(df.head())
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Stage 1: Get data as a dataframe")

    parser.add_argument("--config", default="params.yaml")

    args = parser.parse_args()
    get_data(args.config)