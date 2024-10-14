# Overview

Create an ETL pipeline for processing 2021 Bengals data for Mindex

## Running Locally

To run locally make sure the env vars are in a `.env` file in the root of the repo.

```.env
AWS_ACCESS_KEY_ID=<your_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_access_key>
S3_BUCKET_NAME=<s3_bucket_name>
```

More auth info can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)

## Data Notes

- bye week was week 10
- higgins missed games 3 and 4
- there is a record for the bye week in bengals.csv
- Chase, Higgins, and Boyd dont have preseason stats but the bengals.csv file does
