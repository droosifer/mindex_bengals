#%%
import boto3
from dotenv import load_dotenv
import os
from pandas import DataFrame
import pandas as pd
import io

#%%

# load .env file to auth to AWS
load_dotenv()

#%%

def get_session():
    """Get boto3 s3 session

    Returns:
        s3.client: an s3 AWS session
    """    

    # check .env is sourced
    if "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
        pass

    s3 = boto3.client('s3')

    return s3


#%%
def read_s3_to_pandas_df(file_name: str) -> DataFrame:
    """Read an s3 csv into a pandas dataframe

    Args:
        file_name (str): filename in bucket

    Returns:
        DataFrame: Pandas Dataframe
    """    

    s3 = get_session()

    obj = s3.get_object(Bucket=os.getenv('S3_BUCKET_NAME'), Key=file_name)

    dataframe = pd.read_csv(io.BytesIO(obj['Body'].read()))

    return dataframe


#%%
def remove_bad_weeks(dataframe: DataFrame) -> DataFrame:
    """remove week 10 and 18 from dataframes

    Args:
        dataframe (DataFrame): dataframe with column "Week"

    Returns:
        DataFrame: pandas DataFrame
    """    

    assert "Week" in dataframe.columns, "Week col not in dataframe"

    dataframe = dataframe[~dataframe.Week.isin(['REG18', 'REG10'])]

    return dataframe

#%%
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
    player_name = file_name.split('_')[0].title()

    receiver_df['player_name'] = player_name

    # clean individual recievers data

    # remove fake game
    receiver_df = remove_bad_weeks(receiver_df)

    return receiver_df

#%%
def get_reciever_data() -> DataFrame:
    """Get all recievers unioned as a single DataFrame

    Returns:
        DataFrame: A DataFrame of all recievers
    """    

    reciever_list = [
        'boyd_receiving.csv',
        'chase_receiving.csv',
        'higgins_receiving.csv'
    ]

    pandas_df_list = [process_reciever(reciever) for reciever in reciever_list]
    
    all_recievers = pd.concat(pandas_df_list)

    all_recievers = all_recievers.pivot(index='Week', columns='player_name', values=['Yards', 'TD'])

    # make columns pretty
    all_recievers.columns = [' '.join(col).strip() for col in all_recievers.columns.values]

    # fill 0 for games players havent played
    all_recievers = all_recievers.fillna(value=0, axis=1)

    return all_recievers


#%%

def clean_team_data(dataframe: DataFrame) -> DataFrame:
    
    dataframe = remove_bad_weeks(dataframe)

    return dataframe

# %%
def get_team_data() -> DataFrame:

    bengals_team_data = read_s3_to_pandas_df('bengals.csv')

    # remove week 18 and/or bye week
    bengals_team_data = remove_bad_weeks(bengals_team_data)

    bengals_team_data["Result"] = (
        bengals_team_data["Result"]
        .case_when(
            [
                (bengals_team_data["Result"] == 1.0, 'Win'),
                (bengals_team_data["Result"] == 0.0, 'Loss')
            ]
        )
    )

    return bengals_team_data
# %%
