from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'

load_dotenv(env_path)

user = os.getenv("POSTGRES_DATA_USER")
password = os.getenv("POSTGRES_DATA_PASSWORD")
database = os.getenv("POSTGRES_DATA_DATABASE")
# host = 'postgresql-data'
host = 'postgresql-data'
port = 5432


def get_engine():
    logging.info("Conectando no banco de dados")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str,df:pd.DataFrame):
    df.to_sql(
        con=engine,
        name=table_name,
        if_exists='append',
        index=False
    )

    logging.info("Ddados carregados com sucesso")

    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

    logging.info(f"Total de registros na tabela: {len(df_check)}")