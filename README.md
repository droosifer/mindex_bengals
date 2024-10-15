# Overview

Create an ETL pipeline for processing 2021 Bengals data for Mindex

## Project Structure

Project is built as python package which is importable into a command line runnable script `main.py`
or a jupyter notebook `bengals_notebook.ipynb`.

The codebase is housed in module `mindex_bengals.py`

The `main.py` has logging included to inform the user which steps the pipeline are on.

## Running Locally

```bash
git clone https://github.com/droosifer/mindex_bengals.git
```

```bash
cd mindex_bengals
```

```bash
virtualenv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

To run locally make sure the env vars are in a `.env` file in the root of the repo.

```.env
AWS_ACCESS_KEY_ID=<your_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_access_key>
S3_BUCKET_NAME=<s3_bucket_name>
DB_CONNECTION_STRING=postgresql://{user}:{pass}@{host}:5432/postgres
```

Once the above is completed you can either step through the [notebook](bengals_notebook.ipynb) or run....

```bash
python main.py
```

More auth info can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)

## Running Tests

```bash
pytest 
```

## SQL

The SQL file is located at `sql/dbeaver_query.sql`

The screenshot of installed dbeaver and the query running is at `docs/dbeaver_installation_and_query.png`

Furthermore there is a function in mindex_bengals module called `run_test_query` which will read the sql file and run it against the databse and produce the aggregate results outlined in the intial request. The notebook also runs this as a final step.

## Data Notes

- bye week was week 10
- higgins missed games 3 and 4
- there is a record for the bye week in bengals.csv
- Chase, Higgins, and Boyd dont have preseason stats but the bengals.csv file does

## Other Notes

The code base does not download the files to disk. It reads them into a byte string into memory in order to mimic what I would do in a 'production' pipeline. For EDA (Exploratory Data Analysis) I started out by downloading them the traditional way using the boto3 s3 client and then exploring them manually or using pandas to understand how to clean and manipulate.

## Hardships 

I am running Fedora 40 on my laptop and was runnign into issues using `psycopg` for python so had to use SQL alchemy which I had never used before. Seems to integrate well with pandas.

I come from an Azure shop so it was the first time using the boto3 client. Way more intuitive and easier to use than the Azure alternative.

Tried connecting vscode extension SQL tools to preview the postgres db. I couldn't figure out the connection string and reluctantly went to dbeaver (thankfully they had an RPM distribution for my Fedora PC). I ended up liking dbeaver more than I thought I would.

## TODO/Future

- set up auto linting and formatting on commit using prehooks
- branch protection policies 