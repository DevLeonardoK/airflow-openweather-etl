from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys,os
from dotenv import load_dotenv

sys.path.insert(0, '/opt/airflow/src') #Tornar pasta visivel ao airflow, além da 'dags'

from extract_data import extract_weather_data
from load_data import load_weather_data
from transform_data import data_transformations

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'

load_dotenv(env_path)

API_KEY = os.getenv("API_KEY_OPENWEATHERMAP")
url = f'https://api.openweathermap.org/data/2.5/weather?q=Novo Hamburgo&units=metric&appid={API_KEY}'

@dag(
    dag_id='weather_data_dag',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False, #Tarefa depende de outras no passado para rodar
        'retries': 2, #Tentativas caso erro
        'retry_delay': timedelta(minutes=5) #Tempo entre cada tentativa
    },
    description='Pipeline clima Novo Hamburgo',
    schedule='0 */1 * * *', #minuto, hora, dia do mes, mes, dia da semana,
    start_date=datetime(2026, 7, 31),
    catchup=False, #Rodar execuções paradas
    tags = ['weather', 'etl']

)

def weather_pipeline():
    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False) #Dados não ficam persistente entre as tasks, então salvar em arquivo

    @task
    def load():
        import pandas as pd;
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_weather_data('nh_weather', df)

    extract() >> transform() >> load()

weather_pipeline()