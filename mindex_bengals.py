import boto3
import os
from pandas import DataFrame
import pandas as pd
import io
from sqlalchemy import create_engine


def get_session():
    """Get boto3 s3 session

    Returns:
        s3.client: an s3 AWS session
    """

    # check .env is sourced
    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        pass

    s3 = boto3.client("s3")

    return s3


def read_s3_to_pandas_df(file_name: str) -> DataFrame:
    """Read an s3 csv into a pandas dataframe without downloading

    Args:
        file_name (str): filename in bucket

    Returns:
        DataFrame: Pandas Dataframe
    """

    s3 = get_session()

    obj = s3.get_object(Bucket=os.getenv("S3_BUCKET_NAME"), Key=file_name)

    dataframe = pd.read_csv(io.BytesIO(obj["Body"].read()))

    return dataframe


def remove_bad_weeks(dataframe: DataFrame) -> DataFrame:
    """remove week 10 and 18 from dataframes

    Args:
        dataframe (DataFrame): dataframe with column "Week"

    Returns:
        DataFrame: pandas DataFrame
    """

    assert "Week" in dataframe.columns, "Week col not in dataframe"

    dataframe = dataframe[~dataframe.Week.isin(["REG10"])]

    return dataframe


def process_reciever(file_name) -> DataFrame:
    """Pandas datframe

    Args:
        dataframe (DataFrame): dataframe of reciever data

    Returns:
        DataFrame: cleaned datafrane if reciver data
    """

    # Get data
    receiver_df = read_s3_to_pandas_df(file_name=file_name)

    # get reciever name
    player_name = file_name.split("_")[0].title()

    receiver_df["player_name"] = player_name

    # clean individual recievers data

    # remove by week
    receiver_df = remove_bad_weeks(receiver_df)

    return receiver_df


def get_reciever_data() -> DataFrame:
    """Get all recievers unioned as a single DataFrame

    Returns:
        DataFrame: A DataFrame of all recievers
    """

    reciever_list = [
        "boyd_receiving.csv",
        "chase_receiving.csv",
        "higgins_receiving.csv",
    ]

    pandas_df_list = [process_reciever(reciever) for reciever in reciever_list]

    all_recievers = pd.concat(pandas_df_list)

    all_recievers = all_recievers.pivot(
        index="Week", columns="player_name", values=["Yards", "TD"]
    )

    # make columns pretty
    all_recievers.columns = [
        " ".join(col).strip() for col in all_recievers.columns.values
    ]

    # fill 0 for games players havent played
    all_recievers = all_recievers.fillna(value=0, axis=1)

    return all_recievers


def clean_team_data(dataframe: DataFrame) -> DataFrame:
    """apply cleaning transformations to team data

    Args:
        dataframe (DataFrame): pandas dataframe

    Returns:
        DataFrame: pandas DataFrame
    """

    dataframe = remove_bad_weeks(dataframe)

    return dataframe


def get_team_data() -> DataFrame:
    """Get Bengals team data

    Returns:
        DataFrame: pandas DataFrame
    """

    bengals_team_data = read_s3_to_pandas_df("bengals.csv")

    # remove bye week
    bengals_team_data = remove_bad_weeks(bengals_team_data)

    # tansform wins/losses
    bengals_team_data["Result"] = bengals_team_data["Result"].case_when(
        [
            (bengals_team_data["Result"] == 1.0, "Win"),
            (bengals_team_data["Result"] == 0.0, "Loss"),
        ]
    )

    return bengals_team_data


def get_bengals_data() -> DataFrame:
    team_data = get_team_data()

    reciever_data = get_reciever_data()

    all_data = team_data.join(other=reciever_data, on="Week", how="left")

    all_data = all_data.fillna(value=0, axis=0)

    return all_data


def load_data_to_database(dataframe: DataFrame, table_name: str):
    """Load pandas df to mindex postgres db

    Args:
        dataframe (DataFrame): pandas DataFrame
        table_name (str): name of table to write to
    """

    engine = create_engine(os.getenv("DB_CONNECTION_STRING"))

    dataframe.to_sql(name=table_name, con=engine, index=False, if_exists="replace")


def view_bengals_data_in_db(table_name: str) -> DataFrame:
    """name of table to view

    Args:
        table_name (str): table name to preview
    """

    engine = create_engine(os.getenv("DB_CONNECTION_STRING"))

    dataframe = pd.read_sql_table("drew_ringo", con=engine)

    return dataframe


def run_test_query() -> DataFrame:
    engine = create_engine(os.getenv("DB_CONNECTION_STRING"))

    with open("./sql/dbeaver_query.sql", "r") as query:
        dataframe = pd.read_sql_query(sql=query.read(), con=engine)

    return dataframe
