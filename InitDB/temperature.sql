CREATE TABLE innovacity.temperatures_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    uuid UUID
) ENGINE = Kafka('kafka:9092', 'temperature', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.temperatures (
    timestamp DATETIME64,
    value Float32,
    type String,
    latitude Float64,
    longitude Float64,
    uuid UUID
) ENGINE = MergeTree()
ORDER BY (uuid, timestamp);

CREATE MATERIALIZED VIEW consumer TO innovacity.temperatures
AS SELECT * FROM innovacity.temperatures_queue;

CREATE TABLE innovacity.temperatures5m
(
    uuid UUID,
    timestamp5m DATETIME64,
    avgTemperature AggregateFunction(avg, Float32),
    latitude Float64,
    longitude Float64
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp5m, uuid, longitude, latitude);

CREATE MATERIALIZED VIEW innovacity.temperatures5m_mv
TO innovacity.temperatures5m
AS
SELECT
    toStartOfFiveMinutes(timestamp) AS timestamp5m,
    uuid,
    avgState(value) as avgTemperature,
    latitude,
    longitude
FROM innovacity.temperatures
GROUP BY (timestamp5m, uuid, latitude, longitude);