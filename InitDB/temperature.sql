CREATE TABLE innovacity.temperatures_queue (
    timestamp DATETIME64,
    value Float32,
    type String,
    uuid UUID
) ENGINE = Kafka('kafka:9092', 'temperature', 'ch_group_1', 'JSONEachRow');

CREATE TABLE innovacity.temperatures (
    timestamp DATETIME64,
    value Float32,
    type String,
    uuid UUID
) ENGINE = MergeTree()
ORDER BY (uuid, timestamp);

CREATE MATERIALIZED VIEW consumer TO innovacity.temperatures
AS SELECT * FROM innovacity.temperatures_queue;

CREATE TABLE innovacity.temperatures5m
(
    `timestamp5m` DATETIME64,
    `uuid` UUID,
    `avgTemperature` AggregateFunction(avg, Float32)
)
ENGINE = AggregatingMergeTree
ORDER BY (timestamp5m, uuid);

CREATE MATERIALIZED VIEW innovacity.temperatures5m_mv
TO innovacity.temperatures5m
AS
SELECT
    toStartOfFiveMinutes(timestamp) AS timestamp5m,
    uuid,
    avgState(value) as avgTemperature
FROM innovacity.temperatures
GROUP BY (timestamp5m, uuid);