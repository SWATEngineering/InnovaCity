CREATE TABLE innovacity.temperatures_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = Kafka('kafka:9092', 'temperature', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.temperatures (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = MergeTree()
ORDER BY (nome_sensore, timestamp);

CREATE MATERIALIZED VIEW consumer_mv TO innovacity.temperatures
AS SELECT * FROM innovacity.temperatures_queue;


CREATE TABLE innovacity.temperatures1m
(
    nome_sensore String,
    timestamp1m DATETIME64,
    avgTemperature AggregateFunction(avgState, Float32), 
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, nome_sensore, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.temperatures1m_mv
TO innovacity.temperatures1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    nome_sensore,
    avgState(value) as avgTemperature,
    latitude,
    longitude
FROM innovacity.temperatures
GROUP BY (timestamp1m, nome_sensore, latitude, longitude); 


-- tabella per il calcolo della moving avarage. 
CREATE TABLE innovacity.moving_average_calculated_general_temperatures
(
    moving_avg_temperature Float32,
    timestamp1m DATETIME64
)
ENGINE = MergeTree
ORDER BY timestamp1m;
 
CREATE MATERIALIZED VIEW innovacity.mv_moving_average_temperatures
TO innovacity.moving_average_calculated_general_temperatures
AS  
SELECT DISTINCT
            avgState(value) OVER (PARTITION BY toStartOfMinute(timestamp) Rows BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_temperature,
        toStartOfMinute(timestamp) AS timestamp1m
    FROM innovacity.temperatures
    ORDER BY timestamp1m; 
--------------------------------------------------------------------------------------------------------------------------------


CREATE TABLE innovacity.rain_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = Kafka('kafka:9092', 'rain', 'ch_group_1', 'JSONEachRow');


CREATE TABLE innovacity.rain (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    nome_sensore String
) ENGINE = MergeTree()
ORDER BY (nome_sensore, timestamp);


CREATE MATERIALIZED VIEW rain_consumer_mv TO innovacity.rain
AS SELECT * FROM innovacity.rain_queue;


CREATE TABLE innovacity.rain1m
(
    nome_sensore String,
    timestamp1m DATETIME64,
    avgRain AggregateFunction(avgState, Float32), -- Using sumState for stateful aggregation
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp1m, nome_sensore, longitude, latitude);


CREATE MATERIALIZED VIEW innovacity.rain1m_mv
TO innovacity.rain1m
AS
SELECT
    toStartOfMinute(timestamp) AS timestamp1m,
    nome_sensore,
    avgState(value) as avgRain,
    latitude,
    longitude
FROM innovacity.rain_queue
GROUP BY (timestamp1m, nome_sensore, latitude, longitude);






