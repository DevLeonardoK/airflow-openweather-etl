import pandas as pd
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
columns_names_to_drop = ["weather", "weather_icon", "sys.type"]
columns_names_to_renames = {
    "base": "base", 
    "visibility": "visibility", 
    "dt": "datetime", 
    "timezone": "timezone", 
    "id": "city_id", 
    "name": "city_name", 
    "cod": "code", 
    "coord.lon": "longitude", 
    "coord.lat": "latitude", 
    "main.temp": "temperature", 
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
}
columns_names_to_normalize_datetime = ["datetime", "sunrise", "sunset"]

def create_dataframe(path_name:str) -> pd.DataFrame:

    logging.info("Criando DataFrame do arquivo JSON")

    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)

    logging.info(f"DataFrame criado com {len(df)} linhas")

    return df

def normalize_weather_columns(df:pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df["weather"].apply(lambda x: x[0]))
    df_weather = df_weather.rename(
        columns={
            "id": "weather_id",
            "main": "weather_main",
            "description": "weather_description",
            "icon": "weather_icon"
        }
    )

    df = pd.concat([df, df_weather], axis=1) # Concatenar colunas (axis=1)

    logging.info("Coluna weather normalizada")

    return df

def drop_columns(df:pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:

    df = df.drop(columns=columns_names)

    logging.info(f"Colunas desnecessárias removidas com sucesso: {columns_names}")

    return df

def rename_columns(df:pd.DataFrame, columns_names: dict[str, str]) -> pd.DataFrame:
    df = df.rename(columns=columns_names)
    logging.info(f"Colunas renomeadas com sucesso")
    return df

def normalize_datetime_columns(df:pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit="s", utc=True).dt.tz_convert("America/Sao_Paulo")
    logging.info(f"Colunas de data, ajustadas corretamente: {columns_names}")

    return df

def data_transformations():
    print("Iniciando transformações")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_renames)
    df = normalize_datetime_columns(df, columns_names_to_normalize_datetime)

    logging.info("Transformações concluídas")

    return df

if __name__ == '__main__':
   df = data_transformations()
   print(df.head())
