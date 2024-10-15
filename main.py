import logging
from dotenv import load_dotenv
from mindex_bengals import get_bengals_data, load_data_to_database

logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    
    logging.info('Loading .env')
    load_dotenv()

    logging.info('Getting Bengals Data')
    bengals_data = get_bengals_data()

    logging.info('Loading to Database')
    load_data_to_database(bengals_data, 'drew_ringo')
