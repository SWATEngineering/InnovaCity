/*
CREATE TABLE innovacity.humidity_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = Kafka('kafka:9092', 'humidity', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.humidity (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = MergeTree()
ORDER BY (nome_sensore, timestamp);

CREATE MATERIALIZED VIEW humidity_consumer_mv TO innovacity.humidity
AS SELECT * FROM innovacity.humidity_queue;


CREATE TABLE innovacity.humidity1m
(
    nome_sensore String,
    timestamp1m DATETIME64,
    avgHumidity AggregateFunction(avgState, Float32), 
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, nome_sensore, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.humidity1m_mv
TO innovacity.humidity1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    nome_sensore,
    avgState(value) as avgHumidity,
    latitude,
    longitude
FROM innovacity.humidity
GROUP BY (timestamp1m, nome_sensore, latitude, longitude); 


/*
-- Creare la tabella aggregata
CREATE TABLE innovacity.humidity_ma (
    nome_sensore String,
    timestamp1m DATETIME64,
    avgHumidity Float32,
    latitude Float64,
    longitude Float64
) ENGINE = MergeTree()
ORDER BY (timestamp1m, nome_sensore, latitude, longitude);

-- Creare una Materialized View
CREATE MATERIALIZED VIEW innovacity.humidity1m_mov_avg
TO innovacity.humidity_ma
AS
SELECT
    nome_sensore,
    toStartOfMinute(timestamp) AS timestamp1m,
    avg(value) OVER (PARTITION BY  toStartOfMinute(timestamp) ORDER BY timestamp1m ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avgHumidity,
    latitude,
    longitude
FROM innovacity.humidity;
*/






   



