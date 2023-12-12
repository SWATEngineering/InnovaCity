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

---CREATE TABLE innovacity.temperatures5m
---(
---    nome_sensore String,
---    timestamp5m DATETIME64,
---    avgTemperature AggregateFunction(avg, Float32),
---    latitude Float64,
---    longitude Float64
---)
---ENGINE = AggregatingMergeTree
---ORDER BY (timestamp5m, nome_sensore, longitude, latitude);

--CREATE MATERIALIZED VIEW innovacity.temperatures5m_mv
--TO innovacity.temperatures5m
--AS
--SELECT
--    toStartOfFiveMinutes(timestamp) AS timestamp5m,
--    nome_sensore,
--    avgState(value) as avgTemperature,
--    latitude,
--    longitude
--FROM innovacity.temperatures
--GROUP BY (timestamp5m, nome_sensore, latitude, longitude);

CREATE TABLE innovacity.temperatures1m
(
    nome_sensore String,
    timestamp1m DATETIME64,
    avgTemperature AggregateFunction(avgState, Float32), -- Using avgState for stateful aggregation
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
        AVG(value) OVER (PARTITION BY toStartOfMinute(timestamp) ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS moving_avg_temperature,
        toStartOfMinute(timestamp) AS timestamp1m
    FROM innovacity.temperatures
    ORDER BY timestamp1m; 






