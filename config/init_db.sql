CREATE TABLE nh_weather (
    id BIGSERIAL PRIMARY KEY,

    base VARCHAR(50),
    visibility INTEGER,

    datetime TIMESTAMPTZ NOT NULL,
    timezone INTEGER,

    city_id INTEGER,
    city_name VARCHAR(100),
    code INTEGER,

    longitude NUMERIC(9,6),
    latitude NUMERIC(9,6),

    temperature NUMERIC(5,2),
    feels_like NUMERIC(5,2),
    temp_min NUMERIC(5,2),
    temp_max NUMERIC(5,2),

    pressure INTEGER,
    humidity INTEGER,
    sea_level INTEGER,
    grnd_level INTEGER,

    wind_speed NUMERIC(5,2),
    wind_deg INTEGER,
    wind_gust NUMERIC(5,2),

    rain_1h NUMERIC(5,2),
    clouds INTEGER,

    sys_id INTEGER,
    country CHAR(2),

    sunrise TIMESTAMPTZ,
    sunset TIMESTAMPTZ,

    weather_id INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100)
)


SET TIME ZONE 'America/Sao_Paulo';