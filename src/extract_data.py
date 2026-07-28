import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import logging
import os

load_dotenv(Path('/home/devleonardo/data_home_lab/airflow-openweather-etl/config/.env'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_weather_data(url:str) -> list:

    try:
        response = requests.get(url)

        response.raise_for_status()

        data = response.json() #Transforma dicionário

        if not data:
            logging.error("Nenhum dado encontrado")
            return []

        output_path = 'data/weather_data.json'
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True) #parents = Cria subdiretórios

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
            logging.info("Arquivo salvo com sucesso")

        return data
    except requests.exceptions.HTTPError:
        logging.exception("Erro HTTP ao consultar a API.")
        raise
    except requests.exceptions.RequestException:
        logging.exception("Erro na requisição.")
        raise



if __name__ == '__main__':
    extract_weather_data(f'https://api.openweathermap.org/data/2.5/weather?q=Novo Hamburgo&units=metric&appid={os.getenv("API_KEY_OPENWEATHERMAP")}')