#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("Loading artifact to dataframe")
    df = pd.read_csv(artifact_local_path) 
    logger.info("Cleaning the data")
    df['last_review'] = pd.to_datetime(df['last_review'])
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    


    filename = "clean_data.csv"
    df.to_csv(filename, index=False)
    
    logger.info("Creating artifact")
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)

    logger.info("Logging artifact")
    run.log_artifact(artifact)
    
    os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help="Name of the input artifact", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help="Name of the output artifact", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help="Type of the output artifact", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str, ## INSERT TYPE HERE: str, float or int,
        help="Description of the output artifact", ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,## INSERT TYPE HERE: str, float or int,
        help="Min Price",## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max Price", # INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
