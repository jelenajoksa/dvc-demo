# read data from the datasource and save it to data/raw for the further process

import os
import get_data
from get_data import read_params, get_data
import argparse


def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)
    new_cols = [col.replace(" ", "_") for col in df.columns]
    # new_cols = [col for col in df.columns]
    # print(new_cols) #we can use this to preview the columns, we are doing this new_cols to avoid the problems with spaces in .csv document
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    df.to_csv(raw_data_path, sep=",", index=False, header=new_cols)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 2: Load data and save it to data/raw folder")

    parser.add_argument("--config", default="params.yaml")

    args = parser.parse_args()
    load_and_save(args.config)
