# 🌦️ Airflow OpenWeather ETL (Home Lab de Dados)

Home lab de dados focado em **consumo de API**: um pipeline ETL batch que extrai dados
meteorológicos da [OpenWeather API](https://openweathermap.org/api) para a cidade de
Novo Hamburgo, transforma com **pandas** e carrega em **PostgreSQL**, tudo orquestrado
pelo **Apache Airflow** e conteinerizado com **Docker Compose**.

Diferente dos outros home labs desta série (que exploram processamento distribuído com
Spark e streaming com Kafka), o objetivo aqui é dominar o ciclo básico e mais comum de
um pipeline de dados — **extrair de uma API REST externa, tratar com pandas e persistir
em um banco relacional** — com boas práticas de agendamento e tratamento de erros
dentro do Airflow.

---

## A ideia

- **Extract** (`src/extract_data.py`) — chama o endpoint *Current Weather Data* da
  OpenWeather API para Novo Hamburgo e salva a resposta bruta em `data/weather_data.json`.
- **Transform** (`src/transform_data.py`) — pandas normaliza os campos aninhados do JSON
  (temperatura, vento, condição climática), remove colunas desnecessárias, renomeia e
  ajusta timestamps (`sunrise`/`sunset`/`datetime`) para o fuso `America/Sao_Paulo`.
- **Load** (`src/load_data.py`) — os dados tratados são gravados na tabela `nh_weather`
  do PostgreSQL via SQLAlchemy (`append`).
- **Orquestração** (`dags/weather_data.py`) — uma DAG do Airflow (`weather_data_dag`)
  roda a cada hora (`0 */1 * * *`), com `catchup` desligado e 2 re-tentativas em caso de
  falha, passando os dados entre as tasks via um parquet intermediário
  (`data/temp_data.parquet`).

---

## Serviços (containers)

| Serviço | Papel | Porta(s) |
|---|---|---|
| `airflow-apiserver` / `airflow-scheduler` / `airflow-dag-processor` / `airflow-worker` / `airflow-triggerer` | Orquestração da DAG via **CeleryExecutor** | 8080 (UI) |
| `postgres` | Metadados do Airflow | — (interno) |
| `redis` | Broker do Celery | — (interno) |
| `postgresql-data` | Dados da coleta de clima (tabela `nh_weather`) | 5432 |

---

## Modelo de dados

Tabela `nh_weather` (definida em `config/init_db.sql`), com uma linha por coleta:

| Campo | Descrição |
|---|---|
| `city_id` / `city_name` / `country` | Identificação da cidade e país |
| `longitude` / `latitude` | Coordenadas geográficas |
| `datetime` | Timestamp UTC da coleta |
| `temperature` / `feels_like` / `temp_min` / `temp_max` | Temperaturas (°C) |
| `pressure` / `humidity` | Pressão (hPa) e umidade (%) |
| `wind_speed` / `wind_deg` / `wind_gust` | Velocidade, direção e rajada do vento |
| `rain_1h` | Volume de chuva na última hora (mm) |
| `clouds` | Cobertura de nuvens (%) |
| `weather_id` / `weather_main` / `weather_description` | Condição climática |
| `sunrise` / `sunset` | Horários do nascer/pôr do sol |

---

## Estrutura

```
.
├── config/
│   ├── .env             # Variáveis de ambiente (API key, credenciais Postgres) — não versionado
│   └── init_db.sql      # DDL da tabela nh_weather
├── dags/
│   └── weather_data.py  # DAG do Airflow (extract → transform → load)
├── docker/
│   └── docker-compose.yaml
├── notebooks/
│   └── analysis_data.ipynb  # Exploração dos dados da API
├── src/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
└── requirements.txt
```

---

## Stack

`Apache Airflow` (CeleryExecutor) · `Python` · `pandas` · `PostgreSQL` · `Redis` ·
`Docker Compose` · `OpenWeather API`
